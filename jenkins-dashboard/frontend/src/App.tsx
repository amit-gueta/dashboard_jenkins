import React from 'react';
import { Routes, Route, Link, Navigate } from 'react-router-dom';
// Pages
import HomePage from '@/pages/HomePage'; // Assuming HomePage shows some overview or links
import ProjectPage from '@/pages/ProjectPage'; // Keep if used for other purposes
import AnalyticsPage from '@/pages/AnalyticsPage'; // Keep if used
import BuildsListPage from '@/pages/BuildsListPage';
import BuildDetailPage from '@/pages/BuildDetailPage';

// Basic Layout Structure
const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="min-h-screen bg-gray-100 text-gray-800">
    <nav className="bg-blue-600 text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold hover:text-blue-200">Jenkins Dashboard</Link>
        <div>
          <Link to="/builds" className="px-3 py-2 hover:bg-blue-700 rounded">Builds</Link>
          {/* <Link to="/projects/sample-project" className="px-3 py-2 hover:bg-blue-700 rounded">Project View</Link> */}
          {/* <Link to="/analytics" className="px-3 py-2 hover:bg-blue-700 rounded">Analytics</Link> */}
        </div>
      </div>
    </nav>
    <main className="container mx-auto p-4">
      {children}
    </main>
    <footer className="text-center p-4 bg-gray-200 text-gray-600 mt-8">
      © $(date +%Y) Jenkins Dashboard
    </footer>
  </div>
);

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/builds" replace />} /> {/* Default to builds list */}
        <Route path="/home" element={<HomePage />} /> {/* Kept if needed, but / is now /builds */}
        <Route path="/builds" element={<BuildsListPage />} />
        <Route path="/builds/:buildId" element={<BuildDetailPage />} />

        {/* Old routes, can be removed or repurposed if ProjectPage/AnalyticsPage are not used for now */}
        <Route path="/projects/:projectId" element={<ProjectPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
      </Routes>
    </Layout>
  );
}

export default App;
