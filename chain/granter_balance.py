import os
import asyncio
import logging

from pyinjective.async_client import AsyncClient
from pyinjective.constant import Network


async def check_portfolio(inj_address: str) -> None:
    network = Network.testnet()
    client = AsyncClient(network, insecure=False)
    portfolio = await client.get_portfolio(account_address=inj_address)
    # print(type(portfolio.subaccount))
    logging.info(f"Portfolio {portfolio.portfolio.subaccounts[0].subaccount_id}")
    logging.info(f"Portfolio {portfolio.portfolio.subaccounts[0]}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    granter_inj_address = os.getenv("granter_inj_address")  # None
    if granter_inj_address is not None:
        asyncio.get_event_loop().run_until_complete(
            check_portfolio(granter_inj_address)
        )
    else:
        logging.info(f"granter address not None")
