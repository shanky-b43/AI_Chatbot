import React from "react";
import { MainLayout } from "./MainLayout";
import { ChatWindow } from "@/components/Chat/ChatWindow";

export const ChatPage = () => {
  return (
    <MainLayout>
      <ChatWindow />
    </MainLayout>
  );
};
