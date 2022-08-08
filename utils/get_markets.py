from requests import get


data = get(
    "https://k8s.testnet.lcd.injective.network/injective/exchange/v1beta1/binary_options/markets"
)
