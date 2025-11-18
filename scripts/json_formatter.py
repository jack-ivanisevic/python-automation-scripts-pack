import json
from typing import Any, Dict


def load_json(input_file: str) -> Any:
    """
    Load JSON data from a file.
    """
    with open(input_file, "r", encoding="utf-8") as infile:
        return json.load(infile)


def save_json(data: Any, output_file: str) -> None:
    """
    Save JSON data to a file with pretty formatting.
    """
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
        outfile.write("\n")


def normalize_keys(obj: Any) -> Any:
    """
    Recursively normalize JSON keys:
    - lowercases keys
    - replaces spaces with underscores

    This is useful when preparing JSON for systems
    that expect consistent and machine-friendly keys.
    """
    if isinstance(obj, dict):
        new_dict: Dict[str, Any] = {}
        for key, value in obj.items():
            if isinstance(key, str):
                normalized_key = key.strip().lower().replace(" ", "_")
            else:
                normalized_key = key
            new_dict[normalized_key] = normalize_keys(value)
        return new_dict
    elif isinstance(obj, list):
        return [normalize_keys(item) for item in obj]
    else:
        return obj


def flatten_simple_object(obj: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """
    Flatten a simple nested dictionary into a single level using dot notation.
    Example:
        {"user": {"name": "Jack"}} -> {"user.name": "Jack"}

    This is useful when preparing JSON for flat storage or CRM properties.
    """
    items: Dict[str, Any] = {}
    for key, value in obj.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(flatten_simple_object(value, new_key, sep=sep))
        else:
            items[new_key] = value
    return items


def process_json_file(input_file: str, output_file: str, flatten: bool = False) -> None:
    """
    High-level utility:
    - Load JSON
    - Normalize keys
    - Optionally flatten nested dictionaries
    - Save to output file with pretty formatting
    """
    data = load_json(input_file)
    data = normalize_keys(data)

    if flatten and isinstance(data, dict):
        data = flatten_simple_object(data)

    save_json(data, output_file)
    print(f"Processed JSON saved to {output_file}")


if __name__ == "__main__":
    # Example usage: adjust file paths as needed
    # Place an input JSON file in the data/ directory (e.g., data/input.json)
    process_json_file("data/input.json", "data/output_normalized.json", flatten=False)
