import tkinter as tk
from tkinter import scrolledtext
import tarfile
import io

virtual_fs = {
    "God": {
        "home": {
            "user": {
                "file1.txt": "user",
                "file2.txt": "user"
            },
            "admin": {
                "file3.txt": "admin"
            }
        },
        "mirea": {
            "Kudzh": {
                "file4.txt": "Kudzh"
            }
        }
    }
}

current_path = ["God", "home"]
current_user = "user"
computer_name = "VirtualOS"

def create_gui():
    root = tk.Tk()
    root.title(f"{computer_name} Emulator")

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20)
    output_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    input_frame = tk.Frame(root)
    input_frame.pack(side=tk.BOTTOM, fill=tk.X)

    input_entry = tk.Entry(input_frame)
    input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def execute_command(event=None):
        command = input_entry.get()
        input_entry.delete(0, tk.END)
        handle_command(command, output_text)

    input_entry.bind("<Return>", execute_command)
    execute_button = tk.Button(input_frame, text="Execute", command=execute_command)
    execute_button.pack(side=tk.RIGHT)

    return root, output_text, input_entry

def ls(path):
    dir_content = virtual_fs
    for p in path:
        dir_content = dir_content.get(p, {})
    return list(dir_content.keys())

def cd(path, new_dir):
    global current_path
    if new_dir == "..":
        if path:
            path.pop()
    else:
        dir_content = virtual_fs
        for p in path:
            dir_content = dir_content.get(p, {})
        if new_dir in dir_content:
            path.append(new_dir)

def clear(output_text):
    output_text.delete(1.0, tk.END)

def chmod(path, file, mode):
    dir_content = virtual_fs
    for p in path:
        dir_content = dir_content.get(p, {})
    if file in dir_content:
        dir_content[file] = mode

def save_to_tar():
    memory_file = io.BytesIO()
    with tarfile.open(fileobj=memory_file, mode='w') as tar:
        def add_to_tar(path, tar_path):
            if isinstance(path, dict):
                for key, value in path.items():
                    new_path = f"{tar_path}/{key}"
                    if isinstance(value, dict):
                        add_to_tar(value, new_path)
                    else:
                        tarinfo = tarfile.TarInfo(name=new_path)
                        tarinfo.size = len(value.encode('utf-8'))
                        tar.addfile(tarinfo, io.BytesIO(value.encode('utf-8')))
        add_to_tar(virtual_fs, "")
    memory_file.seek(0)
    with open("vfs.tar", "wb") as f:
        f.write(memory_file.read())
    return "vfs.tar"

def handle_command(command, output_text):
    if command.startswith("ls"):
        result = ls(current_path)
        output_text.insert(tk.END, f"{' '.join(result)}\n")
    elif command.startswith("cd "):
        new_dir = command[3:]
        cd(current_path, new_dir)
        output_text.insert(tk.END, f"Changed directory to {current_path}\n")
    elif command.startswith("chmod "):
        _, file, mode = command.split()
        chmod(current_path, file, mode)
        output_text.insert(tk.END, f"Changed mode of {file} to {mode}\n")
    elif command == "clear":
        clear(output_text)
    elif command == "exit":
        output_text.insert(tk.END, "Exiting...\n")
        root.quit()
    else:
        output_text.insert(tk.END, "Unknown command\n")
    output_text.see(tk.END)

def on_closing():
    tar_file = save_to_tar()
    output_text.insert(tk.END, f"Virtual file system saved to {tar_file}\n")
    root.quit()

if __name__ == "__main__":
    root, output_text, input_entry = create_gui()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()