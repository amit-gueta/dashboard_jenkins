import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { getAllBuilds, getDistinctProjects } from '@/services/api';
import { Build } from '@/types';

const BuildsListPage: React.FC = () => {
  const [selectedProject, setSelectedProject] = useState<string | undefined>(undefined);

  const { data: projects, isLoading: isLoadingProjects } = useQuery<string[], Error>({
    queryKey: ['projects'],
    queryFn: getDistinctProjects,
  });

  const { data: builds, isLoading: isLoadingBuilds, error, refetch } = useQuery<Build[], Error>({
    queryKey: ['builds', selectedProject],
    queryFn: () => getAllBuilds(selectedProject),
    enabled: true, // Fetch initially, and when selectedProject changes
  });

  useEffect(() => {
    refetch(); // Refetch when selectedProject changes
  }, [selectedProject, refetch]);

  const handleProjectFilterChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedProject(event.target.value === "" ? undefined : event.target.value);
  };

  const formatDate = (dateString?: string | null) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  return (
    <div>
      <h1 className="text-3xl font-semibold mb-6">Builds</h1>

      <div className="mb-4">
        <label htmlFor="projectFilter" className="mr-2">Filter by project:</label>
        <select
          id="projectFilter"
          value={selectedProject || ""}
          onChange={handleProjectFilterChange}
          className="p-2 border rounded"
        >
          <option value="">All Projects</option>
          {isLoadingProjects && <option value="">Loading projects...</option>}
          {projects?.map(proj => (
            <option key={proj} value={proj}>{proj}</option>
          ))}
        </select>
      </div>

      {isLoadingBuilds && <p>Loading builds...</p>}
      {error && <p className="text-red-500">Error fetching builds: {error.message}</p>}

      {!isLoadingBuilds && builds && builds.length === 0 && <p>No builds found.</p>}

      {builds && builds.length > 0 && (
        <div className="overflow-x-auto bg-white shadow-md rounded-lg">
          <table className="min-w-full table-auto">
            <thead className="bg-gray-200">
              <tr>
                <th className="px-4 py-2 text-left">Project</th>
                <th className="px-4 py-2 text-left">MR#</th>
                <th className="px-4 py-2 text-left">Build#</th>
                <th className="px-4 py-2 text-left">Status</th>
                <th className="px-4 py-2 text-left">Start Time</th>
                <th className="px-4 py-2 text-left">Duration (ms)</th>
                <th className="px-4 py-2 text-left">Stages</th>
                <th className="px-4 py-2 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {builds.map(build => (
                <tr key={build.id} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-2">{build.project}</td>
                  <td className="px-4 py-2">{build.mr_number}</td>
                  <td className="px-4 py-2">{build.build_number}</td>
                  <td className="px-4 py-2">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                      build.status === 'SUCCESS' ? 'bg-green-200 text-green-800' :
                      build.status === 'FAILURE' ? 'bg-red-200 text-red-800' :
                      build.status === 'UNSTABLE' ? 'bg-yellow-200 text-yellow-800' :
                      build.status === 'IN_PROGRESS' ? 'bg-blue-200 text-blue-800' :
                      'bg-gray-200 text-gray-800'
                    }`}>
                      {build.status}
                    </span>
                  </td>
                  <td className="px-4 py-2">{formatDate(build.start_time)}</td>
                  <td className="px-4 py-2">{build.duration_millis ?? 'N/A'}</td>
                  <td className="px-4 py-2">{build.stages?.length || 0}</td>
                  <td className="px-4 py-2">
                    <Link to={`/builds/${build.id}`} className="text-blue-600 hover:underline">
                      View Details
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default BuildsListPage;
