import { io } from "socket.io-client";

const URL = process.env.URL || "http://localhost:3000";

let mmCount = 0;
let userCount = 0;
let lastReport = new Date().getTime();
let requestsSinceLastReport = 0;

const createRandomOrder = () => {
    const user_id = Math.round(Math.random() * 1000000)
    const is_bid = Math.random() > 0.5 ? true : false
    const limit_price = is_bid ? Math.round(Math.random() * 70) : Math.round(Math.random() * 70) + 30
    // console.log("sending packet", packetsSinceLastReport++)
    return JSON.stringify({
        "user": "user_" + user_id, 
        "is_bid": is_bid, // true // remove crossing to check socket / redis
        "limit_price": limit_price, 
        "amount": Math.round(Math.random() * 10), 
        "order_expiry": Math.floor((new Date().getTime() / 1000) + 10)
    }); 
}

const clientRamp = (emitInterval, isMarketMaker) => {
    // for demonstration purposes, some clients stay stuck in HTTP long-polling
    const transports = ["polling", "websocket"];
    const socket = io(URL, {
        transports,
    });

    setInterval(() => {
        requestsSinceLastReport++

        // console.log("sending packet", packetsSinceLastReport++)
        socket.emit("order:create", createRandomOrder());
        }, 
        emitInterval
    );

    if (isMarketMaker) {
        mmCount++;
        // console.log(`Market maker ${mmCount} connected`);
    } else {
        userCount++;
        // console.log(`User ${userCount} connected`);
    }

    socket.on("order:created", (payload) => {
        // processedSinceLastReport++
    });

    socket.on("disconnect", (reason) => {
        if (isMarketMaker) {
            mmCount--;
            console.log(`Market maker disconnected due to ${reason}`);
        } else {
            userCount--;
            console.log(`User disconnected due to ${reason}`);
        }
    });
};

// Market Makers
for (let i = 0; i < 3; i++) {
    setTimeout(() => clientRamp(10, true), i * 100);
}

// Traders
for (let i = 0; i < 100; i++) {
    setTimeout(() => clientRamp(1000, false), i * 100);
}

const printReport = () => {
    const now = new Date().getTime();
    const durationSinceLastReport = (now - lastReport) / 1000;
    const packetsPerSeconds = (
        requestsSinceLastReport / durationSinceLastReport
    ).toFixed(2);

  console.log(
    `MMs: ${mmCount}  |  Users: ${userCount}  |  Req/S: ${packetsPerSeconds}`
  );

  requestsSinceLastReport = 0;
  lastReport = now;
};

setInterval(printReport, 5000);