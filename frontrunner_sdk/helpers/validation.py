from datetime import datetime
from typing import Any
from typing import Optional

from frontrunner_sdk.exceptions import FrontrunnerArgumentException


def validate_mutually_exclusive(name1: str, val1: Optional[Any], name2: str, val2: Optional[Any]):
  if val1 is not None and val2 is not None:
    kwargs = {name1: val1, name2: val2}
    raise FrontrunnerArgumentException(f"'{name1}' and '{name2}' are mutually exclusive", **kwargs)


def validate_start_time_end_time(start_time: Optional[datetime], end_time: Optional[datetime]):
  now = datetime.now()

  if start_time and start_time > now:
    raise FrontrunnerArgumentException(
      "Start time cannot be in the future",
      now=now,
      start_time=start_time,
    )

  if end_time and end_time > now:
    raise FrontrunnerArgumentException(
      "End time cannot be in the future",
      now=now,
      end_time=end_time,
    )

  if start_time and end_time and start_time > end_time:
    raise FrontrunnerArgumentException(
      "Start time cannot be after end time",
      start_time=start_time,
      end_time=end_time,
    )
