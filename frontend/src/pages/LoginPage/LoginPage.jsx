import { useState } from 'react'
import { QRCodeSVG } from 'qrcode.react'
import {
  loginUser,
  confirmChallenge,
  startReset,
  confirmResetFlow,
} from '../../auth/authService'
import './LoginPage.css'

export default function LoginPage() {
  const [isRegister, setIsRegister] = useState(false)

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const [mfaStage, setMfaStage] = useState(null)
  const [mfaCode, setMfaCode] = useState('')
  const [qrUri, setQrUri] = useState('')

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
        const uri = nextStep.totpSetupDetails.getSetupUri({
          issuer: 'Grammy',
          label: email,
        })
        setQrUri(uri)
        setMfaStage('totpSetup')
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

  /* ---------------- TOTP ---------------- */

  const handleTotpSubmit = async () => {
    try {
      const { nextStep } = await confirmChallenge(mfaCode)
      setMfaCode('')
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
    } catch (err) {
      alert(err.message)
    }
  }

  return (
    <div className="login-wrapper">
      <div className={`login-container ${isRegister ? 'right-panel-active' : ''}`}>

        {/* ---------------- RIGHT PANEL (FORM SIDE) ---------------- */}
        <div className="login-right">

          {/* ===== MFA SETUP ===== */}
          {mfaStage === 'totpSetup' && (
            <div className="auth-block">
              <h2>Enable MFA</h2>
              <QRCodeSVG value={qrUri} />
              <input
                placeholder="6 digit code"
                value={mfaCode}
                onChange={(e) => setMfaCode(e.target.value)}
              />
              <button className="login-button" onClick={handleTotpSubmit}>
                Verify
              </button>
            </div>
          )}

          {/* ===== MFA SIGNIN ===== */}
          {mfaStage === 'signinTotp' && (
            <div className="auth-block">
              <h2>Enter MFA Code</h2>
              <input
                placeholder="6 digit code"
                value={mfaCode}
                onChange={(e) => setMfaCode(e.target.value)}
              />
              <button className="login-button" onClick={handleTotpSubmit}>
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
            </div>
          )}

          {/* ===== NORMAL LOGIN / REGISTER ===== */}
          {!mfaStage && !resetStage && (
            <form onSubmit={handleLogin}>
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
