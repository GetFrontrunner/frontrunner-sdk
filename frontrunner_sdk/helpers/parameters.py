from typing import Any
from typing import Dict
from typing import List
from typing import Tuple


def as_request_args(args: Dict[str, Any]) -> Dict:
  kwargs = args.copy()
  kwargs.pop("self", None)
  return kwargs


def ignore_none(args: List[Tuple[str, Any]]) -> Any:
  return {k: v for (k, v) in args if v is not None}
