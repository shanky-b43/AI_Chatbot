import React, { useState, useRef, useEffect } from "react";
import { Send, Loader2, Paperclip } from "lucide-react";
import { Button } from "@/components/ui/button";
import { UploadDocumentModal } from "@/components/Dialogs/UploadDocumentModal";

interface Props {
  onSend: (message: string) => void;
  disabled: boolean;
}

export const MessageInput = ({ onSend, disabled }: Props) => {
  const [text, setText] = useState("");
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [text]);

  const handleSend = () => {
    if (text.trim() && !disabled) {
      onSend(text.trim());
      setText("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      <div className="relative flex items-end w-full bg-white dark:bg-zinc-900 border border-zinc-300 dark:border-zinc-700 rounded-2xl overflow-hidden focus-within:ring-1 focus-within:ring-zinc-400 dark:focus-within:ring-zinc-500 transition-shadow">
        <div className="p-2">
          <Button
            size="icon"
            variant="ghost"
            onClick={() => setIsUploadModalOpen(true)}
            disabled={disabled}
            className="h-8 w-8 text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 rounded-xl"
            title="Upload Knowledge Document"
          >
            <Paperclip className="w-4 h-4" />
          </Button>
        </div>
        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          disabled={disabled}
          className="w-full max-h-[200px] bg-transparent resize-none outline-none py-3 px-2 text-zinc-900 dark:text-zinc-100 placeholder-zinc-500 disabled:opacity-50"
          rows={1}
        />
      <div className="p-2">
        <Button 
          size="icon" 
          onClick={handleSend} 
          disabled={!text.trim() || disabled}
          className="h-8 w-8 bg-zinc-900 hover:bg-zinc-800 dark:bg-white dark:hover:bg-zinc-200 dark:text-zinc-900 rounded-xl"
        >
          {disabled ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
        </Button>
      </div>
      </div>
      <UploadDocumentModal open={isUploadModalOpen} onOpenChange={setIsUploadModalOpen} />
    </>
  );
};
