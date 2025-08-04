import React from 'react'
import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom"
import Settings from "./pages/Settings";
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import NotFound from "./pages/NotFound.jsx";
import ProtectedRoute from "./components/ProtectedRoute";


function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
            path="/"
            element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />
      <Route
          path="/settings"
          element={
            <ProtectedRoute>
              <Settings />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="*" element={<NotFound />}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
