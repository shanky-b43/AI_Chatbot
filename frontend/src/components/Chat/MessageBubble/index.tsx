import React from "react";
import ReactMarkdown from "react-markdown";
import { User, Bot, Copy, Check } from "lucide-react";
import { Message } from "@/types";
import { cn } from "@/lib/utils";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";

interface Props {
  message: Message;
}

export const MessageBubble = ({ message }: Props) => {
  const [copied, setCopied] = React.useState(false);
  const isUser = message.role === "user";

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={cn("flex gap-4 w-full py-4 group", isUser ? "flex-row-reverse" : "")}>
      <Avatar className={cn("w-8 h-8 shrink-0", isUser ? "bg-zinc-200 dark:bg-zinc-800" : "bg-blue-600")}>
        <AvatarFallback className={cn(isUser ? "text-zinc-600 dark:text-zinc-400" : "text-white")}>
          {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
        </AvatarFallback>
      </Avatar>
      
      <div className={cn("flex flex-col gap-1 max-w-[80%]", isUser ? "items-end" : "items-start")}>
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold">{isUser ? "You" : "AI Assistant"}</span>
          <span className="text-xs text-zinc-400">
            {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
        
        <div className={cn(
          "px-4 py-3 rounded-2xl prose dark:prose-invert max-w-none text-sm break-words",
          isUser 
            ? "bg-zinc-100 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 rounded-tr-sm" 
            : "bg-transparent text-zinc-800 dark:text-zinc-200"
        )}>
          {isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : (
            <ReactMarkdown>{message.content}</ReactMarkdown>
          )}
        </div>

        {!isUser && (
          <div className="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-2 mt-1">
            <Button variant="ghost" size="icon" className="h-6 w-6" onClick={handleCopy}>
              {copied ? <Check className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4 text-zinc-400" />}
            </Button>
            {message.metadata?.workflow && (
              <span className="text-xs bg-zinc-100 dark:bg-zinc-800 text-zinc-500 px-2 py-0.5 rounded-full">
                {message.metadata.workflow}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
