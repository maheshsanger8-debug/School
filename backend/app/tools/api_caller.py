"""API caller tool for making HTTP requests."""

import httpx
from typing import Any, Dict, Optional, List
from app.tools.base import BaseTool, ToolResult


class APICallerTool(BaseTool):
    """Tool for making HTTP API calls."""
    
    # Timeout for requests
    TIMEOUT = 30.0
    
    # Max response size (5MB)
    MAX_RESPONSE_SIZE = 5 * 1024 * 1024
    
    def __init__(self):
        super().__init__(
            name="api_caller",
            description="Make HTTP API calls (GET, POST, PUT, DELETE). Returns response data."
        )
    
    async def execute(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        timeout: float = TIMEOUT
    ) -> ToolResult:
        """
        Make an HTTP API call.
        
        Args:
            url: URL to call
            method: HTTP method (GET, POST, PUT, DELETE)
            headers: HTTP headers
            params: Query parameters
            json_data: JSON body data
            timeout: Request timeout in seconds
            
        Returns:
            ToolResult with response data
        """
        try:
            # Validate URL
            if not url.startswith(("http://", "https://")):
                return ToolResult(
                    success=False,
                    data=None,
                    error="Invalid URL: must start with http:// or https://"
                )
            
            # Validate method
            method = method.upper()
            if method not in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"]:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Invalid HTTP method: {method}"
                )
            
            # Make request
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers or {},
                    params=params or {},
                    json=json_data
                )
            
            # Check response size
            if len(response.content) > self.MAX_RESPONSE_SIZE:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Response too large: {len(response.content)} bytes"
                )
            
            # Parse response
            try:
                response_data = response.json()
            except:
                response_data = response.text
            
            return ToolResult(
                success=response.status_code < 400,
                data=response_data,
                metadata={
                    "status_code": response.status_code,
                    "url": url,
                    "method": method,
                    "response_size": len(response.content)
                }
            )
        
        except httpx.TimeoutException:
            return ToolResult(
                success=False,
                data=None,
                error=f"Request timeout after {timeout} seconds"
            )
        
        except httpx.RequestError as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Request error: {str(e)}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Error making API call: {str(e)}"
            )
    
    def get_schema(self) -> Dict[str, Any]:
        """Get JSON schema for API caller parameters."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to call"
                    },
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"],
                        "description": "HTTP method"
                    },
                    "headers": {
                        "type": "object",
                        "description": "HTTP headers"
                    },
                    "params": {
                        "type": "object",
                        "description": "Query parameters"
                    },
                    "json_data": {
                        "type": "object",
                        "description": "JSON body data"
                    }
                },
                "required": ["url"]
            }
        }
