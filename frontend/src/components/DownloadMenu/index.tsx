import React from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { FileText, FileDown, FileCode2 } from "lucide-react";
import { Conversation } from "@/types";
import { downloadApi } from "@/api/downloadApi";

interface Props {
  conversation: Conversation | null;
  onClose: () => void;
}

export const DownloadMenu = ({ conversation, onClose }: Props) => {
  const handleDownload = (format: "md" | "txt" | "pdf") => {
    if (conversation) {
      downloadApi.downloadConversation(conversation.id, format);
      onClose();
    }
  };

  return (
    <Dialog open={!!conversation} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Download Conversation</DialogTitle>
          <DialogDescription>
            Choose a format to export "{conversation?.title}".
          </DialogDescription>
        </DialogHeader>
        <div className="grid grid-cols-3 gap-4 py-4">
          <Button variant="outline" className="flex flex-col h-24 gap-2" onClick={() => handleDownload("md")}>
            <FileCode2 className="w-8 h-8" />
            Markdown
          </Button>
          <Button variant="outline" className="flex flex-col h-24 gap-2" onClick={() => handleDownload("txt")}>
            <FileText className="w-8 h-8" />
            Text File
          </Button>
          <Button variant="outline" className="flex flex-col h-24 gap-2" onClick={() => handleDownload("pdf")}>
            <FileDown className="w-8 h-8" />
            PDF
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};
