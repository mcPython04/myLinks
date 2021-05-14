import asyncio
import time

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
    file_path = 'logs/myLinks.log'

    # Referenced from stack overflow https://stackoverflow.com/a/24818607
    last_line = None
    with open(file_path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            last_line = line

    while True:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        if lines[-1] != last_line:
            last_line = lines[-1]
            await client.room_send(
                # Watch out! If you join an old room you'll see lots of old messages
                room_id="!nXDYFQhwioFnAwUHiB:ether.ai",
                message_type="m.room.message",
                content={
                    "msgtype": "m.text",
                    "body": lines[-1]
                }
            )
        time.sleep(0.00000000000001)

    # while True:
    #     line = file1.readline()
    #
    #     if not line:
    #         await client.sync_forever(timeout=1000)  # milliseconds
    #
    #     else:
    #         await client.room_send(
    #             # Watch out! If you join an old room you'll see lots of old messages
    #             room_id="!nXDYFQhwioFnAwUHiB:ether.ai",
    #             message_type="m.room.message",
    #             content={
    #                 "msgtype": "m.text",
    #                 "body": line
    #             }
    #         )
    await client.sync_forever(timeout=30000)  # milliseconds


asyncio.get_event_loop().run_until_complete(main())

