import { Server } from "socket.io";
import { createOrder, deleteOrder } from "./orderHandler.js";

const io = new Server({ /* options */ });

io.on('connection', (socket) => {
    console.log('A client connected');

    socket.on("order:create", createOrder);
    socket.on("order:delete", deleteOrder);
});


io.listen(3000, () => {
  console.log('Server listening on port 3000');
});
