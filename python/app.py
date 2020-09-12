import simplejson as json
import asyncio
from aiofile import AIOFile
import io
import sys
import re
import time
import logging

import os
import os.path
from os import path
from os import environ

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

# load tracked orders from json file
async def save_tracked_orders(dt, trackedOrders):
    try:
        if len(Settings.tracked_orders.trackedOrders) == 0:
            return

        filename = get_tracked_order_filename(dt)

        data = json.dumps(trackedOrders, default=lambda o: o.__dict__, sort_keys=True, indent=4)

        async with AIOFile(filename, 'w+') as afp:
            await afp.write(data)
            await afp.fsync()

            LOGGER.info(f'Saved {len(Settings.tracked_orders.trackedOrders)} tracked orders in file {filename}')

    except Exception as ex:
        LOGGER.error(f'Failed to load from tracked orders file {filename}')
        LOGGER.error('An unexpected error occurred in the main loop: {}'.format(ex))
        LOGGER.fatal(ex, exc_info=True)


async def OpenJsonDataFile():
    try:
        filename = 'data.json'
        if path.exists(filename) == False:
            return

        async with AIOFile(filename, 'r+') as afp:
            data = await afp.read()

            dataObjs = json.loads(data)
            LOGGER.info(f'Loaded json data from file {filename}')

            for dataObj in dataObjs:
                print(dataObj['category'])
                print(dataObj['name'])

            return dataObjs

    except Exception as ex:
        LOGGER.error(f'Failed to load from json data file {filename}')
        LOGGER.error('An unexpected error occurred in the main loop: {}'.format(ex))
        LOGGER.fatal(ex, exc_info=True)

    return None


try:
    loop = asyncio.get_event_loop()
    task1 = loop.create_task(OpenJsonDataFile())
    loop.run_until_complete(asyncio.gather(task1))
except KeyboardInterrupt:
    pass
except Exception as ex:
    LOGGER.error('An unexpected error occurred in the main loop: {}'.format(ex))
    LOGGER.fatal(ex, exc_info=True)
finally:
    time.sleep(3)
    loop.close()
 