from decimal import Decimal, getcontext
from typing import Optional

"""
market_type = str(input("Enter spot or derivative as market type:"))
maker = Decimal(input("Enter the maker fees:"))
taker = Decimal(input("Enter the taker fees:"))

if market_type == "spot":
    price_tick_size = Decimal(input("Enter the price tick size:"))
    quantity_tick_size = Decimal(input("Enter the quantity tick size:"))
    quote_decimals = Decimal(input("Enter the decimals for the quote asset:"))
    base_decimals = Decimal(input("Enter the decimals for the base asset:"))

    print("maker fees:", f"{Decimal(maker / 100):.18f}")
    print("taker fees:", f"{Decimal(taker / 100):.18f}")
    print(
        "price tick size:",
        f"{Decimal(price_tick_size) * pow(10, quote_decimals - base_decimals):.18f}",
    )
    print(
        "quantity tick size: ",
        f"{Decimal(quantity_tick_size) / pow(10, - base_decimals):.18f}",
    )

elif market_type == "derivative":
    price_tick_size = Decimal(input("Enter the price tick size:"))
    quantity_tick_size = Decimal(input("Enter the quantity tick size:"))
    quote_decimals = Decimal(input("Enter the decimals for the quote asset:"))
    initial_margin = Decimal(input("Enter the initial margin ratio:"))
    maintenance_margin = Decimal(input("Enter the maintenance margin ratio:"))

    print("maker fees:", f"{Decimal(maker / 100):.18f}")
    print("taker fees:", f"{Decimal(taker / 100):.18f}")
    print("initial margin ratio:", f"{Decimal(initial_margin):.18f}")
    print("maintenance margin ratio:", f"{Decimal(maintenance_margin):.18f}")
    print(
        "price tick size:",
        f"{Decimal(price_tick_size) / pow(10, - quote_decimals):.18f}",
    )
    print("quantity tick size: ", f"{Decimal(quantity_tick_size):.18f}")

else:
    print("Invalid market type")
"""


def human_readable_to_on_chain(
    maker_fee_f: float,
    take_fee_f: float,
    price_tick_size_f: float,
    quantity_tick_size_f: float,
    quote_decimals_f: float,
    initial_margin_f: float,
    maintenance_margin_f: float,
):
    getcontext().prec = 18
    maker = Decimal(maker_fee_f / 100)
    taker = Decimal(take_fee_f / 100)

    quote_decimals = Decimal(quote_decimals_f)
    initial_margin = Decimal(initial_margin_f)
    price_tick_size = Decimal(price_tick_size_f) / pow(10, -quote_decimals)
    quantity_tick_size = Decimal(quantity_tick_size_f)
    maintenance_margin = Decimal(maintenance_margin_f)

    print("maker fees:", f"{Decimal(maker / 100):.18f}")
    print("taker fees:", f"{Decimal(taker / 100):.18f}")
    print("initial margin ratio:", f"{Decimal(initial_margin):.18f}")
    print("maintenance margin ratio:", f"{Decimal(maintenance_margin):.18f}")
    print(
        "price tick size:",
        f"{Decimal(price_tick_size) / pow(10, - quote_decimals):.18f}",
    )
    print("quantity tick size: ", f"{Decimal(quantity_tick_size):.18f}")
    return (
        maker,
        taker,
        price_tick_size,
        quantity_tick_size,
        quote_decimals,
        initial_margin,
        maintenance_margin,
    )


def on_chain_to_human_readable(
    maker_fee_d: Decimal,
    take_fee_d: Decimal,
    price_tick_size_d: Decimal,
    quantity_tick_size_d: Decimal,
    quote_decimals_d: Decimal,
    initial_margin_d: Decimal,
    maintenance_margin_d: Decimal,
):
    getcontext().prec = 18
    maker = float(maker_fee_d * 100)
    taker = float(take_fee_d * 100)

    quote_decimals = Decimal(quote_decimals_d)
    initial_margin = Decimal(initial_margin_d)
    price_tick_size = float(price_tick_size_d * pow(10, -quote_decimals))
    quantity_tick_size = float(quantity_tick_size_d)
    maintenance_margin = float(maintenance_margin_d)

    print("maker fees:", f"{maker}")
    print("taker fees:", f"{taker}")
    print("initial margin ratio:", f"{initial_margin}")
    print("maintenance margin ratio:", f"{maintenance_margin}")
    print(
        "price tick size:",
        f"{price_tick_size}",
    )
    print("quantity tick size: ", f"{quantity_tick_size}")
    return (
        maker,
        taker,
        price_tick_size,
        quantity_tick_size,
        quote_decimals,
        initial_margin,
        maintenance_margin,
    )


if __name__ == "__main__":
    (
        maker,
        taker,
        price_tick_size,
        quantity_tick_size,
        quote_decimals,
        initial_margin,
        maintenance_margin,
    ) = human_readable_to_on_chain(
        maker_fee_f=0.00001,
        take_fee_f=0.00001,
        price_tick_size_f=0.01,
        quantity_tick_size_f=1,
        quote_decimals_f=0.01,
        initial_margin_f=0.01,
        maintenance_margin_f=0.01,
    )

    x = on_chain_to_human_readable(
        maker_fee_d=maker,
        take_fee_d=taker,
        price_tick_size_d=price_tick_size,
        quantity_tick_size_d=quantity_tick_size,
        quote_decimals_d=quote_decimals,
        initial_margin_d=initial_margin,
        maintenance_margin_d=maintenance_margin,
    )
