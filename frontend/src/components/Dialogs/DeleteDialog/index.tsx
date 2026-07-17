import React from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Conversation } from "@/types";
import { useConversations } from "@/hooks/useConversations";
import { useChatStore } from "@/store/useChatStore";

interface Props {
  conversation: Conversation | null;
  onClose: () => void;
}

export const DeleteDialog = ({ conversation, onClose }: Props) => {
  const { deleteConversation, conversations } = useConversations();
  const { currentConversation, setCurrentConversation } = useChatStore();

  const handleDelete = () => {
    if (conversation) {
      deleteConversation(conversation.id);
      
      // Auto-open newest if the deleted one was open
      if (currentConversation?.id === conversation.id) {
        const remaining = conversations?.filter(c => c.id !== conversation.id) || [];
        if (remaining.length > 0) {
          setCurrentConversation(remaining[0]);
        } else {
          setCurrentConversation(null);
        }
      }
      onClose();
    }
  };

  return (
    <Dialog open={!!conversation} onOpenChange={(open) => !open && onClose()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Delete Conversation</DialogTitle>
          <DialogDescription>
            Are you sure you want to delete "{conversation?.title}"? This action cannot be undone.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button variant="destructive" onClick={handleDelete}>Delete</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
