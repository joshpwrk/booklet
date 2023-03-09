# Matching Engine

## Installing Redis Server

On Linux
```bash
sudo apt update.
sudo apt install redis-server.
sudo systemctl start redis-server path_to_redis.conf
redis-cli ping
```

On Mac
```bash
brew install redis
redis-server path_to_redis.conf
redis-cli ping
```

## Testing
testing scripts will spin up and wind down redis servers on their own

```bash
python -m unittest -v matching_engine/test/*.py
```


