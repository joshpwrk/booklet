import { v4 as uuidv4 } from 'uuid';

function createOrder(redisQueue) {
    return (payload) => {
        // Generate a unique UUID for the order
        const orderId = uuidv4();
        console.log(JSON.parse(payload));
        payload = {...JSON.parse(payload), "order_id": orderId}

        console.log(`Received request to create order: ${payload}`);
        console.log(JSON.stringify(payload));
        console.log(Date.now());

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
    }
}

async function deleteOrder(payload) {
    const socket = this;
    
    // notify the other users
    socket.broadcast.emit("order:deleted", "yay");

    console.log(`Deleted order: ${payload}`);
}
  
export { createOrder, deleteOrder };