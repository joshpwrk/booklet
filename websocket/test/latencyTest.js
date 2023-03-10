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
        console.log(`Order ID: ${orderId}`);

        socket.once('order:created', () => {
            console.log('Order created');
            const endTime = Date.now();
            const latency = endTime - startTime;
            console.log(`Total latency: ${latency} ms`);
        });
    });
}

// call sendOrder() to send the order and wait for the response
sendOrder();
