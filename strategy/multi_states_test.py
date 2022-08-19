import os
import logging

from strategy.multi_states_market_market_making import MultiStatesMarketModel

grantee_private_key = os.getenv("grantee_private_key")  # None
grantee_inj_address = os.getenv("grantee_inj_address")  # None

#
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)

if grantee_private_key:
    model = MultiStatesMarketModel(
        private_key=grantee_private_key,
        topics=["BetRadar/probabilities"],
        is_testnet=True,
    )
    model.create_granters_for_multi_states_markets()
    loop = model.get_loop()
    loop.run_until_complete(model.run())
else:
    raise Exception("private key is None")
