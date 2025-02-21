// code to connnect backend to front end using AuthO - this code would be applied to the main.jsx of the front end dev 

import React from 'react';
import { createRoot } from 'react-dom/client';
import { Auth0Provider } from '@auth0/auth0-react';
import App from './App';

const root = createRoot(document.getElementById('root'));

root.render(
    <Auth0Provider
        domain="Auth0 App Domain"
        clientID="Auth0 App Client-ID"
        authorizationParams={{
            redirect_uri: window.location.origin,
            audience: "MSAPI000001",
            scope: "permission"
        }}
    >
        <App />
    </Auth0Provider>
);