import React, { useEffect, useRef } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { MessageBubble } from "../MessageBubble";
import { MessageInput } from "../MessageInput";
import { TypingIndicator } from "../TypingIndicator";
import { useChatStore } from "@/store/useChatStore";
import { chatApi } from "@/api/chatApi";
import { conversationApi } from "@/api/conversationApi";
import { useToast } from "@/hooks/use-toast";

export const ChatWindow = () => {
  const { 
    currentConversation, 
    setCurrentConversation,
    messages, 
    setMessages,
    addMessage,
    appendStreamChunk,
    loading, 
    setLoading,
    streaming,
    setStreaming
  } = useChatStore();
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, streaming]);

  // Load history when conversation changes
  useQuery({
    queryKey: ["chatHistory", currentConversation?.id],
    queryFn: async () => {
      if (!currentConversation) return [];
      const history = await chatApi.getHistory(currentConversation.id);
      setMessages(history);
      return history;
    },
    enabled: !!currentConversation,
  });

  const handleSend = async (text: string) => {
    const tempId = currentConversation?.id || crypto.randomUUID();
    
    // Optimistic UI update
    addMessage({
      role: "user",
      content: text,
      timestamp: new Date().toISOString()
    });

    setLoading(true);
    setStreaming(true);

    try {
      let activeThreadId = currentConversation?.id || tempId;

      // If new conversation, create it first on backend
      if (!currentConversation) {
        // Technically backend should create on POST /chat, 
        // but based on API contract: POST /conversations creates one
        const newConv = await conversationApi.createConversation();
        setCurrentConversation(newConv);
        activeThreadId = newConv.id;
        queryClient.invalidateQueries({ queryKey: ["conversations"] });
      }

      const url = chatApi.getStreamUrl(activeThreadId);

      // Using Fetch for SSE to easily send POST body
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text, user_id: "default_user", thread_id: activeThreadId })
      });

      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || ""; // Keep incomplete line in buffer
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6).trim();
            if (dataStr === '[DONE]') {
              setStreaming(false);
            } else if (dataStr.startsWith('[ERROR]')) {
              throw new Error(dataStr);
            } else if (dataStr) {
              try {
                const parsed = JSON.parse(dataStr);
                if (parsed.chunk) {
                  appendStreamChunk(parsed.chunk);
                } else if (parsed.error) {
                  throw new Error(parsed.error);
                }
              } catch (e) {
                // If the backend yields raw text instead of JSON
                if (!dataStr.startsWith('{')) {
                  appendStreamChunk(dataStr);
                }
              }
            }
          }
        }
      }
    } catch (err: any) {
      toast({
        title: "Error",
        description: err.message || "Failed to send message.",
        variant: "destructive"
      });
      setStreaming(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full max-w-4xl mx-auto">
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto px-4 md:px-8 py-8 flex flex-col gap-2 scroll-smooth"
      >
        {messages.length === 0 && !loading && (
          <div className="flex-1 flex flex-col items-center justify-center text-zinc-500">
            <h2 className="text-2xl font-semibold text-zinc-800 dark:text-zinc-200 mb-2">How can I help you today?</h2>
            <p>Send a message to start the conversation.</p>
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} message={msg} />
        ))}
        
        {loading && !streaming && <TypingIndicator />}
      </div>
      
      <div className="p-4 bg-white dark:bg-zinc-950">
        <MessageInput onSend={handleSend} disabled={loading} />
        <div className="text-center text-xs text-zinc-400 mt-2">
          AI can make mistakes. Consider verifying important information.
        </div>
      </div>
    </div>
  );
};
