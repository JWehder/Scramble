import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Test from './components/Test'

function App() {
  const [count, setCount] = useState(0)
  // const [test, setTest] = useState([])

  // useEffect(() => {
  //   fetch('test url')
  //   .then(r => r.json())
  //   .then(data => setTest(data))
  // }, [])


  // console.log(test)
  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      {/* <div>
        {test.length > 0 ? test.map(e => <Test key={e} name={e} />) : null}
      </div> */}
    </>
  )
}

export default App
