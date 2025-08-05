// frontend/src/pages/ScheduleWorkout.jsx
import React, { useState, useEffect } from 'react';
import { Calendar, Views, dateFnsLocalizer } from 'react-big-calendar';
import { format, parse, startOfWeek, getDay } from 'date-fns';
import { enUS } from 'date-fns/locale';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import './ScheduleWorkout.css';

const locales = { 'en-US': enUS };
const localizer = dateFnsLocalizer({ format, parse, startOfWeek, getDay, locales });

export default function ScheduleWorkout() {
  const [events, setEvents] = useState([]);
  const [view, setView]   = useState(Views.MONTH);
  const navigate         = useNavigate();

  useEffect(() => {
    api.listScheduledWorkouts().then(data => {
      setEvents(data.map(s => ({
        id:      s.id,
        title:   s.workout_type.name,
        start:   new Date(s.scheduled_date),
        end:     new Date(s.scheduled_date),
        allDay:  true,
      })));
    });
  }, []);

  // ─── Custom Month‐view Date Header ──────────────────────────────────────────
  function CustomDateHeader({ date, label }) {
  const iso = date.toISOString().slice(0, 10);
  return (
    <div className="rbc-header-with-button">
      <span className="rbc-header-label">{label}</span>
      <button
        className="rbc-date-add-btn"
        onClick={() => navigate(`/workouts/new?date=${iso}`)}
      >
        ＋
      </button>
    </div>
  );
}
  // ────────────────────────────────────────────────────────────────────────────

  return (
    <div className="schedule-page">
      <header className="schedule-header">
        <h1>Schedule Workout</h1>
        <div className="controls">
          <Link to="/workouts/new" className="add-btn">+ Add Workout</Link>
        </div>
      </header>

      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        view={view}
        onView={setView}
        selectable
        components={{
          // <- this hooks into month‐view only
          month: { dateHeader: CustomDateHeader }
        }}
        style={{ height: 600, margin: '1rem' }}
      />
    </div>
  );
}
