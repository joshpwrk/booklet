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
    const pattern = /^__keyspace@0__:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
    console.log(pattern.test(channel))
    if (message == "set" && pattern.test(channel)) {
      // todo: change to actual order_id -> ideally when added to settlementQueue
      // set __keyspace@0__:524a0e6d-fd71-4f07-af0d-caea25b53bb5
      io.emit("order:created", channel)
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
