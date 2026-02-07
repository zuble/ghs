import json
import sys

from rich import print as pprint


def read_json(file_path):
  """Loads data from the specified JSON file."""
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      return json.load(f)
  except FileNotFoundError:
    pprint(f"Error: JSON file '{file_path}' not found.")
    sys.exit(1)
  except json.JSONDecodeError as e:
    pprint(f"Error: Invalid JSON format in '{file_path}': {e}")
    sys.exit(1)
