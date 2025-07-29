import csv
import os
csv_path = os.path.join(os.path.dirname(__file__), "..", "csv", "employees.csv")


with open(csv_path, newline="") as file:

    reader = csv.reader(file)
    employees = list(reader)
    
employee_names = [row[1] + row[2] for row in employees[1:]]

print("Employee names:")
print(employee_names)

names_with_e = [name for name in employee_names if "e" in name]

print("\nEmployee names iwth 'e':")
print(names_with_e)