import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import './App.css';
import Auth from './pages/Auth';
import Dashboard from './pages/Dashboard';
import SubmitComplaint from './pages/SubmitComplaint';
import MLTester from './pages/MLTester';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  return (
    <Router>
      <div className="App">
        <Navigation user={user} setUser={setUser} />
        <Routes>
          <Route path="/" element={<Auth />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/submit"
            element={
              <ProtectedRoute>
                <SubmitComplaint />
              </ProtectedRoute>
            }
          />
          <Route
            path="/ml-tester"
            element={
              <ProtectedRoute>
                <MLTester />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

function Navigation({ user, setUser }) {
  const navigate = useNavigate();
  const location = useLocation();
  const isAuthPage = location.pathname === '/';

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
    navigate('/');
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center gap-6">
          <h1 className="text-2xl font-bold">📋 Complaint System</h1>
          {user && !isAuthPage && (
            <div className="flex gap-4">
              <NavLink to="/dashboard">Dashboard</NavLink>
              <NavLink to="/submit">Submit</NavLink>
              <NavLink to="/ml-tester">ML Tester</NavLink>
            </div>
          )}
        </div>
        {user && !isAuthPage && (
          <div className="flex items-center gap-4">
            <span className="text-sm opacity-90">{user.email}</span>
            <button
              onClick={handleLogout}
              className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded transition"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
}

function NavLink({ to, children }) {
  const navigate = useNavigate();
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <button
      onClick={() => navigate(to)}
      className={`px-3 py-2 rounded transition ${
        isActive
          ? 'bg-white text-blue-600 font-semibold'
          : 'hover:bg-white hover:bg-opacity-20'
      }`}
    >
      {children}
    </button>
  );
}

export default App;
