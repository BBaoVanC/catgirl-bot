function:

[Memory tracking - Changes - Call Thread MainThread]
Change in memory usage: -970.752 kb
C:\Python39\lib\tracemalloc.py:558: size=72.7 KiB (+67.8 KiB), count=1538 (+1445), average=48 B
C:\Python39\lib\tracemalloc.py:193: size=52.6 KiB (-15.4 KiB), count=1123 (-328), average=48 B
C:\Python39\lib\asyncio\base_events.py:729: size=1800 B (-2576 B), count=13 (-23), average=138 B
C:\Python39\lib\tracemalloc.py:115: size=96.1 KiB (+2080 B), count=1230 (+26), average=80 B
C:\Python39\lib\site-packages\aiohttp\helpers.py:494: size=960 B (+960 B), count=2 (+2), average=480 B
mod\filtercheck.py:54: size=888 B (+888 B), count=2 (+2), average=444 B
C:\Python39\lib\site-packages\aiohttp\helpers.py:493: size=816 B (+816 B), count=2 (+2), average=408 B
C:\Python39\lib\site-packages\aiohttp\tcp_helpers.py:42: size=0 B (-816 B), count=0 (-2)
C:\Python39\lib\site-packages\discord\state.py:486: size=2888 B (+792 B), count=10 (+3), average=289 B
C:\Python39\lib\asyncio\base_events.py:732: size=32 B (-680 B), count=1 (-2), average=32 B


adr:

old adr on enter cmd snap: <tracemalloc.Snapshot object at 0x000002227BD20100> Thread: MainThread
new adr on exit cmd snap: <tracemalloc.Snapshot object at 0x000002227C877C70> Thread: MainThread
old adr on enter loop snap: <tracemalloc.Snapshot object at 0x000002227C877C70> Thread: MemoryDebugThread
new adr on exit loop snap: <tracemalloc.Snapshot object at 0x000002227C9EA6D0> Thread: MemoryDebugThread
old adr on enter cmd snap: <tracemalloc.Snapshot object at 0x000002227C9EA6D0> Thread: MainThread
new adr on exit cmd snap: <tracemalloc.Snapshot object at 0x000002227C9EA8E0> Thread: MainThread
old adr on enter loop snap: <tracemalloc.Snapshot object at 0x000002227C9EA8E0> Thread: MemoryDebugThread
new adr on exit loop snap: <tracemalloc.Snapshot object at 0x000002227CB570D0> Thread: MemoryDebugThread