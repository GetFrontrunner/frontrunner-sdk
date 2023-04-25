from dataclasses import dataclass
from typing import Any
from typing import Mapping


@dataclass(frozen=True)
class FrontrunnerExceptionDetail:
  subjects: Mapping[str, Any]
  reason: str


class FrontrunnerException(Exception):
  """Base exception type."""

  def __init__(self, reason: str, **kwargs: Any):
    super().__init__(reason)
    self.detail = FrontrunnerExceptionDetail(reason=reason, subjects=kwargs)

  def __str__(self) -> str:
    parts = [
      self.detail.reason,
      *[f"{key}={repr(subject)}" for key, subject in sorted(self.detail.subjects.items(), key=lambda item: item[0])],
    ]

    return " ".join(parts)


class FrontrunnerUserException(FrontrunnerException):
  """Exception where the user is at fault."""

  def __init__(self, reason: str, **kwargs: Any):
    if self.__class__ == FrontrunnerUserException:
      raise TypeError(f"Do not directly instantiate {self.__class__.__name__}")

    super().__init__(reason, **kwargs)


class FrontrunnerExternalException(FrontrunnerException):
  """Exception where the user is not at fault."""

  def __init__(self, reason: str, **kwargs: Any):
    if self.__class__ == FrontrunnerExternalException:
      raise TypeError(f"Do not directly instantiate {self.__class__.__name__}")

    super().__init__(reason, **kwargs)


class FrontrunnerConfigurationException(FrontrunnerUserException):

  def __init__(self, reason: str, **kwargs: Any):
    super().__init__(reason, **kwargs)


class FrontrunnerArgumentException(FrontrunnerUserException):

  def __init__(self, reason: str, **kwargs: Any):
    super().__init__(reason, **kwargs)


class FrontrunnerInjectiveException(FrontrunnerUserException):

  def __init__(self, reason: str, **kwargs: Any):
    super().__init__(reason, **kwargs)


class FrontrunnerUnserviceableException(FrontrunnerExternalException):

  def __init__(self, reason: str, **kwargs: Any):
    super().__init__(reason, **kwargs)
