#!/usr/bin/env python3
"""Nagios checks for generator data recorded by monitor_CAT_generator.sh.

The plugin reads the latest row written by the generator monitor instead of
opening another Modbus connection.  This avoids competing with the monitor for
the Moxa serial connection and makes it possible to verify that the database is
still receiving fresh data.
"""

from __future__ import annotations

import argparse
import configparser
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

STATUS_NAMES = {
    OK: "OK",
    WARNING: "WARNING",
    CRITICAL: "CRITICAL",
    UNKNOWN: "UNKNOWN",
}

# For the combined check, an equipment alarm should take precedence over a
# plugin/data error, followed by warning and OK.
STATUS_PRIORITY = {
    OK: 0,
    WARNING: 1,
    UNKNOWN: 2,
    CRITICAL: 3,
}


@dataclass(frozen=True)
class Result:
    status: int
    message: str
    perfdata: tuple[str, ...] = field(default_factory=tuple)


def clean_output(value: Any) -> str:
    """Keep Nagios output on one line."""
    return str(value).replace("\r", " ").replace("\n", " ").replace("|", "/")


def parse_boolean(value: Any) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return None


def load_settings(config_path: Path) -> dict[str, Any]:
    config = configparser.ConfigParser()
    if not config.read(config_path):
        raise ValueError(f"configuration file not found: {config_path}")

    table = config.get("MySQL SPECIFIC SETTINGS", "SQL_Table").strip()
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table):
        raise ValueError("SQL_Table must be a valid MySQL identifier")

    cadence = config.getint("GENERAL SETTINGS", "Cadance")
    if cadence <= 0:
        raise ValueError("Cadance must be greater than zero")

    return {
        "host": config.get("MySQL SPECIFIC SETTINGS", "SQL_Host").strip(),
        "user": config.get("MySQL SPECIFIC SETTINGS", "SQL_User").strip(),
        "password": config.get("MySQL SPECIFIC SETTINGS", "SQL_Password"),
        "database": config.get("MySQL SPECIFIC SETTINGS", "SQL_Database").strip(),
        "table": table,
        "auth_plugin": config.get(
            "MySQL SPECIFIC SETTINGS",
            "SQL_Auth",
            fallback="",
        ).strip(),
        "generator": config.get(
            "COMMUNICATION SETTINGS",
            "Generator_Type",
        ).strip(),
        "cadence": cadence,
    }


