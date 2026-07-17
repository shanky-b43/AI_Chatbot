import { apiClient } from "./axiosClient";
import { Conversation } from "@/types";

export const conversationApi = {
  getConversations: async (): Promise<Conversation[]> => {
    const response = await apiClient.get<Conversation[]>("/conversations");
    return response.data;
  },

  getConversation: async (id: string): Promise<Conversation> => {
    const response = await apiClient.get<Conversation>(`/conversations/${id}`);
    return response.data;
  },

  createConversation: async (): Promise<Conversation> => {
    const response = await apiClient.post<Conversation>("/conversations");
    return response.data;
  },

  updateConversation: async (id: string, title: string): Promise<Conversation> => {
    const response = await apiClient.patch<Conversation>(`/conversations/${id}`, { title });
    return response.data;
  },

  deleteConversation: async (id: string): Promise<void> => {
    await apiClient.delete(`/conversations/${id}`);
  },

  searchConversations: async (query: string): Promise<Conversation[]> => {
    const response = await apiClient.get<Conversation[]>("/conversations/search", {
      params: { q: query },
    });
    return response.data;
  },
};
