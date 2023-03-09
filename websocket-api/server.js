import { Server } from "socket.io";
import { createOrder, deleteOrder } from "./orderHandler.js";
import redis from "redis";

const io = new Server({ /* options */ });
const redisQueue = redis.createClient({ 
  socket: {
    host: 'localhost',
    port: 6379,
    keepAlive: true
  },
  database: 1
});
await redisQueue.connect()

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
