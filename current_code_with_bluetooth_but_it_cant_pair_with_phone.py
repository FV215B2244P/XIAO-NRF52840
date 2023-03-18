import os
import time
import board
import digitalio
import asyncio
import adafruit_ble_file_transfer
import adafruit_ble

async def ble():
    blue = adafruit_ble.BLERadio()
    advertisement = adafruit_ble.Advertisement()
    advertisement.complete_name = "Your device name"
    advertisement.tx_power = 0
    blue.start_advertising(advertisement)

    while not adafruit_ble.BLERadio().connected:
        await asyncio.sleep(1)
        pass

    file_transfer_service = adafruit_ble_file_transfer.FileTransferService()

    while not file_transfer_service.transfer_in_progress:
        await asyncio.sleep(1)
        pass

    with open(file_transfer_service.filename, "wb") as file:
        while file_transfer_service.transfer_in_progress:
            file.write(file_transfer_service.read())
    print("Received file: {} bytes".format(os.path.getsize(file_transfer_service.filename)))
    await asyncio.sleep(1)


async def bl(led):
    while True:
        led.value = False
        await asyncio.sleep(0.1)
        led.value = True
        await asyncio.sleep(599.9)


async def gr(led):
    while True:
        led.value = False
        await asyncio.sleep(0.1)
        led.value = True
        await asyncio.sleep(59.9)


async def rd(led):
    while True:
        led.value = False
        await asyncio.sleep(0.1)
        led.value = True
        await asyncio.sleep(0.9)

l1 = digitalio.DigitalInOut(board.LED_BLUE)
l1.direction = digitalio.Direction.OUTPUT
l2 = digitalio.DigitalInOut(board.LED_GREEN)
l2.direction = digitalio.Direction.OUTPUT
l3 = digitalio.DigitalInOut(board.LED_RED)
l3.direction = digitalio.Direction.OUTPUT

lp = asyncio.get_event_loop()

lp.create_task(bl(l1))
lp.create_task(gr(l2))
lp.create_task(rd(l3))
lp.create_task(ble())

lp.run_forever()
