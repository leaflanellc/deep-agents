"use client";

import React, { useState, useCallback, useEffect } from "react";
import { useQueryState } from "nuqs";
import { ChatInterface } from "./components/ChatInterface/ChatInterface";
import { TasksFilesSidebar } from "./components/TasksFilesSidebar/TasksFilesSidebar";
import { SubAgentPanel } from "./components/SubAgentPanel/SubAgentPanel";
import { FileViewDialog } from "./components/FileViewDialog/FileViewDialog";
import { AgentSwitcher } from "./components/AgentSwitcher/AgentSwitcher";
import { ThreadHistorySidebar } from "./components/ThreadHistorySidebar/ThreadHistorySidebar";
import { createClient } from "@/lib/client";
import { useAuthContext } from "@/providers/Auth";
import type { SubAgent, FileItem, TodoItem } from "./types/types";
import styles from "./page.module.scss";

export default function HomePage() {
  const { session } = useAuthContext();
  const [threadId, setThreadId] = useQueryState("threadId");
  const [currentAgent, setCurrentAgent] = useState<string>("n8n_agent");
  const [selectedSubAgent, setSelectedSubAgent] = useState<SubAgent | null>(
    null,
  );
  const [selectedFile, setSelectedFile] = useState<FileItem | null>(null);
  const [todos, setTodos] = useState<TodoItem[]>([]);
  const [files, setFiles] = useState<Record<string, string>>({});
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isLoadingThreadState, setIsLoadingThreadState] = useState(false);
  const [isThreadHistoryOpen, setIsThreadHistoryOpen] = useState(false);

  // Store thread IDs per agent
  const [agentThreadIds, setAgentThreadIds] = useState<Record<string, string | null>>({
    research_agent: null,
    simple_agent: null,
    coding_agent: null,
    weaviate_agent: null,
    n8n_agent: null,
  });

  // Initialize agent thread IDs from URL parameter on first load
  useEffect(() => {
    if (threadId && !agentThreadIds[currentAgent]) {
      setAgentThreadIds(prev => ({
        ...prev,
        [currentAgent]: threadId
      }));
    }
  }, [threadId, currentAgent, agentThreadIds]);

  const toggleSidebar = useCallback(() => {
    setSidebarCollapsed((prev) => !prev);
  }, []);

  // Get the current thread ID for the selected agent
  const currentThreadId = agentThreadIds[currentAgent];

  // When the threadId or agent changes, grab the thread state from the graph server
  useEffect(() => {
    const fetchThreadState = async () => {
      if (!currentThreadId || !session?.accessToken) {
        setTodos([]);
        setFiles({});
        setIsLoadingThreadState(false);
        return;
      }
      setIsLoadingThreadState(true);
      try {
        const client = createClient(session.accessToken, currentAgent);
        const state = await client.threads.getState(currentThreadId);

        if (state.values) {
          const currentState = state.values as {
            todos?: TodoItem[];
            files?: Record<string, string>;
          };
          setTodos(currentState.todos || []);
          setFiles(currentState.files || {});
        }
      } catch (error) {
        console.error("Failed to fetch thread state:", error);
        setTodos([]);
        setFiles({});
      } finally {
        setIsLoadingThreadState(false);
      }
    };
    fetchThreadState();
  }, [currentThreadId, session?.accessToken, currentAgent]);

  const handleNewThread = useCallback(() => {
    // Clear thread for current agent
    setAgentThreadIds(prev => ({
      ...prev,
      [currentAgent]: null
    }));
    setThreadId(null);
    setSelectedSubAgent(null);
    setTodos([]);
    setFiles({});
  }, [setThreadId, currentAgent]);

  const handleAgentChange = useCallback((agentId: string) => {
    setCurrentAgent(agentId);
    // Don't reset thread - just switch to agent's thread
    setSelectedSubAgent(null);
    // Clear current state, it will be loaded from the agent's thread
    setTodos([]);
    setFiles({});
  }, []);

  const toggleThreadHistory = useCallback(() => {
    setIsThreadHistoryOpen((prev) => !prev);
  }, []);

  return (
    <div className={styles.container}>
      <TasksFilesSidebar
        todos={todos}
        files={files}
        onFileClick={setSelectedFile}
        collapsed={sidebarCollapsed}
        onToggleCollapse={toggleSidebar}
      />
      <div className={styles.mainContent}>
        <div className={styles.header}>
          <div className={styles.headerLeft}>
            <AgentSwitcher
              currentAgent={currentAgent}
              onAgentChange={handleAgentChange}
              className={styles.agentSwitcher}
            />
          </div>
          <div className={styles.headerRight}>
            <button
              className={styles.headerButton}
              onClick={handleNewThread}
              disabled={!currentThreadId}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z"></path>
              </svg>
            </button>
            <button
              className={styles.headerButton}
              onClick={toggleThreadHistory}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
                <path d="M12 7v5l4 2"></path>
              </svg>
            </button>
          </div>
        </div>
        <div className={styles.chatContainer}>
          <ThreadHistorySidebar
            open={isThreadHistoryOpen}
            setOpen={setIsThreadHistoryOpen}
            currentThreadId={currentThreadId}
            currentAgentId={currentAgent}
            onThreadSelect={(threadId) => {
              setAgentThreadIds(prev => ({
                ...prev,
                [currentAgent]: threadId
              }));
              setThreadId(threadId);
              setIsThreadHistoryOpen(false);
            }}
          />
          <ChatInterface
            threadId={currentThreadId}
            selectedSubAgent={selectedSubAgent}
            setThreadId={(newThreadId) => {
              // Update the agent-specific thread ID
              setAgentThreadIds(prev => ({
                ...prev,
                [currentAgent]: newThreadId
              }));
              setThreadId(newThreadId);
            }}
            onSelectSubAgent={setSelectedSubAgent}
            onTodosUpdate={setTodos}
            onFilesUpdate={setFiles}
            onNewThread={handleNewThread}
            isLoadingThreadState={isLoadingThreadState}
            currentAgentId={currentAgent}
          />
        </div>
        {selectedSubAgent && (
          <SubAgentPanel
            subAgent={selectedSubAgent}
            onClose={() => setSelectedSubAgent(null)}
          />
        )}
      </div>
      {selectedFile && (
        <FileViewDialog
          file={selectedFile}
          onClose={() => setSelectedFile(null)}
        />
      )}
    </div>
  );
}
