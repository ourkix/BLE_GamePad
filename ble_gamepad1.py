
import asyncio
from bleak import BleakClient
import keyboard
from bleak import BleakScanner


TARGET_DEVICE = "LBW_GAMER"
SERVICE_UUID = "EF933FD3-F6F2-E572-EF3D-928AB415CB0E"
CHAR_UUID = "C02E69C2-E503-43F8-A74D-B95C1F5AF088"

KEY_MAP = {
    'j': 0b00000001, 'k': 0b00000010,
    'g': 0b00000100, 'h': 0b00001000,
    'w': 0b00010000, 's': 0b00100000,
    'a': 0b01000000, 'd': 0b10000000
}

async def main():
    device = await BleakScanner.find_device_by_name(TARGET_DEVICE)
    if not device:
        raise Exception("目标设备未找到")

    # 连接设备
    client = BleakClient(device.address)
    await client.connect()
    print(f"已连接到设备: {device.name}")

    key_state = 0x00
    loop = asyncio.get_event_loop()
    
    def sync_update_keys(e):
        nonlocal key_state
        if e.name in KEY_MAP:
            key_state = (key_state | KEY_MAP[e.name]) if e.event_type == keyboard.KEY_DOWN else (key_state & ~KEY_MAP[e.name])
            asyncio.run_coroutine_threadsafe(
                client.write_gatt_char(CHAR_UUID, bytes([0xBB, 0x00, key_state, 0xEE])),
                loop
            )

    for key in KEY_MAP:
        keyboard.on_press_key(key, sync_update_keys)
        keyboard.on_release_key(key, sync_update_keys)
    
    print("运行中...")
    await asyncio.Event().wait()

asyncio.run(main())
