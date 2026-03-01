import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import LoginPage from './pages/LoginPage/LoginPage.jsx'
import HomePage from './pages/HomePage/HomePage.jsx'
import { getIdToken } from './auth/authService.js'
import ProtectedRoute from './auth/protectedRoute.jsx'

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
            <HomePage />
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}

export default App
