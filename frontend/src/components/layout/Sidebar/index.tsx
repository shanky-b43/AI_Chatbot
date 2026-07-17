import React from "react";
import { MessageSquarePlus, Settings, User } from "lucide-react";
import { useChatStore } from "@/store/useChatStore";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { ConversationList } from "@/components/ConversationList";
import { SearchBar } from "@/components/SearchBar";

export const Sidebar = () => {
  const { startNewConversation } = useChatStore();

  return (
    <aside className="w-64 bg-zinc-50 dark:bg-zinc-900 border-r border-zinc-200 dark:border-zinc-800 flex flex-col h-screen hidden md:flex">
      {/* Top Section */}
      <div className="p-4 flex flex-col gap-4">
        <div className="flex items-center gap-2 px-2 text-zinc-900 dark:text-white font-semibold text-lg">
          <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm">
            AI
          </div>
          Chatbot
        </div>
        
        <Button 
          onClick={startNewConversation}
          className="w-full flex items-center justify-start gap-2 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 hover:bg-zinc-100 dark:hover:bg-zinc-700 border border-zinc-200 dark:border-zinc-700"
          variant="outline"
        >
          <MessageSquarePlus className="w-4 h-4" />
          New Conversation
        </Button>
      </div>

      <SearchBar />

      {/* Middle Section (Scrollable History) */}
      <ScrollArea className="flex-1 px-3">
        <ConversationList />
      </ScrollArea>

      {/* Bottom Section */}
      <div className="p-4 border-t border-zinc-200 dark:border-zinc-800 flex flex-col gap-2">
        <Button variant="ghost" className="w-full flex justify-start gap-2 text-zinc-600 dark:text-zinc-400">
          <Settings className="w-4 h-4" />
          Settings
        </Button>
        <div className="flex items-center gap-3 p-2 mt-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 cursor-pointer transition-colors">
          <Avatar className="w-8 h-8">
            <AvatarFallback className="bg-blue-100 text-blue-700"><User className="w-4 h-4" /></AvatarFallback>
          </Avatar>
          <div className="flex flex-col">
            <span className="text-sm font-medium">Default User</span>
            <span className="text-xs text-zinc-500">Free Plan</span>
          </div>
        </div>
      </div>
    </aside>
  );
};
