from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 10080
    database_url: str = "sqlite:///./boaforma.db"
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_ssl_mode: str = ""
    trusted_hosts: str = "localhost,127.0.0.1,testserver"
    cors_allowed_origins: str = "http://localhost:3000,http://localhost:3001"
    cors_allowed_origin_regex: str = r"https?://(localhost|127\.0\.0\.1)(:\d+)?"
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    login_rate_limit: int = 30
    login_rate_window_seconds: int = 60
    login_lockout_threshold: int = 5
    login_lockout_seconds: int = 300
    chat_rate_limit: int = 60
    chat_rate_window_seconds: int = 60
    workout_rate_limit: int = 30
    workout_rate_window_seconds: int = 60
    llm_timeout_seconds: int = 20
    llm_max_retries: int = 2
    llm_retry_backoff_seconds: float = 0.6
    llm_enable_fallback: bool = True
    google_oauth_client_id: str = ""
    social_default_age: int = 25
    social_default_weight_kg: float = 70
    social_default_height_cm: float = 170
    social_default_goal: str = "saude"
    social_default_level: str = "iniciante"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    @property
    def trusted_hosts_list(self) -> list[str]:
        return [host.strip() for host in self.trusted_hosts.split(",") if host.strip()]


settings = Settings()
