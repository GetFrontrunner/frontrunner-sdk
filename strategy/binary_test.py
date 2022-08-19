import os
import logging
from strategy.binary_states_market_market_making import BinaryMarketModel

grantee_private_key = os.getenv("frontrunner_test_1_private_key")
grantee_inj_address = os.getenv("frontrunner_test_1_inj_address")
logging.info(f"private_key: {grantee_private_key}")

#
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)

if grantee_private_key:
    model = BinaryMarketModel(
        private_key=grantee_private_key,
        topics=["BetRadar/probabilities"],
        is_testnet=True,
    )
    model.create_granters_for_binary_states_markets()
    loop = model.get_loop()
    loop.run_until_complete(model.run())
else:
    raise Exception("private key is None")
