import React, { useState } from "react";
import { ConversationCard } from "./ConversationCard";
import { useConversations } from "@/hooks/useConversations";
import { Conversation } from "@/types";
import { Skeleton } from "@/components/ui/skeleton";
import { RenameDialog } from "@/components/Dialogs/RenameDialog";
import { DeleteDialog } from "@/components/Dialogs/DeleteDialog";
import { DownloadMenu } from "@/components/DownloadMenu";

export const ConversationList = () => {
  const { conversations, isLoading, error } = useConversations();

  const [renameItem, setRenameItem] = useState<Conversation | null>(null);
  const [deleteItem, setDeleteItem] = useState<Conversation | null>(null);
  const [downloadItem, setDownloadItem] = useState<Conversation | null>(null);

  if (error) {
    return <div className="text-sm text-red-500 p-4">Failed to load conversations.</div>;
  }

  if (isLoading) {
    return (
      <div className="flex flex-col gap-2 p-2">
        <Skeleton className="h-10 w-full" />
        <Skeleton className="h-10 w-full" />
        <Skeleton className="h-10 w-full" />
      </div>
    );
  }

  if (!conversations || conversations.length === 0) {
    return <div className="text-sm text-zinc-500 p-4 text-center">No conversations found.</div>;
  }

  // Simple grouping (Ideally you'd use a real date library like date-fns)
  const grouped = {
    Today: conversations.slice(0, 3), // Mock grouping for now
    "Previous 7 Days": conversations.slice(3, 10),
  };

  return (
    <div className="flex flex-col gap-4 py-2">
      {Object.entries(grouped).map(([groupName, items]) => {
        if (items.length === 0) return null;
        return (
          <div key={groupName}>
            <h3 className="text-xs font-semibold text-zinc-400 dark:text-zinc-500 px-3 py-1 mb-1">{groupName}</h3>
            <div className="flex flex-col px-2">
              {items.map((conv) => (
                <ConversationCard 
                  key={conv.id} 
                  conversation={conv} 
                  onRename={setRenameItem}
                  onDelete={setDeleteItem}
                  onDownload={setDownloadItem}
                />
              ))}
            </div>
          </div>
        );
      })}

      <RenameDialog conversation={renameItem} onClose={() => setRenameItem(null)} />
      <DeleteDialog conversation={deleteItem} onClose={() => setDeleteItem(null)} />
      <DownloadMenu conversation={downloadItem} onClose={() => setDownloadItem(null)} />
    </div>
  );
};
