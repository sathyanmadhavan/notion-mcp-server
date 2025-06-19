#!/usr/bin/env python3

import os
import requests
from typing import Any, Sequence
from mcp.server.fastmcp import FastMCP
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

# Initialize Notion client
notion = Client(auth=os.environ.get("NOTION_API_KEY"))

# Additional constants for direct API calls
NOTION_API_URL = "https://api.notion.com/v1"
NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_VERSION = "2022-06-28"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}

# Create FastMCP server
mcp = FastMCP("notion-server", dependencies=[
    "requests",
    "notion-client",
    "python-dotenv"
])

@mcp.resource("notion://databases")
async def list_databases():
    """List all Notion databases"""
    try:
        databases = notion.search(filter={"property": "object", "value": "database"})
        
        result = []
        for db in databases.get("results", []):
            title = "Untitled"
            if db.get('title') and len(db['title']) > 0:
                title = db['title'][0].get('plain_text', 'Untitled')
            
            result.append({
                "id": db['id'],
                "title": title,
                "url": db.get('url', '')
            })
        
        return result
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("notion://database/{database_id}")
async def get_database(database_id: str):
    """Get a specific database and its pages"""
    try:
        # Get database info
        database = notion.databases.retrieve(database_id=database_id)
        
        # Get database entries
        pages = notion.databases.query(database_id=database_id)
        
        return {
            "database": database,
            "pages": pages["results"]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def search_notion(query: str, filter_type: str = None) -> str:
    """Search Notion pages and databases
    
    Args:
        query: Search query
        filter_type: Filter by object type ('page' or 'database')
    """
    try:
        search_filter = {}
        if filter_type:
            search_filter = {"property": "object", "value": filter_type}
        
        results = notion.search(query=query, filter=search_filter)
        
        output = f"Found {len(results['results'])} results:\n\n"
        
        for item in results["results"]:
            title = "Untitled"
            if item.get('title') and len(item['title']) > 0:
                title = item['title'][0].get('plain_text', 'Untitled')
            elif item.get('properties'):
                # For database entries, look for title property
                for prop_name, prop_data in item['properties'].items():
                    if prop_data.get('type') == 'title' and prop_data.get('title'):
                        if len(prop_data['title']) > 0:
                            title = prop_data['title'][0].get('plain_text', 'Untitled')
                        break
            
            url = item.get('url', 'No URL')
            output += f"- {title} ({url})\n"
        
        return output
        
    except Exception as e:
        return f"Error searching Notion: {str(e)}"

@mcp.tool()
async def get_page_content(page_id: str) -> str:
    """Get the content of a specific Notion page
    
    Args:
        page_id: The ID of the Notion page
    """
    try:
        # Get page info
        page = notion.pages.retrieve(page_id=page_id)
        
        # Get page blocks (content)
        blocks = notion.blocks.children.list(block_id=page_id)
        
        # Extract title from page properties
        title = "Untitled"
        if page.get('properties'):
            for prop_name, prop_data in page['properties'].items():
                if prop_data.get('type') == 'title' and prop_data.get('title'):
                    if len(prop_data['title']) > 0:
                        title = prop_data['title'][0].get('plain_text', 'Untitled')
                    break
        
        content = f"Page Title: {title}\n"
        content += f"URL: {page.get('url', 'No URL')}\n\n"
        content += "Content:\n"
        
        for block in blocks["results"]:
            block_type = block["type"]
            if block_type in block and "rich_text" in block[block_type]:
                text = "".join([t["plain_text"] for t in block[block_type]["rich_text"]])
                if text.strip():
                    content += f"- {text}\n"
        
        return content
        
    except Exception as e:
        return f"Error getting page content: {str(e)}"

@mcp.tool()
async def query_database(database_id: str, filter: dict = None, sorts: list = None) -> str:
    """Query a Notion database with filters
    
    Args:
        database_id: The ID of the Notion database
        filter: Filter conditions (optional)
        sorts: Sort conditions (optional)
    """
    try:
        query_params = {"database_id": database_id}
        if filter:
            query_params["filter"] = filter
        if sorts:
            query_params["sorts"] = sorts
            
        results = notion.databases.query(**query_params)
        
        content = f"Database query returned {len(results['results'])} results:\n\n"
        
        for page in results["results"]:
            title = "Untitled"
            # Look for title property
            for prop_name, prop_data in page["properties"].items():
                if prop_data["type"] == "title" and prop_data.get("title"):
                    if len(prop_data["title"]) > 0:
                        title = prop_data["title"][0]["plain_text"]
                    break
                
            content += f"- {title} ({page['url']})\n"
        
        return content
        
    except Exception as e:
        return f"Error querying database: {str(e)}"

@mcp.tool()
async def append_to_notion_page(page_id: str, text: str) -> str:
    """Append a text paragraph to a Notion page
    
    Args:
        page_id: The ID of the Notion page or block
        text: The content to append
    """
    try:
        url = f"{NOTION_API_URL}/blocks/{page_id}/children"
        data = {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": text}}]
                    },
                }
            ]
        }

        response = requests.patch(url, headers=headers, json=data)

        if response.status_code == 200:
            return "Successfully added content to Notion page"
        else:
            return f"Failed to add content: {response.text}"
            
    except Exception as e:
        return f"Error appending to page: {str(e)}"

@mcp.tool()
async def create_and_append_page(parent_page_id: str, title: str, content: str) -> str:
    """Create a new Notion page under a parent and append content
    
    Args:
        parent_page_id: ID of the parent page
        title: Title of the new page
        content: Text content to append to the new page
    """
    try:
        # Step 1: Create a new page
        create_url = f"{NOTION_API_URL}/pages"
        page_data = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "properties": {
                "title": {
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": title}
                        }
                    ]
                }
            }
        }

        create_response = requests.post(create_url, headers=headers, json=page_data)

        if create_response.status_code != 200:
            return f"Failed to create page: {create_response.text}"

        page_id = create_response.json().get("id")

        # Step 2: Append content
        append_url = f"{NOTION_API_URL}/blocks/{page_id}/children"
        append_data = {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                }
            ]
        }

        append_response = requests.patch(append_url, headers=headers, json=append_data)

        if append_response.status_code == 200:
            return f"Page created and content appended successfully. Page ID: {page_id}"
        else:
            return f"Page created but failed to append content: {append_response.text}"
            
    except Exception as e:
        return f"Error creating and appending page: {str(e)}"