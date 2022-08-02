from pyinjective.async_client import AsyncClient
from pyinjective.constant import Network  # , Denom
from pyinjective.composer import Composer


def build_client(node_idx=3, nodes=["sentry0", "sentry1", "sentry3", "k8s"]):
    node_idx %= len(nodes)
    network = Network.mainnet(node=nodes[node_idx])
    composer = Composer(network=network.string())
    client = AsyncClient(network, insecure=False if node_idx == 3 else True)
    lcd_endpoint = network.lcd_endpoint
    return node_idx, network, composer, client, lcd_endpoint


def switch_node(node_idx=3, nodes=["sentry0", "sentry1", "sentry3", "k8s"]):
    node_idx += 1
    node_idx %= len(nodes)
    network = Network.mainnet(node=nodes[node_idx])
    composer = Composer(network=network.string())
    client = AsyncClient(network, insecure=False if node_idx == 3 else True)
    lcd_endpoint = network.lcd_endpoint
    return node_idx, network, composer, client, lcd_endpoint
