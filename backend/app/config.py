from pydantic import BaseModel
import os
class Settings(BaseModel):
    database_url: str = os.getenv('DATABASE_URL','postgresql+psycopg://limpeza:limpeza@postgres:5432/limpeza')
    secret_key: str = os.getenv('SECRET_KEY','dev-change-me')
    access_token_minutes: int = int(os.getenv('ACCESS_TOKEN_MINUTES','30'))
    refresh_token_days: int = int(os.getenv('REFRESH_TOKEN_DAYS','7'))
settings=Settings()
