from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import db
import pandas as pd

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/export", methods=["GET"])
@jwt_required()
def export_stats():
    logs = list(db.logs.find({}, {"_id": 0}))
    df = pd.DataFrame(logs)

    summary = {
        "total_requests": len(df),
        "success_count": len(df[df["status_code"] < 400]),
        "error_count": len(df[df["status_code"] >= 400]),
        "average_response_time": df["response_time"].mean()
    }

    per_api = df.groupby("api_name").size().to_dict()

    return jsonify({
        "summary": summary,
        "per_api_breakdown": per_api
    })
