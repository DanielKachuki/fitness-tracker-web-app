import React from 'react'
import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom"
import NavBar from './components/NavBar';
import Settings from "./pages/Settings";
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import WorkoutList from './pages/WorkoutList';
import NotFound from "./pages/NotFound.jsx";
import ProtectedRoute from "./components/ProtectedRoute";
import ScheduleWorkout from "./pages/ScheduleWorkout";
import CreateWorkout from './pages/CreateWorkout';


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
        <NavBar />
      <Routes>
          <Route
         path="/workouts/new"
         element={
           <ProtectedRoute>
             <CreateWorkout />
           </ProtectedRoute>
         }
       />
          <Route path="/scheduled-workouts"
          element={
              <ProtectedRoute>
                  <ScheduleWorkout />
              </ProtectedRoute>}
          />
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
        <Route path="/workouts" element={
        <ProtectedRoute>
            <WorkoutList />
        </ProtectedRoute> } />
        <Route path="*" element={<NotFound />}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
