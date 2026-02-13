import { useState } from 'react'
import './LoginPage.css'

export default function LoginPage() {
  const [isRegister, setIsRegister] = useState(false)

  return (
    <div className="login-wrapper">
      <div className={`login-container ${isRegister ? 'right-panel-active' : ''}`}>

        <div className="login-right">
          <form>
            <h2>{isRegister ? 'REGISTER' : 'LOGIN'}</h2>

            <input placeholder="EMAIL" />
            <input type="password" placeholder="PASSWORD" />

            {isRegister && (
              <input type="password" placeholder="REPEAT PASSWORD" />
            )}

            <button className="login-button">
              {isRegister ? 'REGISTER' : 'LOGIN'}
            </button>

            <button type="button" className="google-button">
              {isRegister ? 'Register with Google' : 'Log in with Google'}
            </button>
          </form>
        </div>

        <div className="login-left">
          <h1>{isRegister ? 'GRAMMY REGISTER' : "GRAMMY LOGIN"}</h1>
          <p>{isRegister ? 'Already have an account?' : "Don't have an account?"}</p>
          <button className="toggle-button" onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? 'LOGIN' : 'REGISTER'}
          </button>
        </div>

      </div>
    </div>
  )
}
