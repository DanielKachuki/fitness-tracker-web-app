
import { Outlet } from "react-router-dom";
import NavBar from "./NavBar";

export default function AuthenticatedLayout() {
  return (
    <>
      <NavBar />
      <main style={{ padding: "1rem" }}>
        <Outlet />
      </main>
    </>
  );
}