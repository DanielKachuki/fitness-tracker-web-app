import { useState, useEffect } from 'react'
import { getToken } from '../utils/auth'   // your JWT helper
//import { getProfile, updateProfile } from '../api'
//import { listWorkouts } from '../api'

export default function Settings() {
  const [form, setForm] = useState({
    name: '', sex: 'O', height: '', weight: ''
  })

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/profile/`, {
      headers: { 'Authorization': `Bearer ${getToken()}` }
    })
    .then(res => res.json())
    .then(data => setForm(data))
  }, [])

  const handleChange = e =>
    setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = e => {
    e.preventDefault()
    fetch(`${import.meta.env.VITE_API_URL}/api/profile/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      },
      body: JSON.stringify(form)
    })
    .then(res => res.json())
    .then(() => alert('Profile updated!'))
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name</label>
        <input name="name" value={form.name} onChange={handleChange}/>
      </div>
      <div>
        <label>Sex</label>
        <select name="sex" value={form.sex} onChange={handleChange}>
          <option value="M">Male</option>
          <option value="F">Female</option>
          <option value="O">Other</option>
        </select>
      </div>
      <div>
        <label>Height (cm)</label>
        <input
          name="height"
          type="number"
          step="0.1"
          value={form.height}
          onChange={handleChange}
        />
      </div>
      <div>
        <label>Weight (kg)</label>
        <input
          name="weight"
          type="number"
          step="0.1"
          value={form.weight}
          onChange={handleChange}
        />
      </div>
      <button type="submit">Save Settings</button>
    </form>
  )
}
