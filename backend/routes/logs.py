from flask import Blueprint, request, jsonify,Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import logs_collection,db
import pandas as pd
from datetime import datetime
from utils import serialize_docs
from bson import ObjectId

logs_bp = Blueprint('logs', __name__, url_prefix='/api/logs')

@logs_bp.route("/export", methods=["GET"])
@jwt_required()
def export_logs():
    """
    Export logs data in CSV / JSON / Excel format
    """
    export_format = request.args.get("format", "csv")
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    query = {}

    if from_date and to_date:
        query["timestamp"] = {
            "$gte": datetime.fromisoformat(from_date),
            "$lte": datetime.fromisoformat(to_date)
        }

    logs = list(db.logs.find(query, {"_id": 0}))

    if not logs:
        return jsonify({"message": "No data available"}), 404

    df = pd.DataFrame(logs)

    if export_format == "json":
        return jsonify(logs)

    if export_format == "csv":
        return Response(
            df.to_csv(index=False),
            mimetype="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=logs.csv"
            }
        )

    if export_format == "excel":
        output = df.to_excel(index=False)
        return Response(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=logs.xlsx"
            }
        )

    return jsonify({"error": "Invalid format"}), 400

@logs_bp.route('/', methods=['GET'])
@jwt_required()
def get_logs():
    user_id = get_jwt_identity()
    
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    skip = (page - 1) * limit
    
    api_id = request.args.get('api_id')
    
    query = {'user_id': ObjectId(user_id)}
    
    if api_id:
        try:
            query['api_id'] = ObjectId(api_id)
        except:
            return jsonify({'error': 'Invalid API ID'}), 400
    
    logs = list(logs_collection.find(query).skip(skip).limit(limit).sort('timestamp', -1))
    total = logs_collection.count_documents(query)
    
    return jsonify({
        'logs': serialize_docs(logs),
        'total': total,
        'page': page,
        'pages': (total + limit - 1) // limit
    }), 200

@logs_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    
    total_requests = logs_collection.count_documents({'user_id': ObjectId(user_id)})
    
    success_requests = logs_collection.count_documents({
        'user_id': ObjectId(user_id),
        'status_code': {'$gte': 200, '$lt': 300}
    })
    
    error_requests = logs_collection.count_documents({
        'user_id': ObjectId(user_id),
        'status_code': {'$gte': 400}
    })
    
    pipeline = [
        {'$match': {'user_id': ObjectId(user_id)}},
        {'$group': {
            '_id': None,
            'avg_response_time': {'$avg': '$response_time'}
        }}
    ]
    
    result = list(logs_collection.aggregate(pipeline))
    avg_response_time = result[0]['avg_response_time'] if result else 0
    
    return jsonify({
        'total_requests': total_requests,
        'success_requests': success_requests,
        'error_requests': error_requests,
        'avg_response_time': round(avg_response_time, 2)
    }), 200

