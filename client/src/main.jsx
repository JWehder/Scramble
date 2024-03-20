import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import store from './store.jsx';
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";

// import { ApolloServer } from '@apollo/server';
// import { startStandaloneServer } from '@apollo/server/standalone';

// server setup
// const server = new ApolloServer( {
     // typeDefs: definitions of types of data like player
     // resolvers: 
// });

// const { url } = await startStandaloneServer(server, {
//     listen: { port: 4000 }
// })

console.log('sever ready at port', 4000);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Provider>
  </React.StrictMode>,
)
