import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import NavBar from "./components/NavBar";
import LandingPage from "./pages/LandingPage.jsx";
import Settings from "./pages/Settings";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import WorkoutList from "./pages/WorkoutList";
import NotFound from "./pages/NotFound.jsx";
import ProtectedRoute from "./components/ProtectedRoute";
import ScheduleWorkout from "./pages/ScheduleWorkout";
import CreateWorkout from "./pages/CreateWorkout";
import AuthenticatedLayout from "./components/AuthenticatedLayout";

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" replace />;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="/logout" element={<Logout />} />

        {/* Protected routes */}
        <Route element={
            <ProtectedRoute>
                <AuthenticatedLayout />
            </ProtectedRoute>
          }
        >
        <Route
          path="/home"
          element={
              <Home />
          }
        />
        <Route
          path="/settings"
          element={
              <Settings />
          }
        />
        <Route
          path="/workouts"
          element={
              <WorkoutList />
          }
        />
        <Route
          path="/workouts/new"
          element={
              <CreateWorkout />
          }
        />
        <Route
          path="/scheduled-workouts"
          element={
              <ScheduleWorkout />
          }
        />
        </Route>

        {/* 404 */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
