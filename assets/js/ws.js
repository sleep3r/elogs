import ReconnectingWebSocket from 'reconnecting-websocket';
window.ReconnectingWebSocket = ReconnectingWebSocket;
import WS from 'ws';

const options = {
    WebSocket: WebSocket, // custom WebSocket constructor
    connectionTimeout: 1000,
    maxRetries: 1000,
    debug: true
};

function show_notification() {
    Notification.requestPermission(function (permission) {
        if (permission === "granted") {
            const data = JSON.parse(event.data);
            const options = {
                body: "Asmet Omarov comes",
                icon: '',
            };
            const title = 'E-LOGS: У вас новое сообщение';
            const notification = new Notification(title, options);
        }
    });
}

$(document).ready(() => {
    // <---------------------------------------MESSAGES------------------------------------------->
    const messages_endpoint = 'ws://' + window.location.host + '/messages/';
    const messages_socket = new ReconnectingWebSocket(messages_endpoint, [], options);
    messages_socket.onmessage = function (event) {console.log("message", event);show_notification();};
    messages_socket.onopen = function (event) {console.log("Messages connected", event);};
    messages_socket.onerror = function (event) {console.log("Messages error", event);};
    messages_socket.onclose = function (event) {console.log("Messages closed", event);};

    // <-----------------------------------------DATA--------------------------------------------->
    const data_endpoint = 'ws://' + window.location.host + '/data/';
    const data_socket = new ReconnectingWebSocket(data_endpoint, [], options);
    data_socket.onmessage = function (event) {console.log("message", event);};
    data_socket.onopen = function (event) {console.log("Data connected", event);};
    data_socket.onerror = function (event) {console.log("Data error", event);};
    data_socket.onclose = function (event) {console.log("Data closed", event);};
});
