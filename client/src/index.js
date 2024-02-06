import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

// server setup
const server = new ApolloServer( {
    // typeDefs: definitions of types of data like player
    // resolvers: 
});

const { url } = await startStandaloneServer(server, {
    listen: { port: 4000 }
})

console.log('sever ready at port', 4000);