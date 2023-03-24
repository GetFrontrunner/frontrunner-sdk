from typing import Any
from typing import Mapping

from attr import dataclass


@dataclass(frozen=True)
class FrontrunnerExceptionDetail:
  subjects: Mapping[str, Any]
  reason: str


class FrontrunnerException(Exception):

  def __init__(self, reason: str, **kwargs: Any):
    super().__init__(reason)
    self.detail = FrontrunnerExceptionDetail(reason=reason, subjects=kwargs)

  def __str__(self) -> str:
    parts = [
      self.detail.reason,
      *[f"{key}={repr(subject)}" for key, subject in sorted(self.detail.subjects.items(), key=lambda item: item[0])],
    ]

    return " ".join(parts)


class FrontrunnerConfigurationException(FrontrunnerException):

  def __init__(self, reason: str, **kwargs: Any):
    super().__init__(reason, **kwargs)


class FrontrunnerInjectiveException(FrontrunnerException):

  def __init__(self, reason: str, **kwargs: Any):
    super().__init__(reason, **kwargs)
