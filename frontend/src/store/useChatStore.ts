import { create } from "zustand";
import { Conversation, Message } from "@/types";

interface ChatState {
  currentConversation: Conversation | null;
  conversationList: Conversation[];
  messages: Message[];
  loading: boolean;
  streaming: boolean;
  searchQuery: string;
  
  // Actions
  setCurrentConversation: (conversation: Conversation | null) => void;
  setConversationList: (list: Conversation[]) => void;
  addConversation: (conversation: Conversation) => void;
  removeConversation: (id: string) => void;
  updateConversation: (id: string, partial: Partial<Conversation>) => void;
  
  setMessages: (messages: Message[]) => void;
  addMessage: (message: Message) => void;
  appendStreamChunk: (chunk: string) => void;
  
  setLoading: (loading: boolean) => void;
  setStreaming: (streaming: boolean) => void;
  setSearchQuery: (query: string) => void;
  
  startNewConversation: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  currentConversation: null,
  conversationList: [],
  messages: [],
  loading: false,
  streaming: false,
  searchQuery: "",

  setCurrentConversation: (conversation) => set({ currentConversation: conversation }),
  
  setConversationList: (list) => set({ conversationList: list }),
  
  addConversation: (conversation) => set((state) => ({ 
    conversationList: [conversation, ...state.conversationList] 
  })),
  
  removeConversation: (id) => set((state) => ({
    conversationList: state.conversationList.filter((c) => c.id !== id),
    currentConversation: state.currentConversation?.id === id ? null : state.currentConversation
  })),
  
  updateConversation: (id, partial) => set((state) => ({
    conversationList: state.conversationList.map((c) => 
      c.id === id ? { ...c, ...partial } : c
    ),
    currentConversation: state.currentConversation?.id === id 
      ? { ...state.currentConversation, ...partial }
      : state.currentConversation
  })),

  setMessages: (messages) => set({ messages }),
  
  addMessage: (message) => set((state) => ({ 
    messages: [...state.messages, message] 
  })),
  
  appendStreamChunk: (chunk) => set((state) => {
    const lastMsg = state.messages[state.messages.length - 1];
    if (lastMsg && lastMsg.role === "assistant") {
      // Append to the existing assistant message
      const updatedMessages = [...state.messages];
      updatedMessages[updatedMessages.length - 1] = {
        ...lastMsg,
        content: lastMsg.content + chunk
      };
      return { messages: updatedMessages };
    } else {
      // Create a new assistant message if it doesn't exist yet
      return {
        messages: [
          ...state.messages, 
          { role: "assistant", content: chunk, timestamp: new Date().toISOString() }
        ]
      };
    }
  }),

  setLoading: (loading) => set({ loading }),
  setStreaming: (streaming) => set({ streaming }),
  setSearchQuery: (searchQuery) => set({ searchQuery }),

  startNewConversation: () => set({
    currentConversation: null,
    messages: [],
    streaming: false,
    loading: false
  })
}));
