import {
    signIn,
    signUp,
    confirmSignUp as awsConfirmSignUp,
    confirmSignIn,
    signOut,
    getCurrentUser,
    fetchAuthSession,
    resetPassword,
    confirmResetPassword,
  } from 'aws-amplify/auth'
  
  export async function getIdToken() {
    const { tokens } = await fetchAuthSession()
    return tokens?.idToken?.toString() ?? null
  }
  
  export async function loginUser(email, password) {
    return await signIn({ username: email, password })
  }

  export async function registerUser(email, password) {
    return await signUp({
      username: email,
      password,
      options: {
        userAttributes: {
          email,
        },
      },
    })
  }

  export async function confirmSignUp(username, code) {
    return await awsConfirmSignUp({ username, confirmationCode: code })
  }
  
  export async function confirmChallenge(code, rememberDevice = false) {
    const options = rememberDevice ? { userAttributes: { 'device:trusted': 'true' } } : {}
    return await confirmSignIn({ challengeResponse: code, options })
  }
  
  export async function logoutUser() {
    await signOut()
  }
  
  export async function checkSession() {
    try {
      await getCurrentUser()
      return true
    } catch {
      return false
    }
  }
  
  export async function startReset(username) {
    return await resetPassword({ username })
  }
  
  export async function confirmResetFlow(username, code, newPassword) {
    return await confirmResetPassword({
      username,
      confirmationCode: code,
      newPassword,
    })
  }
  