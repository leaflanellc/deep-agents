"use client";

import React, { useState, useEffect } from "react";
import { ChevronDown } from "lucide-react";
import styles from "./AgentSwitcher.module.scss";

export interface Agent {
    id: string;
    name: string;
    description: string;
}

interface AgentSwitcherProps {
    currentAgent: string;
    onAgentChange: (agentId: string) => void;
    className?: string;
}

const AVAILABLE_AGENTS: Agent[] = [
    {
        id: "simple_agent",
        name: "Simple Agent",
        description: "Basic math and weather assistant"
    },
    {
        id: "research_agent",
        name: "Research Agent",
        description: "Advanced research with web search capabilities"
    },
    {
        id: "coding_agent",
        name: "Coding Agent",
        description: "Code assistance, debugging, and reviews"
    }
];

export function AgentSwitcher({
    currentAgent,
    onAgentChange,
    className
}: AgentSwitcherProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

    // Find the current agent details
    useEffect(() => {
        const agent = AVAILABLE_AGENTS.find(a => a.id === currentAgent);
        setSelectedAgent(agent || AVAILABLE_AGENTS[0]);
    }, [currentAgent]);

    const handleAgentSelect = (agent: Agent) => {
        setSelectedAgent(agent);
        onAgentChange(agent.id);
        setIsOpen(false);
    };

    const toggleDropdown = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div className={`${styles.container} ${className || ""}`}>
            <button
                className={styles.trigger}
                onClick={toggleDropdown}
                aria-expanded={isOpen}
                aria-haspopup="listbox"
            >
                <div className={styles.agentInfo}>
                    <span className={styles.agentName}>
                        {selectedAgent?.name || "Select Agent"}
                    </span>
                    <span className={styles.agentDescription}>
                        {selectedAgent?.description || ""}
                    </span>
                </div>
                <ChevronDown
                    className={`${styles.chevron} ${isOpen ? styles.chevronOpen : ""}`}
                />
            </button>

            {isOpen && (
                <div className={styles.dropdown}>
                    <div className={styles.dropdownContent}>
                        {AVAILABLE_AGENTS.map((agent) => (
                            <button
                                key={agent.id}
                                className={`${styles.agentOption} ${agent.id === currentAgent ? styles.agentOptionSelected : ""
                                    }`}
                                onClick={() => handleAgentSelect(agent)}
                                role="option"
                                aria-selected={agent.id === currentAgent}
                            >
                                <div className={styles.agentOptionInfo}>
                                    <span className={styles.agentOptionName}>
                                        {agent.name}
                                    </span>
                                    <span className={styles.agentOptionDescription}>
                                        {agent.description}
                                    </span>
                                </div>
                                {agent.id === currentAgent && (
                                    <div className={styles.checkmark}>✓</div>
                                )}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
