import os
import sys
import argparse
import mimetypes
import fitz  # PyMuPDF

def is_binary_file(file_path):
    """Check if a file is binary by reading its first 1024 bytes."""
    text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
        if not chunk:  # Empty file
            return False
        # Check if any null bytes in the first 1024 bytes
        if b'\x00' in chunk:
            return True
        # Check if the file contains mostly non-text characters
        non_text = chunk.translate(None, text_chars)
        return len(non_text) / len(chunk) > 0.3
    except Exception:
        return True

def extract_pdf_text(file_path):
    """Extract text from PDF file using PyMuPDF."""
    try:
        doc = fitz.open(file_path)
        text = []
        for page in doc:
            text.append(page.get_text())
        return '\n'.join(text)
    except Exception as e:
        return f"[Error extracting text from PDF: {str(e)}]"

def read_list_file(file_path):
    """
    Read a list file (.il or .wl) and return the list of patterns.
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"List file not found: {file_path}")
        return []

def match_pattern(path, patterns):
    """
    Check if a given path matches any of the patterns in the list.
    Patterns can be:
    - 'dir/' to match directory 'dir' in any part of the path
    - 'file.ext' to match any file with that name
    - '*.ext' to match any file with that extension
    """
    if not patterns:
        return False
        
    # Normalize path for consistent matching
    path = path.replace('\\', '/').lower()
    
    for pattern in patterns:
        pattern = pattern.strip().lower()
        if not pattern:
            continue
            
        # If pattern ends with /, it's a directory pattern
        if pattern.endswith('/'):
            dir_name = pattern.rstrip('/')
            # Check if any directory in path matches the pattern
            if f'/{dir_name}/' in path or path.endswith(f'/{dir_name}') or path == dir_name:
                return True
        # If pattern starts with *., it's an extension pattern
        elif pattern.startswith('*.'):
            ext = pattern[1:]
            if path.endswith(ext):
                return True
        # Otherwise, it's a filename pattern
        else:
            if path.endswith(f'/{pattern}') or path == pattern:
                return True
                
    return False

def save_project_structure_and_files(root_path, output_file, ignore_list=None, whitelist=None):
    """
    Save the project structure and contents of all files in the project to a text file,
    considering ignore and whitelist. Skips binary files and non-text content.
    """
    project_structure = []
    file_contents = []
    
    # Common binary file extensions to ignore
    binary_extensions = {
        # Images
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.ico', '.svg', '.webp',
        # Videos
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm',
        # Archives
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',
        # Executables and libraries
        '.exe', '.dll', '.so', '.dylib',
        # Documents (handled separately)
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'
    }

    for root, dirs, files in os.walk(root_path):
        # Filter hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        # Filter directories and files based on ignore_list and whitelist
        dirs[:] = [
            d for d in dirs
            if not match_pattern(d, ignore_list) and
               (not whitelist or match_pattern(d, whitelist))
        ]
        files = [
            f for f in files
            if not f.startswith('.') and  # Skip hidden files
               not match_pattern(f, ignore_list) and
               (not whitelist or match_pattern(f, whitelist))
        ]

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_path).replace("\\", "/")
            
            # Skip binary files by extension
            _, ext = os.path.splitext(file.lower())
            if ext in binary_extensions and ext != '.pdf':  # Handle PDFs separately
                project_structure.append(f"{rel_path} [SKIPPED - binary file]")
                continue
                
            # Skip binary files by content
            if is_binary_file(file_path) and ext != '.pdf':  # Still check PDFs
                project_structure.append(f"{rel_path} [SKIPPED - binary content]")
                continue
                
            project_structure.append(rel_path)
            
            try:
                content = None
                
                # Special handling for PDFs
                if ext == '.pdf':
                    content = extract_pdf_text(file_path)
                    if content:
                        file_contents.append(f"\n=== File: {rel_path} (PDF content) ===\n")
                        file_contents.append(f"{content}\n")
                    continue
                
                # Handle text files
                encodings = ['utf-8', 'cp1251', 'latin1', 'iso-8859-1', 'windows-1251']
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            content = f.read()
                        break
                    except UnicodeDecodeError:
                        continue
                
                if content is None:
                    raise Exception(f"Failed to read file with any encoding: {encodings}")
                    
                file_contents.append(f"\n=== File: {rel_path} ===\n")
                file_contents.append(f"{content}\n")
                
            except Exception as e:
                file_contents.append(f"\n=== Error reading {rel_path} ===\n")
                file_contents.append(f"Error: {str(e)}\n")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Project Structure:\n")
            f.write("\n".join(project_structure) + "\n\n")
            f.write("File Contents:\n")
            f.write("\n".join(file_contents))
        print(f"Successfully saved project contents to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

def main():
    script_dir = os.path.dirname(__file__)
    il_file = os.path.join(script_dir, '.il')
    wl_file = os.path.join(script_dir, '.wl')

    parser = argparse.ArgumentParser(description="Save project structure and file contents.")
    parser.add_argument("--il", help="Use ignore list (.il file)", action="store_true")
    parser.add_argument("--wl", help="Use whitelist (.wl file)", action="store_true")
    parser.add_argument("--show-locations", help="Show the location of the .il and .wl files", action="store_true")

    args = parser.parse_args()

    if args.show_locations:
        print("IL file is located at:", il_file)
        print("WL file is located at:", wl_file)
        sys.exit(0)

    ignore_list = read_list_file(il_file) if args.il else None
    whitelist = read_list_file(wl_file) if args.wl else None

    save_project_structure_and_files('.', 'project_contents.txt', ignore_list, whitelist)
