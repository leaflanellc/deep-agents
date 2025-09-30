# Supabase Agent Guide

The Supabase Agent is a powerful knowledge management system that combines web research, file uploads, and semantic search capabilities using Supabase's pgvector extension for PostgreSQL.

## 🚀 Features

### Core Capabilities
- **Web Research**: Search the web and automatically create knowledge bases
- **File Upload**: Process and store various file types (JSON, CSV, Markdown, etc.)
- **Semantic Search**: Find information using vector similarity with OpenAI embeddings
- **Database Management**: Create, organize, and manage PostgreSQL tables with vector support
- **SQL Migrations**: Apply schema changes with proper migration tracking

### Supported File Types
- **JSON**: Structured data with metadata
- **CSV**: Tabular data with headers
- **Markdown**: Text documents with sections
- **Plain Text**: General text files
- **HTML**: Web content (basic parsing)

## 🛠 Setup

### Prerequisites
1. Supabase project (created via MCP)
2. OpenAI API key for embedding generation
3. Valid environment variables configured

### Environment Variables
Add these to your `.env` file:
```bash
SUPABASE_PROJECT_ID=your-project-id
OPENAI_API_KEY=your-openai-api-key
```

### Installation
The Supabase agent is included in the Deep Agents package. Make sure you have the required dependencies:

```bash
pip install openai>=1.0.0
```

## 📖 Usage

### 1. Creating a New Knowledge Base Collection

**Create a table for storing documents:**
```
Create a collection called "ai_research" with fields for title, content, topic, source, difficulty, and tags
```

The agent will:
1. Generate the SQL migration with pgvector support
2. Create HNSW index for fast vector search
3. Create a match function for semantic queries
4. Apply the migration using `mcp_supabase_apply_migration`

**Example SQL generated:**
```sql
CREATE TABLE IF NOT EXISTS ai_research (
    id BIGSERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    topic TEXT,
    source TEXT,
    difficulty TEXT,
    tags TEXT,
    embedding VECTOR(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ai_research_embedding_idx 
ON ai_research 
USING hnsw (embedding vector_cosine_ops);

CREATE OR REPLACE FUNCTION match_ai_research (
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.78,
    match_count INT DEFAULT 10
)
RETURNS SETOF ai_research
LANGUAGE sql
AS $$
    SELECT *
    FROM ai_research
    WHERE ai_research.embedding <=> query_embedding < 1 - match_threshold
    ORDER BY ai_research.embedding <=> query_embedding ASC
    LIMIT LEAST(match_count, 200);
$$;
```

### 2. Adding Documents

**Add documents with automatic embedding generation:**
```
Add these 3 documents to the ai_research collection:
1. Title: "Introduction to Neural Networks", Content: "Neural networks are..."
2. Title: "Deep Learning Basics", Content: "Deep learning is..."
3. Title: "Transformer Models", Content: "Transformers revolutionized..."
```

The agent will:
1. Generate OpenAI embeddings for each document (combining title + content)
2. Create INSERT SQL statements with vector data
3. Execute using `mcp_supabase_execute_sql`

### 3. Semantic Search

**Search for similar documents:**
```
Search for "machine learning fundamentals" in the ai_research collection
```

The agent will:
1. Generate an embedding for your query using OpenAI
2. Use the `match_ai_research` function to find similar documents
3. Return results sorted by similarity (cosine distance)

**Example search results:**
```json
[
  {
    "id": 1,
    "title": "Introduction to Neural Networks",
    "content": "Neural networks are...",
    "similarity_score": 0.89
  },
  {
    "id": 2,
    "title": "Deep Learning Basics",
    "content": "Deep learning is...",
    "similarity_score": 0.85
  }
]
```

### 4. Web Research & Knowledge Base Creation

**Research a topic and create a collection:**
```
Research "quantum computing breakthroughs 2024" and create a knowledge base
```

The agent will:
1. Use the web-research sub-agent to search and extract information
2. Structure the data with metadata
3. Create a new table with pgvector support
4. Generate embeddings and insert the documents
5. Provide a summary of the created knowledge base

### 5. File Upload & Processing

**Upload and process a JSON file:**
```
I've uploaded a JSON file called "ml_concepts.json" with machine learning concepts.
Please process it and add it to a collection called "ml_knowledge"
```

The agent will:
1. Parse the JSON file
2. Extract and structure the data
3. Create a table if it doesn't exist
4. Generate embeddings and insert the documents

### 6. Database Management

**List all tables:**
```
Show me all the knowledge base collections
```

