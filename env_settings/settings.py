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
    terfit_admins_group_id: int = Field(alias="terfit_admins_group_id")
    terfit_discussion_group_id: int = Field(aslias="terfit_discussion_group_id")
    athletx_admins_group_id: int = Field(alias="athletx_admins_group_id")
    athletx_discussion_group_id: int = Field(aslias="athletx_discussion_group_id")
    assistant_token: str = Field(alias="assistant_token")
    terfit_assistant_id: str = Field(alias="terfit_assistant_id")
    athletx_assistant_id: str = Field(alias="athletx_assistant_id")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
