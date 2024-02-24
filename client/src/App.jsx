import { useEffect, useState } from 'react'
import Home from './components/Home'
import LoggedOut from './components/LoggedOut'
import SideBar from './components/User/components/sidebar/SideBar'
import { GoogleOAuthProvider } from '@react-oauth/google';
import axios from 'axios';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [clientId, setClientId] = useState();

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
            console.log(clientId)
        })
        .catch(error => {
            // Handle errors if necessary
            console.error('Error fetching client ID:', error);
        });
  }, []); 

  if(isLoggedIn) return (
    <div className='bg-dark flex items-center justify-center'>
      <div className='w-3/4'>
      <GoogleOAuthProvider clientId={clientId}>
        <Home setIsLoggedIn={setIsLoggedIn} />
        {/* <SideBar /> */}
      </GoogleOAuthProvider>;
      </div>
    </div>
  ) 
  else return (
    <div>
      <LoggedOut setIsLoggedIn={setIsLoggedIn} />
    </div>
  )
}
