
async function createOrder(payload) {
    const socket = this;
    
    // notify the other users
    socket.broadcast.emit("order:created", "yay");

    console.log(`Created order: ${payload}`);
}

async function deleteOrder(payload) {
    const socket = this;
    
    // notify the other users
    socket.broadcast.emit("order:deleted", "yay");

    console.log(`Deleted order: ${payload}`);
}
  
export { createOrder, deleteOrder };