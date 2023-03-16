# syntax=docker/dockerfile:1

FROM redis:7-alpine
COPY . .
COPY redis.conf /usr/local/etc/redis/redis.conf
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
EXPOSE 6379