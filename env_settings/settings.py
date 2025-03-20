from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class  ProjectSettings(BaseSettings):
    """Валидационная модель для данных проекта"""
    db_host: str = Field(alias="db_host")
    db_port: int = Field(alias="db_port")
    db_name: str = Field(alias="db_name")
    db_user: str = Field(alias="db_user")
    db_pass: str = Field(alias="db_pass")
    bot_token: str = Field(alias="bot_token")
    admins_group_id: int = Field(alias="admins_group_id")
    discussion_group_id: int = Field(aslias="discussion_group_id")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
