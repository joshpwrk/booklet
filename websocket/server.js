import { Server } from "socket.io";
import { createOrder, deleteOrder } from "./orderHandler.js";
import redis from "redis";

////////////////////////
// Redis Client Setup //
////////////////////////

const redisQueue = redis.createClient({ 
  socket: {
    host: 'localhost',
    port: 6379,
    keepAlive: true
  },
  database: 1
});
await redisQueue.connect()

const redisOrderbook = redis.createClient({ 
  socket: {
    host: 'localhost',
    port: 6379,
    keepAlive: true
  },
  database: 0
});
await redisOrderbook.connect()


// ////////////////////////////
// // Socket.io Client Setup //
// ////////////////////////////

const io = new Server({ /* options */ });


// subscribe to all changes to orderbook
await redisOrderbook.pSubscribe(
  [`__key*@*__:*`, `*`], 
  (message, channel) =>  {
    console.log(message, channel)
    const orderbook_pattern = /^__keyspace@0__:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
    const settlement_pattern = /^__keyspace@2__:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
    if (message == "set" && orderbook_pattern.test(channel)) {
      // notify when posted to orderbook
      io.emit("order:created", channel.split(":")[1])
    } else if (message == "set" && settlement_pattern.test(channel)) {
      // notify when queued to settlement
      io.emit("order:created", channel.split(":")[1])
    }
  }
)

redisQueue.on('error', err => {
  console.log('Error ' + err);
});

io.on('connection', (socket) => {
  console.log('A client connected');

  socket.on('order:create', createOrder(socket, redisQueue));
  socket.on("order:delete", deleteOrder);
});

io.listen(3000, () => {
  console.log('Server listening on port 3000');
});
