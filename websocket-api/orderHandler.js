import { v4 as uuidv4 } from 'uuid';

async function createOrder(redisQueue) {
    return async function (payload) {
        // Generate a unique UUID for the order
        const orderId = uuidv4();
        payload = {...payload, "order_id": orderId}

        console.log(`Received request to create order: ${payload}`);
    
        // add the order to a Redis database
        redisQueue.zadd('queue', Date.now(), payload, (err, result) => {
            if (err) {
                console.error(`Error adding order to Redis: ${err}`);
            } else {
                console.log(`Added order to Redis: ${result}`);
            }
        });
    }
}

async function deleteOrder(payload) {
    const socket = this;
    
    // notify the other users
    socket.broadcast.emit("order:deleted", "yay");

    console.log(`Deleted order: ${payload}`);
}
  
export { createOrder, deleteOrder };