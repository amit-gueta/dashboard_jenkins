import axios from 'axios';
import { Build, Stage } from '@/types'; // Assuming types will be defined in @/types

// Base URL for the API, proxied by Vite dev server or Nginx in production
const API_BASE_URL = '/api/v1'; // Matches backend API_V1_STR

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ----- Build Endpoints -----
export const getAllBuilds = async (project?: string): Promise<Build[]> => {
  const params = project ? { project } : {};
  const response = await apiClient.get('/builds/', { params });
  return response.data;
};

export const getBuildById = async (buildId: number | string): Promise<Build> => {
  const response = await apiClient.get(`/builds/${buildId}`);
  return response.data;
};

export const getDistinctProjects = async (): Promise<string[]> => {
  const response = await apiClient.get('/builds/projects');
  return response.data;
};

// ----- Stage Ingress Endpoint (for seeding/testing if needed from frontend) -----
// This is the sample data structure the user provided for stages.
export interface StageIngressPayload {
  pipeURL: string;
  group: string;
  repo: string;
  MR_num: string;
  build_num: string;
  displayName: string;
  durationInMillis?: number | null;
  result: string;
  startTime?: string | null; // ISO string or null
}

export const postStageData = async (stageData: StageIngressPayload): Promise<Stage> => {
  const response = await apiClient.post('/ingress/stage', stageData);
  return response.data;
};


// ----- Health Check -----
export const getHealth = async (): Promise<any> => {
  const response = await apiClient.get('/health');
  return response.data;
};

export default apiClient;
