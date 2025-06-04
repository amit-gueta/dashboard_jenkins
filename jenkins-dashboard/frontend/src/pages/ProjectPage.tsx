import React from 'react';
import { useParams } from 'react-router-dom';

const ProjectPage: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  return (
    <div>
      <h1 className="text-3xl font-semibold mb-6">Project Deep Dive: {projectId}</h1>
      <p className="text-gray-600">(Content for project {projectId} will go here: MR history, build comparison, etc.)</p>
      {/* Placeholder for project specific components */}
      <div className="mt-8 bg-white p-4 rounded shadow">
        <h2 className="text-xl font-semibold mb-2">MR Build History</h2>
        <p className="text-gray-500">(Table placeholder)</p>
      </div>
    </div>
  );
};

export default ProjectPage;
