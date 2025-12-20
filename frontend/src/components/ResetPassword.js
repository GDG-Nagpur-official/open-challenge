import { useSearchParams, useNavigate } from "react-router-dom";
import { useState } from "react";
import api from "../api/axios";
import { toast } from "react-toastify";
import { Lock } from "lucide-react";

export default function ResetPassword() {
  const [params] = useSearchParams();
  const token = params.get("token");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const reset = async () => {
    try {
      await api.post("/auth/reset-password", { token, password });
      toast.success("Password reset successful");
      navigate("/login");
    } catch {
      toast.error("Invalid or expired link");
    }
  };

  return (
    <div>
      <Lock />
      <input type="password" onChange={e => setPassword(e.target.value)} />
      <button onClick={reset}>Reset Password</button>
    </div>
  );
}
