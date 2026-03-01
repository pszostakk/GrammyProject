import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"
import '../LoginPage/LoginPage.css'
import { confirmSignUp } from '../../auth/authService'

export default function VerifyPage() {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState("We are verifying your account...");
  const email = searchParams.get("email");
  const code = searchParams.get("code");

  useEffect(() => {
    if (email && code) {
      setStatus("Verifying your account...");
      
      confirmSignUp(email, code)
        .then(() => {
          setStatus("Account has been successfully verified! You can now log in.");
        })
        .catch((err) => {
          console.error(err);
          setStatus("Verification failed: " + err.message);
        });
    } else {
      setStatus("Invalid verification data.");
    }
  }, [email, code]);

  return (
    <div className="login-wrapper">
      <div className="login-container">
        <div className="login-left">
          <h1>GRAMMY</h1>
          <p>Account verification</p>
        </div>
        <div className="login-right">
          <div className="auth-block">
            <h2>Account verification</h2>
            <p>{status}</p>
            {status === "Account has been successfully verified! You can now log in." && (
            <button
              className="login-button"
              onClick={() => window.location.href = '/loginPage'}
            >
              Go to Login Page
            </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}