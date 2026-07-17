export interface Conversation {
  id: string;
  title: string;
  updated_at: string; // ISO string
}

export interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: string; // ISO string
  metadata?: any;
}

export interface ChatResponse {
  workflow: string;
  response: string;
  thread_id: string;
}
