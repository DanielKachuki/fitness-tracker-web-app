import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import "./Home.css";

export default function Home() {
  const [upcoming, setUpcoming] = useState([]);

  useEffect(() => {
    api.listScheduledWorkouts()
      .then(setUpcoming)
      .catch(console.error);
  }, []);

  return (
    <div className="home-dashboard">
      <div className="upcoming-card">
        <h2>Upcoming Workouts</h2>
        {upcoming.length ? (
          <ul>
            {upcoming.map(s => {
              // if workout_type is an object, use its name,
              // otherwise just display the ID
              const typeLabel =
                s.workout_type && typeof s.workout_type === 'object'
                  ? s.workout_type.name
                  : `#${s.workout_type}`;
              return (
                <li key={s.id}>
                  <strong>
                    {new Date(s.scheduled_date).toLocaleDateString()}
                  </strong>{" "}
                  — {typeLabel} ({s.duration})
                </li>
              );
            })}
          </ul>
        ) : (
          <p>No workouts scheduled.</p>
        )}
      </div>

      <div className="actions-grid">
        <Link to="/workouts" className="action-card">
          <img src="/icons/log.svg" alt="" />
          <span>Log Workout</span>
        </Link>
        <Link to="/scheduled-workouts" className="action-card">
          <img src="/icons/calendar.svg" alt="" />
          <span>Schedule Workout</span>
        </Link>
        <Link to="/goals" className="action-card set-goals">
          <img src="/icons/target.svg" alt="" />
          <span>Set Goals</span>
        </Link>
      </div>
    </div>
  );
}