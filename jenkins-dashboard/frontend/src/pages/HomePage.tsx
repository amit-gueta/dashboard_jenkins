import React from 'react';

const HomePage: React.FC = () => {
  return (
    <div>
      <h1 className="text-3xl font-semibold mb-6">Executive Overview</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Placeholder KPI Cards */}
        <div className="bg-white p-4 rounded shadow">Total Builds (24h): N/A</div>
        <div className="bg-white p-4 rounded shadow">Success Rate: N/A%</div>
        <div className="bg-white p-4 rounded shadow">Avg Duration: N/A</div>
        <div className="bg-white p-4 rounded shadow">Queue Depth: N/A</div>
      </div>
      {/* Placeholder for charts */}
      <div className="mt-8 bg-white p-4 rounded shadow">
        <h2 className="text-xl font-semibold mb-2">Build Status Distribution</h2>
        <p className="text-gray-500">(Pie chart placeholder)</p>
      </div>
    </div>
  );
};

export default HomePage;
