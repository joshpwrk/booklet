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
  [`__key*__:*`], 
  (message, channel) =>  {
    console.log(message, channel)
    if (message == "zrem" && channel == "__keyspace@1__:queue") {
      // todo: change to actual order_id -> ideally when added to settlementQueue
      io.emit("order:created", channel)
    }
  }
)

redisQueue.on('error', err => {
  console.log('Error ' + err);
});

io.on('connection', (socket) => {
  console.log('A client connected');

  socket.on('order:create', createOrder(redisQueue));
  socket.on("order:delete", deleteOrder);
});

io.listen(3000, () => {
  console.log('Server listening on port 3000');
});
