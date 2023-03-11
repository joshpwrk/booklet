import { io } from "socket.io-client";


const socket = io.connect('http://localhost:3000');

function sendOrder() {
    const user_id = Math.round(Math.random() * 1000)
    const is_bid = Math.random() > 0.5 ? true : false
    const limit_price = is_bid ? Math.round(Math.random() * 70) : Math.round(Math.random() * 70) + 30
    const order = {
        "user": "user_" + user_id, 
        "is_bid": is_bid, 
        "limit_price": limit_price, 
        "amount": Math.round(Math.random() * 10), 
        "order_expiry": 1679155437
    };

    const startTime = Date.now();

    socket.emit('order:create', JSON.stringify(order));

    socket.once('order:id', (orderId) => {
        const original_order = orderId
        socket.on('order:created', (nextOrderId) => {
            if (nextOrderId == original_order) {
                const latency = Date.now() - startTime;
                process.stdout.write(`Total latency: ${latency} ms       \r`);
                socket.off("order:created");
            }
        });
    });
}

// call sendOrder() to send the order and wait for the response
setInterval(
    sendOrder, 
    5000 // every second
);
