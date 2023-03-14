# Booklet
Monorepo of a super light order-book for pre-PMF exchanges.

The goals is to create the simplest MVP that'll break just beyond the point of Product-Market-Fit.

## PMF

Defining this is tough, but using dYdX/Deribit as a conservative threshold, we can come to these conclusions:
- <2,000 req/sec (5MMs @ Deribit rate limits + 500 traders / sec), latency around 100ms 
- up to 1GB live order-book size
- up to 500 traders per sec + ~5 highly-active market makers 
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
1) Redis Server: `redis-server path-to/booklet/matching_engine/redis.conf`, use `redis-cli --stat` to monitor
2) Engine: `cd matching_engine` -> `source venv/bin/activate` -> `python3 server.py`
3) Websocket Server: `cd websocket` -> `node server.js`
4) Booklet Visualizer: `cd matching_engine` -> `source venv/bin/activate` -> `cd test` -> `python3 terminalBooklet.py`
5) Mock Clients: load testing, simulations and latency mock clients can be found in `websocket/test`

Note: on MacOS there are many system controls preventing large number of socket connections from being open:
https://k6.io/docs/misc/fine-tuning-os/
https://socket.io/docs/v4/performance-tuning/
