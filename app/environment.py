import os

from dotenv import load_dotenv

load_dotenv()


def get_env_var(env_var: str):
    try:
        return os.environ[env_var]
    except KeyError:
        raise ValueError(f"Required environment variable '{env_var}' is not set.")


DATABASE_URL = get_env_var("DATABASE_URL")
GROQ_API_KEY = get_env_var("GROQ_API_KEY")
JWT_SECRET_KEY = get_env_var("JWT_SECRET_KEY")
OTP_SECRET_KEY = get_env_var("OTP_SECRET_KEY")
SPITCH_API_KEY = get_env_var("SPITCH_API_KEY")
