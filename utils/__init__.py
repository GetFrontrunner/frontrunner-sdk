import os
import sys
from typing import Dict, Optional
from objects import OrderInfo


def check_env_is_set(env_name: str):
    try:
        if os.environ[env_name]:
            print(f"error: {env_name} is set to {os.environ[env_name]}")
            sys.exit(1)
    except KeyError:
        pass
        # print(f"{env_name} is not set.")


def check_env_is_on(env_name: str):
    # Checking the value of the environment variable
    if os.environ.get(env_name):
        print(f"{env_name}    is on")
    else:
        print(f"{env_name}    is off")


def set_env(env_name: str, env_value: str, file_location: str):
    os.environ.setdefault(env_name, env_value)
    with open(file_location, "a") as file:
        file.write("export {env_name}={env_value}")
    print(f"{env_name} has saved to {file_location}")


def set_env_variables(secret_obj: Dict[str, str], file_location: str):
    for key, value in secret_obj.items():
        if key in ("inj_address", "inj_private_key"):
            check_env_is_set(key.upper())
            set_env(key.upper(), value, file_location)


def get_env(env_name: str) -> Optional[str]:
    return os.environ.get(env_name)


def order_info(order_info_str: str, market_map: Dict[str, str]) -> OrderInfo:
    order_infos = order_info_str.split(",")
    return OrderInfo(
        market_id=market_map[order_infos[0]],
        side=order_infos[1],
        price=float(order_infos[2]),
        quantity=int(order_infos[3]),
        post_only=order_infos[4] == "true",
        reduce_only=order_infos[5] == "false",
    )
