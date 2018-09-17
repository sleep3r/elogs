import VueWebsocket from "vue-websocket"

import ReconnectingWebSocket from 'reconnecting-websocket';
window.ReconnectingWebSocket = ReconnectingWebSocket;

// <---------------------------------------MESSAGES------------------------------------------------>
var messages_endpoint = 'ws://' + window.location.host + '/messages/';
var messages_socket = new ReconnectingWebSocket(messages_endpoint);

messages_socket.onmessage = function (event) {
    console.log("message", event);

    Notification.requestPermission(function (permission) {
        if (permission === "granted") {
            var data = JSON.parse(event.data);
            var options = {
                body: "Asmet Omarov comes",
                icon: '',
            };
            var title = 'E-LOGS: У вас новое сообщение';
            var notification = new Notification(title, options);
        }
    });

};
messages_socket.onopen = function (event) {
    console.log("Messages connected", event);
};
messages_socket.onerror = function (event) {
    console.log("Messages error", event);
};
messages_socket.onclose = function (event) {
    console.log("Messages closed", event);
};

// <-----------------------------------------DATA-------------------------------------------------->
var data_endpoint = 'ws://' + window.location.host + '/data/';
var data_socket = new ReconnectingWebSocket(data_endpoint);

data_socket.onmessage = function (event) {
    console.log("message", event);


};
data_socket.onopen = function (event) {
    console.log("Data connected", event);
};
data_socket.onerror = function (event) {
    console.log("Data error", event);
};
data_socket.onclose = function (event) {
    console.log("Data closed", event);
};