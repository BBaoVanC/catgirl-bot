#!/usr/bin/env python3
# debug.py
# clyde
import tracemalloc, asyncio, threading

async def do_loop():
    last_snapshot = tracemalloc.take_snapshot()

    while True:
        print('')
        snapshot = tracemalloc.take_snapshot()
        
        # get changes in memory
        changes = snapshot.compare_to(last_snapshot, 'lineno')

        print("[Memory tracking - Changes in last hour]")
        for stat in changes[:10]:
            print(stat)

        print('')
        last_snapshot = snapshot
        await asyncio.sleep(3600)

def loop_init():

    # create a new event loop for our thread
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    # create tasks and start on the event loop
    tasks = list()
    tasks.append(event_loop.create_task(do_loop()))
    event_loop.run_until_complete(asyncio.wait(tasks))

def start_run_loop():
    # start tracking memory
    tracemalloc.start()

    # create new thread and set it as a daemon
    thread = threading.Thread(target=loop_init, args=())
    thread.daemon = True
    thread.start()
