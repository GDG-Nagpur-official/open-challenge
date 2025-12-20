import { useState } from "react";
import { toast } from "react-toastify";
import { Mail } from "lucide-react";
import { Link } from "react-router-dom";
import api from "../utils/api";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.post("/api/auth/forgot-password", { email });
      toast.success("Reset link sent if email exists");
    } catch {
      toast.error("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div className="card" style={{ maxWidth: "400px", width: "100%" }}>
        <h2 style={{ marginBottom: "20px", textAlign: "center" }}>
          Reset Password
        </h2>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <div style={{ position: "relative" }}>
              <Mail style={{ position: "absolute", top: "10px", left: "10px" }} />
              <input
                type="email"
                className="form-control"
                style={{ paddingLeft: "35px" }}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>
          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: "100%" }}
            disabled={loading}
          >
            {loading ? "Sending..." : "Send Reset Link"}
          </button>
        </form>
        <p style={{ marginTop: "20px", textAlign: "center" }}>
          <Link to="/login">Back to Login</Link>
        </p>
      </div>
    </div>
  );
}