import argparse
import csv
import os
import sys


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Filter the PortWatch CSV by year and write a new CSV with the same header. "
            "This is intended to help split the large source file into smaller chunks."
        )
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input CSV file (e.g. Daily_Port_Activity_Data_and_Trade_Estimates.csv)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to write the filtered CSV (will be overwritten).",
    )
    parser.add_argument(
        "--year",
        required=True,
        help="Year value to filter on, e.g. 2024",
    )
    args = parser.parse_args(argv)

    if not os.path.exists(args.input):
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 2

    with open(args.input, "r", newline="", encoding="utf-8") as file_in, open(
        args.output, "w", newline="", encoding="utf-8"
    ) as file_out:
        reader = csv.DictReader(file_in)
        if not reader.fieldnames:
            print("ERROR: input CSV appears to have no header", file=sys.stderr)
            return 2

        writer = csv.DictWriter(file_out, fieldnames=reader.fieldnames)
        writer.writeheader()

        in_rows = 0
        out_rows = 0
        for row in reader:
            in_rows += 1
            if row.get("year") == str(args.year):
                writer.writerow(row)
                out_rows += 1

    print(f"Filtered {out_rows} of {in_rows} rows into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
