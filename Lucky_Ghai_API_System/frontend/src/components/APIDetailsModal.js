import React from 'react';
import { X } from 'lucide-react';

const APIDetailsModal = ({ api, onClose }) => {
  return (
    <div className="modal" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>API Details</h2>
          <button className="close-btn" onClick={onClose}>
            <X size={24} />
          </button>
        </div>
        <div>
          <div style={{ marginBottom: '15px' }}>
            <strong>Name:</strong>
            <p>{api.name}</p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <strong>Description:</strong>
            <p>{api.description || 'No description'}</p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <strong>Endpoint:</strong>
            <p style={{ wordBreak: 'break-all' }}>{api.endpoint}</p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <strong>Method:</strong>
            <p>
              <span className={`badge badge-${api.method === 'GET' ? 'info' : api.method === 'POST' ? 'success' : 'warning'}`}>
                {api.method}
              </span>
            </p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <strong>Status:</strong>
            <p>
              <span className={`badge badge-${api.status === 'active' ? 'success' : 'danger'}`}>
                {api.status}
              </span>
            </p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <strong>Created:</strong>
            <p>{new Date(api.created_at).toLocaleString()}</p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <strong>Last Updated:</strong>
            <p>{new Date(api.updated_at).toLocaleString()}</p>
          </div>
          <button className="btn btn-secondary" onClick={onClose} style={{ width: '100%' }}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default APIDetailsModal;
