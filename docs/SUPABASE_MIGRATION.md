# Migration from Weaviate to Supabase

This document describes the transition from Weaviate to Supabase for vector-based knowledge management in Deep Agents.

## Overview

The Deep Agent project now supports **Supabase** as the primary vector database solution, offering:

- ✅ **PostgreSQL + pgvector**: Industry-standard database with vector extensions
- ✅ **OpenAI Embeddings**: High-quality text-embedding-3-small model (1536 dimensions)
- ✅ **HNSW Indexes**: Fast approximate nearest neighbor search
- ✅ **SQL Migrations**: Proper schema versioning and audit trails
- ✅ **MCP Integration**: Direct database operations via Supabase MCP tools
- ✅ **Cost Effective**: $10/month for production-grade database

## What Changed

### New Files Created

1. **`src/tools/supabase_tools.py`**
   - `create_supabase_collection`: Creates tables with pgvector support
   - `add_documents_to_supabase`: Adds documents with automatic embedding generation
   - `search_similar_supabase_documents`: Vector similarity search
   - `list_supabase_collections`: Lists all tables
   - `get_supabase_collection_info`: Gets table schema
   - `check_supabase_connection`: Checks connection status

2. **`src/agents/supabase_agent.py`**
   - Complete agent implementation with web research and data processing sub-agents
   - Integrated with Supabase MCP tools for direct database operations
   - Supports semantic search, file uploads, and knowledge base management

3. **`docs/SUPABASE_AGENT_GUIDE.md`**
   - Comprehensive guide with examples and best practices
   - Troubleshooting section
   - Advanced usage patterns

4. **`examples/supabase_agent_example.py`**
   - Working example with US States knowledge base
   - Demonstrates creation, insertion, and semantic search

### Existing Files Updated

1. **`src/tools/__init__.py`**
   - Added Supabase tools exports

2. **`src/agents/__init__.py`**
   - Added `supabase_agent` export

### Files Preserved

The following Weaviate files remain unchanged for backward compatibility:
- `src/tools/weaviate_tools.py`
- `src/agents/weaviate_agent.py`
- `docs/WEAVIATE_AGENT_GUIDE.md`
- `examples/weaviate_agent_example.py`

## New Supabase Project

A new Supabase project has been created for this Deep Agent:

- **Project Name**: deep-agent-kb
- **Project ID**: `hwssdopejehykwvaezwv`
- **Region**: us-east-1
- **Status**: ACTIVE_HEALTHY
- **Database**: PostgreSQL 17.6.1.011
- **Cost**: $10/month

## Setup Instructions

### 1. Environment Variables

Add these to your `.env` file:

```bash
# Supabase Configuration
SUPABASE_PROJECT_ID=hwssdopejehykwvaezwv

# OpenAI Configuration (for embeddings)
OPENAI_API_KEY=your-openai-api-key-here
```

### 2. Install Dependencies

```bash
pip install openai>=1.0.0
```

### 3. Enable pgvector Extension

The `pgvector` extension should be auto-enabled in your Supabase project. To verify:

```python
from agents.supabase_agent import agent

result = agent.invoke({
    "messages": [("user", "Check the Supabase connection and verify pgvector is enabled")]
})
```

### 4. Run the Example

```bash
python examples/supabase_agent_example.py
```

## Key Differences: Weaviate vs Supabase

| Feature | Weaviate | Supabase |
|---------|----------|----------|
| Database | Weaviate Cloud | PostgreSQL + pgvector |
| Embeddings | Snowflake/arctic-embed or Hugging Face | OpenAI text-embedding-3-small |
| Dimensions | 1024 (Snowflake) | 1536 (OpenAI) |
| Vector Index | HNSW (built-in) | HNSW (pgvector extension) |
| Schema Changes | API calls | SQL migrations |
| Cost | Variable (cloud) | $10/month |
| Querying | Weaviate Query Language | SQL with vector operators |
| MCP Integration | No | Yes ✅ |

## Migration Path

If you have existing Weaviate collections, here's how to migrate:

### Option 1: Export and Re-import

1. Export data from Weaviate:
```python
from tools.weaviate_tools import search_similar_documents, list_weaviate_collections

# List collections
collections = list_weaviate_collections()

# Export each collection (you'll need to implement full export)
```

2. Transform data format:
```python
# Weaviate format
{
    "title": "...",
    "content": "...",
    "properties": {...}
}

# Supabase format (same!)
{
    "title": "...",
    "content": "...",
    "other_fields": {...}
}
```

3. Import to Supabase:
```python
from agents.supabase_agent import agent

agent.invoke({
    "messages": [("user", f"Create a collection and add these documents: {documents}")]
})
```

