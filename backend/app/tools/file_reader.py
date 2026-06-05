"""File reader tool for reading file contents."""

import os
from pathlib import Path
from typing import Any, Dict, Optional
from app.tools.base import BaseTool, ToolResult


class FileReaderTool(BaseTool):
    """Tool for reading file contents."""
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        ".txt", ".md", ".json", ".yaml", ".yml",
        ".py", ".js", ".ts", ".tsx", ".jsx",
        ".html", ".css", ".sql", ".xml", ".csv"
    }
    
    # Max file size (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    def __init__(self, base_dir: Optional[str] = None):
        super().__init__(
            name="file_reader",
            description="Read contents of a file. Supports text-based files."
        )
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
    
    async def execute(self, file_path: str) -> ToolResult:
        """
        Read file contents.
        
        Args:
            file_path: Path to file to read
            
        Returns:
            ToolResult with file contents
        """
        try:
            # Resolve path
            full_path = self._resolve_path(file_path)
            
            if not full_path.exists():
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"File not found: {file_path}"
                )
            
            if not full_path.is_file():
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Path is not a file: {file_path}"
                )
            
            # Check file extension
            if full_path.suffix not in self.ALLOWED_EXTENSIONS:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"File type not allowed: {full_path.suffix}"
                )
            
            # Check file size
            file_size = full_path.stat().st_size
            if file_size > self.MAX_FILE_SIZE:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"File too large: {file_size} bytes (max: {self.MAX_FILE_SIZE})"
                )
            
            # Read file
            with open(full_path, 'r', encoding='utf-8') as f:
                contents = f.read()
            
            return ToolResult(
                success=True,
                data=contents,
                metadata={
                    "file_path": str(full_path),
                    "size": file_size,
                    "lines": len(contents.split('\n'))
                }
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Error reading file: {str(e)}"
            )
    
    def _resolve_path(self, file_path: str) -> Path:
        """Resolve and validate file path."""
        # Convert to absolute path
        if os.path.isabs(file_path):
            path = Path(file_path)
        else:
            path = self.base_dir / file_path
        
        # Resolve symlinks
        path = path.resolve()
        
        # Ensure path is within base directory for security
        try:
            path.relative_to(self.base_dir)
        except ValueError:
            raise ValueError(f"Path outside base directory: {file_path}")
        
        return path
    
    def get_schema(self) -> Dict[str, Any]:
        """Get JSON schema for file reader parameters."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to file to read"
                    }
                },
                "required": ["file_path"]
            }
        }
