import React, { useState, useEffect } from "react";
import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { useChatStore } from "@/store/useChatStore";
import { useDebounce } from "@/hooks/useDebounce";

export const SearchBar = () => {
  const [localQuery, setLocalQuery] = useState("");
  const debouncedQuery = useDebounce(localQuery, 300);
  const { setSearchQuery } = useChatStore();

  useEffect(() => {
    setSearchQuery(debouncedQuery);
  }, [debouncedQuery, setSearchQuery]);

  return (
    <div className="relative px-4 pb-2">
      <Search className="absolute left-7 top-2.5 h-4 w-4 text-zinc-500" />
      <Input
        type="text"
        placeholder="Search conversations..."
        value={localQuery}
        onChange={(e) => setLocalQuery(e.target.value)}
        className="pl-9 bg-white dark:bg-zinc-950 border-zinc-200 dark:border-zinc-800 focus-visible:ring-1 focus-visible:ring-zinc-300 dark:focus-visible:ring-zinc-700 h-9"
      />
    </div>
  );
};