### Option 2: Dual Operation

Run both systems in parallel during transition:
- Keep Weaviate agent for existing collections
- Use Supabase agent for new collections
- Gradually migrate as needed

## Usage Examples

### Create a Knowledge Base

```python
from agents.supabase_agent import agent

result = agent.invoke({
    "messages": [
        ("user", """Create a collection called 'tech_articles' and add these documents:
        
        1. Title: "Introduction to AI", Content: "Artificial intelligence is..."
        2. Title: "Machine Learning Basics", Content: "Machine learning involves..."
        3. Title: "Deep Learning Overview", Content: "Deep learning uses neural networks..."
        """)
    ]
})
```

### Semantic Search

```python
result = agent.invoke({
    "messages": [
        ("user", "Search tech_articles for 'neural networks and AI' - return top 3")
    ]
})
```

### Web Research

```python
result = agent.invoke({
    "messages": [
        ("user", "Research 'quantum computing breakthroughs 2024' and create a knowledge base")
    ]
})
```

## Architecture

### Supabase Agent Architecture

```
┌─────────────────────────────────────┐
│      Supabase Agent                 │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Web Research Sub-Agent      │  │
│  │  - Internet search           │  │
│  │  - Data extraction           │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Data Processing Sub-Agent   │  │
│  │  - File parsing              │  │
│  │  - Data structuring          │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Supabase Tools              │  │
│  │  - create_collection         │  │
│  │  - add_documents             │  │
│  │  - search_similar            │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│      Supabase MCP Tools             │
│  - apply_migration                  │
│  - execute_sql                      │
│  - list_tables                      │
│  - get_advisors                     │
└─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│   Supabase Database                 │
│   (PostgreSQL + pgvector)           │
│                                     │
│   Tables with:                      │
│   - id (bigserial)                  │
│   - title, content (text)           │
│   - embedding (vector(1536))        │
│   - metadata fields                 │
│   - created_at (timestamp)          │
│                                     │
│   Indexes:                          │
│   - HNSW on embedding column        │
│                                     │
│   Functions:                        │
│   - match_<table_name>()            │
└─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│   OpenAI Embeddings API             │
│   - text-embedding-3-small          │
│   - 1536 dimensions                 │
└─────────────────────────────────────┘
```

## Best Practices

### 1. Schema Design
- Use `mcp_supabase_apply_migration` for all DDL operations (CREATE, ALTER, DROP)
- Use `mcp_supabase_execute_sql` for all DML operations (INSERT, UPDATE, DELETE, SELECT)
- Always include `title` and `content` fields for best search results
- Add metadata fields for filtering (topic, source, difficulty, tags)

### 2. Performance
- HNSW indexes provide O(log n) search time
- Limit search results to 10-20 for best performance
- Use match thresholds between 0.7-0.85 for quality results
- Batch insertions when adding many documents

### 3. Security
- Run `mcp_supabase_get_advisors` after schema changes
- Implement Row Level Security (RLS) for multi-tenant apps
- Keep API keys in environment variables
- Use migrations for audit trails

### 4. Cost Management
- OpenAI embeddings cost: ~$0.00002/1K tokens
- For 1000 documents averaging 500 tokens each: ~$0.01
- Supabase: $10/month for unlimited queries
- Very cost-effective for most use cases

## Troubleshooting

### Common Issues

**"SUPABASE_PROJECT_ID not set"**
```bash
export SUPABASE_PROJECT_ID=hwssdopejehykwvaezwv
```

**"OPENAI_API_KEY not set"**
```bash
export OPENAI_API_KEY=sk-...
```

**"pgvector extension not found"**
```python
# Check if extension is enabled
from agents.supabase_agent import agent

agent.invoke({
    "messages": [("user", "List all enabled extensions in the database")]
})
```

**Slow searches**
```sql
-- Check if HNSW index exists
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'your_table_name';
```

## Next Steps

1. ✅ Set up environment variables
2. ✅ Run the example script
3. ✅ Create your first knowledge base
4. ✅ Experiment with semantic search
5. ✅ Integrate with your applications

## Resources

- [Supabase Agent Guide](./SUPABASE_AGENT_GUIDE.md)
- [Supabase pgvector Docs](https://supabase.com/docs/guides/ai/vector-columns)
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)
- [pgvector GitHub](https://github.com/pgvector/pgvector)

## Support

For questions or issues:
- Check the [Supabase Agent Guide](./SUPABASE_AGENT_GUIDE.md)
- Review the [example script](../examples/supabase_agent_example.py)
- Open an issue on GitHub

