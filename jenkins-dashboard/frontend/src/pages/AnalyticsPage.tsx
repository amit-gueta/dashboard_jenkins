import React from 'react';

const AnalyticsPage: React.FC = () => {
  return (
    <div>
      <h1 className="text-3xl font-semibold mb-6">Pipeline Analytics</h1>
      <p className="text-gray-600">(Content for pipeline analytics: heatmaps, bottleneck charts, etc.)</p>
      {/* Placeholder for analytics components */}
      <div className="mt-8 bg-white p-4 rounded shadow">
        <h2 className="text-xl font-semibold mb-2">Stage Duration Heatmap</h2>
        <p className="text-gray-500">(Heatmap placeholder)</p>
      </div>
    </div>
  );
};

export default AnalyticsPage;
