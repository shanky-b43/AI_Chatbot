import React from "react";
import { Bot } from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

export const TypingIndicator = () => {
  return (
    <div className="flex gap-4 w-full py-4">
      <Avatar className="w-8 h-8 shrink-0 bg-blue-600">
        <AvatarFallback className="text-white">
          <Bot className="w-5 h-5" />
        </AvatarFallback>
      </Avatar>
      
      <div className="flex flex-col gap-1 items-start">
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold">AI Assistant</span>
        </div>
        
        <div className="px-4 py-4 rounded-2xl bg-transparent flex gap-1 items-center">
          <div className="w-2 h-2 rounded-full bg-zinc-400 animate-bounce" style={{ animationDelay: "0ms" }} />
          <div className="w-2 h-2 rounded-full bg-zinc-400 animate-bounce" style={{ animationDelay: "150ms" }} />
          <div className="w-2 h-2 rounded-full bg-zinc-400 animate-bounce" style={{ animationDelay: "300ms" }} />
        </div>
      </div>
    </div>
  );
};
