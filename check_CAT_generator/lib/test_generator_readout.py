#!/usr/bin/env python3
"""Query and validate all D300GC generator readout methods.

This is a live communication test. It opens the Moxa-created serial device,
queries each value independently, prints the returned engineering value, and
continues when an individual query fails. Values outside the ranges defined
by the GenComm standard are reported as failures. GenComm sentinel values
(unimplemented, transducer fault, bad data, and similar) are reported as
UNAVAILABLE rather than being mistaken for real measurements.

Example:

    python3 test_generator_readout.py --port /dev/ttys001
"""

from __future__ import annotations

import argparse
import inspect
import json
import sys
import traceback
from dataclasses import dataclass
from typing import Any, Callable

import serial

from generator_com import D300GC, GeneratorCommunicationError


@dataclass(frozen=True)
class ReadoutTest:
    """Description and expected range for one generator read method."""

    method: str
    label: str
    unit: str = ""
    minimum: float | None = None
    maximum: float | None = None
    allow_none: bool = True


READOUT_TESTS = (
    ReadoutTest("read_communication_status", "Communication status", allow_none=False),
    ReadoutTest("read_overall_status", "Overall status", allow_none=False),
    ReadoutTest("read_control_mode_code", "Control mode code", minimum=0, maximum=7),
    ReadoutTest("read_control_mode", "Control mode", allow_none=False),
    ReadoutTest("read_auto_start_enabled", "Automatic start enabled"),
    ReadoutTest("read_transfer_to_generator", "Transferred to generator"),
    ReadoutTest("read_transfer_status", "Transfer status", allow_none=False),
    ReadoutTest("read_engine_state_code", "Engine state code", minimum=0, maximum=15),
    ReadoutTest("read_engine_state", "Engine state", allow_none=False),
    ReadoutTest("read_oil_pressure", "Oil pressure", "kPa", 0, 10000),
    ReadoutTest("read_coolant_temperature", "Coolant temperature", "deg C", -50, 200),
    ReadoutTest("read_oil_temperature", "Oil temperature", "deg C", -50, 200),
    ReadoutTest("read_fuel_level", "Fuel level", "%", 0, 130),
    ReadoutTest(
        "read_charge_alternator_voltage",
        "Charge alternator voltage",
        "V",
        0,
        40,
    ),
    ReadoutTest("read_battery_voltage", "Starter battery voltage", "V", 0, 40),
    ReadoutTest("read_engine_speed", "Engine speed", "RPM", 0, 6000),
    ReadoutTest("read_generator_frequency", "Generator frequency", "Hz", 0, 70),
    ReadoutTest("read_generator_l1_n_voltage", "Generator L1-N voltage", "V", 0, 18000),
    ReadoutTest("read_generator_l2_n_voltage", "Generator L2-N voltage", "V", 0, 18000),
    ReadoutTest("read_generator_l3_n_voltage", "Generator L3-N voltage", "V", 0, 18000),
    ReadoutTest("read_generator_l1_current", "Generator L1 current", "A", 0, 99999.9),
    ReadoutTest("read_generator_l2_current", "Generator L2 current", "A", 0, 99999.9),
    ReadoutTest("read_generator_l3_current", "Generator L3 current", "A", 0, 99999.9),
    ReadoutTest(
        "read_generator_total_power",
        "Generator total real power",
        "W",
        -99999999,
        99999999,
    ),
    ReadoutTest("read_generator_power_factor", "Generator power factor", "", -1, 1),
    ReadoutTest("read_engine_run_time", "Engine run time", "s", 0, 4294967295),
    ReadoutTest("read_number_of_starts", "Number of starts", "", 0, 99999),
    ReadoutTest(
        "read_generator_positive_kwh",
        "Generator positive energy",
        "kWh",
        0,
        429496729.5,
    ),
    ReadoutTest("read_named_alarm_count", "Implemented named alarms", "", 0, 256),
    ReadoutTest("read_active_alarms", "Active alarms", allow_none=False),
    ReadoutTest("read_active_alarm_count", "Active alarm count", "", 0, 256),
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query every D300GC generator readout through the Moxa serial port."
    )
    parser.add_argument(
        "--port",
        default="/dev/ttyr00",
        help="Moxa virtual serial device (default: /dev/ttyr00)",
    )
    parser.add_argument(
        "--slave-id",
        type=int,
        default=10,
        help="Modbus RTU slave ID (default: 10)",
    )
    parser.add_argument(
        "--baudrate",
        type=int,
        default=115200,
        help="Serial baud rate (default: 115200)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Response timeout in seconds (default: 1.0)",
    )
    parser.add_argument(
        "--alarm-page",
        type=int,
        default=None,
        help="Force a GenComm alarm page; default auto-detects page 154 then page 8",
    )
    parser.add_argument(
        "--request-delay",
        type=float,
        default=0.1,
        help="Minimum quiet period between Modbus requests in seconds (default: 0.1)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print Python tracebacks for failed queries",
    )
    return parser.parse_args()


