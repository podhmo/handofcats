import typing as t
import dataclasses


@dataclasses.dataclass(frozen=True)
class CodegenConfig:
    inplace: bool = False
    typed: bool = True
    use_primitive_parser: bool = False

    @classmethod
    def as_simple(cls, *, inplace: bool) -> "CodegenConfig":
        return cls(inplace=inplace, typed=False, use_primitive_parser=False)


@dataclasses.dataclass(frozen=True)
class Config:
    ignore_logging: bool = False
    ignore_expose: bool = False
    cont: t.Callable[[t.Any], t.Any] = print
    codegen_config: CodegenConfig = dataclasses.field(default_factory=CodegenConfig)


default_config = Config()
