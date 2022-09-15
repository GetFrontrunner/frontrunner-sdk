import os
import logging
from strategy.market_making import Model

grantee_private_key = os.getenv("grantee_private_key")  # None
grantee_inj_address = os.getenv("grantee_inj_address")  # None

granter_private_key = os.getenv("granter_private_key")  # None
granter_inj_address = os.getenv("granter_inj_address")  # None

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)

if grantee_private_key and granter_inj_address:
    model = Model(
        private_key=grantee_private_key, topics=["Matchbook/events"], is_testnet=True
    )
    # model.create_granters([granter_inj_address])
    model.create_granters()
    loop = model.get_loop()
    loop.run_until_complete(model.run())
    # loop.create_task(model.run())
    # loop.run_forever()
    # model.create_limit_orders_for_granters()
    # model.create_market_orders_for_granters()
else:
    raise Exception("private key is None")