def format_value(value: Any) -> str:
    """Return a readable single- or multi-line representation of a value."""
    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2, sort_keys=True)
    return str(value)


def validate_value(test: ReadoutTest, value: Any) -> str | None:
    """Return a validation error message, or ``None`` for a valid value."""
    if value is None:
        return None if test.allow_none else "method returned None"
    if test.minimum is None and test.maximum is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return f"expected a numeric value, received {type(value).__name__}"
    if test.minimum is not None and value < test.minimum:
        return f"value is below the GenComm minimum {test.minimum}"
    if test.maximum is not None and value > test.maximum:
        return f"value is above the GenComm maximum {test.maximum}"
    return None


def print_result(status: str, label: str, value: Any, unit: str = "") -> None:
    rendered = format_value(value)
    suffix = f" {unit}" if unit and not isinstance(value, (dict, list)) else ""
    if "\n" in rendered:
        print(f"[{status:<11}] {label}:")
        for line in rendered.splitlines():
            print(f"               {line}")
    else:
        print(f"[{status:<11}] {label}: {rendered}{suffix}")


def test_readout(generator: D300GC, test: ReadoutTest, verbose: bool) -> str:
    """Execute one read method and return PASS, UNAVAILABLE, or FAILED."""
    method: Callable[[], Any] = getattr(generator, test.method)
    try:
        value = method()
        if value is None and test.allow_none:
            sentinel = generator.last_sentinel or {"reason": "value unavailable"}
            print_result("UNAVAILABLE", test.label, sentinel)
            return "UNAVAILABLE"

        validation_error = validate_value(test, value)
        if validation_error:
            print_result("FAILED", test.label, value, test.unit)
            print(f"               Reason: {validation_error}")
            return "FAILED"

        print_result("PASS", test.label, value, test.unit)
        return "PASS"
    except Exception as error:
        print(f"[FAILED     ] {test.label}: {type(error).__name__}: {error}")
        if verbose:
            traceback.print_exc()
        return "FAILED"


def discover_untested_read_methods() -> list[str]:
    """Find newly added no-argument read methods missing from READOUT_TESTS."""
    tested = {test.method for test in READOUT_TESTS}
    excluded = {"read_register", "read_generator_data"}
    methods = []
    for name, method in inspect.getmembers(D300GC, predicate=inspect.isfunction):
        if not name.startswith("read_") or name in tested or name in excluded:
            continue
        signature = inspect.signature(method)
        required_parameters = [
            parameter
            for parameter in signature.parameters.values()
            if parameter.name != "self"
            and parameter.default is inspect.Parameter.empty
            and parameter.kind
            in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        ]
        if not required_parameters:
            methods.append(name)
    return methods


def main() -> int:
    args = parse_arguments()
    generator = D300GC(
        port=args.port,
        slave_id=args.slave_id,
        baudrate=args.baudrate,
        timeout=args.timeout,
        alarm_page=args.alarm_page,
        request_delay=args.request_delay,
    )

    print("D300GC generator live readout test")
    print(f"Port      : {args.port}")
    print(f"Slave ID  : {args.slave_id}")
    print(f"Serial    : {args.baudrate},8,N,1")
    print(f"Timeout   : {args.timeout:.2f} seconds")
    print(f"Req. delay: {args.request_delay:.3f} seconds")
    print("-" * 78)

    try:
        generator.open()
    except (serial.SerialException, OSError, GeneratorCommunicationError) as error:
        print(f"[FAILED     ] Open serial connection: {type(error).__name__}: {error}")
        return 2

    results: list[str] = []
    try:
        for test in READOUT_TESTS:
            results.append(test_readout(generator, test, args.verbose))

        print("-" * 78)
        print("Combined read_generator_data() result:")
        try:
            combined = generator.read_generator_data()
            print(format_value(combined))
            results.append("PASS")
        except Exception as error:
            print(f"[FAILED     ] read_generator_data: {type(error).__name__}: {error}")
            if args.verbose:
                traceback.print_exc()
            results.append("FAILED")
    finally:
        generator.close()

    untested = discover_untested_read_methods()
    if untested:
        print("-" * 78)
        print("WARNING: untested read methods detected: " + ", ".join(untested))

    passed = results.count("PASS")
    unavailable = results.count("UNAVAILABLE")
    failed = results.count("FAILED")
    print("-" * 78)
    print(
        f"Summary: {passed} passed, {unavailable} unavailable, "
        f"{failed} failed, {len(results)} total"
    )

    if failed:
        print("Result: FAIL - one or more read methods did not work or returned invalid data")
        return 1
    print("Result: PASS - all implemented read methods responded correctly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
