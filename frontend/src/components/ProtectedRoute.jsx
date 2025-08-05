import React from "react";
import { Navigate } from "react-router-dom";
import { ACCESS_TOKEN } from "../constants.js";

export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem(ACCESS_TOKEN);

  // If there's no token, send them to /login
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Otherwise show the protected page
  return children;
}