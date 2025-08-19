import {useState} from 'react'
import api from "../api"
import {useNavigate} from "react-router-dom"
import {ACCESS_TOKEN, REFRESH_TOKEN} from "../constants"
import "../styles/Form.css"

export default function Form({ method }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading]   = useState(false);
  const navigate                 = useNavigate();

  const name = method === "login" ? "Login" : "Register";

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);

    try {
      if (method === "login") {
        // Call the dedicated login helper
        const { access, refresh } = await api.login({ username, password });
        localStorage.setItem(ACCESS_TOKEN, access);
        localStorage.setItem(REFRESH_TOKEN, refresh);
        navigate("/home");
      } else {
        // Call the dedicated register helper
        await api.register({ username, password });
        navigate("/login");
      }
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h1>{name}</h1>
      <input
        className="form-input"
        type="text"
        value={username}
        onChange={e => setUsername(e.target.value)}
        placeholder="Username"
        required
      />
      <input
        className="form-input"
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      <button className="form-button" type="submit" disabled={loading}>
        {loading ? `${name}…` : name}
      </button>
    </form>
  );
}