import { io } from "socket.io-client";

const URL = process.env.URL || "http://localhost:3000";
const MAX_CLIENTS = 100;
const POLLING_PERCENTAGE = 0;
const CLIENT_CREATION_INTERVAL_IN_MS = 10;
const EMIT_INTERVAL_IN_MS = 10;

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

    setInterval(() => {
            socket.emit("client to server event");
        }, 
        EMIT_INTERVAL_IN_MS
    );

    socket.on("server to client event", () => {
        packetsSinceLastReport++;
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
    ).toFixed(2);

    console.log(
        `client count: ${clientCount} ; average packets received per second: ${packetsPerSeconds}`
    );

    packetsSinceLastReport = 0;
    lastReport = now;
};

setInterval(printReport, 5000);