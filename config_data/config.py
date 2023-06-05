from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class TgBot:
    token: str


@dataclass
class TCSClient:
    token: str


@dataclass
class Config:
    tcs_client: TCSClient
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('TG_TOKEN')),
                  tcs_client=TCSClient(token=env('TCS_TOKEN')),
                  db=DatabaseConfig(database=env('DATABASE'),
                                    db_host=env('DB_HOST'),
                                    db_user=env('DB_USER'),
                                    db_password=env('DB_PASSWORD')))
