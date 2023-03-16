# Lyra Orderbook
This repo contains all the pods / images required to deploy an off-chain orderbook. The goal is to start with a scalable / modular system using Kubernetes + Redis.

## PMF

Defining this is tough, but using dYdX/Deribit as a conservative threshold, we can come to these conclusions:
- <2,500 req/sec (3MMs @ Deribit rate limits + 1000 traders / sec)
- @ 500 tps: <10ms
- @ 2,500 tps: <100ms
- Catch up to latest order-book state in <5 sec
- Ability to roll back if settlement layer reverts

Some other important atttributes:
- Chain / settlement agnostic
- KYC plug-in functionality
- An easy language that the whole team can contrubite in

## Architecture [In-Progress]

Language: Python
WebSocket + Redis

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
