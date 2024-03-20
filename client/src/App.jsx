import { useEffect, useState } from 'react';
import SideBar from './components/User/components/sidebar/SideBar';
import { GoogleOAuthProvider } from '@react-oauth/google';
import axios from 'axios';
import Header from './components/Header';
import Dashboard from './components/LeagueDashboard';
import SignedOutHome from './components/SignedOutHome';
import { useSelector } from 'react-redux';
import { redirect, Routes, Route } from "react-router-dom";
import League from './components/League';

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

  const leagueLoader = async () => {
    return null;
  };

  const userLoader = async () => {
    if (signedIn) {
      return redirect("/leagues");
    }
    return null;
  }

  console.log(signedIn);

    return (
    <div className='w-full h-screen relative'>
      <Header />
      <GoogleOAuthProvider clientId={clientId}>
        <div className='w-full bg-dark h-full'>
          <Routes>
            <Route 
              path='/' 
              element={<SignedOutHome />}
              loader={userLoader()}
            />
            <Route 
            exact
            path='/leagues' 
            element={<><League /> <SideBar /></>}
            loader={leagueLoader()}
            />
            <Route 
                path="/leagues/:id"
                element={<Dashboard />} 
                loader={leagueLoader()}
              />
          </Routes>
        </div>
      </GoogleOAuthProvider>
    </div>
  ) 
}
