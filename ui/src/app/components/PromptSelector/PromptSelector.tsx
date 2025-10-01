"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Search, Zap, ChevronDown } from "lucide-react";
import { PromptTemplate } from "../PromptManager/PromptManager";
import styles from "./PromptSelector.module.scss";

interface PromptSelectorProps {
    onSelectPrompt: (prompt: PromptTemplate) => void;
    className?: string;
}

export function PromptSelector({ onSelectPrompt, className }: PromptSelectorProps) {
    const [prompts, setPrompts] = useState<PromptTemplate[]>([]);
    const [filteredPrompts, setFilteredPrompts] = useState<PromptTemplate[]>([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [isOpen, setIsOpen] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    // Load prompts from the database
    const loadPrompts = useCallback(async () => {
        setIsLoading(true);
        try {
            // This would be replaced with actual API call
            // For now, we'll use mock data
            const mockPrompts: PromptTemplate[] = [
                {
                    id: 1,
                    name: "Research Report",
                    description: "Template for creating comprehensive research reports",
                    content: "You are a research analyst. Create a detailed report on {topic} covering:\n1. Overview\n2. Key findings\n3. Analysis\n4. Conclusions\n5. Recommendations",
                    category: "research",
                    tags: ["research", "report", "analysis"],
                    created_at: "2024-01-15T10:30:00Z",
                    updated_at: "2024-01-15T10:30:00Z"
                },
                {
                    id: 2,
                    name: "Code Review",
                    description: "Template for conducting thorough code reviews",
                    content: "Review the following code for {language}:\n\n{code}\n\nFocus on:\n- Code quality\n- Performance\n- Security\n- Best practices\n- Documentation",
                    category: "coding",
                    tags: ["code", "review", "quality"],
                    created_at: "2024-01-14T15:20:00Z",
                    updated_at: "2024-01-14T15:20:00Z"
                },
                {
                    id: 3,
                    name: "Meeting Summary",
                    description: "Template for summarizing meeting discussions",
                    content: "Summarize the meeting on {topic}:\n\nKey Points:\n- {point1}\n- {point2}\n- {point3}\n\nAction Items:\n- {action1}\n- {action2}\n\nNext Steps: {next_steps}",
                    category: "general",
                    tags: ["meeting", "summary", "notes"],
                    created_at: "2024-01-13T09:15:00Z",
                    updated_at: "2024-01-13T09:15:00Z"
                },
                {
                    id: 4,
                    name: "Data Analysis",
                    description: "Template for analyzing datasets and generating insights",
                    content: "Analyze the following dataset: {dataset}\n\nProvide:\n1. Data overview and summary statistics\n2. Key patterns and trends\n3. Outliers and anomalies\n4. Insights and recommendations\n5. Visualizations (if applicable)",
                    category: "analysis",
                    tags: ["data", "analysis", "insights"],
                    created_at: "2024-01-12T14:45:00Z",
                    updated_at: "2024-01-12T14:45:00Z"
                },
                {
                    id: 5,
                    name: "Creative Writing",
                    description: "Template for creative writing and storytelling",
                    content: "Write a creative piece about {theme} in the style of {style}.\n\nInclude:\n- Engaging opening\n- Character development\n- Plot progression\n- Descriptive language\n- Satisfying conclusion",
                    category: "writing",
                    tags: ["creative", "writing", "story"],
                    created_at: "2024-01-11T11:20:00Z",
                    updated_at: "2024-01-11T11:20:00Z"
                }
            ];

            setPrompts(mockPrompts);
        } catch (error) {
            console.error("Error loading prompts:", error);
        } finally {
            setIsLoading(false);
        }
    }, []);

    // Filter prompts based on search
    useEffect(() => {
        if (!searchQuery.trim()) {
            setFilteredPrompts(prompts);
        } else {
            const filtered = prompts.filter(prompt =>
                prompt.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                prompt.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                prompt.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
            );
            setFilteredPrompts(filtered);
        }
    }, [prompts, searchQuery]);

    // Load prompts on component mount
    useEffect(() => {
        loadPrompts();
    }, [loadPrompts]);

    const handleSelectPrompt = (prompt: PromptTemplate) => {
        onSelectPrompt(prompt);
        setIsOpen(false);
        setSearchQuery("");
    };

    return (
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
            <DialogTrigger asChild>
                <Button variant="outline" className={`${styles.triggerButton} ${className || ""}`}>
                    <Zap size={16} />
                    Use Prompt
                    <ChevronDown size={14} />
                </Button>
            </DialogTrigger>
            <DialogContent className={styles.dialogContent}>
                <DialogHeader>
                    <DialogTitle>Select a Prompt Template</DialogTitle>
                </DialogHeader>

                <div className={styles.searchContainer}>
                    <Search size={16} className={styles.searchIcon} />
                    <Input
                        placeholder="Search prompts..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className={styles.searchInput}
                    />
                </div>

                <ScrollArea className={styles.promptsList}>
                    {isLoading ? (
                        <div className={styles.loading}>Loading prompts...</div>
                    ) : filteredPrompts.length === 0 ? (
                        <div className={styles.empty}>
                            {searchQuery ? "No prompts match your search" : "No prompts available"}
                        </div>
                    ) : (
                        filteredPrompts.map(prompt => (
                            <div
                                key={prompt.id}
                                className={styles.promptItem}
                                onClick={() => handleSelectPrompt(prompt)}
                            >
                                <div className={styles.promptHeader}>
                                    <h3 className={styles.promptName}>{prompt.name}</h3>
                                    <span className={styles.promptCategory}>{prompt.category}</span>
                                </div>
                                <p className={styles.promptDescription}>{prompt.description}</p>
                                <div className={styles.promptTags}>
                                    {prompt.tags.slice(0, 3).map(tag => (
                                        <span key={tag} className={styles.tag}>
                                            {tag}
                                        </span>
                                    ))}
                                    {prompt.tags.length > 3 && (
                                        <span className={styles.moreTags}>+{prompt.tags.length - 3} more</span>
                                    )}
                                </div>
                            </div>
                        ))
                    )}
                </ScrollArea>
            </DialogContent>
        </Dialog>
    );
}
