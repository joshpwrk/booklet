import { v4 as uuidv4 } from 'uuid';

const createOrder = (socket, redisQueue) => {
    return (payload) => {
        // Generate a unique UUID for the order
        const orderId = uuidv4();
        payload = {...JSON.parse(payload), "order_id": orderId}
        console.log(JSON.stringify(payload));

        // add the order to a Redis database
        redisQueue.ZADD('queue', [{
            score: Date.now(), 
            value: JSON.stringify(payload)
        }], (err, result) => {
            if (err) {
                console.error(`Error adding order to Redis: ${err}`);
            } else {
                console.log(`Added order to Redis: ${result}`);
            }
        });

        // return order_id so client can track
        socket.emit("order:id", orderId);
    }
}

const deleteOrder = (payload) => {
    const socket = this;
    
    // notify all users
    socket.broadcast.emit("order:deleted", "yay");

    console.log(`Deleted order: ${payload}`);
}
  
export { createOrder, deleteOrder };