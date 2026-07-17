import React, { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Conversation } from "@/types";
import { useConversations } from "@/hooks/useConversations";

interface Props {
  conversation: Conversation | null;
  onClose: () => void;
}

export const RenameDialog = ({ conversation, onClose }: Props) => {
  const [title, setTitle] = useState("");
  const { renameConversation } = useConversations();

  useEffect(() => {
    if (conversation) {
      setTitle(conversation.title);
    }
  }, [conversation]);

  const handleRename = () => {
    if (conversation && title.trim()) {
      renameConversation({ id: conversation.id, title });
      onClose();
    }
  };

  return (
    <Dialog open={!!conversation} onOpenChange={(open) => !open && onClose()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Rename Conversation</DialogTitle>
        </DialogHeader>
        <Input 
          value={title} 
          onChange={(e) => setTitle(e.target.value)} 
          onKeyDown={(e) => e.key === "Enter" && handleRename()}
          autoFocus
        />
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleRename}>Save</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
