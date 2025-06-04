import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getBuildById } from '@/services/api';
import { Build, Stage } from '@/types';

const BuildDetailPage: React.FC = () => {
  const { buildId } = useParams<{ buildId: string }>();

  const { data: build, isLoading, error } = useQuery<Build, Error>({
    queryKey: ['build', buildId],
    queryFn: () => getBuildById(buildId!),
    enabled: !!buildId,
  });

  const formatDate = (dateString?: string | null) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  const formatDuration = (ms?: number | null) => {
    if (ms === null || typeof ms === 'undefined') return 'N/A';
    if (ms < 1000) return `${ms} ms`;
    return `${(ms / 1000).toFixed(2)} s`;
  }

  if (isLoading) return <p>Loading build details...</p>;
  if (error) return <p className="text-red-500">Error fetching build: {error.message}</p>;
  if (!build) return <p>Build not found.</p>;

  return (
    <div className="container mx-auto p-4">
      <div className="mb-4">
        <Link to="/builds" className="text-blue-600 hover:underline">&larr; Back to Builds List</Link>
      </div>
      <div className="bg-white shadow-lg rounded-lg p-6 mb-6">
        <h1 className="text-3xl font-bold mb-2">
          Build: {build.project} / MR-{build.mr_number} / #{build.build_number}
        </h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-gray-700 mb-4">
          <p><strong>Status:</strong>
            <span className={`ml-1 px-2 py-1 text-sm font-semibold rounded-full ${
              build.status === 'SUCCESS' ? 'bg-green-200 text-green-800' :
              build.status === 'FAILURE' ? 'bg-red-200 text-red-800' :
              build.status === 'UNSTABLE' ? 'bg-yellow-200 text-yellow-800' :
              build.status === 'IN_PROGRESS' ? 'bg-blue-200 text-blue-800' :
              'bg-gray-200 text-gray-800'
            }`}>
              {build.status}
            </span>
          </p>
          <p><strong>Pipeline URL:</strong> {build.pipeline_url ? <a href={build.pipeline_url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">Link</a> : 'N/A'}</p>
          <p><strong>Start Time:</strong> {formatDate(build.start_time)}</p>
          <p><strong>End Time:</strong> {formatDate(build.end_time)}</p>
          <p><strong>Total Duration:</strong> {formatDuration(build.duration_millis)}</p>
          <p><strong>Queue Duration:</strong> {formatDuration(build.queue_duration_millis)}</p>
          <p><strong>Commit Hash:</strong> {build.commit_hash || 'N/A'}</p>
          <p><strong>Branch:</strong> {build.branch_name || 'N/A'}</p>
          <p><strong>Triggered By:</strong> {build.triggered_by || 'N/A'}</p>
        </div>
      </div>

      <h2 className="text-2xl font-semibold mb-4">Stages ({build.stages?.length || 0})</h2>
      {build.stages && build.stages.length > 0 ? (
        <div className="overflow-x-auto bg-white shadow-md rounded-lg">
          <table className="min-w-full table-auto">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left">Name</th>
                <th className="px-4 py-2 text-left">Status</th>
                <th className="px-4 py-2 text-left">Start Time</th>
                <th className="px-4 py-2 text-left">Duration</th>
                <th className="px-4 py-2 text-left">Order</th>
              </tr>
            </thead>
            <tbody>
              {build.stages.sort((a, b) => (a.stage_order ?? 0) - (b.stage_order ?? 0)).map(stage => (
                <tr key={stage.id} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-2">{stage.stage_name}</td>
                  <td className="px-4 py-2">
                     <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                      stage.status === 'SUCCESS' ? 'bg-green-200 text-green-800' :
                      stage.status === 'FAILURE' ? 'bg-red-200 text-red-800' :
                      stage.status === 'UNSTABLE' ? 'bg-yellow-200 text-yellow-800' :
                      stage.status === 'SKIPPED' || stage.status === 'NOT_EXECUTED' || stage.status === 'ABORTED' ? 'bg-gray-300 text-gray-700' :
                      'bg-blue-200 text-blue-800' // Default for IN_PROGRESS or others
                    }`}>
                      {stage.status}
                    </span>
                  </td>
                  <td className="px-4 py-2">{formatDate(stage.start_time)}</td>
                  <td className="px-4 py-2">{formatDuration(stage.duration_millis)}</td>
                  <td className="px-4 py-2">{stage.stage_order ?? 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No stages found for this build.</p>
      )}
    </div>
  );
};

export default BuildDetailPage;
