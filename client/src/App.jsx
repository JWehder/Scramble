import { useEffect, useState } from 'react'
import Home from './components/Home'
import LoggedOut from './components/LoggedOut'
import SideBar from './components/User/Sidebar/SideBar'

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    fetch('/api/tournaments')
      .then((r) => r.json())
      .then((data) => console.log(data))
  })

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
