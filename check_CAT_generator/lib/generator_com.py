"""Communication helpers for the D300GC generator controller.

The generator exposes the GenComm register map over Modbus RTU.  A Moxa
serial-device server presents the RS-485 connection as a local serial device
(for example ``/dev/ttyr00``).  This module therefore sends complete Modbus
RTU frames, including the CRC, through that serial device.

GenComm divides its register map into pages of 256 registers.  All addresses
used here are zero-based Modbus protocol addresses; a value shown as register
1026 by one-based tools such as Modscan is protocol address 1025.
"""

from __future__ import annotations

import math
import struct
import threading
import time
from typing import Any

import serial


class GeneratorCommunicationError(RuntimeError):
    """Raised when communication with the generator fails."""


class GeneratorProtocolError(GeneratorCommunicationError):
    """Raised when the generator returns an invalid Modbus response."""


class ModbusExceptionResponse(GeneratorCommunicationError):
    """Raised when the generator returns a Modbus exception response."""

    EXCEPTION_NAMES = {
        1: "illegal function",
        2: "illegal data address",
        3: "illegal data value",
        4: "slave device failure",
        6: "slave device busy",
        12: "reserved register",
    }

    def __init__(self, code: int):
        self.code = code
        name = self.EXCEPTION_NAMES.get(code, "unknown exception")
        super().__init__(f"Modbus exception {code}: {name}")


