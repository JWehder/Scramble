import { useState } from 'react'
import Home from './components/Home'
import LoggedOut from './components/LoggedOut'
import SideBar from './components/Sidebar/SideBar'

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  if(isLoggedIn) return (
    <div>
        <Home setIsLoggedIn={setIsLoggedIn} />
        <SideBar />
    </div>
  ) 
  else return (
    <div>
      <LoggedOut setIsLoggedIn={setIsLoggedIn} />
    </div>
  )
}
