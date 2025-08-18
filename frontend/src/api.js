import axios from "axios";
import { REFRESH_TOKEN, ACCESS_TOKEN } from "./constants.js";
import { setTokens } from "./utils/auth.js";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL + "/api",
});

axiosInstance.interceptors.request.use(config => {
  const token = localStorage.getItem(ACCESS_TOKEN);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const api = {
  login: ({ username, password }) =>
    axiosInstance.post("/token/", { username, password })
      .then(({ data }) => {
        setTokens(data);
        return data;
      }),

  register: ({ username, password }) =>
    axiosInstance.post("/user/register/", { username, password })
      .then(r => r.data),


  // Profile
  getProfile:    () => axiosInstance.get("/profile/").then(r => r.data),
  updateProfile: data => axiosInstance.put("/profile/", data).then(r => r.data),

  // Workouts
  getWorkoutTypes: () => axiosInstance.get("/workout-types/").then(r => r.data),
  listWorkouts:    () => axiosInstance.get("/workouts/").then(r => r.data),
  createWorkout:   data => axiosInstance.post("/workouts/", data).then(r => r.data),

  // **Scheduled Workouts** ← add this!
  listScheduledWorkouts: () =>
    axiosInstance.get("/scheduled-workouts/").then(r => r.data),

  // Goals
  listGoals: () => axiosInstance.get("/goals/").then(r => r.data),

};

export default api;
export { api };