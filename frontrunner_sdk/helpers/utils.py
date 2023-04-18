from typing import Any
from typing import Dict
from typing import List
from typing import Tuple


def get_cleaned_kwargs(args: Dict) -> Dict:
  kwargs = args.copy()
  kwargs.pop("self", None)
  return kwargs


def ignore_none(args: List[Tuple[str, Any]]) -> Any:
  return {k: v for (k, v) in args if v is not None}
