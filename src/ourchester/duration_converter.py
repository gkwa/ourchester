import argparse
import re


def convert_duration(duration):
    seconds_per_unit = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800,
        "M": 2592000,
        "y": 31536000,
    }

    pattern = re.compile(r"(\d*\.?\d+)([smhdwMy])")
    matches = pattern.findall(duration)
    if not matches:
        raise ValueError(f"Invalid duration format: {duration}")

    total_seconds = 0
    for value, unit in matches:
        if not value:
            value = "1"
        seconds = float(value) * seconds_per_unit[unit]
        total_seconds += seconds

    return int(total_seconds)


def main():
    parser = argparse.ArgumentParser(
        description="Convert user-friendly duration to seconds"
    )
    parser.add_argument(
        "duration", help="Duration in user-friendly format (e.g., 1d3w, 2.5h30m)"
    )
    args = parser.parse_args()

    try:
        seconds = convert_duration(args.duration)
        print(f"{args.duration} is equal to {seconds} seconds")
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()
