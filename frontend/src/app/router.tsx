import { Navigate, createBrowserRouter } from "react-router-dom";
import { useAuth } from "@/shared/auth/AuthContext";
import { AppLayout } from "./AppLayout";
import { features } from "./features";

function HomeRedirect() {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  return <Navigate to={user.rol === "TECNICO" ? "/mis-obras" : "/dashboard"} replace />;
}

export const router = createBrowserRouter([
  ...features.filter((f) => f.public).flatMap((f) => f.routes),
  {
    element: <AppLayout />,
    children: [
      { path: "/", element: <HomeRedirect /> },
      ...features.filter((f) => !f.public).flatMap((f) => f.routes),
    ],
  },
]);
