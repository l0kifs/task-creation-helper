from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvVars(BaseSettings):
    JIRA_EMAIL: str
    JIRA_API_TOKEN: str
        
    model_config = SettingsConfigDict(env_file='.env')


def get_env_vars() -> EnvVars:
    """
    Get the environment variables from the .env file.

    Returns:
        EnvVars: An instance of the EnvVars class containing the environment variables.
    """
    env_vars = EnvVars()  # type: ignore
    return env_vars
