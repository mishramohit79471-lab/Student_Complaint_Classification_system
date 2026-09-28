import React, { useState, useEffect } from 'react';
import api from '../services/api';

export default function MLTester() {
  const [testText, setTestText] = useState('');
  const [result, setResult] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [statsLoading, setStatsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setStatsLoading(true);
      const response = await api.get('/complaints/ml/stats');
      setStats(response.data);
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    } finally {
      setStatsLoading(false);
    }
  };

  const handleClassify = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);

    try {
      const response = await api.post('/complaints/ml/classify', {
        text: testText,
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to classify text');
    } finally {
      setLoading(false);
    }
  };

  const exampleComplaints = [
    'The WiFi in classroom 201 has been down for 3 days. We cannot access online resources for our coursework.',
    'I was charged double for my semester fees. Please check my account and refund the extra amount.',
    'The hostel food quality has deteriorated significantly. Many students are getting sick.',
    'My attendance record shows 2 extra absences that I did not take. Please correct this immediately.',
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold mb-8">ML Classification Tester</h2>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Test Form */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h3 className="text-xl font-bold mb-4">Test Classification</h3>

              {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                  {error}
                </div>
              )}

              <form onSubmit={handleClassify}>
                <div className="mb-6">
                  <label className="block text-gray-700 font-bold mb-2">Enter complaint text:</label>
                  <textarea
                    value={testText}
                    onChange={(e) => setTestText(e.target.value)}
                    placeholder="Type or paste a complaint here..."
                    rows="6"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                    required
                  ></textarea>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-blue-600 text-white font-bold py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
                >
                  {loading ? 'Classifying...' : 'Classify Text'}
                </button>
              </form>

              {/* Quick Examples */}
              <div className="mt-8 pt-8 border-t">
                <h4 className="font-bold mb-3">Quick Examples:</h4>
                <div className="space-y-2">
                  {exampleComplaints.map((example, idx) => (
                    <button
                      key={idx}
                      onClick={() => setTestText(example)}
                      className="w-full text-left px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded text-sm text-gray-700 transition"
                    >
                      {example.substring(0, 60)}...
                    </button>
                  ))}
                </div>
              </div>

              {/* Result */}
              {result && (
                <div className="mt-8 pt-8 border-t">
                  <h4 className="font-bold mb-4">Classification Result:</h4>
                  <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg p-6 border border-blue-200">
                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div>
                        <p className="text-sm text-gray-600">Predicted Category</p>
                        <p className="text-2xl font-bold text-blue-600">{result.predicted_category}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Confidence Score</p>
                        <p className="text-2xl font-bold text-green-600">{(result.confidence_score * 100).toFixed(1)}%</p>
                      </div>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Assigned Department</p>
                      <p className="text-lg font-semibold text-purple-600">{result.assigned_department}</p>
                    </div>
                    <div className="mt-4 pt-4 border-t border-blue-200">
                      <p className="text-xs text-gray-600">Model Status</p>
                      <span className={`inline-block mt-1 px-3 py-1 rounded-full text-sm font-semibold ${
                        result.model_status === 'trained'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {result.model_status === 'trained' ? '✓ Trained' : '⚠ Not Trained'}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Stats Panel */}
          <div>
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold mb-4">ML Model Statistics</h3>

              {statsLoading ? (
                <p className="text-gray-500">Loading stats...</p>
              ) : stats ? (
                <div className="space-y-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-600">Model Status</p>
                    <p className="text-2xl font-bold text-blue-600">
                      {stats.model_trained ? '✓ Trained' : '⚠ Not Trained'}
                    </p>
                  </div>

                  <div className="bg-green-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-600">Total Complaints</p>
                    <p className="text-2xl font-bold text-green-600">{stats.total_complaints}</p>
                  </div>

                  <div className="bg-purple-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-600">Auto-Classified</p>
                    <p className="text-2xl font-bold text-purple-600">{stats.auto_classified}</p>
                  </div>

                  <div className="bg-orange-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-600">Classification Rate</p>
                    <p className="text-2xl font-bold text-orange-600">{stats.classification_rate}%</p>
                  </div>

                  <div className="bg-indigo-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-600">Avg Confidence</p>
                    <p className="text-2xl font-bold text-indigo-600">{(stats.average_confidence * 100).toFixed(1)}%</p>
                  </div>

                  {/* Category Distribution */}
                  <div className="pt-4 border-t">
                    <p className="font-bold mb-3">Category Distribution:</p>
                    <div className="space-y-2 text-sm">
                      {Object.entries(stats.category_distribution || {})
                        .sort(([, a], [, b]) => b - a)
                        .slice(0, 5)
                        .map(([category, count]) => (
                          <div key={category} className="flex justify-between">
                            <span className="text-gray-600">{category}</span>
                            <span className="font-semibold">{count}</span>
                          </div>
                        ))}
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">Failed to load stats</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
