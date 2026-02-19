import { Amplify } from 'aws-amplify'

// TODO: Handle runtimeCfg when there is no window.__GRAMMY_CONFIG__ (e.g. during tests)
const runtimeCfg = window.__GRAMMY_CONFIG__ ?? {}

const cfg = {
  API_URL: runtimeCfg.API_URL ?? import.meta.env.GRAMMY_API_URL,
  USER_POOL_ID: runtimeCfg.USER_POOL_ID ?? import.meta.env.VITE_USER_POOL_ID,
  USER_POOL_CLIENT_ID:
    runtimeCfg.USER_POOL_CLIENT_ID ?? import.meta.env.VITE_USER_POOL_CLIENT_ID,
}

const awsconfig = {
  Auth: {
    Cognito: {
      userPoolId: cfg.USER_POOL_ID,
      userPoolClientId: cfg.USER_POOL_CLIENT_ID,
      loginWith: { email: true },
      region: 'eu-central-1'
    },
  },
}

Amplify.configure(awsconfig)

export const API_BASE = cfg.API_URL
export const GRAMMY_CFG = cfg
