import { apiClient } from './axiosClient';

export const analyzeDocument = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post('/api/documents/analyze', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const ingestDocument = async (filename: string, tmp_path: string, workflow: string) => {
    const response = await apiClient.post('/api/documents/ingest', {
        filename,
        tmp_path,
        workflow,
    });
    return response.data;
};
