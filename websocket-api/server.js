import { Server } from "socket.io";
import { createOrder, deleteOrder } from "./orderHandler.js";

const io = new Server({ /* options */ });
const redisQueue = redis.createClient({ 
    host: 'localhost',
    port: 6379,
    db: 1 ,
    retry_strategy: (options) => {
      console.error(`Redis connection failed. Retrying in ${options.attempt * 1000}ms`);
      return options.attempt * 1000;
    }
});

io.on('connection', (socket) => {
    console.log('A client connected');

    socket.on('order:create', createOrder(redisQueue));
    socket.on("order:delete", deleteOrder);
});


io.listen(3000, () => {
  console.log('Server listening on port 3000');
});
