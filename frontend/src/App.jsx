import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)

  const callApi = async (endpoint) => {
    setLoading(true)
    setResponse('Loading...')
    try {
      const result = await fetch(`https://7vg071hn2m.execute-api.eu-central-1.amazonaws.com/dev/${endpoint}`)
      const data = await result.json()
      setResponse(`${endpoint}: ${JSON.stringify(data)}`)
    } catch (error) {
      setResponse(`Error calling ${endpoint}: ${error.message}`)
    }
    setLoading(false)
  }

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
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

      <div className="card">
        <h2>API Calls</h2>
        <button onClick={() => callApi('pawel')} disabled={loading}>
          Call Pawel API
        </button>
        <button onClick={() => callApi('kacper')} disabled={loading}>
          Call Kacper API
        </button>
        {response && <p>{response}</p>}
      </div>

      <p className="read-the-docs">
        Click on the Vite and React logos to learn more - Grammy
      </p>
    </>
  )
}

export default App
