from typing import Any, AsyncIterable
from typing import AsyncIterator
from typing import Awaitable
from typing import Callable
from typing import TypeVar

Item = TypeVar("Item")


async def injective_stream_iterator(
        call: Callable[..., Awaitable[AsyncIterable]],
        field: str,
        *call_args: Any,
        **call_kwargs: Any,
) -> AsyncIterator[Item]:

    response = await call(*call_args, **call_kwargs)

    async for item in response:
        yield getattr(item, field)


async def injective_stream(
        call: Callable[..., Awaitable[AsyncIterable]],
        field: str,
        *call_args: Any,
        **call_kwargs: Any,
) -> AsyncIterator[Item]:
    response: AsyncIterator[Item] = injective_stream_iterator(call, field, *call_args, **call_kwargs)
    return response
