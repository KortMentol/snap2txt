# Snap2Txt (Improved Fork)

> Enhanced version of [vorniches/snap2txt](https://github.com/vorniches/snap2txt) with better encoding support and error handling.

Snap2Txt is a Python utility that captures the structure and contents of a project directory and saves them into a text file. It's designed for quick documentation of your project's file system.

## 🚀 Key Improvements

- **Better Encoding Support**: Handles UTF-8, cp1251, windows-1251, and other encodings with automatic detection
- **Improved Error Handling**: Clear error messages and graceful handling of file reading issues
- **Robust Pattern Matching**: Advanced pattern support for ignore and whitelist options
- **Cross-Platform**: Works consistently across Windows, macOS, and Linux

## Features

- **Complete Capture**: Records the entire file structure and contents of the project.
- **Customizable Filters**: Offers ignore and whitelist options for targeted scanning.
- **Command-Line Interface**: Simple and easy-to-use command-line tool.

## Prerequisites

- [Python 3.6 or higher](https://www.python.org/downloads/) (includes pip)
  - [Download Python for Windows](https://www.python.org/downloads/windows/)
  - [Download Python for macOS](https://www.python.org/downloads/macos/)
  - For Linux: Use your distribution's package manager (e.g., `sudo apt install python3 python3-pip`)

## Installation

Install Snap2Txt with pip:

```bash
pip install git+https://github.com/KortMentol/snap2txt.git@improved
```

> **Note**: The installation automatically provides `.il` and `.wl` files along with the package.

## Usage

Navigate to your project directory and run:

```bash
snap2txt
```

By default, Snap2Txt will scan all files and directories in the current folder and produce an output file called `project_contents.txt`.

### Locate the .il and .wl Files

To find where Snap2Txt's `.il` and `.wl` files are located on your system, run:

```bash
snap2txt --show-locations
```

This will print the full path to each file for easy customization.

### Command Line Options

- `--il`: Use ignore list defined in `.il`
- `--wl`: Use whitelist defined in `.wl`
- `--show-locations`: Show paths to `.il` and `.wl` files

Examples:

```bash
# Basic usage
snap2txt

# Use ignore list
snap2txt --il

# Use whitelist
snap2txt --wl
```

## Pattern Matching

Examples of patterns for `.il` and `.wl` files:

- `*.py` - all Python files
- `logs/` - any directory named "logs"
- `file.txt` - exact filename match
- `**/temp/` - any "temp" directory at any level

Case-insensitive, works on Windows/Linux/Mac.

## Configuration

Snap2Txt respects two files for filtering:

1. **Ignore List (`.il`)**: Exclude certain files/directories.
2. **Whitelist (`.wl`)**: Include only certain files/directories.

By default, Snap2Txt installs a basic `.il` and `.wl` in the package directory. To tailor the behavior for your project, you can edit those files or replace them with your own custom rules.

> **Tip**: To quickly locate where these files were installed, use `snap2txt --show-locations`.

### Example `.il` File

```text
node_modules/
*.log
```

### Example `.wl` File

```text
*.py
*.md
```

## Contributing

Contributions to Snap2Txt are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## License

Snap2Txt is open-sourced software licensed under the [MIT license](LICENSE).

## Uninstallation

To uninstall Snap2Txt:

```bash
pip uninstall snap2txt
```

## Support

For support, questions, or feedback, please [open an issue](https://github.com/KortMentol/snap2txt/issues) in this repository.
