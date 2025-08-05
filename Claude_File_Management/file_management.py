from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("file_management")

import os

@mcp.tool()
def list_files(directory: str) -> list[str]:
    """List all files in the given directory.

    Args:
        directory: Path to the directory.
    Returns:
        List of file names in the directory.
    """
    try:
        return os.listdir(directory)
    except FileNotFoundError:
        return []
    except NotADirectoryError:
        return []
    except PermissionError:
        return []
    
@mcp.tool()
def read_file(file_path: str) -> str:
    """Read the contents of a file.

    Args:
        file_path: Path to the file.
    Returns:
        Contents of the file as a string.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."
    except IsADirectoryError:
        return "Path is a directory, not a file."
    except PermissionError:
        return "Permission denied."
    except Exception as e:
        return str(e)

import shutil
@mcp.tool()
def move_file(src: str, dest: str) -> str:
    """Move a file from src to dest.

    Args:
        src: Source file path.
        dest: Destination file path.
    Returns:
        Success or error message.
    """
    try:
        shutil.move(src, dest)
        return "File moved successfully."
    except FileNotFoundError:
        return "Source file not found."
    except PermissionError:
        return "Permission denied."
    except Exception as e:
        return str(e)
    

import pathlib
SAFE_ROOT = pathlib.Path("~/Documents/ClaudeAccessible").expanduser().resolve()

@mcp.tool()
def delete_file(file_path: str) -> str:
    """Delete a file, only if it is inside the ClaudeAccessible folder."""
    try:
        # Get absolute, resolved path
        abs_path = pathlib.Path(file_path).expanduser().resolve()
    except Exception as e:
        return f"Invalid path: {e}"

    # Normalize paths to lowercase strings for case-insensitive comparison
    abs_path_str = abs_path.as_posix().lower()
    safe_root_str = SAFE_ROOT.as_posix().lower()

    if not abs_path_str.startswith(safe_root_str + "/") and abs_path_str != safe_root_str:
        return f"Permission denied: Can only delete files inside '{SAFE_ROOT}'"

    if not abs_path.exists():
        return f"File not found: '{abs_path}'"
    if abs_path.is_dir():
        return f"Path is a directory, not a file: '{abs_path}'"

    try:
        abs_path.unlink()
        return f"File deleted successfully: '{abs_path}'"
    except PermissionError:
        return "Permission denied."
    except Exception as e:
        return f"Error deleting file: {e}"
    

import asyncio

if __name__ == "__main__":
    # Initialize and run the server
    asyncio.run(mcp.run(transport="stdio"))    

