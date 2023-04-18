from typing import Dict


def get_cleaned_kwargs(args: Dict) -> Dict:
  kwargs = args.copy()
  kwargs.pop("self", None)
  return kwargs
