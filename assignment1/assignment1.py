# Write your code here.
def hello():
    return ("Hello!")

def greet(name):
    return f"Hello, {name}!"
    
def calc(a, b, operator="multiply"):
    if operator == "add":
        return a + b
    elif operator == "subtract":
        return a - b
    elif operator == "divide":
        if b == 0:
            return "You can't divide by 0!"
        return a / b
    elif operator == "modulo":
        return a % b
    elif operator == "int_divide":
        return a // b
    elif operator == "power":
        return a ** b
    elif operator == "multiply":
        if type(a) == str or type(b) == str:
            return "You can't multiply those values!"
        return a * b

def data_type_conversion(value, type):
    try:
        if type == "int":
            return int(value)
        elif type == "str":
            return str(value)
        elif type == "float":
            return float(value)
    except:
        return f"You can't convert {value} into a {type}."
    
def grade(*score):
    for stringcheck in(score):
        if type(stringcheck) == str:
            return "Invalid data was provided."
    average = sum(score) / len(score)
    if average > 90:
            return "A"
    elif average > 80:
            return "B"
    elif average > 70:
            return "C"
    elif average > 60:
            return "D"
    else:
            return "F"
    
def repeat(string, count):
    newstring = (string * count)
    return newstring

def repeat(string, count):
    newstring = ""
    for number in range(count):
         newstring = (newstring + string)
    return newstring

def student_scores(choice, **kwargs):
    if choice == "mean":
        return sum(kwargs.values()) / len(kwargs)
    elif choice == "best":
        best_student = ""
        best_score = -1
        for key, value in kwargs.items():
            if value > best_score:
                best_score = value
                best_student = key
        return best_student

def titleize(input):
    words = input.split()
    littlewords = ["a", "on", "an", "the", "of", "and", "is", "in"]

    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1:
            words[i] = word.capitalize()
        elif word.lower() not in littlewords:
            words[i] = word.capitalize()
        else:
            words[i] = word.lower()
    return " ".join(words)



def hangman(secret, guess):
    result = ""
    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result += "_"
    return result

def titleize(input):
    words = input.split()
    littlewords = ["a", "on", "an", "the", "of", "and", "is", "in"]

    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1:
            words[i] = word.capitalize()
        elif word.lower() not in littlewords:
            words[i] = word.capitalize()
        else:
            words[i] = word.lower()

    return " ".join(words)

def pig_latin(input):
    vowels = ["a", "e", "i", "o", "u"]
    words = input.split()
    result = []

    for word in words:
        if word.startswith("qu"):
            pigword = word[2:] + "quay"
        elif word[0] in vowels:
            pigword = word + "ay"
        else:
            vowelcut = 0
            while vowelcut < len(word) and word[vowelcut] not in vowels:
                if word[vowelcut:vowelcut+2] == "qu":
                    vowelcut += 2
                    break
                vowelcut += 1
            pigword = word[vowelcut:] + word[:vowelcut] + "ay"
        result.append(pigword)
    return " ".join(result)

# temporary change to allow PR

