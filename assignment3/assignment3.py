#task1
# log-decorator.py
import logging

# === Logger Setup ===
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

# === Task 1: Writing and Testing a Decorator ===
def logger_decorator(func):
    def wrapper(*args, **kwargs):
        # Call the original function
        result = func(*args, **kwargs)

        # Prepare values for logging
        pos_args = args if args else "none"
        kw_args = kwargs if kwargs else "none"

        log_message = (
            f"function: {func.__name__} | "
            f"positional parameters: {pos_args} | "
            f"keyword parameters: {kw_args} | "
            f"return: {result}"
        )
        logger.info(log_message)
        return result
    return wrapper

# === Example Function 1 ===
@logger_decorator
def hello_world():
    print("Hello, World!")

# === Example Function 2 ===
@logger_decorator
def always_true(*args):
    return True

# === Example Function 3 ===
@logger_decorator
def keyword_args_only(**kwargs):
    return logger_decorator  # returning the decorator function itself

# === Main Program ===
if __name__ == "__main__":
    hello_world()
    always_true(1, 2, 3)
    keyword_args_only(name="Tom", mood="focused")
