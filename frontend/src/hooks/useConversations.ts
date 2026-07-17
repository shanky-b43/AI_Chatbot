import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { conversationApi } from "@/api/conversationApi";
import { useChatStore } from "@/store/useChatStore";
import { useEffect } from "react";

export const useConversations = () => {
  const queryClient = useQueryClient();
  const { setConversationList, searchQuery } = useChatStore();

  const { data: conversations, isLoading, error } = useQuery({
    queryKey: ["conversations", searchQuery],
    queryFn: () => searchQuery 
      ? conversationApi.searchConversations(searchQuery)
      : conversationApi.getConversations(),
  });

  useEffect(() => {
    if (conversations) {
      setConversationList(conversations);
    }
  }, [conversations, setConversationList]);

  const deleteMutation = useMutation({
    mutationFn: conversationApi.deleteConversation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
  });

  const renameMutation = useMutation({
    mutationFn: ({ id, title }: { id: string, title: string }) => 
      conversationApi.updateConversation(id, title),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
  });

  return {
    conversations,
    isLoading,
    error,
    deleteConversation: deleteMutation.mutate,
    renameConversation: renameMutation.mutate,
  };
};
