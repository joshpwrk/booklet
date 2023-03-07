const addOrder = (payload) => {  
    console.log(`Received order: ${payload}`);
}

const cancelOrder = (payload) => {  
    console.log(`Cancelled order: ${payload}`);
}
  
export { addOrder, cancelOrder };