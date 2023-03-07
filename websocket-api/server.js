import { Server } from "socket.io";
import { addOrder, cancelOrder } from "./orderHandler";

const io = new Server({ /* options */ });

io.on('connection', (socket) => {
    console.log('A client connected');

    socket.on("order:add", addOrder);
    socket.on("order:cancel", cancelOrder);
});


io.listen(3000, () => {
  console.log('Server listening on port 3000');
});
