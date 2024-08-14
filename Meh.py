import os
import shutil
import readline
import subprocess

# Detect operating system
os_type = os.name

# Command history file (to persist history across sessions)
history_file = os.path.expanduser("~/.cli_history")

# Load command history if on a posix system (Linux/macOS)
if os_type == "posix" and os.path.exists(history_file):
    readline.read_history_file(history_file)

def clear_screen():
    """Clears the terminal screen."""
    if os_type == "nt":  # Windows
        os.system("cls")
    else:  # macOS and Linux
        os.system("clear")

def change_directory(path):
    """Changes the current working directory."""
    try:
        os.chdir(path)
    except FileNotFoundError:
        print(f"cd: no such file or directory: {path}")
    except NotADirectoryError:
        print(f"cd: not a directory: {path}")
    except PermissionError:
        print(f"cd: permission denied: {path}")

def list_directory():
    """Lists contents of the current directory, i think i need a day off."""
    if os_type == "nt":
        os.system("dir")
    else:
        os.system("ls -la")

def remove_file_or_directory(path):
    """Removes a file or directory."""
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            print(f"rm: cannot remove '{path}': No such file or directory")
    except Exception as e:
        print(f"rm: cannot remove '{path}': {e}")

def make_directory(path):
    #create a new directory
    try:
        os.makedirs(path)
    except FileExistsError:
        print(f"mkdir: cannot create directory ‘{path}’: File exists")
    except Exception as e:
        print(f"mkdir: cannot create directory ‘{path}’: {e}")

def execute_command(command):
    args = command.split()

    if not args:
        return

    cmd = args[0].lower()

    if cmd in ["cls", "clear"]:
        clear_screen()
    elif cmd == "cd" and len(args) > 1:
        change_directory(args[1])
    elif cmd in ["dir", "ls"]:
        list_directory()
    elif cmd in ["rm", "del"] and len(args) > 1:
        remove_file_or_directory(args[1])
    elif cmd == "mkdir" and len(args) > 1:
        make_directory(args[1])
    elif cmd == "exit" or cmd == "quit":
        save_history()
        print("Exiting the terminal, Credits: Aaron.......")
        exit(0)
    else:
        run_system_command(command)

def run_system_command(command):
    """Runs a system command not directly supported by the CLI."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def save_history():
    """Saves the command history if on a posix system."""
    if os_type == "posix":
        readline.write_history_file(history_file)

def setup_autocomplete():
    """Sets up command autocomplete if on a posix system."""
    if os_type == "posix":
        readline.parse_and_bind("tab: complete")

def main():
    setup_autocomplete()

    # Set the initial prompt based on Operating sysytem i hate my fingers
    if os_type == "nt":
        prompt = "C:\\Users\\Admin> "
    else:
        prompt = "user@hostname:~$ "

    while True:
        try:
            command = input(prompt)
            execute_command(command)
        except EOFError:
            print("\nUse 'exit' or 'quit' to exit.")
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected. Use 'exit' or 'quit' to exit.")
        finally:
            save_history()

if __name__ == "__main__":
    # Inform the user of the operating system!
    if os_type == "nt":
        print("Operating System: Windows")
    elif os_type == "posix":
        print("Operating System: Linux or macOS")
    else:
        print(f"Operating System: {os_type} (Unrecognized)")

    main()
