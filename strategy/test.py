import os
from market_making import Model

grantee_private_key = os.getenv("grantee_private_key")  # None
grantee_inj_address = os.getenv("grantee_inj_address")  # None

granter_private_key = os.getenv("granter_private_key")  # None
granter_inj_address = os.getenv("granter_inj_address")  # None

if grantee_private_key and granter_inj_address:
    model = Model(private_key=grantee_private_key, topics=[], is_testnet=True)
    model.create_granters([granter_inj_address])
else:
    raise Exception("private key is None")
