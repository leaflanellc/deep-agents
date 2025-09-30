# Project Reorganization Plan

## Goal
Reorganize the project structure to separate agents and tools into their own folders for better reusability and maintainability.

## Current Structure Analysis
- **Tools**: Currently in `src/deepagents/tools.py` (filesystem operations)
- **Agents**: Scattered across root directory and examples
  - `coding_agent.py` - Coding assistant agent
  - `examples/research/research_agent.py` - Research agent with custom tools
  - `simple_example.py` - Simple example with basic tools

## Final Structure (Fully Organized)
```
├── docs/                    # All documentation
│   ├── README.md
│   ├── LANGGRAPH_UI_GUIDE.md
│   ├── MULTIPLE_AGENTS_GUIDE.md
│   ├── PROJECT_PLAN.md
│   ├── QUICK_REFERENCE.md
│   ├── REORGANIZATION_PLAN.md
│   └── STARTUP_GUIDE.md
├── server/                  # LangGraph server files
│   ├── langgraph.json
│   ├── simple_agent_server.py
│   ├── start_all.sh
│   ├── stop_all.sh
│   ├── switch_agent.sh
│   └── open_uis.sh
├── src/
│   ├── deepagents/          # Core framework
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── middleware.py
│   │   ├── model.py
│   │   ├── prompts.py
│   │   ├── state.py
│   │   ├── types.py
│   │   └── tools.py (legacy compatibility layer)
│   ├── agents/              # All agent implementations
│   │   ├── __init__.py
│   │   ├── coding_agent.py
│   │   ├── research_agent.py
│   │   └── simple_agent.py
│   └── tools/               # All tool implementations
│       ├── __init__.py
│       ├── filesystem_tools.py
│       ├── research_tools.py
│       ├── coding_tools.py
│       └── example_tools.py
├── ui/                      # React UI
├── examples/                # Example projects
└── tests/                   # Test files
```

## Migration Steps
1. ✅ Create new directory structure
2. ✅ Move and refactor tools into appropriate tool modules
3. ✅ Move and refactor agents into agents directory
4. ✅ Update imports across the codebase
5. ✅ Update examples to use new structure
6. ✅ Test that everything still works
7. ✅ Clean up redundant files outside src/
8. ✅ Update documentation to reflect new structure
9. ✅ Organize documentation into docs/ folder
10. ✅ Organize server files into server/ folder
11. ✅ Update all references to new file locations

## Benefits
- **Reusability**: Tools can be easily imported and used by multiple agents
- **Maintainability**: Clear separation of concerns
- **Scalability**: Easy to add new tools and agents
- **Organization**: Logical grouping of related functionality

## Summary
✅ **Reorganization Complete!**

The project has been successfully reorganized with the following improvements:

### New Structure
- **Agents**: All agents are now in `src/agents/` with proper imports
- **Tools**: All tools are organized in `src/tools/` by category  
- **Backward Compatibility**: Existing code continues to work through legacy imports
- **Corrected Structure**: Used existing `src/agents/` and `src/tools/` directories instead of creating duplicates

### Key Changes
1. **Tools Organization**:
   - `filesystem_tools.py` - File operations and todo management
   - `research_tools.py` - Web search and research capabilities
   - `coding_tools.py` - Code development and review tools
   - `example_tools.py` - Simple demonstration tools

2. **Agents Organization**:
   - `coding_agent.py` - Coding assistant with development tools
   - `research_agent.py` - Research agent with web search capabilities
   - `simple_agent.py` - Basic example agent

3. **Import Structure**:
   - All agents and tools can be imported from `deepagents`
   - Individual tools can be imported from `deepagents.tools`
   - Individual agents can be imported from `deepagents.agents`

### Usage Examples
```python
# Import agents
from deepagents import coding_agent, research_agent, simple_agent

# Import specific tools
from deepagents.tools import write_file, internet_search, write_code

# Import from specific modules
from deepagents.tools.filesystem_tools import read_file, edit_file
from deepagents.tools.research_tools import internet_search
```

All existing examples and scripts continue to work without modification!

### Cleanup Summary
**Removed Redundant Files:**
- `coding_agent.py` - Redundant wrapper, now use `src/agents/coding_agent.py`
- `simple_example.py` - Redundant wrapper, now use `src/agents/simple_agent.py`
- `examples/research/research_agent.py` - Redundant wrapper, now use `src/agents/research_agent.py`

**Updated Files:**
- `simple_agent_server.py` - Now imports from new structure instead of duplicating code
- Documentation files - Updated references to point to new locations

**Final Clean Structure:**
- All agents are in `src/agents/`
- All tools are in `src/tools/`
- All documentation is in `docs/`
- All server files are in `server/`
- No duplicate files outside `src/`
- Clean imports and references throughout
- Well-organized project structure
