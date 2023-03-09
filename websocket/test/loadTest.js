import { io } from "socket.io-client";

const URL = process.env.URL || "http://localhost:3000";
const MAX_CLIENTS = 100;
const POLLING_PERCENTAGE = 0;
const CLIENT_CREATION_INTERVAL_IN_MS = 100;
const EMIT_INTERVAL_IN_MS = 100;

let clientCount = 0;
let lastReport = Date.now();
let packetsSinceLastReport = 0;

const createClient = () => {
    // for demonstration purposes, some clients stay stuck in HTTP long-polling
    const transports = Math.random() < POLLING_PERCENTAGE 
        ? ["polling"] 
        : ["polling", "websocket"];

    const socket = io(URL, {
        transports,
    });

    const user_id = Math.round(Math.random() * MAX_CLIENTS)
    setInterval(() => {
        // console.log("sending packet", packetsSinceLastReport++)
            socket.emit("order:create", JSON.stringify({
                "user": "user_" + user_id, 
                "is_bid": Math.random() > 0.5, 
                "limit_price": Math.round(Math.random() * 1000), 
                "amount": Math.round(Math.random() * 10), 
                "order_expiry": 1679155437
            }));
        }, 
        EMIT_INTERVAL_IN_MS
    );

    socket.on("order:created", (payload) => {
        packetsSinceLastReport++
        // console.log(payload);
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
    const now = Date.now();
    const durationSinceLastReport = (now - lastReport) / 1000;
    const packetsPerSeconds = (
        packetsSinceLastReport / durationSinceLastReport
        // todo: currently catching 5 events per order creation...
    ).toFixed(2);

    console.log(
        `client count: ${clientCount} ; average packets received per second: ${packetsPerSeconds}`
    );

    packetsSinceLastReport = 0;
    lastReport = now;
};

// printReport()
setInterval(printReport, 5000);