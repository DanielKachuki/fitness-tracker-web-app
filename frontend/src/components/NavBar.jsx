import React from "react";
import { Link } from "react-router-dom";

export default function NavBar() {
  return (
    <nav style={{ padding: '1rem', background: '#f5f5f5' }}>
      <ul style={{
        listStyle: 'none',
        display: 'flex',
        gap: '1rem',
        margin: 0,
        padding: 0,
      }}>
        <li><Link to="/home">Home</Link></li>
        <li><Link to="/settings">Settings</Link></li>
        <li><Link to="/workouts">Workouts</Link></li>
        <li><Link to="/goals">Goals</Link></li>
        <li><Link to="/logout">Logout</Link></li>
      </ul>
    </nav>
  );
}
