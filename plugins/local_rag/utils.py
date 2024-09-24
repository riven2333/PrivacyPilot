import os
from contextlib import contextmanager
from importlib import import_module
from os.path import dirname, relpath
from pkgutil import iter_modules
from types import FunctionType

__all__ = ["Registry", "change_sub_dir", "import_submodules"]


@contextmanager
def change_sub_dir(path: str, create: bool = False):
    cwd = os.getcwd()
    if create:
        os.makedirs(path, exist_ok=True)
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)


def import_submodules(module_path: str = "", submodule_path: str = ""):
    if module_path == "":
        module_path = relpath(dirname(submodule_path))
    module_str = module_path.replace("\\", ".").replace("/", ".")
    for _, name, _ in iter_modules([module_path]):
        import_module(f"{module_str}.{name}")


class Registry:
    _registry = {}

    def __init__(self, *args, **kwargs):
        raise RuntimeError("Registry class cannot be instantiated")

    @classmethod
    def key_type(cls) -> type:
        raise NotImplementedError("Registry.key_type must be implemented")

    @classmethod
    def base_class(cls) -> type:
        raise NotImplementedError("Registry.base_class must be implemented")

    @classmethod
    def register(cls, key):
        def decorator(cls_type: type):
            cls._register(key, cls_type)
            return cls_type

        return decorator

    @classmethod
    def _register(cls, key, cls_type):
        if not isinstance(key, cls.key_type()):
            raise TypeError(f"Key must be of type {cls.key_type}, not {type(key)}")
        if not isinstance(cls_type, FunctionType) and not issubclass(
            cls_type, cls.base_class()
        ):
            raise TypeError(
                f"Class must be a get function or a subclass of {cls.base_class}, not {cls_type}"
            )

        cls._registry[key] = cls_type

    @classmethod
    def from_config(cls, class_config):
        pass

    @classmethod
    def get_class(cls, key, default=None):
        return cls._registry.get(key, default)

    @classmethod
    def get_all_keys(cls):
        return list(cls._registry.keys())

    @classmethod
    def has(cls, key):
        return key in cls._registry
