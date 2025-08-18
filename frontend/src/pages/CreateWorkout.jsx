import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import api from "../api";
import "../styles/CreateWorkout.css";

export default function CreateWorkout() {
  const navigate = useNavigate();
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const defaultDate = params.get("date") || new Date().toISOString().slice(0,10);

  // form state
  const [workoutName, setWorkoutName] = useState("");
  const [activity,   setActivity]    = useState("");
  const [date,       setDate]        = useState(defaultDate);
  const [hh,         setHh]          = useState("00");
  const [mm,         setMm]          = useState("30");
  const [ss,         setSs]          = useState("00");
  const [calories,   setCalories]    = useState("");
  const [notes,      setNotes]       = useState("");
  const [showAddl,   setShowAddl]    = useState(false);

  const [types,      setTypes]       = useState([]);

  // load activity types
  useEffect(() => {
    api.getWorkoutTypes().then(setTypes).catch(console.error);
  }, []);

  // placeholder calorie calculator (you can swap in real logic)
  const handleCalculate = () => {
    const durationH = Number(hh) + Number(mm)/60 + Number(ss)/3600;
    // naive formula: 50 kcal per hour → adjust as you like
    const est = Math.round(durationH * 50);
    setCalories(est);
  };

  const handleSubmit = async e => {
    e.preventDefault();
    if (!activity) {
      return alert("Please select an activity.");
    }
    const duration = `${hh.padStart(2,"0")}:${mm.padStart(2,"0")}:${ss.padStart(2,"0")}`;
    try {
      await api.createWorkout({
        workout_type: Number(activity),
        duration,
        workout_date: date,
        notes: workoutName.trim() || notes.trim(),
      });
      navigate("/");
    } catch (err) {
      console.error(err);
      alert("Could not save workout.");
    }
  };

  return (
    <form className="cw-form" onSubmit={handleSubmit}>
      <h1>Log Workout</h1>

      <label>Workout name</label>
      <input
        type="text"
        value={workoutName}
        onChange={e => setWorkoutName(e.target.value)}
        placeholder=""
      />

      <div className="cw-row">
        <div>
          <label>Date *</label>
          <input
            type="date"
            value={date}
            onChange={e => setDate(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Activity *</label>
          <select
            value={activity}
            onChange={e => setActivity(e.target.value)}
            required
          >
            <option value="">Select an activity</option>
            {types.map(t => (
              <option
                key={t.workout_type_id}
                value={t.workout_type_id}
              >
                {t.workout_name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <fieldset className="cw-fieldset cw-duration">
        <legend>Duration</legend>
        <div className="cw-duration-inputs">
          <input
            type="number" min="0" max="23"
            value={hh}
            onChange={e => setHh(e.target.value)}
            placeholder="hh"
            required
          />:
          <input
            type="number" min="0" max="59"
            value={mm}
            onChange={e => setMm(e.target.value)}
            placeholder="mm"
            required
          />:
          <input
            type="number" min="0" max="59"
            value={ss}
            onChange={e => setSs(e.target.value)}
            placeholder="ss"
            required
          />
        </div>
      </fieldset>

      <div className="cw-row">
        <div className="cw-calories">
          <label>Calories Burned (kcal)</label>
          <input
            type="text"
            value={calories}
            readOnly
            placeholder="—"
          />
        </div>
        <button
          type="button"
          className="cw-calc-btn"
          onClick={handleCalculate}
        >
          Calculate
        </button>
      </div>

      <label>Notes</label>
      <textarea
        rows="3"
        value={notes}
        onChange={e => setNotes(e.target.value)}
        placeholder="Add any extra details..."
      />

      <button
        type="button"
        className="cw-addl-toggle"
        onClick={() => setShowAddl(x => !x)}
      >
        Additional Stats {showAddl ? "▲" : "▼"}
      </button>

      {showAddl && (
        <div className="cw-addl-section">
          {/* add your extra inputs here */}
          <label>RPE (1-10)</label>
          <input type="number" min="1" max="10" placeholder="5" />
          <label>Heart Rate (bpm)</label>
          <input type="number" placeholder="—" />
        </div>
      )}

      <button type="submit" className="cw-save-btn">
        Save
      </button>
    </form>
  );
}