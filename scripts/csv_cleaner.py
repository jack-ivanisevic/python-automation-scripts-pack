import csv

def clean_csv(input_file, output_file):
    """
    Basic CSV cleaning script.
    - Removes duplicate rows
    - Trims whitespace
    - Normalizes email fields (lowercase)
    - Ensures consistent column ordering
    """

    cleaned_rows = []
    seen = set()

    with open(input_file, "r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        for row in reader:
            # Trim whitespace
            row = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}

            # Normalize email (if exists)
            if "email" in row:
                row["email"] = row["email"].lower()

            # Deduplicate based on row tuple
            row_tuple = tuple(row.items())
            if row_tuple not in seen:
                seen.add(row_tuple)
                cleaned_rows.append(row)

    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"Cleaning complete. {len(cleaned_rows)} rows written to {output_file}.")


if __name__ == "__main__":
    # Example usage: adjust filenames as needed
    clean_csv("data/input.csv", "data/output_clean.csv")
