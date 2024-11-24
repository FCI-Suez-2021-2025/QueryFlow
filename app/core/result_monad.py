from typing import Generic, TypeVar, Union, Optional

T = TypeVar("T")  # Represents the successful value type
E = TypeVar("E")  # Represents the error type (can be any type)


class Result(Generic[T]):
    """Base class for Result monad."""

    def is_success(self) -> bool:
        raise NotImplementedError()

    def is_failure(self) -> bool:
        return not self.is_success()

    def unwrap(self) -> T:
        raise NotImplementedError()


class Success(Result[T]):
    """Represents a successful result."""

    def __init__(self, value: T):
        self.value = value

    def is_success(self) -> bool:
        return True

    def unwrap(self) -> T:
        return self.value


class Failure(Generic[E, T], Result[T]):
    """Represents a failed result with an error."""

    def __init__(self, error: E, fallback_value: T = None):
        self.error = error
        self.fallback_value = fallback_value

    def is_success(self) -> bool:
        return False

    def unwrap_error(self) -> E:
        return self.error

    def unwrap(self) -> T:
        if self.fallback_value is not None:
            return self.fallback_value
        raise RuntimeError(
            f"Cannot unwrap Failure without fallback value. Error: {self.error}"
        )
