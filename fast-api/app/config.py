from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    app_name: str = "FastAPI CRUD Example"
    app_description: str = (
        "A small FastAPI app that demonstrates CRUD operations, external API calls, "
        "and Pydantic-powered validation."
    )
    app_version: str = "0.1.0"
    external_activity_url: HttpUrl = "https://bored-api.appbrewery.com/filter?type=education"

    class Config:
        env_file = ".env"


settings = Settings()
