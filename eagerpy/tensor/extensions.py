from typing import TypeVar, Callable, Any, Generic
import typing
import functools

from .. import norms

from .tensor import Tensor


T = TypeVar("T")


def extensionmethod(f: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(f)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        return f(self._instance, *args, **kwargs)

    return wrapper


class ExtensionMeta(type):
    def __new__(cls, name, bases, attrs):  # type: ignore
        if bases == ():
            # creating the ExtensionMethod class
            # remember all attributes
            cls._base_attrs = attrs.keys()
        else:
            # creating a subclass of ExtensionMethods
            # wrap all new attributes with extensionmethod
            known = cls._base_attrs
            attrs = {
                k: extensionmethod(v) if k not in known else v for k, v in attrs.items()
            }
        return super().__new__(cls, name, bases, attrs)


if hasattr(typing, "GenericMeta"):  # Python 3.6
    # workaround for https://github.com/python/typing/issues/449
    class GenericExtensionMeta(typing.GenericMeta, ExtensionMeta):
        pass


else:  # Python 3.7 and newer

    class GenericExtensionMeta(ExtensionMeta):  # type: ignore
        pass


class ExtensionMethods(metaclass=GenericExtensionMeta):
    def __init__(self, instance: Tensor) -> None:
        self._instance = instance


T_co = TypeVar("T_co", bound=Tensor, covariant=True)


class NormsMethods(Generic[T_co], ExtensionMethods):
    l0: Callable[..., T_co] = norms.l0
    l1: Callable[..., T_co] = norms.l1
    l2: Callable[..., T_co] = norms.l2
    linf: Callable[..., T_co] = norms.linf
    lp: Callable[..., T_co] = norms.lp