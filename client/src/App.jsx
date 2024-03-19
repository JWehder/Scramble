import { useEffect, useState } from 'react';
import SideBar from './components/User/components/sidebar/SideBar';
import { GoogleOAuthProvider } from '@react-oauth/google';
import axios from 'axios';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import SignedOutHome from './components/SignedOutHome';
import { useSelector } from 'react-redux';
import { redirect } from "react-router-dom";

export default function App() {
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


  const loader = async () => {
    const user = await getUser();
    if (!user) {
      return redirect("/");
    }
    return null;
  };

    return (
    <div className='w-full h-full relative'>
      <Header />
      <GoogleOAuthProvider clientId={clientId}>
        <div className='w-full bg-dark h-full'>
            {
                signedIn ?
                  <Dashboard />
                :
                  <SignedOutHome />
            }
        </div>
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
