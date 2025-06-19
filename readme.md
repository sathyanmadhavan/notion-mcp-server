# Complete Notion MCP Server Setup Guide

A comprehensive guide for setting up the Notion MCP Server.

## Prerequisites

- Python 3.7+
- Notion workspace with API access
- Notion API integration set up

## Complete Installation Process

### Step 1: Clone and Setup Project Directory

```bash
git clone <your-repository-url>
cd notion-mcp-server
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
# Command Prompt
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Note:** You should see `(venv)` at the beginning of your command prompt when the virtual environment is activated.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install requests notion-client python-dotenv fastmcp
```

## Notion API Setup

### Quick Setup Reference

For detailed Notion integration setup, follow the official guide:
**👉 [Notion MCP Server - Integration Setup](https://github.com/makenotion/notion-mcp-server#setup)**

### Summary of Required Steps:

1. **Create Notion Integration** - Follow the official guide above
2. **Share Pages/Databases** - Grant access to your integration
3. **Get API Token** - Copy your integration token

### Environment Configuration

Create a `.env` file in the project root:

```env
NOTION_API_KEY=your_notion_integration_token_here
```

Replace `your_notion_integration_token_here` with the token from your integration setup.

## Running the Script

### Run via MCP Command

```bash
mcp install `your_python_filename.py`
```

## MCP Client Configuration

### For Claude Desktop

Add the following configuration to your Claude Desktop MCP settings file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

**Configuration with Virtual Environment:**

```json
{
  "mcpServers": {
    "notion-server": {
      "command": "C:\\path\\to\\your\\project\\venv\\Scripts\\uv.exe",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "notion-client",
        "--with",
        "python-dotenv",
        "--with",
        "requests",
        "mcp",
        "run",
        "C:\\path\\to\\your\\project\\notion_mcp_server.py"
      ]
    }
  }
}
```

**For macOS/Linux:**
```json
{
  "mcpServers": {
    "notion-server": {
      "command": "/path/to/your/project/venv/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "notion-client",
        "--with",
        "python-dotenv",
        "--with",
        "requests",
        "mcp",
        "run",
        "/path/to/your/project/notion_mcp_server.py"
      ]
    }
  }
}
```

### Alternative: Direct Python Configuration

```json
{
  "mcpServers": {
    "notion-server": {
      "command": "/path/to/your/project/venv/bin/python",
      "args": [
        "/path/to/your/project/notion_mcp_server.py"
      ],
      "env": {
        "NOTION_API_KEY": "your_notion_api_key_here"
      }
    }
  }
}
```

**Windows version:**
```json
{
  "mcpServers": {
    "notion-server": {
      "command": "C:\\path\\to\\your\\project\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\path\\to\\your\\project\\notion_mcp_server.py"
      ],
      "env": {
        "NOTION_API_KEY": "your_notion_api_key_here"
      }
    }
  }
}
```

## Important Path Updates

Make sure to replace the following paths with your actual project paths:

**Windows:**
- Virtual environment Python: `C:\path\to\your\project\venv\Scripts\python.exe`
- Virtual environment uv: `C:\path\to\your\project\venv\Scripts\uv.exe`
- Script path: `C:\path\to\your\project\notion_mcp_server.py`

**macOS/Linux:**
- Virtual environment Python: `/path/to/your/project/venv/bin/python`
- Virtual environment uv: `/path/to/your/project/venv/bin/uv`
- Script path: `/path/to/your/project/notion_mcp_server.py`

## Testing Your Setup

1. **Activate your virtual environment**
2. **Test the script directly:**
   ```bash
    mcp install `your_python_filename.py`
   ```
3. **If successful, restart Claude Desktop**
4. **Check that the Notion tools are available in Claude**

## Troubleshooting Virtual Environment

### If activation fails:

**Windows PowerShell execution policy issue:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Verify virtual environment is activated:**
- Look for `(venv)` in your command prompt
- Check Python path: `which python` (macOS/Linux) or `where python` (Windows)

### Deactivating Virtual Environment

When you're done working:
```bash
deactivate
```

## Dependencies

- `requests`: HTTP client for API calls
- `notion-client`: Official Notion Python SDK
- `python-dotenv`: Environment variable management
- `fastmcp`: MCP server framework
- `uv`: Fast Python package installer and runner

## Security Notes

- Never commit your `.env` file or API keys to version control
- Keep your Notion API key secure and rotate it regularly
- Only grant necessary permissions to your integration
- Regularly review which pages/databases are shared with your integration
- Always use virtual environments to isolate project dependencies