// this file contains code that would be used to connect the back end created to a front end application

// this code would be applied to the main.jsx file

import React from 'react';
import { createRoot } from 'react-dom/client';
import { Auth0Provider } from '@auth0/auth0-react';
import App from './App';

const root = createRoot(document.getElementById('root'));

root.render(
    <Auth0Provider
        domain="Auth0 App Domain" // application api domain
        clientID="Auth0 App Client-ID" // application client id
        authorizationParams={{
            redirect_uri: window.location.origin,
            audience: "MSAPI000001", // api identifier
            scope: "read:customer" // list all permissions required
        }}
    >
        <App />
    </Auth0Provider>
);

// example of send request using Auth0

import { useAuth0 } from '@auth0/auth0-react';

const SendRequest = () => {

    const { getAccessTokenSilently } = useAuth0();

    const fetchProtectedData = async () => {
        const token = await getAccessTokenSilently();
        console.log(token)
        const response = await fetch("http://localhost:5000/protected", {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        const data = await response.json();
        console.log(data);
    };

    return (
        <button onClick={() => fetchProtectedData()}>SendRequest</button>
    )
}

export default SendRequest