import { io } from "socket.io-client";

const URL = process.env.URL || "http://localhost:3000";
const MAX_CLIENTS = 5;
const POLLING_PERCENTAGE = 0;
const CLIENT_CREATION_INTERVAL_IN_MS = 50;
const EMIT_INTERVAL_IN_MS = 100;

let clientCount = 0;
let lastReport = new Date().getTime();
let packetsSinceLastReport = 0;
let processedSinceLastReport = 0;

const createClient = () => {
    // for demonstration purposes, some clients stay stuck in HTTP long-polling
    const transports = Math.random() < POLLING_PERCENTAGE 
        ? ["polling"] 
        : ["polling", "websocket"];

    const socket = io(URL, {
        transports,
    });

    const user_id = Math.round(Math.random() * 1000 * MAX_CLIENTS)
    setInterval(() => {
        packetsSinceLastReport++

        const is_bid = Math.random() > 0.5 ? true : false
        const limit_price = is_bid ? Math.round(Math.random() * 70) : Math.round(Math.random() * 70) + 30
        // console.log("sending packet", packetsSinceLastReport++)
        socket.emit("order:create", JSON.stringify({
            "user": "user_" + user_id, 
            "is_bid": is_bid, // true // remove crossing to check socket / redis
            "limit_price": limit_price, 
            "amount": Math.round(Math.random() * 10), 
            "order_expiry": 1679155437
        }));
        }, 
        EMIT_INTERVAL_IN_MS
    );

    socket.on("order:created", (payload) => {
        processedSinceLastReport++
        // console.log(processedSinceLastReport);
    });

    socket.on("disconnect", (reason) => {
        console.log(`disconnected due to ${reason}`);
    });

    if (++clientCount < MAX_CLIENTS) {
        setTimeout(createClient, CLIENT_CREATION_INTERVAL_IN_MS);
    }
};

createClient();

const printReport = () => {
    const now = new Date().getTime();
    const durationSinceLastReport = (now - lastReport) / 1000;
    const packetsPerSeconds = (
        packetsSinceLastReport / durationSinceLastReport
    ).toFixed(2);

    const processedPerSeconds = (
        processedSinceLastReport / durationSinceLastReport
    )

  console.log(
    `clients: ${clientCount} ; posts per sec: ${packetsPerSeconds} ; processed per sec: ${processedPerSeconds}`
  );

  packetsSinceLastReport = 0;
  processedSinceLastReport = 0;
  lastReport = now;
};

// printReport()
setInterval(printReport, 5000);