**Get table schema:**
```
Show me the schema for the ai_research table
```

**Check for issues:**
```
Run security and performance advisors on my database
```

## 🔍 How It Works

### Vector Embeddings
- Uses OpenAI's `text-embedding-3-small` model
- Generates 1536-dimensional vectors
- Combines title and content for comprehensive embeddings
- Stored in PostgreSQL using the `vector` data type

### Similarity Search
- Uses pgvector's HNSW (Hierarchical Navigable Small World) index
- Cosine distance metric (`<=>` operator)
- Returns results ranked by similarity
- Configurable match threshold (default: 0.78)

### Database Schema
Every knowledge base table includes:
- `id`: Auto-incrementing primary key
- `title`: Document title (TEXT)
- `content`: Document content (TEXT)
- Custom fields: topic, source, difficulty, tags, etc.
- `embedding`: Vector representation (VECTOR(1536))
- `created_at`: Timestamp (auto-generated)

### Search Function
Each table gets a custom `match_<table_name>` function:
```sql
SELECT * FROM match_ai_research(
    '<query_embedding>'::vector,
    0.78,  -- match threshold
    10     -- max results
);
```

## 🎯 Best Practices

### Schema Design
- Use snake_case for table names
- Include title and content fields for best search results
- Add metadata fields for filtering (topic, difficulty, tags)
- Always use `mcp_supabase_apply_migration` for DDL operations

### Data Management
- Combine title and content for rich embeddings
- Keep content focused and relevant
- Use appropriate match thresholds (0.7-0.85 typical range)
- Limit search results to reasonable numbers (5-20)

### Performance
- HNSW indexes provide fast approximate nearest neighbor search
- Adjust index parameters based on dataset size
- Use the generated match functions for optimized queries
- Consider batch operations for large datasets

### Security
- Run advisors after schema changes
- Use RLS (Row Level Security) for multi-tenant applications
- Keep API keys secure in environment variables
- Use migrations for audit trails

## 📊 Examples

### Example 1: Create US States Knowledge Base
```
Create a collection called "us_states" and add information about 10 US states including their capitals, regions, and key features
```

### Example 2: Search for Similar Content
```
Search the us_states collection for "states with beaches and warm weather"
```

Expected results: California, Florida, Hawaii (ranked by similarity)

### Example 3: Research and Build Knowledge Base
```
Research "renewable energy technologies" and create a comprehensive knowledge base with at least 15 articles
```

## 🔧 Troubleshooting

### Common Issues

**"OPENAI_API_KEY not set"**
- Add your OpenAI API key to `.env` file
- Restart your application

**"SUPABASE_PROJECT_ID not set"**
- Get your project ID from the Supabase dashboard
- Add to `.env` file

**"pgvector extension not found"**
- The extension should be auto-enabled
- Use MCP tools to check extension status

**Low search quality**
- Adjust match_threshold (lower = more permissive)
- Ensure title and content are descriptive
- Check that embeddings were generated correctly

**Slow searches**
- Verify HNSW index is created
- Check table size (large tables may need index tuning)
- Limit result count appropriately

## 🚀 Advanced Usage

### Custom Embeddings Model
To use a different embedding model, modify `add_documents_to_supabase` to use your preferred model and adjust the vector dimensions accordingly.

### Hybrid Search
Combine vector search with PostgreSQL full-text search:
```sql
SELECT * FROM ai_research
WHERE 
    ai_research.embedding <=> query_embedding < 0.3
    AND to_tsvector('english', title || ' ' || content) @@ plainto_tsquery('quantum')
ORDER BY ai_research.embedding <=> query_embedding
LIMIT 10;
```

### Filtering by Metadata
Combine semantic search with traditional filters:
```sql
SELECT * FROM match_ai_research(query_embedding, 0.78, 50)
WHERE difficulty = 'Beginner'
AND topic = 'Machine Learning'
LIMIT 10;
```

## 📚 Resources

- [Supabase pgvector Documentation](https://supabase.com/docs/guides/ai/vector-columns)
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [HNSW Algorithm](https://arxiv.org/abs/1603.09320)

## 🆘 Support

For issues or questions:
- Check the [Supabase Documentation](https://supabase.com/docs)
- Review the [Deep Agents GitHub](https://github.com/yourrepo/deepagent)
- Open an issue on GitHub

## 🎉 Next Steps

1. Try the examples above
2. Create your own knowledge bases
3. Experiment with different match thresholds
4. Build custom workflows with sub-agents
5. Integrate with your applications

