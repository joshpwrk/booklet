# Booklet
Monorepo of a super light order-book for pre-PMF exchanges.

The goals is to create the simplest MVP that'll break just beyond the point of Product-Market-Fit.

## PMF

Defining this is tough, but using dYdX/Deribit as a conservative threshold, we can come to these conclusions:
- @ 10,000 req/sec, response around 100ms 
- up to 1GB live order-book size
- up to 200 traders per sec + ~5 highly-active market makers 
- Catch up to latest order-book state in <5 sec
- Ability to roll back if settlement layer reverts

Some other important atttributes:
- Chain / settlement agnostic
- KYC plug-in functionality
- An easy language that the whole team can contrubite in

## Architecture [In-Progress]

Language: Python
REST + WebSocket + Redis

## Running Locally [In-Progress]
Running bare-bones locally consists of three steps:
1) Redis Server: `redis-server path-to/booklet/matching_engine/redis.conf`
2) Engine: `cd matching_engine` -> `source venv/bin/activate` -> `python3 server.py`
3) Websocket Server: `cd websocket` -> `node server.js`
4) Booklet Visualizer: `cd matching_engine` -> `source venv/bin/activate` -> `cd test` -> `python3 terminalBooklet.py`