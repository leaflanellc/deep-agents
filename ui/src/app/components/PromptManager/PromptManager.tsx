"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Plus, Search, Edit, Trash2, Copy, Tag } from "lucide-react";
import styles from "./PromptManager.module.scss";

export interface PromptTemplate {
    id: number;
    name: string;
    description: string;
    content: string;
    category: string;
    tags: string[];
    created_at: string;
    updated_at: string;
}

interface PromptManagerProps {
    onSelectPrompt?: (prompt: PromptTemplate) => void;
    className?: string;
}

export function PromptManager({ onSelectPrompt, className }: PromptManagerProps) {
    const [prompts, setPrompts] = useState<PromptTemplate[]>([]);
    const [filteredPrompts, setFilteredPrompts] = useState<PromptTemplate[]>([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [selectedCategory, setSelectedCategory] = useState<string>("all");
    const [categories, setCategories] = useState<string[]>([]);
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [editingPrompt, setEditingPrompt] = useState<PromptTemplate | null>(null);
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
                }
            ];

            setPrompts(mockPrompts);
            setCategories(["all", "research", "coding", "general"]);
        } catch (error) {
            console.error("Error loading prompts:", error);
        } finally {
            setIsLoading(false);
        }
    }, []);

    // Filter prompts based on search and category
    useEffect(() => {
        let filtered = prompts;

        if (searchQuery) {
            filtered = filtered.filter(prompt =>
                prompt.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                prompt.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                prompt.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
                prompt.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
            );
        }

        if (selectedCategory !== "all") {
            filtered = filtered.filter(prompt => prompt.category === selectedCategory);
        }

        setFilteredPrompts(filtered);
    }, [prompts, searchQuery, selectedCategory]);

    // Load prompts on component mount
    useEffect(() => {
        loadPrompts();
    }, [loadPrompts]);

    const handleSelectPrompt = (prompt: PromptTemplate) => {
        if (onSelectPrompt) {
            onSelectPrompt(prompt);
        }
    };

    const handleEditPrompt = (prompt: PromptTemplate) => {
        setEditingPrompt(prompt);
        setIsDialogOpen(true);
    };

    const handleDeletePrompt = async (promptId: number) => {
        if (window.confirm("Are you sure you want to delete this prompt?")) {
            try {
                // This would be replaced with actual API call
                setPrompts(prev => prev.filter(p => p.id !== promptId));
            } catch (error) {
                console.error("Error deleting prompt:", error);
            }
        }
    };

    const handleCopyPrompt = (prompt: PromptTemplate) => {
        navigator.clipboard.writeText(prompt.content);
        // You could add a toast notification here
    };

    return (
        <div className={`${styles.promptManager} ${className || ""}`}>
            <div className={styles.header}>
                <h2 className={styles.title}>Prompt Templates</h2>
                <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                    <DialogTrigger asChild>
                        <Button size="sm" className={styles.addButton}>
                            <Plus size={16} />
                            New Prompt
                        </Button>
                    </DialogTrigger>
                    <DialogContent className={styles.dialogContent}>
                        <DialogHeader>
                            <DialogTitle>
                                {editingPrompt ? "Edit Prompt" : "Create New Prompt"}
                            </DialogTitle>
                        </DialogHeader>
                        <PromptEditor
                            prompt={editingPrompt}
                            onSave={(prompt) => {
                                if (editingPrompt) {
                                    setPrompts(prev => prev.map(p => p.id === prompt.id ? prompt : p));
                                } else {
                                    setPrompts(prev => [...prev, { ...prompt, id: Date.now() }]);
                                }
                                setIsDialogOpen(false);
                                setEditingPrompt(null);
                            }}
                            onCancel={() => {
                                setIsDialogOpen(false);
                                setEditingPrompt(null);
                            }}
                        />
                    </DialogContent>
                </Dialog>
            </div>

            <div className={styles.filters}>
                <div className={styles.searchContainer}>
                    <Search size={16} className={styles.searchIcon} />
                    <Input
                        placeholder="Search prompts..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className={styles.searchInput}
                    />
                </div>

                <Tabs value={selectedCategory} onValueChange={setSelectedCategory}>
                    <TabsList className={styles.categoryTabs}>
                        {categories.map(category => (
                            <TabsTrigger key={category} value={category} className={styles.categoryTab}>
                                {category === "all" ? "All" : category.charAt(0).toUpperCase() + category.slice(1)}
                            </TabsTrigger>
                        ))}
                    </TabsList>
                </Tabs>
            </div>

            <ScrollArea className={styles.promptsList}>
                {isLoading ? (
                    <div className={styles.loading}>Loading prompts...</div>
                ) : filteredPrompts.length === 0 ? (
                    <div className={styles.empty}>
                        {searchQuery || selectedCategory !== "all"
                            ? "No prompts match your filters"
                            : "No prompts created yet"}
                    </div>
                ) : (
                    filteredPrompts.map(prompt => (
                        <div key={prompt.id} className={styles.promptItem}>
                            <div className={styles.promptHeader}>
                                <h3 className={styles.promptName}>{prompt.name}</h3>
                                <div className={styles.promptActions}>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() => handleSelectPrompt(prompt)}
                                        className={styles.actionButton}
                                    >
                                        <Copy size={14} />
                                    </Button>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() => handleEditPrompt(prompt)}
                                        className={styles.actionButton}
                                    >
                                        <Edit size={14} />
                                    </Button>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() => handleDeletePrompt(prompt.id)}
                                        className={styles.actionButton}
                                    >
                                        <Trash2 size={14} />
                                    </Button>
                                </div>
                            </div>

                            <p className={styles.promptDescription}>{prompt.description}</p>

                            <div className={styles.promptMeta}>
                                <span className={styles.promptCategory}>{prompt.category}</span>
                                <div className={styles.promptTags}>
                                    {prompt.tags.map(tag => (
                                        <span key={tag} className={styles.tag}>
                                            <Tag size={12} />
                                            {tag}
                                        </span>
                                    ))}
                                </div>
                            </div>

                            <div className={styles.promptContent}>
                                <pre className={styles.promptText}>{prompt.content}</pre>
                            </div>
                        </div>
                    ))
                )}
            </ScrollArea>
        </div>
    );
}

