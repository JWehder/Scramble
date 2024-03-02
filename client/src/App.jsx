import { useEffect, useState } from 'react';
import Home from './components/Home';
import SideBar from './components/User/components/sidebar/SideBar';
import { GoogleOAuthProvider } from '@react-oauth/google';
import axios from 'axios';
import Header from './components/Header';
import { useSelector } from 'react-redux';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
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
    <div className='w-full h-full relative'>
      <Header />
      <GoogleOAuthProvider clientId={clientId}>
        <Home />
        {
          signedIn ?
          <SideBar />
          // ""
          :
          ""
        }
      </GoogleOAuthProvider>
    </div>
  ) 
}
