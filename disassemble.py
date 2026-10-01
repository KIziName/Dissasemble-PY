import sys
import dis
import os
import io
import tokenize
import contextlib
import tkinter as tk

from tkinter import filedialog, messagebox, scrolledtext


def get_bytecode_text(filepath):
    try:
        with tokenize.open(filepath) as f:
            source = f.read()
    except UnicodeDecodeError as e:
        return False, ("❌ Cannot decode file '{}' using the declared "
                       "encoding: {}").format(filepath, e)
    except SyntaxError as e:
        return False, ("❌ Invalid coding declaration in '{}' "
                       "(PEP 263): {}").format(filepath, e)
    except FileNotFoundError:
        return False, "❌ File '{}' not found.".format(filepath)
    except OSError as e:
        return False, "❌ Read error: {}".format(e)

    if not source.strip():
        return False, ("⚠️ File '{}' is empty or contains only whitespace. "
                       "No bytecode.").format(filepath)

    try:
        code_obj = compile(source, filepath, 'exec')
    except SyntaxError as e:
        return False, "❌ Syntax error: {}".format(e)
    except Exception as e:
        return False, "❌ Compilation error: {}".format(e)

    buf = io.StringIO()
    buf.write("\n===== Bytecode for {} (Python {}) =====\n".format(
        filepath, sys.version.split()[0]
    ))

    with contextlib.redirect_stdout(buf):
        dis.dis(code_obj)

    buf.write("===== End of bytecode =====\n")
    return True, buf.getvalue()



class DisassemblerApp(object):
    def __init__(self, root):
        self.root = root
        root.title("Python Bytecode Disassembler")
        root.geometry("820x600")

        top = tk.Frame(root)
        top.pack(fill=tk.X, padx=8, pady=6)

        tk.Label(top, text="File:").pack(side=tk.LEFT)

        self.path_var = tk.StringVar()
        entry = tk.Entry(top, textvariable=self.path_var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 6))
        entry.bind("<Return>", lambda e: self.run_disassemble())

        tk.Button(top, text="Browse...", command=self.browse).pack(side=tk.LEFT, padx=(0, 4))
        tk.Button(top, text="Disassemble", command=self.run_disassemble).pack(side=tk.LEFT, padx=(0, 4))
        tk.Button(top, text="Copy", command=self.copy).pack(side=tk.LEFT, padx=(0, 4))           
        tk.Button(top, text="Clear", command=self.clear).pack(side=tk.LEFT)

        self.text = scrolledtext.ScrolledText(root, wrap=tk.NONE,
                                              font=("Courier New", 10))
        self.text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        xscroll = tk.Scrollbar(root, orient=tk.HORIZONTAL,
                               command=self.text.xview)
        self.text.configure(xscrollcommand=xscroll.set)
        xscroll.pack(fill=tk.X, side=tk.BOTTOM)

        self.status = tk.Label(root, text="Ready.", anchor="w", relief=tk.SUNKEN)
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

        self.text.bind("<Button-3>", lambda e: self.copy())

        self.set_text("Enter a .py filename and press Disassemble.\n"
                      "Python: {}\n".format(sys.version.split()[0]))

    def set_text(self, s):
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, s)

    def clear(self):
        self.set_text("")
        self.status.config(text="Cleared.")

    def copy(self):
        try:
            data = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            data = self.text.get("1.0", tk.END)
            
        self.root.clipboard_clear()
        self.root.clipboard_append(data)
        self.root.update()
        self.status.config(text="Copied to clipboard.")

    def browse(self):
        path = filedialog.askopenfilename(
            title="Select a Python file",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if path:
            self.path_var.set(path)

    def run_disassemble(self):
        filepath = self.path_var.get().strip()
        if not filepath:
            messagebox.showwarning("No file", "Please choose or enter a file.")
            return
        if not os.path.isfile(filepath):
            messagebox.showerror("Not found",
                                 "File not found:\n{}".format(filepath))
            self.status.config(text="File not found.")
            return

        ok, text = get_bytecode_text(filepath)
        self.set_text(text)
        if ok:
            self.status.config(text="OK: {}".format(os.path.abspath(filepath)))
        else:
            self.status.config(text="Error.")
            

def show_bytecode_cli(filepath):
    ok, text = get_bytecode_text(filepath)
    if ok:
        sys.stdout.write(text)
    else:
        sys.stderr.write(text + "\n")
        sys.exit(1)
        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        show_bytecode_cli(sys.argv[1])
    else:
        root = tk.Tk()
        app = DisassemblerApp(root)
        root.mainloop()
