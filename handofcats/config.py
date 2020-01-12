import dataclasses


@dataclasses.dataclass(frozen=True)
class Config:
    ignore_logging: bool = False
    ignore_expose: bool = False


default_config = Config()
