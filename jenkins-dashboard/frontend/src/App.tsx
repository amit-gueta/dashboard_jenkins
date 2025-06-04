import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import HomePage from '@/pages/HomePage';
import ProjectPage from '@/pages/ProjectPage';
import AnalyticsPage from '@/pages/AnalyticsPage';

// Basic Layout Structure
const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="min-h-screen bg-gray-100 text-gray-800">
    <nav className="bg-blue-600 text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold hover:text-blue-200">Jenkins Dashboard</Link>
        <div>
          <Link to="/" className="px-3 py-2 hover:bg-blue-700 rounded">Home</Link>
          <Link to="/projects/sample-project" className="px-3 py-2 hover:bg-blue-700 rounded">Project View</Link>
          <Link to="/analytics" className="px-3 py-2 hover:bg-blue-700 rounded">Analytics</Link>
        </div>
      </div>
    </nav>
    <main className="container mx-auto p-4">
      {children}
    </main>
    <footer className="text-center p-4 bg-gray-200 text-gray-600 mt-8">
      © 2023 Jenkins Dashboard
    </footer>
  </div>
);

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/projects/:projectId" element={<ProjectPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        {/* Add more routes for other pages like Realtime, Historical Trends etc. */}
      </Routes>
    </Layout>
  );
}

export default App;
