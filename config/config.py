from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class TgBot:
    token: str

@dataclass
class LogSettings:
    level: str
    format: str

@dataclass
class ProxySettings:
    type: str
    ip: str
    port: str
    login: str
    password: str

    @property
    def url(self) -> str | None:
        if not self.ip or not self.port:
            return None
        auth = f"{self.login}:{self.password}@" if self.login and self.password else ""
        return f"{self.type}://{auth}{self.ip}:{self.port}"

@dataclass
class Config:
    bot: TgBot
    log: LogSettings
    proxy: Optional[ProxySettings]


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    proxy_ip = env.str('PROXY_IP', default='')

    return Config(
        bot=TgBot(token=env('BOT_TOKEN')),
        log=LogSettings(
            level=env('LOG_LEVEL', default='INFO'),
            format=env('LOG_FORMAT', default='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ),
        proxy=ProxySettings(
            type=env('PROXY_TYPE', default='http'),
            ip=proxy_ip,
            port=env('PROXY_PORT', default=''),
            login=env('PROXY_LOGIN', default=''),
            password=env('PROXY_PASSWORD', default='')
        ) if proxy_ip else None,
    )