import asyncio
import json

import aio_pika


async def main() -> None:
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@172.18.0.3/",
    )

    async with connection:
        routing_key = "from_fastapi"

        channel = await connection.channel()
        some_dict = {
            "tg_user_id": "fdgf"
        }
        message_body = json.dumps(some_dict)

        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body.encode()),
            routing_key=routing_key,
        )


if __name__ == "__main__":
    asyncio.run(main())