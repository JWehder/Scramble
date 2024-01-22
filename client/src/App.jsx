import { useState, useEffect } from 'react'
import Test from './components/Test'
import SideBar from './components/Sidebar/SideBar'

export default function App() {
  const [test, setTest] = useState([])

  useEffect(() => {
    fetch('/api/dummy')
    .then(r => r.json())
    .then(data => setTest(data))
    .catch(err => console.log(err))
  }, [])

  return (
    <>
      <h1 className="text-3xl font-bold underline text-center">
        Scramble
      </h1>
      <div className="flex">
        <SideBar />
      </div>



      <div>
        {test.length !== 0 ? test.players.map(e => <Test key={e.player_name} name={e.player_name} />) : null}
      </div>

    </>
  )
}
