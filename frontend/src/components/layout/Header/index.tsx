import React from "react";
import { Menu, Share, MoreHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useChatStore } from "@/store/useChatStore";

export const Header = () => {
  const { currentConversation } = useChatStore();

  return (
    <header className="h-14 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between px-4 bg-white dark:bg-zinc-950">
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon" className="md:hidden">
          <Menu className="w-5 h-5" />
        </Button>
        <h1 className="font-medium text-zinc-800 dark:text-zinc-200 truncate max-w-[200px] md:max-w-md">
          {currentConversation?.title || "New Conversation"}
        </h1>
      </div>
      
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="sm" className="hidden md:flex gap-2">
          <Share className="w-4 h-4" />
          Share
        </Button>
        <Button variant="ghost" size="icon">
          <MoreHorizontal className="w-5 h-5" />
        </Button>
      </div>
    </header>
  );
};