def fetch_latest(settings: dict[str, Any], generator: str) -> dict[str, Any] | None:
    try:
        import mysql.connector
    except ImportError as error:
        raise RuntimeError(
            "mysql-connector-python is not installed"
        ) from error

    connection_options = {
        "host": settings["host"],
        "user": settings["user"],
        "password": settings["password"],
        "database": settings["database"],
        "connection_timeout": 5,
    }
    if settings["auth_plugin"]:
        connection_options["auth_plugin"] = settings["auth_plugin"]

    connection = mysql.connector.connect(**connection_options)
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = f"""
            SELECT
                `ts`,
                TIMESTAMPDIFF(
                    SECOND,
                    `ts`,
                    CURRENT_TIMESTAMP(3)
                ) AS `age_seconds`,
                `communication_status`,
                `control_mode`,
                `auto_start_enabled`,
                `fuel_level_pct`,
                `active_alarm_count`,
                `active_alarms`
            FROM `{settings['table']}`
            WHERE `generator` = %s
            ORDER BY `ts` DESC
            LIMIT 1
        """
        cursor.execute(query, (generator,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def check_control_mode(row: dict[str, Any]) -> Result:
    mode = clean_output(row.get("control_mode") or "Unknown")
    auto_start = parse_boolean(row.get("auto_start_enabled"))
    if auto_start is None:
        return Result(UNKNOWN, f"control mode={mode}, auto-start state is unknown")
    if not auto_start:
        return Result(CRITICAL, f"control mode={mode}, auto-start is disabled")
    return Result(OK, f"control mode={mode}, auto-start is enabled")


def check_fuel_level(row: dict[str, Any], threshold: float) -> Result:
    raw_level = row.get("fuel_level_pct")
    if raw_level is None:
        return Result(UNKNOWN, "fuel level is unavailable")
    try:
        level = float(raw_level)
    except (TypeError, ValueError):
        return Result(UNKNOWN, f"invalid fuel level: {clean_output(raw_level)}")

    perfdata = (f"fuel_level={level:g}%;;{threshold:g};0;100",)
    if level < threshold:
        return Result(
            CRITICAL,
            f"fuel level {level:g}% is below the {threshold:g}% threshold",
            perfdata,
        )
    return Result(
        OK,
        f"fuel level {level:g}% is at or above the {threshold:g}% threshold",
        perfdata,
    )


def alarm_description(raw_alarms: Any, alarm_count: int) -> str:
    if raw_alarms in (None, "", [], ()):
        return ""
    alarms = raw_alarms
    if isinstance(raw_alarms, (str, bytes, bytearray)):
        try:
            alarms = json.loads(raw_alarms)
        except (json.JSONDecodeError, UnicodeDecodeError, TypeError):
            return clean_output(raw_alarms)
    if not isinstance(alarms, list):
        return clean_output(alarms)

    names = []
    for alarm in alarms[:5]:
        if isinstance(alarm, dict):
            name = alarm.get("name", "unnamed alarm")
            condition = alarm.get("condition")
            names.append(f"{name} ({condition})" if condition else str(name))
        else:
            names.append(str(alarm))
    if alarm_count > len(names):
        names.append(f"+{alarm_count - len(names)} more")
    return ", ".join(clean_output(name) for name in names)


def check_active_alarms(row: dict[str, Any]) -> Result:
    raw_count = row.get("active_alarm_count")
    if raw_count is None:
        return Result(UNKNOWN, "active alarm count is unavailable")
    try:
        count = int(raw_count)
    except (TypeError, ValueError):
        return Result(UNKNOWN, f"invalid active alarm count: {clean_output(raw_count)}")

    perfdata = (f"active_alarms={count};;;0;",)
    if count <= 0:
        return Result(OK, "no active alarms", perfdata)

    description = alarm_description(row.get("active_alarms"), count)
    suffix = f": {description}" if description else ""
    return Result(CRITICAL, f"{count} active alarm(s){suffix}", perfdata)


def check_communication(row: dict[str, Any], max_age: int) -> Result:
    raw_age = row.get("age_seconds")
    if raw_age is None:
        return Result(UNKNOWN, "database row age is unavailable")
    try:
        age = int(raw_age)
    except (TypeError, ValueError):
        return Result(UNKNOWN, f"invalid database row age: {clean_output(raw_age)}")

    if age < -max_age:
        return Result(
            UNKNOWN,
            f"latest database timestamp is {-age}s in the future; check system clocks",
            (f"data_age={age}s;;;0;",),
        )
    age = max(0, age)
    perfdata = (f"data_age={age}s;;{max_age};0;",)
    communication = str(row.get("communication_status") or "UNKNOWN").upper()

    if age > max_age:
        return Result(
            CRITICAL,
            f"database data is stale ({age}s old, maximum {max_age}s); "
            f"last communication status={clean_output(communication)}",
            perfdata,
        )
    if communication != "CONNECTED":
        return Result(
            CRITICAL,
            f"generator communication status={clean_output(communication)}; "
            f"database data age={age}s",
            perfdata,
        )
    return Result(
        OK,
        f"generator communication is connected and database data is fresh ({age}s old)",
        perfdata,
    )


def combine_results(results: list[tuple[str, Result]]) -> Result:
    status = max(
        (result.status for _, result in results),
        key=lambda value: STATUS_PRIORITY[value],
    )
    messages = [
        f"{name}={STATUS_NAMES[result.status]} ({result.message})"
        for name, result in results
    ]
    perfdata = tuple(
        metric
        for _, result in results
        for metric in result.perfdata
    )
    return Result(status, "; ".join(messages), perfdata)


def positive_integer(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def percentage(value: str) -> float:
    parsed = float(value)
    if not 0 <= parsed <= 100:
        raise argparse.ArgumentTypeError("must be between 0 and 100")
    return parsed


def parse_args() -> argparse.Namespace:
    default_config = Path(__file__).resolve().parent / "etc" / "check_CAT_generator.cfg"
    parser = argparse.ArgumentParser(
        description="Run Nagios checks against the latest CAT generator database row."
    )
    parser.add_argument(
        "check",
        choices=(
            "control_mode",
            "autostart",
            "fuel_level",
            "active_alarms",
            "communication",
            "all",
        ),
        help="check to run",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=default_config,
        help=f"configuration file (default: {default_config})",
    )
    parser.add_argument(
        "--generator",
        help="generator name stored in the database (default: Generator_Type from config)",
    )
    parser.add_argument(
        "--fuel-threshold",
        type=percentage,
        default=25.0,
        help="minimum acceptable fuel percentage (default: 25)",
    )
    parser.add_argument(
        "--max-age",
        type=positive_integer,
        help="maximum database row age in seconds (default: twice the configured Cadance)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        settings = load_settings(args.config)
        generator = args.generator or settings["generator"]
        if not generator:
            raise ValueError("generator name must not be empty")
        max_age = args.max_age or settings["cadence"] * 2
        row = fetch_latest(settings, generator)
        if row is None:
            result = Result(UNKNOWN, f"no database data found for generator {generator}")
        else:
            checks: dict[str, Callable[[], Result]] = {
                "control_mode": lambda: check_control_mode(row),
                "autostart": lambda: check_control_mode(row),
                "fuel_level": lambda: check_fuel_level(row, args.fuel_threshold),
                "active_alarms": lambda: check_active_alarms(row),
                "communication": lambda: check_communication(row, max_age),
            }
            if args.check == "all":
                result = combine_results(
                    [
                        ("control_mode", checks["control_mode"]()),
                        ("fuel_level", checks["fuel_level"]()),
                        ("active_alarms", checks["active_alarms"]()),
                        ("communication", checks["communication"]()),
                    ]
                )
            else:
                result = checks[args.check]()
    except Exception as error:
        result = Result(UNKNOWN, clean_output(error))

    output = f"{STATUS_NAMES[result.status]} - {result.message}"
    if result.perfdata:
        output += " | " + " ".join(result.perfdata)
    print(output)
    return result.status


if __name__ == "__main__":
    sys.exit(main())
