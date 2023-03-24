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
    reason = self.detail.reason
    subjects = " ".join([f"{key}={repr(subject)}" for key, subject in self.detail.subjects.items()])
    return f"{reason} {subjects}"


class FrontrunnerConfigurationException(FrontrunnerException):

  def __init__(self, reason: str, **kwargs: Any):
    super().__init__(reason, **kwargs)


class FrontrunnerInjectiveException(FrontrunnerException):

  def __init__(self, reason: str, **kwargs: Any):
    super().__init__(reason, **kwargs)
