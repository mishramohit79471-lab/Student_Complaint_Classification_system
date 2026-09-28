import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function Dashboard() {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchComplaints();
  }, [statusFilter]);

  const fetchComplaints = async () => {
    try {
      setLoading(true);
      const params = statusFilter ? { status_filter: statusFilter } : {};
      const response = await api.get('/complaints/', { params });
      setComplaints(response.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch complaints');
      if (err.response?.status === 401) {
        navigate('/');
      }
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      SUBMITTED: 'bg-yellow-100 text-yellow-800',
      ASSIGNED: 'bg-blue-100 text-blue-800',
      IN_PROGRESS: 'bg-purple-100 text-purple-800',
      RESOLVED: 'bg-green-100 text-green-800',
      CLOSED: 'bg-gray-100 text-gray-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getCategoryColor = (category) => {
    const colors = {
      Academic: 'bg-red-100 text-red-800',
      Attendance: 'bg-orange-100 text-orange-800',
      Examination: 'bg-pink-100 text-pink-800',
      'Fee/Payment': 'bg-green-100 text-green-800',
      Hostel: 'bg-indigo-100 text-indigo-800',
      'Infrastructure/Maintenance': 'bg-cyan-100 text-cyan-800',
      Library: 'bg-teal-100 text-teal-800',
      Scholarship: 'bg-violet-100 text-violet-800',
      'Student Welfare': 'bg-fuchsia-100 text-fuchsia-800',
      'Technical/IT': 'bg-blue-100 text-blue-800',
      Transport: 'bg-lime-100 text-lime-800',
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold">My Complaints</h2>
          <button
            onClick={() => navigate('/submit')}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            + New Complaint
          </button>
        </div>

        <div className="mb-6 flex gap-4">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          >
            <option value="">All Status</option>
            <option value="SUBMITTED">Submitted</option>
            <option value="ASSIGNED">Assigned</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="RESOLVED">Resolved</option>
            <option value="CLOSED">Closed</option>
          </select>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">
            <p className="text-gray-500">Loading complaints...</p>
          </div>
        ) : complaints.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-500 text-lg">No complaints found</p>
            <button
              onClick={() => navigate('/submit')}
              className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
            >
              Submit Your First Complaint
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {complaints.map((complaint) => (
              <div key={complaint.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="text-xl font-bold text-gray-800">{complaint.title}</h3>
                    <p className="text-sm text-gray-500">ID: {complaint.id}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(complaint.status)}`}>
                    {complaint.status}
                  </span>
                </div>

                <p className="text-gray-600 mb-4 line-clamp-2">{complaint.description}</p>

                <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-sm">
                  <div>
                    <p className="text-gray-500">Category</p>
                    <span className={`inline-block px-2 py-1 rounded text-xs font-semibold ${getCategoryColor(complaint.category)}`}>
                      {complaint.category}
                    </span>
                  </div>
                  <div>
                    <p className="text-gray-500">Priority</p>
                    <p className="font-semibold">{complaint.priority || 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Department</p>
                    <p className="font-semibold">{complaint.assigned_department}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Confidence</p>
                    <p className="font-semibold">{(complaint.confidence_score * 100).toFixed(1)}%</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Submitted</p>
                    <p className="font-semibold text-xs">{new Date(complaint.created_at).toLocaleDateString()}</p>
                  </div>
                </div>

                {complaint.resolution && (
                  <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded">
                    <p className="text-sm font-semibold text-green-800">Resolution:</p>
                    <p className="text-sm text-green-700">{complaint.resolution}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
