import { apiClient } from "./axiosClient";
import { Message } from "@/types";

export const chatApi = {
  getHistory: async (threadId: string): Promise<Message[]> => {
    const response = await apiClient.get<Message[]>(`/chat/${threadId}/history`);
    return response.data;
  },
  
  // Note: Streaming is handled differently (via SSE or fetch reader)
  // so we don't strictly need an Axios method for the stream, 
  // but we provide a base URL getter for the EventSource.
  getStreamUrl: (threadId: string): string => {
    const baseUrl = apiClient.defaults.baseURL || "http://127.0.0.1:8000";
    // The backend uses POST /chat for the stream
    return `${baseUrl}/chat`;
  }
};
