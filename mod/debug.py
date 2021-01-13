#!/usr/bin/env python3
# debug.py
# clyde
import tracemalloc, asyncio, threading, os, psutil

async def track_memory_loop():
    # create a global last_snapshot variable for
    # use across functions in the new thread
    global last_snapshot
    global old_bytes
    last_snapshot = tracemalloc.take_snapshot()
    old_bytes = get_bytes()
    # the above line gets the amount of memory used by the
    # process, in bytes. i leave it in byte format

    # forever. the function will never return and
    # the run_until_complete will run forever
    while True:
        # now, this does not execute every hour.
        # it executes with a delay of 1 hour,
        # after execution is finished. if i wanted
        # a perfect hour i could track execution time.

        snapshot = tracemalloc.take_snapshot()
        bytes = get_bytes()
        log_changes(snapshot, bytes)

        # delay
        await asyncio.sleep(3600)

def snap():
    snapshot = tracemalloc.take_snapshot()
    bytes = get_bytes()
    log_changes(snapshot, bytes)

def log_changes(new_snap, current_bytes):
    global old_bytes
    global last_snapshot

    print('')
    # get changes in memory
    changes = new_snap.compare_to(last_snapshot, 'lineno')

    # enumerate through changes list and print top 10
    print(f'[Memory tracking - Changes - Call Thread {threading.current_thread().name}]')
    print(f'Change in memory usage: {(old_bytes - current_bytes) / 1000} kb')
    for stat in changes[:10]:
        print(stat)

    # set last snapshot to current snapshot
    # and old bytes to current bytes
    last_snapshot = new_snap
    old_bytes = current_bytes

    print('')

def get_bytes() -> int:
    return psutil.Process(os.getpid()).memory_info().rss

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
    # start tracking memory allocation
    tracemalloc.start()

    # create new thread and set it as a daemon
    # set thread target as the loop_init method so
    # that it gets executed on the new thread
    thread = threading.Thread(target=loop_init, args=(), name='MemoryDebugThread')
    thread.daemon = True
    thread.start()
