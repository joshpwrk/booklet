# Booklet
Monorepo of a super light order-book I built in <1 week as a hands-on tutorial of what makes up an orderbook.

The goals is to create the simplest PoC that provides a starting point for developing a scalable orderbook back-end.

## What it can handle on your laptop

- ~500 req/sec 
- up to 1GB live order-book size
- up to 100 clients per sec (mostly a max-file system constraint) 
- Simple orderbook terminal visualizer

All the things it doesn't do:
- No connection to ETH and/or L2 JSON RPC
- No load balancer / Docker containers / middleware
- Nothing other than simple limit-orders

## Components

Matching Engine: Python (majority of matching / sorting done via Redis)
Orderbook: Redis
Server: NodeJS Websocket
Visualizer: Simple terminal script

## Running Locally 
Running bare-bones locally consists of three steps:
1) Redis Server: `redis-server path-to/booklet/matching_engine/redis.conf`, use `redis-cli --stat` to monitor
2) Engine: `cd matching_engine` -> `source venv/bin/activate` -> `python3 server.py`
3) Websocket Server: `cd websocket` -> `node server.js`
4) Booklet Visualizer: `cd matching_engine` -> `source venv/bin/activate` -> `cd test` -> `python3 terminalBooklet.py`
5) Mock Clients: load testing, simulations and latency mock clients can be found in `websocket/test`

Note: on MacOS there are many system controls preventing large number of socket connections from being open:
https://k6.io/docs/misc/fine-tuning-os/
https://socket.io/docs/v4/performance-tuning/
