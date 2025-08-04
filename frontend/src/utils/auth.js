// frontend/src/utils/auth.js
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

// grab tokens out of localStorage
export function getToken() {
  return localStorage.getItem(ACCESS_TOKEN);
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN);
}

// optionally a helper to set both tokens after login/refresh
export function setTokens({ access, refresh }) {
  localStorage.setItem(ACCESS_TOKEN, access);
  localStorage.setItem(REFRESH_TOKEN, refresh);
}

// clear on logout
export function clearTokens() {
  localStorage.removeItem(ACCESS_TOKEN);
  localStorage.removeItem(REFRESH_TOKEN);
}
