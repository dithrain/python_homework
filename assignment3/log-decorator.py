import logging

#logger import
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

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

@logger_decorator
def hello_world():
    print("Hello, World!")

@logger_decorator
def always_true(*args):
    return True

@logger_decorator
def keyword_args_only(**kwargs):
    return logger_decorator  # returning the decorator function itself

if __name__ == "__main__":
    hello_world()
    always_true(1, 2, 3)
    keyword_args_only(name="Tom", mood="focused")
