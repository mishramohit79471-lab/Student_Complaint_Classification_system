import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="bg-blue-600 text-white p-4">
          <h1 className="text-2xl font-bold">Student Complaint System</h1>
        </nav>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div className="container mx-auto p-8">
      <h2 className="text-3xl font-bold mb-4">Welcome</h2>
      <p className="text-gray-600">
        AI-Powered Student Complaint Classification & Department Routing System
      </p>
    </div>
  );
}

export default App;
