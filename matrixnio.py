import asyncio

from nio import AsyncClient, MatrixRoom, RoomMessageText


async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    print(
        f"Message received in room {room.display_name}\n"
        f"{room.user_name(event.sender)} | {event.body}"
    )


async def main() -> None:
    client = AsyncClient("https://matrix.ether.ai", "logbot")
    client.add_event_callback(message_callback, RoomMessageText)

    print(await client.login("usb33java"))
    # "Logged in as @alice:example.org device id: RANDOMDID"

    # If you made a new room and haven't joined as that user, you can use
    # await client.join("your-room-id")

    await client.room_send(
        # Watch out! If you join an old room you'll see lots of old messages
        room_id="!nXDYFQhwioFnAwUHiB:ether.ai",
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": "How do we make this read files?"
        }
    )
    await client.sync_forever(timeout=30000)  # milliseconds


asyncio.get_event_loop().run_until_complete(main())

