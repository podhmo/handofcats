import dataclasses


@dataclasses.dataclass
class Config:
    ignore_logging: bool = False
    ignore_expose: bool = False


default_config = Config()
