import { apiClient } from "./axiosClient";

export const downloadApi = {
  downloadConversation: async (id: string, format: "md" | "txt" | "pdf"): Promise<void> => {
    // Assuming backend returns a file stream
    const response = await apiClient.get(`/conversations/${id}/download`, {
      params: { format },
      responseType: 'blob'
    });
    
    // Create a download link and click it programmatically
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `conversation-${id}.${format}`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  }
};
