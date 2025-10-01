"use client";

import React, {
  useState,
  useRef,
  useCallback,
  useMemo,
  useEffect,
  FormEvent,
} from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, LoaderCircle, Bot } from "lucide-react";
import { ChatMessage } from "../ChatMessage/ChatMessage";
import { PromptSelector } from "../PromptSelector/PromptSelector";
import type { SubAgent, TodoItem, ToolCall } from "../../types/types";
import { useChat } from "../../hooks/useChat";
import styles from "./ChatInterface.module.scss";
import { Message } from "@langchain/langgraph-sdk";
import { extractStringFromMessageContent } from "../../utils/utils";
import { PromptTemplate } from "../PromptManager/PromptManager";

interface ChatInterfaceProps {
  threadId: string | null;
  selectedSubAgent: SubAgent | null;
  setThreadId: (
    value: string | ((old: string | null) => string | null) | null,
  ) => void;
  onSelectSubAgent: (subAgent: SubAgent) => void;
  onTodosUpdate: (todos: TodoItem[]) => void;
  onFilesUpdate: (files: Record<string, string>) => void;
  onNewThread: () => void;
  isLoadingThreadState: boolean;
  currentAgentId?: string;
}

export const ChatInterface = React.memo<ChatInterfaceProps>(
  ({
    threadId,
    selectedSubAgent,
    setThreadId,
    onSelectSubAgent,
    onTodosUpdate,
    onFilesUpdate,
    onNewThread,
    isLoadingThreadState,
    currentAgentId,
  }) => {
    const [input, setInput] = useState("");
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const { messages, isLoading, sendMessage, stopStream } = useChat(
      threadId,
      setThreadId,
      onTodosUpdate,
      onFilesUpdate,
      currentAgentId,
    );

    useEffect(() => {
      // Only scroll to bottom if there are messages and we're not loading thread state
      if (messages.length > 0 && !isLoadingThreadState) {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
      }
    }, [messages.length, isLoadingThreadState]);

    const handleSubmit = useCallback(
      async (e: FormEvent) => {
        e.preventDefault();
        const messageText = input.trim();
        if (!messageText || isLoading) return;
        try {
          await sendMessage(messageText);
          setInput("");
        } catch (error) {
          console.error("Failed to send message:", error);
        }
      },
      [input, isLoading, sendMessage],
    );

    const handleSelectPrompt = useCallback(
      (prompt: PromptTemplate) => {
        setInput(prompt.content);
      },
      [],
    );


    const hasMessages = messages.length > 0;

    const processedMessages = useMemo(() => {
      /* 
    1. Loop through all messages
    2. For each AI message, add the AI message, and any tool calls to the messageMap
    3. For each tool message, find the corresponding tool call in the messageMap and update the status and output
    */
      const messageMap = new Map<string, any>();
      messages.forEach((message: Message) => {
        if (message.type === "ai") {
          const toolCallsInMessage: any[] = [];
          if (
            message.additional_kwargs?.tool_calls &&
            Array.isArray(message.additional_kwargs.tool_calls)
          ) {
            toolCallsInMessage.push(...message.additional_kwargs.tool_calls);
          } else if (message.tool_calls && Array.isArray(message.tool_calls)) {
            toolCallsInMessage.push(
              ...message.tool_calls.filter(
                (toolCall: any) => toolCall.name !== "",
              ),
            );
          } else if (Array.isArray(message.content)) {
            const toolUseBlocks = message.content.filter(
              (block: any) => block.type === "tool_use",
            );
            toolCallsInMessage.push(...toolUseBlocks);
          }
          const toolCallsWithStatus = toolCallsInMessage.map(
            (toolCall: any) => {
              const name =
                toolCall.function?.name ||
                toolCall.name ||
                toolCall.type ||
                "unknown";
              const args =
                toolCall.function?.arguments ||
                toolCall.args ||
                toolCall.input ||
                {};
              return {
                id: toolCall.id || `tool-${Math.random()}`,
                name,
                args,
                status: "pending" as const,
              } as ToolCall;
            },
          );
          messageMap.set(message.id!, {
            message,
            toolCalls: toolCallsWithStatus,
          });
        } else if (message.type === "tool") {
          const toolCallId = message.tool_call_id;
          if (!toolCallId) {
            return;
          }
          for (const [, data] of messageMap.entries()) {
            const toolCallIndex = data.toolCalls.findIndex(
              (tc: any) => tc.id === toolCallId,
            );
            if (toolCallIndex === -1) {
              continue;
            }
            data.toolCalls[toolCallIndex] = {
              ...data.toolCalls[toolCallIndex],
              status: "completed" as const,
              // TODO: Make this nicer
              result: extractStringFromMessageContent(message),
            };
            break;
          }
        } else if (message.type === "human") {
          messageMap.set(message.id!, {
            message,
            toolCalls: [],
          });
        }
      });
      const processedArray = Array.from(messageMap.values());
      return processedArray.map((data, index) => {
        const prevMessage =
          index > 0 ? processedArray[index - 1].message : null;
        return {
          ...data,
          showAvatar: data.message.type !== prevMessage?.type,
        };
      });
    }, [messages]);

    return (
      <div className={styles.container}>
        <div className={styles.content}>
          <div className={styles.messagesContainer}>
            {!hasMessages && !isLoading && !isLoadingThreadState && (
              <div className={styles.emptyState}>
                <Bot size={48} className={styles.emptyIcon} />
                <h2>Start a conversation or select a thread from history</h2>
              </div>
            )}
            {isLoadingThreadState && (
              <div className={styles.threadLoadingState}>
                <LoaderCircle className={styles.threadLoadingSpinner} />
              </div>
            )}
            <div className={styles.messagesList}>
              {processedMessages.map((data) => (
                <ChatMessage
                  key={data.message.id}
                  message={data.message}
                  toolCalls={data.toolCalls}
                  showAvatar={data.showAvatar}
                  onSelectSubAgent={onSelectSubAgent}
                  selectedSubAgent={selectedSubAgent}
                />
              ))}
              {isLoading && (
                <div className={styles.loadingMessage}>
                  <LoaderCircle className={styles.spinner} />
                  <span>Working...</span>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>
        </div>
        <form onSubmit={handleSubmit} className={styles.inputForm}>
          <div className={styles.inputContainer}>
            <PromptSelector
              onSelectPrompt={handleSelectPrompt}
              className={styles.promptSelector}
            />
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              disabled={isLoading}
              className={styles.input}
            />
          </div>
          {isLoading ? (
            <Button
              type="button"
              onClick={stopStream}
              className={styles.stopButton}
            >
              Stop
            </Button>
          ) : (
            <Button
              type="submit"
              disabled={!input.trim()}
              className={styles.sendButton}
            >
              <Send size={16} />
            </Button>
          )}
        </form>
      </div>
    );
  },
);

ChatInterface.displayName = "ChatInterface";
