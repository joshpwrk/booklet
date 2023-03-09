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
    io.emit("order:created", "this thing actually works")
  }
)

//    socket.broadcast.emit("order:created", redisKey, redisOpeation);

redisQueue.on('error', err => {
  console.log('Error ' + err);
});

io.on('connection', (socket) => {
  console.log('A client connected');

  socket.on('order:create', createOrder(redisQueue));
  socket.on("order:delete", deleteOrder);
  socket.on("client to server event", () => {
    console.log("received packet")
    socket.emit("server to client event");
  });
});

io.listen(3000, () => {
  console.log('Server listening on port 3000');
});
