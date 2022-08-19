import os
from market_making import Model

# from dotenv import load_dotenv
# load_dotenv()
# Getting non-existent keys
grantee_private_key = os.getenv("grantee_private_key")  # None
grantee_inj_address = os.getenv("grantee_inj_address")  # None

granter_private_key = os.getenv("granter_private_key")  # None
granter_inj_address = os.getenv("granter_inj_address")  # None

print(grantee_private_key)
print(grantee_inj_address)
print(granter_private_key)
print(granter_inj_address)

if granter_private_key:
    model = Model(private_key=granter_private_key, topics=[], is_testnet=True)
    if granter_inj_address:
        model.create_granter(inj_address=granter_inj_address)
else:
    raise Exception("private key is None")
