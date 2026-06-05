"""Web search tool for searching the internet."""

import httpx
from typing import Any, Dict, Optional, List
from app.tools.base import BaseTool, ToolResult


class WebSearchTool(BaseTool):
    """Tool for searching the web."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize web search tool.
        
        Args:
            api_key: Optional API key for search service
        """
        super().__init__(
            name="web_search",
            description="Search the web for information. Returns relevant results."
        )
        self.api_key = api_key
        # Using DuckDuckGo for public searches (no API key required)
        self.search_url = "https://api.duckduckgo.com/"
    
    async def execute(self, query: str, max_results: int = 5) -> ToolResult:
        """
        Search the web.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            ToolResult with search results
        """
        try:
            if not query or len(query.strip()) == 0:
                return ToolResult(
                    success=False,
                    data=None,
                    error="Search query cannot be empty"
                )
            
            # Perform search using DuckDuckGo API
            params = {
                "q": query,
                "format": "json",
                "no_redirect": 1
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.search_url, params=params)
            
            if response.status_code != 200:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Search failed with status {response.status_code}"
                )
            
            data = response.json()
            
            # Extract results
            results = []
            
            # DDG doesn't return direct results in API, but returns abstract information
            # For a production system, you'd use a proper search API like Google Custom Search
            if data.get("AbstractText"):
                results.append({
                    "title": data.get("Heading", "Result"),
                    "description": data.get("AbstractText"),
                    "url": data.get("AbstractURL", "")
                })
            
            return ToolResult(
                success=True,
                data={
                    "query": query,
                    "results": results,
                    "result_count": len(results)
                },
                metadata={
                    "query": query,
                    "results_returned": len(results),
                    "max_requested": max_results
                }
            )
        
        except httpx.TimeoutException:
            return ToolResult(
                success=False,
                data=None,
                error="Search request timeout"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Search error: {str(e)}"
            )
    
    def get_schema(self) -> Dict[str, Any]:
        """Get JSON schema for web search parameters."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
