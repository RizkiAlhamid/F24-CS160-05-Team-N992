import os

def get_env_variable(var_name: str, default: str = "") -> str:
    value = os.getenv(var_name, default)
    if value == "":
        print("Environment variable is not defined var_name= ", var_name)
    return value



