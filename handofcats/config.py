import dataclasses


@dataclasses.dataclass
class Config:
    ignore_logging: bool = False


default_config = Config()
