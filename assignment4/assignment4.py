import pandas as pd
import json
import os

#pathfix
HERE = os.path.dirname(__file__)
CSV_PATH = os.path.join(HERE, "task1_employees.csv")
JSON_PATH = os.path.join(HERE, "additional_employees.json")
DIRTY_PATH = os.path.join(HERE, "dirty_data.csv")

#1.1
task1_data_frame = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
})
print("Step 1.1 - task1_data_frame:")
print(task1_data_frame)

#1.2
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]
print("\nStep 1.2 - task1_with_salary:")
print(task1_with_salary)

#1.3
task1_older = task1_with_salary.copy()
task1_older['Age'] += 1
print("\nStep 1.3 - task1_older:")
print(task1_older)

#1.4
task1_older.to_csv(CSV_PATH, index=False)
print(f"\nStep 1.4 - Saved to {CSV_PATH}")

#2.1
task2_employees = pd.read_csv(CSV_PATH)
print("\nStep 2.1 - task2_employees:")
print(task2_employees)

#2.2
if not os.path.exists(JSON_PATH):
    additional = [
        {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
        {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000}
    ]
    with open(JSON_PATH, "w") as f:
        json.dump(additional, f)

json_employees = pd.read_json(JSON_PATH)
print("\nStep 2.2 - json_employees:")
print(json_employees)

#2.3
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print("\nStep 2.3 - more_employees:")
print(more_employees)


#3.1
first_three = more_employees.head(3)
print("\nStep 3.1 - first_three:")
print(first_three)

#3.2
last_two = more_employees.tail(2)
print("\nStep 3.2 - last_two:")
print(last_two)

#3.3
employee_shape = more_employees.shape
print("\nStep 3.3 - employee_shape:")
print(employee_shape)

#3.4
print("\nStep 3.4 - more_employees.info():")
more_employees.info()

#4.1
dirty_data = pd.read_csv(DIRTY_PATH)
print("\nStep 4.1 - dirty_data:")
print(dirty_data)
clean_data = dirty_data.copy()

#4.2
clean_data = clean_data.drop_duplicates()
print("\nStep 4.3 - After removing duplicates:")
print(clean_data)

#4.3
clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')
print("\nStep 4.4 - Age converted to numeric:")
print(clean_data)

#4.4
clean_data['Salary'] = pd.to_numeric(clean_data['Salary'].replace(["unknown", "n/a"], pd.NA), errors='coerce')
print("\nStep 4.5 - Salary cleaned:")
print(clean_data)

#4.5
clean_data['Age'] = clean_data['Age'].fillna(clean_data['Age'].mean())
clean_data['Salary'] = clean_data['Salary'].fillna(clean_data['Salary'].median())
print("\nStep 4.6 - Filled missing Age/Salary:")
print(clean_data)

#4.6
clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], errors='coerce')
#4.61
most_common_date = clean_data['Hire Date'].mode()[0]
clean_data['Hire Date'] = clean_data['Hire Date'].fillna(most_common_date)
print("\nStep 4.7 - Hire Date to datetime:")
print(clean_data)


#4.7
clean_data['Name'] = clean_data['Name'].str.strip().str.upper()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()
print("\nStep 4.8 - Cleaned Name and Department:")
print(clean_data)
