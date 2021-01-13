#!/usr/bin/env python3
# debug.py
# clyde
import tracemalloc, asyncio, threading

async def track_memory_loop():
    last_snapshot = tracemalloc.take_snapshot()

    # forever. the function will never return and
    # the run_until_complete will run forever
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

    # create a new loop for our thread because
    # by default there isn't an event loop
    # we also have to set the thread's event
    # loop to the loop we just created
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    # create tasks and start on the event loop
    # note that this is a list object
    tasks = [event_loop.create_task(track_memory_loop())]

    # run the task. will never be completed.
    event_loop.run_until_complete(asyncio.wait(tasks))

def spawn_debug_thread():
    # start tracking memory
    tracemalloc.start()

    # create new thread and set it as a daemon
    # set thread target as the loop_init method so
    # that it gets executed on the new thread
    thread = threading.Thread(target=loop_init, args=())
    thread.daemon = True
    thread.start()
