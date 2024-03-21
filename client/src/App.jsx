import { useEffect, useState } from 'react';
import { GoogleOAuthProvider } from '@react-oauth/google';
import axios from 'axios';
import Header from './components/Header';
import { useSelector } from 'react-redux';
import { Outlet } from "react-router-dom";

export default function App({children}) {
  const [clientId, setClientId] = useState();

  const signedIn = useSelector((state) => state.users.user);

  useEffect(() => {
    fetch('/api/tournaments')
      .then((r) => r.json())
      .then((data) => console.log(data));
  });

  useEffect(() => {
    // Make the GET request to retrieve the client ID
    axios.get('/api/get_client_id')
        .then(response => {
            setClientId(response.data.client_id);
        })
        .catch(error => {
            // Handle errors if necessary
            console.error('Error fetching client ID:', error);
        });
  }, []); 

  return (
  <div className='w-full h-screen relative'>
    <Header />
    <GoogleOAuthProvider clientId={clientId}>
      <div className='w-full bg-dark h-full'>
        <Outlet />
      </div>
    </GoogleOAuthProvider>
  </div>
) 
}
