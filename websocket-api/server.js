import { Server } from "socket.io";

const io = new Server({ /* options */ });

io.on('connection', (socket) => {
    console.log('A client connected');

    socket.on('order:add', (data) => {
        console.log(`Received order: ${data}`);
    });

    socket.on('order:remove', (data) => {
        console.log(`Removed order: ${data}`);
    });
});


io.listen(3000, () => {
  console.log('Server listening on port 3000');
});
