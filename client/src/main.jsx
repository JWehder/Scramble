import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
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
    <App />
  </React.StrictMode>,
)