// Prompt Editor Component
interface PromptEditorProps {
    prompt?: PromptTemplate | null;
    onSave: (prompt: Omit<PromptTemplate, "id" | "created_at" | "updated_at">) => void;
    onCancel: () => void;
}

function PromptEditor({ prompt, onSave, onCancel }: PromptEditorProps) {
    const [name, setName] = useState(prompt?.name || "");
    const [description, setDescription] = useState(prompt?.description || "");
    const [content, setContent] = useState(prompt?.content || "");
    const [category, setCategory] = useState(prompt?.category || "general");
    const [tags, setTags] = useState(prompt?.tags.join(", ") || "");

    const handleSave = () => {
        if (!name.trim() || !content.trim()) {
            alert("Name and content are required");
            return;
        }

        onSave({
            name: name.trim(),
            description: description.trim(),
            content: content.trim(),
            category: category.trim(),
            tags: tags.split(",").map(tag => tag.trim()).filter(tag => tag)
        });
    };

    return (
        <div className={styles.promptEditor}>
            <div className={styles.editorField}>
                <label className={styles.fieldLabel}>Name *</label>
                <Input
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter prompt name"
                />
            </div>

            <div className={styles.editorField}>
                <label className={styles.fieldLabel}>Description</label>
                <Input
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Describe what this prompt is for"
                />
            </div>

            <div className={styles.editorField}>
                <label className={styles.fieldLabel}>Category</label>
                <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className={styles.categorySelect}
                >
                    <option value="general">General</option>
                    <option value="research">Research</option>
                    <option value="coding">Coding</option>
                    <option value="writing">Writing</option>
                    <option value="analysis">Analysis</option>
                </select>
            </div>

            <div className={styles.editorField}>
                <label className={styles.fieldLabel}>Tags</label>
                <Input
                    value={tags}
                    onChange={(e) => setTags(e.target.value)}
                    placeholder="Enter tags separated by commas"
                />
            </div>

            <div className={styles.editorField}>
                <label className={styles.fieldLabel}>Content *</label>
                <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="Enter the prompt content. Use {variable} for dynamic content."
                    className={styles.contentTextarea}
                    rows={10}
                />
            </div>

            <div className={styles.editorActions}>
                <Button variant="outline" onClick={onCancel}>
                    Cancel
                </Button>
                <Button onClick={handleSave}>
                    {prompt ? "Update" : "Create"} Prompt
                </Button>
            </div>
        </div>
    );
}
