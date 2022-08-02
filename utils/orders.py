from sortedcontainers import SortedList
from typing import List, Optional
from pyinjective.orderhash import build_eip712_msg, domain_separator
from sha3 import keccak_256 as sha3_keccak_256
from requests import get


class Order:
    def __init__(self, price: float, quantity: float, order_type: str, msg):
        self.price = price
        self.quantity = quantity
        self.hash: Optional[str] = None
        self.order_type = order_type
        self.msg = msg

    def update_orderhash(self, orderhash):
        self.hash = orderhash


class OrderList:
    def __init__(self):
        self.list: SortedList = SortedList([], key=lambda x: x.price)

    def add(self, order: Order):
        self.list.add(order)

    def remove(self, orderhash: str):
        for order in self.list:
            if order.orderhash == orderhash:
                self.list.remove(order)


def compute_order_hashes(orders: List[Order], lcd_endpoint: str):
    # get starting nonce
    nonce = get_subaccount_nonce(orders[0].msg.order_info.subaccount_id, lcd_endpoint)
    # logging.info("starting subaccount nonce: %d" % nonce)
    # compute hashes
    # order_hashes = []
    for order in orders:
        # increase nonce for next order
        nonce += 1
        # construct eip712 msg
        msg = build_eip712_msg(order.msg, nonce)
        # compute order hash
        if msg is not None:
            typed_data_hash = msg.hash_struct()
            typed_bytes = b"\x19\x01" + domain_separator + typed_data_hash
            keccak256 = sha3_keccak_256()
            keccak256.update(typed_bytes)
            order_hash = keccak256.hexdigest()
            order.hash = f"0x{order_hash}"


def get_subaccount_nonce(subaccount_id: str, lcd_endpoint: str) -> int:
    url = f"{lcd_endpoint}/injective/exchange/v1beta1/exchange/{subaccount_id}"
    n = 3
    while n > 0:
        res = get(url=url)
        if res.status_code != 200:
            n -= 1
            # raise Exception(f"failed to get subaccount nonce {res}")
        return res.json()["nonce"]
    return 0
