import { useState } from 'react'
import { QRCodeSVG } from 'qrcode.react'
import {
  loginUser,
  registerUser,
  confirmSignUp,
  confirmChallenge,
  startReset,
  confirmResetFlow,
} from '../../auth/authService'
import './LoginPage.css'

export default function LoginPage() {
  const [isRegister, setIsRegister] = useState(false)

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [repeatPassword, setRepeatPassword] = useState('')

  // Email verification state
  const [emailVerificationStage, setEmailVerificationStage] = useState(null)
  const [verificationEmailCode, setVerificationEmailCode] = useState('')

  // MFA states
  const [mfaStage, setMfaStage] = useState(null)
  const [mfaCode, setMfaCode] = useState('')
  const [qrUri, setQrUri] = useState('')
  const [deviceName, setDeviceName] = useState('')
  const [rememberDevice, setRememberDevice] = useState(false)

  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const [resetStage, setResetStage] = useState(false)
  const [verificationCode, setVerificationCode] = useState('')

  /* ---------------- NEXT STEP HANDLER ---------------- */

  const handleNextStep = (nextStep) => {
    switch (nextStep.signInStep) {
      case 'DONE':
        window.location.href = '/'
        break

      case 'CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED':
        setMfaStage('newPassword')
        break

      case 'CONFIRM_SIGN_IN_WITH_TOTP_CODE':
        setMfaStage('signinTotp')
        break

      case 'CONTINUE_SIGN_IN_WITH_TOTP_SETUP':
        try {
          const secret = nextStep.totpSetupDetails.sharedSecret
          const label = `${email}`
          const issuer = 'Grammy'
          
          // Manually construct otpauth URI
          const uri = `otpauth://totp/${issuer}:${encodeURIComponent(label)}?secret=${secret}&issuer=${issuer}`
          
          setQrUri(uri)
          setMfaStage('totpSetup')
        } catch (err) {
          // Fallback to getSetupUri if manual construction fails
          const uri = nextStep.totpSetupDetails.getSetupUri({
            issuer: 'Grammy',
            label: `${email}`,
          })
          setQrUri(uri)
          setMfaStage('totpSetup')
        }
        break

      default:
        console.log(nextStep)
    }
  }

  /* ---------------- LOGIN ---------------- */

  const handleLogin = async (e) => {
    e.preventDefault()
    try {
      const { nextStep } = await loginUser(email, password)
      handleNextStep(nextStep)
    } catch (err) {
      alert(err.message)
    }
  }

  /* ---------------- REGISTER ---------------- */

  const handleRegister = async (e) => {
    e.preventDefault()
    if (password !== repeatPassword) return alert('Passwords do not match')
    if (!email || !password) return alert('Please fill in all fields')

    try {
      await registerUser(email, password)
      setEmailVerificationStage('pending')
      setEmail(email) // Keep email for verification step
    } catch (err) {
      alert(err.message)
    }
  }

  /* ---------------- EMAIL VERIFICATION ===== */

  const handleEmailVerification = async () => {
    if (!verificationEmailCode) return alert('Enter verification code')

    try {
      await confirmSignUp(email, verificationEmailCode)
      alert('Email verified! You can now login.')
      setEmailVerificationStage(null)
      setVerificationEmailCode('')
      setEmail('')
      setPassword('')
      setRepeatPassword('')
      setIsRegister(false)
    } catch (err) {
      alert(err.message)
    }
  }

  /* ---------------- MFA SETUP ===== */

  const handleMfaSetupSubmit = async () => {
    if (!deviceName) return alert('Please name your device')
    if (!mfaCode) return alert('Enter the 6-digit code')

    try {
      const { nextStep } = await confirmChallenge(mfaCode, rememberDevice)
      setDeviceName('')
      setMfaCode('')
      setRememberDevice(false)
      handleNextStep(nextStep)
    } catch (err) {
      alert(err.message)
    }
  }

  /* ---------------- MFA SIGNIN ===== */

  const handleTotpSubmit = async () => {
    try {
      const { nextStep } = await confirmChallenge(mfaCode, rememberDevice)
      setMfaCode('')
      setRememberDevice(false)
      handleNextStep(nextStep)
    } catch (err) {
      alert(err.message)
    }
  }

  /* ---------------- NEW PASSWORD ---------------- */

  const handleNewPasswordSubmit = async () => {
    if (newPassword !== confirmPassword) return alert('Passwords do not match')

    try {
      const { nextStep } = await confirmChallenge(newPassword)
      handleNextStep(nextStep)
    } catch (err) {
      alert(err.message)
    }
  }

  /* ---------------- RESET ---------------- */

  const handleResetStart = async () => {
    if (!email) return alert('Enter email first')
    await startReset(email)
    setResetStage(true)
  }

  const handleResetConfirm = async () => {
    if (newPassword !== confirmPassword) return alert('Passwords do not match')

    try {
      await confirmResetFlow(email, verificationCode, newPassword)
      alert('Password reset successful')
      setResetStage(false)
      setEmail('')
      setPassword('')
      setNewPassword('')
      setConfirmPassword('')
      setVerificationCode('')
    } catch (err) {
      alert(err.message)
    }
  }

  return (
    <div className="login-wrapper">
      <div className={`login-container ${isRegister ? 'right-panel-active' : ''} ${mfaStage === 'totpSetup' ? 'mfa-setup-mode' : ''}`}>

        {/* ---------------- RIGHT PANEL (FORM SIDE) ---------------- */}
        <div className="login-right">

          {/* ===== EMAIL VERIFICATION VIEW ===== */}
          {emailVerificationStage === 'pending' && (
            <div className="auth-block">
              <h2>Verify Email</h2>
              <p>We sent a verification code to <strong>{email}</strong></p>
              <p className="sub-text">Check your email (and spam folder) for the code.</p>
              <input
                placeholder="Enter verification code"
                value={verificationEmailCode}
                onChange={(e) => setVerificationEmailCode(e.target.value)}
              />
              <button 
                className="login-button" 
                onClick={handleEmailVerification}
              >
                Verify Email
              </button>
              <button 
                type="button"
                className="back-button"
                onClick={() => {
                  setEmailVerificationStage(null)
                  setVerificationEmailCode('')
                  setEmail('')
                  setPassword('')
                  setRepeatPassword('')
                }}
              >
                Back to Register
              </button>
            </div>
          )}

          {/* ===== MFA SETUP VIEW ===== */}
          {mfaStage === 'totpSetup' && (
            <div className="auth-block">
              <h2>Secure Your Account</h2>
              <p>Scan this QR code with your authenticator app:</p>
              <div className="qr-container">
                <QRCodeSVG value={qrUri} size={256} level="H" />
              </div>
              <p className="sub-text">Popular apps: Google Authenticator, Authy, Microsoft Authenticator</p>
              
              <input
                placeholder="Device name (e.g., My iPhone)"
                value={deviceName}
                onChange={(e) => setDeviceName(e.target.value)}
              />
              
              <input
                placeholder="6-digit code from app"
                value={mfaCode}
                maxLength="6"
                onChange={(e) => setMfaCode(e.target.value.replace(/\D/g, ''))}
              />
              
              <label className="remember-device">
                <input
                  type="checkbox"
                  checked={rememberDevice}
                  onChange={(e) => setRememberDevice(e.target.checked)}
                />
                <span>Remember this device for 30 days</span>
              </label>
              
              <button 
                className="login-button" 
                onClick={handleMfaSetupSubmit}
              >
                Verify & Enable MFA
              </button>
            </div>
          )}

          {/* ===== MFA SIGNIN VIEW ===== */}
          {mfaStage === 'signinTotp' && (
            <div className="auth-block">
              <h2>Enter MFA Code</h2>
              <p>Open your authenticator app and enter the 6-digit code.</p>
              <input
                placeholder="6-digit code"
                value={mfaCode}
                maxLength="6"
                onChange={(e) => setMfaCode(e.target.value.replace(/\D/g, ''))}
              />
              <label className="remember-device">
                <input
                  type="checkbox"
                  checked={rememberDevice}
                  onChange={(e) => setRememberDevice(e.target.checked)}
                />
                <span>Remember this device for 30 days</span>
              </label>
              <button 
                className="login-button" 
                onClick={handleTotpSubmit}
              >
                Verify
              </button>
            </div>
          )}

          {/* ===== NEW PASSWORD ===== */}
          {mfaStage === 'newPassword' && (
            <div className="auth-block">
              <h2>Set New Password</h2>
              <input
                type="password"
                placeholder="New password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
              <input
                type="password"
                placeholder="Confirm password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
              <button className="login-button" onClick={handleNewPasswordSubmit}>
                Submit
              </button>
            </div>
          )}

          {/* ===== RESET FLOW ===== */}
          {resetStage && (
            <div className="auth-block">
              <h2>Reset Password</h2>
              <p>Enter the verification code sent to your email.</p>
              <input
                placeholder="Verification code"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value)}
              />
              <input
                type="password"
                placeholder="New password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
              <input
                type="password"
                placeholder="Confirm password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
              <button className="login-button" onClick={handleResetConfirm}>
                Confirm
              </button>
              <button 
                type="button"
                className="back-button"
                onClick={() => {
                  setResetStage(false)
                  setVerificationCode('')
                  setNewPassword('')
                  setConfirmPassword('')
                }}
              >
                Back
              </button>
            </div>
          )}

          {/* ===== NORMAL LOGIN / REGISTER ===== */}
          {!mfaStage && !resetStage && !emailVerificationStage && (
            <form onSubmit={isRegister ? handleRegister : handleLogin}>
              <h2>{isRegister ? 'REGISTER' : 'LOGIN'}</h2>

              <input
                placeholder="EMAIL"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              <input
                type="password"
                placeholder="PASSWORD"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              {isRegister && (
                <input
                  type="password"
                  placeholder="REPEAT PASSWORD"
                  value={repeatPassword}
                  onChange={(e) => setRepeatPassword(e.target.value)}
                />
              )}

              <button className="login-button">
                {isRegister ? 'REGISTER' : 'LOGIN'}
              </button>

              {!isRegister && (
                <button
                  type="button"
                  className="google-button"
                  onClick={handleResetStart}
                >
                  Forgot Password
                </button>
              )}
            </form>
          )}

        </div>

        {/* ---------------- LEFT PANEL (INFO SIDE) ---------------- */}
        <div className="login-left">
          <h1>{isRegister ? 'GRAMMY REGISTER' : 'GRAMMY LOGIN'}</h1>
          <p>
            {isRegister
              ? 'Already have an account?'
              : "Don't have an account?"}
          </p>
          <button
            className="toggle-button"
            onClick={() => setIsRegister(!isRegister)}
          >
            {isRegister ? 'LOGIN' : 'REGISTER'}
          </button>
        </div>

      </div>
    </div>
  )
}
