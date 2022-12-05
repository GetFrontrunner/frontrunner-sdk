import os
import logging
from strategy.market_making import Model

grantee_private_key = os.getenv("grantee_private_key")  # None
grantee_inj_address = os.getenv("grantee_inj_address")  # None

frontrunner_test_1_pk = os.getenv("frontrunner_test_1_private_key")
frontrunner_test_1_ia = os.getenv("frontrunner_test_1_inj_address")
print(frontrunner_test_1_pk)

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)

if frontrunner_test_1_pk:
    model = Model(
        private_key=frontrunner_test_1_pk,
        topics=["BetRadar/probabilities"],
        is_testnet=True,
    )
    # model.create_granters([granter_inj_address])
    model.create_granters_for_bi_states_markets()
    loop = model.get_loop()
    loop.run_until_complete(model.run())
    # loop.create_task(model.run())
    # loop.run_forever()
    # model.create_limit_orders_for_granters()
    # model.create_market_orders_for_granters()
else:
    raise Exception("private key is None")
