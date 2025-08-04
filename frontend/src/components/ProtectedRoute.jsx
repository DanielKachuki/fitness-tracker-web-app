import {Navigate} from "react-router-dom"
import { jwtDecode } from "jwt-decode"
import api from "../api";
import {REFRESH_TOKEN, ACCESS_TOKEN} from "../constants.js";
import {useState, useEffect} from "react";


function ProtectedRoute({children}) {
    const [isAuthorized, setIsAuthorized] = useState(null);

    useEffect(() => {
        auth().catch(() => setIsAuthorized(false))
    }, [])

    const refreshToken = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN)
        try{
            const res = await  api.post("/api/token/refresh/", {
                refresh});
            if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                return true;
            }
        } catch {
            return false;
        }
    };

    const auth = async () => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
            setIsAuthorized(false)
            return
        }
        const { exp } = jwtDecode(token);
        const now = Date.now() / 1000

        if (exp < now) {
            const success = await refreshToken();
            setIsAuthorized(success);
        } else {
            setIsAuthorized(true)
        }
    };

    if (isAuthorized === null) {
        return <div>Loading...</div>;
    }

    return isAuthorized ? children : <Navigate to="/login" />
}

export default ProtectedRoute;