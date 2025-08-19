import { Link } from "react-router-dom";
import "./landing.css";

export default function LandingPage() {
  return (
    <div className="lp-wrap">
      <header className="lp-nav">
        <div className="brand">
          <span className="dot" aria-hidden>●</span> FitnessTrack
        </div>
        <nav className="lp-links">
          <Link to="/login" className="btn ghost">Log in</Link>
          <Link to="/register" className="btn">Sign up</Link>
        </nav>
      </header>

      <main className="lp-hero">
        <h1>Own your routine.</h1>
        <p className="sub">
          Log workouts, schedule sessions, and hit your goals — all in one place.
        </p>

        {/* Card Navigation */}
        <div className="card-nav">
          <Link className="card">
            <div className="icon" aria-hidden>🏋️</div>
            <h3>Log a Workout</h3>
            <p>Quickly record name, duration, RPE, and notes.</p>
          </Link>

          <Link className="card">
            <div className="icon" aria-hidden>📅</div>
            <h3>Schedule Workout</h3>
            <p>Plan your week with a built‑in calendar.</p>
          </Link>

          <Link className="card">
            <div className="icon" aria-hidden>🎯</div>
            <h3>Set Goals</h3>
            <p>Track progress and auto‑complete via workouts.</p>
          </Link>
        </div>

        <div className="cta-row">
          <Link to="/login" className="btn">Get started</Link>
          <Link to="/home" className="btn ghost">View dashboard</Link>
        </div>
      </main>

      <footer className="lp-foot">
        <small>© {new Date().getFullYear()} FitnessTrack</small>
      </footer>
    </div>
  );
}
