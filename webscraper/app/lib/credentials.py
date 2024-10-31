import os

def get_env_variable(var_name: str, default: str = "") -> str:
    value = os.getenv(var_name, default)
    if value == "":
        print("Environment variable is not defined var_name= ", var_name)
    return value

YOUTUBE_API_KEY = get_env_variable("YOUTUBE_API_KEY")
PERPLEXITY_API_KEY = get_env_variable("PERPLEXITY_API_KEY")
OPENAI_API_KEY = get_env_variable("OPENAI_API_KEY")
ANTHROPIC_API_KEY = get_env_variable("ANTHROPIC_API_KEY")


