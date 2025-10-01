# Weaviate Agent Guide

The Weaviate Agent is a powerful knowledge management system that combines web research, file uploads, and semantic search capabilities using Weaviate's vector database.

## 🚀 Features

### Core Capabilities
- **Web Research**: Search the web and automatically create knowledge bases
- **File Upload**: Process and store various file types (JSON, CSV, Markdown, etc.)
- **Semantic Search**: Find information using vector similarity
- **Hybrid Search**: Combine vector and keyword search for better results
- **Collection Management**: Create, organize, and manage knowledge collections

### Supported File Types
- **JSON**: Structured data with metadata
- **CSV**: Tabular data with headers
- **Markdown**: Text documents with sections
- **Plain Text**: General text files
- **HTML**: Web content (basic parsing)

## 🛠 Setup

### Prerequisites
1. Weaviate Cloud account
2. Valid Weaviate credentials in `.env` file

### Environment Variables
Add these to your `.env` file:
```bash
WEAVIATE_URL=https://your-cluster-url.weaviate.network
WEAVIATE_API_KEY=your-weaviate-api-key
```

### Installation
The Weaviate agent is automatically included when you install the Deep Agents package. Make sure you have the required dependencies:

```bash
pip install weaviate-client>=4.9.5
```

## 📖 Usage

### 1. Web Research & Knowledge Base Creation

**Research a topic and create a collection:**
```
Research "artificial intelligence trends 2024" and create a knowledge base collection
```

**Research multiple topics:**
```
Research renewable energy solutions and create a collection called "ClimateSolutions"
```

### 2. File Upload & Processing

**Upload JSON data:**
```
I've uploaded a JSON file called "data.json" with machine learning information. 
Please process it and add it to a collection called "MLKnowledge"
```

**Upload CSV data:**
```
Process this CSV data and add it to a collection:
title,content,topic,difficulty
Python Basics,Introduction to Python,Programming,Beginner
```

**Upload Markdown:**
```
Process this Markdown document and add it to a collection:
# Introduction to AI
This is a comprehensive guide...
```

### 3. Semantic Search

**Search across all collections:**
```
Search for information about "machine learning algorithms"
```

**Search in specific collection:**
```
Search for "blockchain technology" in the BlockchainKnowledge collection
```

**Hybrid search:**
```
Perform a hybrid search for "artificial intelligence" to find both exact matches and similar concepts
```

### 4. Collection Management

**List all collections:**
```
Show me all available collections and their basic information
```

**Get collection details:**
```
Show me detailed information about the TechTopics collection
```

## 🔧 Available Tools

### Weaviate Tools
- `create_weaviate_collection`: Create new collections with vectorization
- `add_documents_to_weaviate`: Add documents to collections
- `search_similar_documents`: Vector similarity search
- `hybrid_search_documents`: Combined vector + keyword search
- `get_weaviate_collection_info`: Get collection details
- `list_weaviate_collections`: List all collections
- `check_weaviate_connection`: Verify Weaviate connection

### Upload Tools
- `process_uploaded_file`: Process uploaded files (JSON, CSV, Markdown, etc.)
- `extract_text_content`: Extract text from various file formats
- `parse_structured_data`: Parse structured data for Weaviate
- `create_upload_collection`: Create collections for uploaded data

### Research Tools
- `internet_search`: Search the web for information

## 📊 Data Structure

All documents in Weaviate collections follow this standard structure:

```json
{
  "title": "Document title",
  "content": "Main content/description",
  "topic": "Category/topic",
  "source": "Source URL or file name",
  "difficulty": "Beginner/Intermediate/Advanced",
  "tags": ["tag1", "tag2", "tag3"]
}
```

## 🎯 Use Cases

### 1. Research Assistant
- Research topics and build comprehensive knowledge bases
- Organize information by categories and difficulty levels
- Search for specific information across all research

### 2. Document Management
- Upload and process various file types
- Create searchable knowledge bases from documents
- Organize documents by topics and tags

### 3. Knowledge Discovery
- Find similar concepts across different collections
- Discover connections between different topics
- Explore knowledge bases through semantic search

### 4. Content Organization
- Categorize content by topics and difficulty
- Tag content for easy discovery
- Maintain multiple specialized collections

## 🔍 Search Examples

### Semantic Search
```
Search for "neural networks" - finds documents about neural networks, deep learning, AI, etc.
```

### Hybrid Search
```
Search for "machine learning" - finds exact matches and similar concepts like AI, algorithms, data science
```

### Collection-Specific Search
```
Search for "blockchain" in "CryptoKnowledge" collection
```

## 🚨 Troubleshooting

### Common Issues

1. **Connection Error**
   - Check your Weaviate credentials in `.env`
   - Verify your Weaviate Cloud instance is running
   - Use `check_weaviate_connection` tool

2. **File Upload Issues**
   - Ensure file format is supported
   - Check file content structure
   - Verify file permissions

3. **Search Issues**
   - Check if collections exist
   - Verify collection names are correct
   - Try different search terms

### Debug Commands
```
Check Weaviate connection status
List all available collections
Show collection information for [collection_name]
```

## 📚 Examples

See the following example files:
- `examples/weaviate_agent_example.py` - Comprehensive usage examples
- `test_weaviate_agent.py` - Test script for all features
- `examples/weaviate_example.py` - Basic Weaviate integration

## 🔄 Workflows

### Research Workflow
1. Research topic using web search
2. Structure data with metadata
3. Create collection with appropriate properties
4. Add structured data to collection
5. Verify collection and data

### Upload Workflow
1. Process uploaded file
2. Extract and structure data
3. Create or use existing collection
4. Add processed data to collection
5. Confirm successful upload

### Search Workflow
1. Choose search type (semantic/hybrid)
2. Specify search terms
3. Select target collections
4. Review and analyze results
5. Refine search if needed

## 🎉 Getting Started

1. **Set up environment**: Add Weaviate credentials to `.env`
2. **Start the agent**: Select "Weaviate Agent" in the UI
3. **Test connection**: Ask "Check Weaviate connection"
4. **Create first collection**: Research a topic you're interested in
5. **Upload data**: Try uploading a file with relevant information
6. **Search**: Explore your knowledge base with semantic search

The Weaviate Agent is now ready to help you build and manage comprehensive knowledge bases!

