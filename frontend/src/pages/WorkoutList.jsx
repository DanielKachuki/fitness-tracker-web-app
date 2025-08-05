import { useEffect, useState } from "react";
import { api } from "../api";

export default function WorkoutList() {
  const [workouts, setWorkouts] = useState([]);
  const [error, setError]       = useState(null);

  useEffect(() => {
    api.listWorkouts()
      .then(setWorkouts)
      .catch(err => setError(err.message));
  }, []);

  if (error) return <div>Error: {error}</div>;
  if (!workouts.length) return <div>Loading workouts…</div>;

  return (
    <ul>
      {workouts.map(w => (
        <li key={w.id}>
          {w.workout_date}: {w.workout_type} for {w.duration}
        </li>
      ))}
    </ul>
  );
}