import axios from 'axios'
import VueCookies from "vue-cookies";
// import runtime from 'serviceworker-webpack-plugin/lib/runtime';

const appServerKey = 'BMD5Tv0jLvfZ65LEnMpnx-ZO2B-l9eGevOvaHVlmKe7SHAiP6awavzZhmoTOqYM10ImQgmVjgxhhfKDYnSxNJsQ'

function urlB64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

function subscribeUser(serviceWorkerRegistration) {
    serviceWorkerRegistration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlB64ToUint8Array(appServerKey)
    })
        .then(function(subscription) {
            axios.post(window.HOSTNAME+'/common/messages/subscribe/', subscription, {
                withCredentials: true,
                headers: {Authorization: 'Token ' + VueCookies.get('Authorization')}
            })
                .then(function(response) {
                    return response;
                })
                .then(function(resp) {
                    if (resp.status === 200) console.log('User is subscribed.');
                    else console.log('Error while subscribing user.');
                })
                .catch(function(error) {
                    console.error('error fetching subscribe', error);
                });

        })
        .catch(function(err) {
            console.log('Failed to subscribe the user: ', err);
        });
}

let registration;

if ('serviceWorker' in navigator) {
    // registration = runtime.register()
    navigator.serviceWorker.register('/service-worker.js')
         .then(function(registration) {
             // Регистрация успешна
             console.log('ServiceWorker registration successful with scope: ', registration.scope);
             subscribeUser(registration)
         })
         .catch(function(err) {
             // Регистрация не успешна
             console.log('ServiceWorker registration failed: ', err);
         });
}