from typing import Dict


def get_cleaned_args(locals: Dict) -> Dict:
  args = locals.copy()
  args.pop("self", None)
  return args
