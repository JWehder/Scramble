import { useState, useEffect } from 'react'
import Test from './components/Test'
import SideBar from './components/Sidebar/SideBar'
import Tooltip from './components/Sidebar/Tooltip'

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
      <div className='items-center justify-items-center'>
        <Tooltip tooltip='I am a tooltip'>
          <button className='bg-gray-900 text-white p-3 rounded'>
            Show Me Tooltip
          </button>
        </Tooltip>
      </div>



      <div>
        {test.length !== 0 ? test.players.map(e => <Test key={e.player_name} name={e.player_name} />) : null}
      </div>

    </>
  )
}
