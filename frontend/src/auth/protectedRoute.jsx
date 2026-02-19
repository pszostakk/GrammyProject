import { useEffect, useState } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { checkSession } from './authService'

export default function ProtectedRoute({ children }) {
  const [ok, setOk] = useState(null)
  const location = useLocation()

  useEffect(() => {
    ;(async () => {
      const isAuthed = await checkSession()
      setOk(isAuthed)
    })()
  }, [])

  if (ok === null) return <div>Loading…</div>

  if (!ok) {
    return <Navigate to="/loginPage" replace state={{ from: location }} />
  }

  return children
}