class D300GC:
    """Read D300GC generator values through a Moxa-backed serial port.

    The class deliberately exposes one method per stored generator value.  A
    method returns ``None`` when GenComm reports an instrumentation sentinel
    (unimplemented, out of range, transducer fault, or bad data).
    """

    PAGE_SIZE = 256
    FUNCTION_READ_HOLDING_REGISTERS = 3

    # GenComm page numbers.
    PAGE_STATUS = 3
    PAGE_BASIC_INSTRUMENTATION = 4
    PAGE_EXTENDED_INSTRUMENTATION = 5
    PAGE_DERIVED_INSTRUMENTATION = 6
    PAGE_ACCUMULATED_INSTRUMENTATION = 7
    PAGE_ALARMS = 8
    PAGE_NAMED_ALARMS = 154
    PAGE_OUTPUT_STATUS = 190

    # D300GC controller allocation: Page 190, offset 19 is the live bus-breaker
    # LED state. A value of 1 means the load has transferred to generator supply.
    TRANSFER_STATUS_OFFSET = 19

    ENGINE_STATE_NAMES = {
        0: "Engine stopped",
        1: "Pre-start",
        2: "Warming up",
        3: "Running",
        4: "Cooling down",
        5: "Engine stopped",
        6: "Post run",
        7: "Reserved",
        8: "SAE state 8",
        9: "SAE state 9",
        10: "SAE state 10",
        11: "SAE state 11",
        12: "SAE state 12",
        13: "SAE state 13",
        14: "Reserved",
        15: "Not available",
    }

    CONTROL_MODE_NAMES = {
        0: "Stop mode",
        1: "Auto mode",
        2: "Manual mode",
        3: "Test on load mode",
        4: "Auto with manual restore mode / Prohibit Return",
        5: "User configuration mode",
        6: "Test off load mode",
        7: "Off mode",
    }
    AUTO_START_CONTROL_MODES = frozenset((1, 4))

    ALARM_CONDITION_NAMES = {
        0: "disabled",
        1: "not active",
        2: "warning",
        3: "shutdown",
        4: "electrical trip",
        5: "controlled shutdown",
        6: "reserved",
        7: "reserved",
        8: "inactive indication",
        9: "inactive indication",
        10: "active indication",
        11: "reserved",
        12: "reserved",
        13: "reserved",
        14: "reserved",
        15: "unimplemented",
    }
    ACTIVE_ALARM_CODES = frozenset((2, 3, 4, 5, 10))

    # The first alarms on legacy GenComm page 8.  Controllers can implement more;
    # unknown entries are returned as "Alarm N" rather than discarded.
    PAGE_8_ALARM_NAMES = (
        "Emergency stop",
        "Low oil pressure",
        "High coolant temperature",
        "High oil temperature",
        "Under speed",
        "Over speed",
        "Fail to start",
        "Fail to come to rest",
        "Loss of speed sensing",
        "Generator low voltage",
        "Generator high voltage",
        "Generator low frequency",
        "Generator high frequency",
        "Generator high current",
        "Generator earth fault",
        "Generator reverse power",
        "Air flap",
        "Oil pressure sender fault",
        "Coolant temperature sender fault",
        "Oil temperature sender fault",
        "Fuel level sender fault",
        "Magnetic pickup fault",
        "Loss of AC speed signal",
        "Charge alternator failure",
        "Low battery voltage",
        "High battery voltage",
        "Low fuel level",
        "High fuel level",
        "Generator failed to close",
        "Mains failed to close",
        "Generator failed to open",
        "Mains failed to open",
        "Mains low voltage",
        "Mains high voltage",
        "Bus failed to close",
        "Bus failed to open",
        "Mains low frequency",
        "Mains high frequency",
        "Mains failed",
        "Mains phase rotation wrong",
        "Generator phase rotation wrong",
        "Maintenance due",
        "Clock not set",
        "Local LCD configuration lost",
        "Local telemetry configuration lost",
        "Control unit not calibrated",
        "Modem power fault",
        "Generator short circuit",
        "Failure to synchronise",
        "Bus live",
        "Scheduled run",
        "Bus phase rotation wrong",
    )

    # D300GC installations normally expose the newer, family-specific alarm
    # map on page 154.  These are the first 8xxx/74xx family entries.
    PAGE_154_ALARM_NAMES = (
        "Emergency stop",
        "Low oil pressure",
        "High coolant temperature",
        "Low coolant temperature",
        "Under speed",
        "Over speed",
        "Generator under frequency",
        "Generator over frequency",
        "Generator low voltage",
        "Generator high voltage",
        "Battery low voltage",
        "Battery high voltage",
        "Charge alternator failure",
        "Fail to start",
        "Fail to stop",
        "Generator fail to close",
        "Mains fail to close",
        "Oil pressure sender fault",
        "Loss of magnetic pickup",
        "Magnetic pickup open circuit",
        "Generator high current",
        "Calibration lost",
        "Low fuel level",
        "CAN ECU warning",
        "CAN ECU shutdown",
        "CAN ECU data failure",
        "Low oil level switch",
        "High temperature switch",
    )

    SENTINEL_NAMES = {
        0: "unimplemented",
        1: "over measurable range",
        2: "under measurable range",
        3: "transducer fault",
        4: "bad data",
        5: "high digital input",
        6: "low digital input",
        7: "reserved",
    }

    def __init__(
        self,
        port: str = "/dev/ttys001",
        slave_id: int = 10,
        baudrate: int = 115200,
        timeout: float = 1.0,
        alarm_page: int | None = None,
        request_delay: float = 0.1,
    ) -> None:
        self._serial: serial.SerialBase | None = None
        self._port_name = port
        self._slave_id = self._validate_slave_id(slave_id)
        self._baudrate = baudrate
        self._timeout = timeout
        self._request_delay = max(0.0, float(request_delay))
        self._last_transaction_finished = 0.0
        self._alarm_page = alarm_page
        self._resolved_alarm_page: int | None = alarm_page
        self._lock = threading.Lock()
        self.last_sentinel: dict[str, Any] | None = None

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            # Destructors must never mask the original application error.
            pass

    @staticmethod
    def _validate_slave_id(slave_id: int) -> int:
        slave_id = int(slave_id)
        if not 1 <= slave_id <= 247:
            raise ValueError("Modbus slave ID must be between 1 and 247")
        return slave_id

    def initialise(
        self,
        port: str | None = None,
        slave_id: int | None = None,
        baudrate: int | None = None,
        timeout: float | None = None,
        request_delay: float | None = None,
    ) -> bool:
        """Set connection parameters without opening the serial device."""
        if self._serial is not None and self._serial.is_open:
            self.close()
        if port is not None:
            self._port_name = port
        if slave_id is not None:
            self._slave_id = self._validate_slave_id(slave_id)
        if baudrate is not None:
            self._baudrate = int(baudrate)
        if timeout is not None:
            self._timeout = float(timeout)
        if request_delay is not None:
            self._request_delay = max(0.0, float(request_delay))
        return True

    def open(
        self,
        port: str | None = None,
        slave_id: int | None = None,
        baudrate: int | None = None,
        timeout: float | None = None,
        request_delay: float | None = None,
    ) -> bool:
        """Open the Moxa TCP socket using 115200,8,N,1 by default."""
        self.initialise(port, slave_id, baudrate, timeout, request_delay)
        self._serial = serial.serial_for_url(
            self._port_name,
            baudrate=self._baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=self._timeout,
            write_timeout=self._timeout,
        )
        return self._serial.is_open

    def close(self) -> bool:
        """Close the serial connection; calling this repeatedly is safe."""
        if self._serial is not None and self._serial.is_open:
            self._serial.close()
        return self._serial is None or not self._serial.is_open

    def reconnect(self) -> bool:
        """Close and reopen the serial connection with the current settings."""
        self.close()
        return self.open()

    def is_connected(self) -> bool:
        """Return ``True`` only if the port is open and the generator responds."""
        if self._serial is None or not self._serial.is_open:
            return False
        try:
            self.read_register(self.register_address(4, 0))
        except (GeneratorCommunicationError, serial.SerialException, OSError):
            return False
        return True

    @classmethod
    def register_address(cls, page: int, offset: int) -> int:
        """Convert a GenComm page and offset to a zero-based Modbus address."""
        if page < 0 or offset < 0 or offset >= cls.PAGE_SIZE:
            raise ValueError("GenComm page must be positive and offset must be 0..255")
        address = page * cls.PAGE_SIZE + offset
        if address > 0xFFFF:
            raise ValueError("Modbus register address is outside the 16-bit range")
        return address

    @staticmethod
    def _crc16(data: bytes) -> int:
        """Return the Modbus RTU CRC-16 for *data*."""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
        return crc

    def _read_exactly(self, size: int) -> bytes:
        if self._serial is None:
            raise GeneratorCommunicationError("Serial port is not open")
        data = bytearray()
        while len(data) < size:
            chunk = self._serial.read(size - len(data))
            if not chunk:
                raise GeneratorCommunicationError(
                    f"Timed out after receiving {len(data)} of {size} response bytes"
                )
            data.extend(chunk)
        return bytes(data)

    def _validate_crc(self, response: bytes) -> None:
        if len(response) < 4:
            raise GeneratorProtocolError("Modbus response is too short")
        received_crc = int.from_bytes(response[-2:], byteorder="little")
        calculated_crc = self._crc16(response[:-2])
        if received_crc != calculated_crc:
            raise GeneratorProtocolError(
                f"Invalid Modbus CRC: received 0x{received_crc:04X}, "
                f"expected 0x{calculated_crc:04X}"
            )

    def read_register(self, register_address: int, count: int = 1) -> int | list[int]:
        """Read one or more zero-based holding-register addresses (function 03)."""
        if not 0 <= register_address <= 0xFFFF:
            raise ValueError("Register address must be between 0 and 65535")
        if not 1 <= count <= 125:
            raise ValueError("Register count must be between 1 and 125")
        if register_address + count - 1 > 0xFFFF:
            raise ValueError("Requested registers exceed the Modbus address range")
        if self._serial is None or not self._serial.is_open:
            raise GeneratorCommunicationError("Serial port is not open")

        request = struct.pack(
            ">BBHH",
            self._slave_id,
            self.FUNCTION_READ_HOLDING_REGISTERS,
            register_address,
            count,
        )
        request += struct.pack("<H", self._crc16(request))

        with self._lock:
            # The controller/Moxa path needs a short quiet period between RTU
            # transactions. Without it, immediate back-to-back requests can
            # cause every second request to time out even though its address is
            # valid. Count time spent by the caller toward the quiet period.
            elapsed = time.monotonic() - self._last_transaction_finished
            remaining_delay = self._request_delay - elapsed
            if remaining_delay > 0:
                time.sleep(remaining_delay)

            try:
                self._serial.reset_input_buffer()
                written = self._serial.write(request)
                self._serial.flush()
                if written != len(request):
                    raise GeneratorCommunicationError(
                        f"Only {written} of {len(request)} request bytes were written"
                    )

                header = self._read_exactly(3)
                slave, function, third_byte = header
                if slave != self._slave_id:
                    raise GeneratorProtocolError(
                        f"Response came from slave {slave}, expected {self._slave_id}"
                    )

                if function == self.FUNCTION_READ_HOLDING_REGISTERS | 0x80:
                    response = header + self._read_exactly(2)
                    self._validate_crc(response)
                    raise ModbusExceptionResponse(third_byte)
                if function != self.FUNCTION_READ_HOLDING_REGISTERS:
                    raise GeneratorProtocolError(
                        f"Unexpected Modbus function code {function}"
                    )

                expected_byte_count = count * 2
                if third_byte != expected_byte_count:
                    raise GeneratorProtocolError(
                        f"Response contains {third_byte} data bytes; "
                        f"expected {expected_byte_count}"
                    )
                response = header + self._read_exactly(third_byte + 2)
                self._validate_crc(response)
            finally:
                self._last_transaction_finished = time.monotonic()

        registers = list(struct.unpack(f">{count}H", response[3:-2]))
        return registers[0] if count == 1 else registers

    def _sentinel_name(self, raw: int, bits: int, signed: bool) -> str | None:
        sentinel_base = (1 << (bits - 1)) - 1 if signed else (1 << bits) - 1
        distance = sentinel_base - raw
        if 0 <= distance <= 7:
            return self.SENTINEL_NAMES[distance]
        return None

    def _read_value(
        self,
        page: int,
        offset: int,
        *,
        bits: int = 16,
        signed: bool = False,
        scale: float = 1.0,
    ) -> int | float | None:
        register_count = bits // 16
        address = self.register_address(page, offset)
        registers = self.read_register(address, register_count)
        if isinstance(registers, int):
            registers = [registers]

        # GenComm stores the most significant word at the lowest address.
        raw = 0
        for register in registers:
            raw = (raw << 16) | register

        sentinel = self._sentinel_name(raw, bits, signed)
        if sentinel is not None:
            self.last_sentinel = {
                "page": page,
                "offset": offset,
                "address": address,
                "reason": sentinel,
            }
            return None

        self.last_sentinel = None
        if signed and raw & (1 << (bits - 1)):
            raw -= 1 << bits
        return raw if scale == 1 else raw * scale

    # Page 3 - controller status -------------------------------------------------

    def read_communication_status(self) -> str:
        """Return ``CONNECTED`` when the controller answers a Modbus request."""
        return "CONNECTED" if self.is_connected() else "DISCONNECTED"

    def read_overall_status(self) -> str:
        """Return an overall OK/WARNING/CRITICAL controller state."""
        flags = self._read_value(self.PAGE_STATUS, 6)
        if flags is None:
            return "UNKNOWN"
        if flags & ((1 << 15) | (1 << 13) | (1 << 12) | (1 << 11) | (1 << 6)):
            return "CRITICAL"
        if flags & (1 << 10):
            return "WARNING"
        return "OK"

    def read_control_mode_code(self) -> int | None:
        """Read the unsigned GenComm control-mode code from page 3, offset 4."""
        return self._read_value(self.PAGE_STATUS, 4)

    def read_control_mode(self) -> str:
        """Read and translate the generator control mode."""
        code = self.read_control_mode_code()
        if code is None:
            return "Unknown"
        return self.CONTROL_MODE_NAMES.get(code, f"Reserved ({code})")

    def read_auto_start_enabled(self) -> bool | None:
        """Return whether the controller is in an automatic-start mode."""
        code = self.read_control_mode_code()
        if code is None:
            return None
        return code in self.AUTO_START_CONTROL_MODES

    # Page 190 - live output status --------------------------------------------

    def read_transfer_to_generator(self) -> bool | None:
        """Return whether the load is transferred to generator supply."""
        value = self._read_value(
            self.PAGE_OUTPUT_STATUS,
            self.TRANSFER_STATUS_OFFSET,
        )
        if value is None:
            return None
        if value not in (0, 1):
            raise GeneratorProtocolError(
                f"Invalid generator transfer status value: {value}"
            )
        return bool(value)

    def read_transfer_status(self) -> str:
        """Return a readable generator transfer status."""
        transferred = self.read_transfer_to_generator()
        if transferred is None:
            return "Unknown"
        if transferred:
            return "Transferred to generator"
        return "Not transferred to generator"

    # Page 4 - basic instrumentation -------------------------------------------

    def read_oil_pressure(self) -> int | None:
        """Read oil pressure in kPa (unsigned 16-bit)."""
        return self._read_value(self.PAGE_BASIC_INSTRUMENTATION, 0)

    def read_coolant_temperature(self) -> int | None:
        """Read coolant temperature in degrees Celsius (signed 16-bit)."""
        return self._read_value(self.PAGE_BASIC_INSTRUMENTATION, 1, signed=True)

    def read_oil_temperature(self) -> int | None:
        """Read oil temperature in degrees Celsius (signed 16-bit)."""
        return self._read_value(self.PAGE_BASIC_INSTRUMENTATION, 2, signed=True)

    def read_fuel_level(self) -> int | None:
        """Read fuel level in percent (unsigned 16-bit)."""
        return self._read_value(self.PAGE_BASIC_INSTRUMENTATION, 3)

    def read_charge_alternator_voltage(self) -> float | None:
        """Read charge-alternator voltage in volts (unsigned 16-bit, x0.1)."""
        return self._read_value(self.PAGE_BASIC_INSTRUMENTATION, 4, scale=0.1)

    def read_battery_voltage(self) -> float | None:
        """Read starter-battery voltage in volts (unsigned 16-bit, x0.1)."""
        return self._read_value(self.PAGE_BASIC_INSTRUMENTATION, 5, scale=0.1)

    def read_engine_speed(self) -> int | None:
        """Read engine speed in RPM (unsigned 16-bit)."""
        return self._read_value(self.PAGE_BASIC_INSTRUMENTATION, 6)

    def read_generator_frequency(self) -> float | None:
        """Read generator frequency in hertz (unsigned 16-bit, x0.1)."""
        return self._read_value(self.PAGE_BASIC_INSTRUMENTATION, 7, scale=0.1)

    def read_generator_l1_n_voltage(self) -> float | None:
        """Read generator L1-N voltage (unsigned 32-bit, x0.1 V)."""
        return self._read_value(
            self.PAGE_BASIC_INSTRUMENTATION, 8, bits=32, scale=0.1
        )

    def read_generator_l2_n_voltage(self) -> float | None:
        """Read generator L2-N voltage (unsigned 32-bit, x0.1 V)."""
        return self._read_value(
            self.PAGE_BASIC_INSTRUMENTATION, 10, bits=32, scale=0.1
        )

    def read_generator_l3_n_voltage(self) -> float | None:
        """Read generator L3-N voltage (unsigned 32-bit, x0.1 V)."""
        return self._read_value(
            self.PAGE_BASIC_INSTRUMENTATION, 12, bits=32, scale=0.1
        )

    def read_generator_l1_current(self) -> float | None:
        """Read generator L1 current (unsigned 32-bit, x0.1 A)."""
        return self._read_value(
            self.PAGE_BASIC_INSTRUMENTATION, 20, bits=32, scale=0.1
        )

    def read_generator_l2_current(self) -> float | None:
        """Read generator L2 current (unsigned 32-bit, x0.1 A)."""
        return self._read_value(
            self.PAGE_BASIC_INSTRUMENTATION, 22, bits=32, scale=0.1
        )

    def read_generator_l3_current(self) -> float | None:
        """Read generator L3 current (unsigned 32-bit, x0.1 A)."""
        return self._read_value(
            self.PAGE_BASIC_INSTRUMENTATION, 24, bits=32, scale=0.1
        )

    # Page 5 - extended instrumentation ----------------------------------------

    def read_engine_state_code(self) -> int | None:
        """Read the unsigned GenComm engine operating-state code."""
        return self._read_value(self.PAGE_EXTENDED_INSTRUMENTATION, 128)

    def read_engine_state(self) -> str:
        """Read and translate the engine operating-state code."""
        code = self.read_engine_state_code()
        if code is None:
            return "Unknown"
        return self.ENGINE_STATE_NAMES.get(code, f"Unknown ({code})")

    # Page 6 - derived instrumentation -----------------------------------------

    def read_generator_total_power(self) -> int | None:
        """Read total generator real power in watts (signed 32-bit)."""
        return self._read_value(
            self.PAGE_DERIVED_INSTRUMENTATION, 0, bits=32, signed=True
        )

    def read_generator_power_factor(self) -> float | None:
        """Read average generator power factor (signed 16-bit, x0.01)."""
        return self._read_value(
            self.PAGE_DERIVED_INSTRUMENTATION, 21, signed=True, scale=0.01
        )

    # Page 7 - accumulated instrumentation -------------------------------------

    def read_engine_run_time(self) -> int | None:
        """Read accumulated engine run time in seconds (unsigned 32-bit)."""
        return self._read_value(
            self.PAGE_ACCUMULATED_INSTRUMENTATION, 6, bits=32
        )

    def read_generator_positive_kwh(self) -> float | None:
        """Read positive generator energy in kWh (unsigned 32-bit, x0.1)."""
        return self._read_value(
            self.PAGE_ACCUMULATED_INSTRUMENTATION, 8, bits=32, scale=0.1
        )

    def read_number_of_starts(self) -> int | None:
        """Read the accumulated number of engine starts (unsigned 32-bit)."""
        return self._read_value(
            self.PAGE_ACCUMULATED_INSTRUMENTATION, 16, bits=32
        )

    # Page 154/page 8 - alarm conditions ----------------------------------------

    def read_named_alarm_count(self) -> int | None:
        """Read the number of named alarm conditions implemented by the unit."""
        pages = (
            (self._alarm_page,)
            if self._alarm_page is not None
            else (self.PAGE_NAMED_ALARMS, self.PAGE_ALARMS)
        )
        for page in pages:
            try:
                count = self._read_value(page, 0)
            except (GeneratorCommunicationError, serial.SerialException, OSError):
                if self._alarm_page is not None:
                    raise
                continue
            if count is None or (count == 0 and self._alarm_page is None):
                continue
            if count > 256:
                if self._alarm_page is not None:
                    raise GeneratorProtocolError(f"Invalid named alarm count: {count}")
                continue
            self._resolved_alarm_page = page
            return count
        self._resolved_alarm_page = None
        return None

    def read_active_alarms(self) -> list[dict[str, Any]]:
        """Return active warning, trip, shutdown, and indication conditions."""
        alarm_count = self.read_named_alarm_count()
        if not alarm_count:
            return []
        if self._resolved_alarm_page is None:
            raise GeneratorProtocolError("Could not resolve the GenComm alarm page")
        alarm_page = self._resolved_alarm_page
        register_count = math.ceil(alarm_count / 4)
        registers = self.read_register(
            self.register_address(alarm_page, 1), register_count
        )
        if isinstance(registers, int):
            registers = [registers]

        active_alarms: list[dict[str, Any]] = []
        for alarm_index in range(alarm_count):
            register = registers[alarm_index // 4]
            shift = 12 - (alarm_index % 4) * 4
            condition_code = (register >> shift) & 0x0F
            if condition_code not in self.ACTIVE_ALARM_CODES:
                continue
            alarm_names = (
                self.PAGE_154_ALARM_NAMES
                if alarm_page == self.PAGE_NAMED_ALARMS
                else self.PAGE_8_ALARM_NAMES
            )
            name = (
                alarm_names[alarm_index]
                if alarm_index < len(alarm_names)
                else f"Alarm {alarm_index + 1}"
            )
            active_alarms.append(
                {
                    "index": alarm_index + 1,
                    "name": name,
                    "condition_code": condition_code,
                    "condition": self.ALARM_CONDITION_NAMES[condition_code],
                }
            )
        return active_alarms

    def read_active_alarm_count(self) -> int:
        """Return the number of alarm conditions that are currently active."""
        return len(self.read_active_alarms())

    def read_generator_data(self) -> dict[str, Any]:
        """Read all values represented by the generator database table."""
        communication_status = self.read_communication_status()
        if communication_status != "CONNECTED":
            raise GeneratorCommunicationError("Generator is not responding")

        control_mode_code = self.read_control_mode_code()
        engine_state_code = self.read_engine_state_code()
        transfer_to_generator = self.read_transfer_to_generator()
        active_alarms = self.read_active_alarms()
        return {
            "communication_status": communication_status,
            "overall_status": self.read_overall_status(),
            "control_mode_code": control_mode_code,
            "control_mode": (
                "Unknown"
                if control_mode_code is None
                else self.CONTROL_MODE_NAMES.get(
                    control_mode_code, f"Reserved ({control_mode_code})"
                )
            ),
            "auto_start_enabled": (
                None
                if control_mode_code is None
                else control_mode_code in self.AUTO_START_CONTROL_MODES
            ),
            "transfer_to_generator": transfer_to_generator,
            "transfer_status": (
                "Unknown"
                if transfer_to_generator is None
                else (
                    "Transferred to generator"
                    if transfer_to_generator
                    else "Not transferred to generator"
                )
            ),
            "engine_state_code": engine_state_code,
            "engine_state": (
                "Unknown"
                if engine_state_code is None
                else self.ENGINE_STATE_NAMES.get(
                    engine_state_code, f"Unknown ({engine_state_code})"
                )
            ),
            "oil_pressure_kpa": self.read_oil_pressure(),
            "coolant_temperature_c": self.read_coolant_temperature(),
            "oil_temperature_c": self.read_oil_temperature(),
            "fuel_level_pct": self.read_fuel_level(),
            "charge_alternator_voltage_v": self.read_charge_alternator_voltage(),
            "battery_voltage_v": self.read_battery_voltage(),
            "engine_speed_rpm": self.read_engine_speed(),
            "generator_frequency_hz": self.read_generator_frequency(),
            "generator_l1_n_voltage_v": self.read_generator_l1_n_voltage(),
            "generator_l2_n_voltage_v": self.read_generator_l2_n_voltage(),
            "generator_l3_n_voltage_v": self.read_generator_l3_n_voltage(),
            "generator_l1_current_a": self.read_generator_l1_current(),
            "generator_l2_current_a": self.read_generator_l2_current(),
            "generator_l3_current_a": self.read_generator_l3_current(),
            "generator_total_power_w": self.read_generator_total_power(),
            "generator_power_factor": self.read_generator_power_factor(),
            "engine_run_time_s": self.read_engine_run_time(),
            "number_of_starts": self.read_number_of_starts(),
            "generator_positive_kwh": self.read_generator_positive_kwh(),
            "active_alarm_count": len(active_alarms),
            "active_alarms": active_alarms,
        }


# Compatibility aliases for older callers that imported ``com`` or ``Generator``.
com = D300GC
Generator = D300GC
