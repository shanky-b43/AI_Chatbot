import React, { useState } from "react";
import { MessageSquare, MoreHorizontal, Pencil, Trash2, Download } from "lucide-react";
import { Conversation } from "@/types";
import { useChatStore } from "@/store/useChatStore";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface Props {
  conversation: Conversation;
  onRename: (conversation: Conversation) => void;
  onDelete: (conversation: Conversation) => void;
  onDownload: (conversation: Conversation) => void;
}

export const ConversationCard = ({ conversation, onRename, onDelete, onDownload }: Props) => {
  const { currentConversation, setCurrentConversation } = useChatStore();
  const isActive = currentConversation?.id === conversation.id;

  return (
    <div
      onClick={() => setCurrentConversation(conversation)}
      className={cn(
        "group relative flex items-center gap-3 p-2 my-1 rounded-lg cursor-pointer transition-colors text-sm",
        isActive 
          ? "bg-zinc-200 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100" 
          : "text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800/50"
      )}
    >
      <MessageSquare className="w-4 h-4 shrink-0" />
      <span className="truncate flex-1 font-medium">{conversation.title}</span>
      
      <div className={cn(
        "absolute right-2 flex items-center gap-1 bg-gradient-to-l from-zinc-200 via-zinc-200 to-transparent dark:from-zinc-800 dark:via-zinc-800 pl-4",
        isActive ? "opacity-100" : "opacity-0 group-hover:opacity-100 dark:from-zinc-800/50 dark:via-zinc-800/50"
      )}>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" className="h-6 w-6 text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100" onClick={(e) => e.stopPropagation()}>
              <MoreHorizontal className="w-4 h-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-40">
            <DropdownMenuItem onClick={(e) => { e.stopPropagation(); onRename(conversation); }}>
              <Pencil className="w-4 h-4 mr-2" /> Rename
            </DropdownMenuItem>
            <DropdownMenuItem onClick={(e) => { e.stopPropagation(); onDownload(conversation); }}>
              <Download className="w-4 h-4 mr-2" /> Download
            </DropdownMenuItem>
            <DropdownMenuItem className="text-red-600 focus:bg-red-50 focus:text-red-700 dark:focus:bg-red-950" onClick={(e) => { e.stopPropagation(); onDelete(conversation); }}>
              <Trash2 className="w-4 h-4 mr-2" /> Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  );
};
