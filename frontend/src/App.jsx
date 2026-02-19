import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import LoginPage from './pages/LoginPage/LoginPage.jsx'
import { getIdToken } from './auth/authService.js'
import ProtectedRoute from './auth/protectedRoute.jsx'

function Home() {
  const [count, setCount] = useState(0)
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)

  const callApi = async (endpoint) => {
    const token = await getIdToken()
  
    const result = await fetch(
      `${import.meta.env.GRAMMY_API_URL}/${endpoint}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
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

function App() {
  return (
    <Routes>
      <Route 
        path="/loginPage" 
        element={
          <LoginPage />
        } 
      />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}

export default App
