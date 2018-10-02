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

            fetch('http://localhost:8000/common/messages/subscribe',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(subscription)
            })
                .then(function(response) {
                    return response;
                })
                .then(function(text) {
                    console.log('User is subscribed.');
                })
                .catch(function(error) {
                    console.error('error fetching subscribe', error);
                });

        })
        .catch(function(err) {
            console.log('Failed to subscribe the user: ', err);
        });
}

if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/service-worker.js').then(function(registration) {
            // Регистрация успешна
            console.log('ServiceWorker registration successful with scope: ', registration.scope);
            subscribeUser(registration)
        }).catch(function(err) {
            // Регистрация не успешна
            console.log('ServiceWorker registration failed: ', err);
        });
    });
}