from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My App"
    environment: str = "development"
    debug: bool = False

settings = Settings()
print(f"App Name: {settings.app_name}")
print(f"Environment: {settings.environment}")
print(f"Debug Mode: {settings.debug}")
