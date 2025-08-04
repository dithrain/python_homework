import pandas as pd
import json

# --- 1. From a Dictionary ---
print("📦 Loading from dictionary...")
dict_data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [24, 27, 22],
    'City': ['New York', 'San Francisco', 'Chicago']
}
df_dict = pd.DataFrame(dict_data)
print(df_dict, end="\n\n")


# --- 2. From a CSV (write and then read) ---
print("📄 Loading from CSV file with custom separator...")
df_dict.to_csv("sample_pipe.csv", sep="|", index=False)  # Save with pipe separator
df_csv = pd.read_csv("sample_pipe.csv", sep="|")
print(df_csv, end="\n\n")


# --- 3. From a JSON (write and then read) ---
print("🗂️ Loading from JSON file...")
json_data = [
    {"Name": "Dana", "Age": 29, "City": "Austin"},
    {"Name": "Eli", "Age": 31, "City": "Seattle"}
]

# Save JSON to file
with open("sample.json", "w") as f:
    json.dump(json_data, f)

# Read JSON back into DataFrame
df_json = pd.read_json("sample.json")
print(df_json)
