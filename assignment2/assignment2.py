import os
import csv
import sys
import custom_module

#task2
def read_employees():
    employees_dict = {}
    rows = []

    try:
        print("Reading from:", os.path.abspath("../csv/employees.csv"))

        with open("../csv/employees.csv", newline="") as f:
            reader = csv.reader(f)

            for index, row in enumerate(reader):
                print(f"Reading line {index}: {row}")

                if index == 0:
                    employees_dict["fields"] = row
                else:
                    rows.append(row)

            print("Total rows read (excluding header):", len(rows))

            employees_dict["rows"] = rows
            return employees_dict

    except Exception as e:
        print("Error reading CSV file:", e)
        sys.exit(1)

employees = read_employees()

print("First 2 rows:")
print(employees["rows"][:2])


#task3

def column_index(column_name):
    return employees["fields"].index(column_name)

employee_id_column = column_index("employee_id")
print("Employee ID column index:", employee_id_column)

#task4

def first_name(row_number):
    index = column_index("first_name")
    return employees["rows"][row_number][index]

#task5

def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    
    matches = list(filter(employee_match, employees["rows"]))
    return matches

#task6

def employee_find_2(employee_id):
    matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
    return matches

#task7
def sort_by_last_name():
    last_name = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[last_name])
    return employees["rows"]

#task8
def employee_dict(row):
    keys = employees["fields"][1:]
    values = row[1:]
    return dict(zip(keys, values))

print("Column index for last_name:", column_index("last_name"))


#task9
def all_employees_dict():
    result = {}
    for row in employees ["rows"]:
        employee_id = row[0]
        print("Adding employee:", employee_id)
        result[employee_id] = employee_dict(row)
    return result
print(all_employees_dict())

#task10
def get_this_value():
    return os.getenv("THISVALUE")

#task11
def set_that_secret(new_value):
    custom_module.set_secret(new_value)

#task12       
def open_minutes_csv(path):
    result = {}
    rows = []

    try:
        print("Reading from:", os.path.abspath(path))

        with open(path, newline="") as f:
            reader = csv.reader(f)
            for index, row in enumerate(reader):
                print(f"Reading line {index}: {row}")
                if index == 0:
                    result["fields"] = row
                else:
                    rows.append(tuple(row))
            result["rows"] = rows
            return result

    except Exception as e:
        print("Error reading", path, e)
        sys.exit(1)

        
        
def read_minutes():
    minutes1 = open_minutes_csv("../csv/minutes1.csv")
    minutes2 = open_minutes_csv("../csv/minutes2.csv")
    return minutes1, minutes2

minutes1, minutes2 = read_minutes()

print("Minutes 1:", minutes1)
print("Minutes 2:", minutes2)

#task13

def open_minutes_csv(path):
    result = {}
    rows = []

    try:
        print("Reading from:", os.path.abspath(path))
        with open(path, newline="") as f:
            reader = csv.reader(f)
            for index, row in enumerate(reader):
                if index == 0:
                    result["fields"] = row
                else:
                    rows.append(tuple(row))
            result["rows"] = rows
            return result
    except Exception as e:
        print("Error reading", path, e)
        sys.exit(1)

def read_minutes():
    minutes1 = open_minutes_csv("../csv/minutes1.csv")
    minutes2 = open_minutes_csv("../csv/minutes2.csv")
    return minutes1, minutes2

minutes1, minutes2 = read_minutes()
print("minutes1:", minutes1)
print("minutes2:", minutes2)

def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    return set1.union(set2)

minutes_set = create_minutes_set()
print("minutes_set:", minutes_set)

def create_minutes_list():
    lst = list(minutes_set)
    return list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), lst))

minutes_list = create_minutes_list()
print("minutes_list:", minutes_list)

#task15
def write_sorted_list():
    sorted_list = sorted(minutes_list, key=lambda x: x[1])

    converted = list(map(lambda x: (x[0], x[1].strftime("%B %d, %Y")), sorted_list))

    with open("./minutes.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(minutes1["fields"])
        writer.writerows(converted)

    return converted

final_minutes = write_sorted_list()
print("Final CSV content:", final_minutes)
