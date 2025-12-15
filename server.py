import tkinter as tk
from tkinter import scrolledtext, ttk
import subprocess
import os

# ------------- COLORS & STYLES -------------
BG_COLOR = "#0f172a"       # window background
CARD_COLOR = "#1e293b"     # panels
ACCENT = "#38bdf8"         # cyan accent
TEXT_PRIMARY = "#e5e7eb"   # main text
TEXT_SECONDARY = "#9ca3af" # secondary text
BUTTON_BG = "#38bdf8"
BUTTON_FG = "#0b1120"

def analyze_code():
    code = input_text.get("1.0", tk.END)

    exe_path = os.path.join(os.getcwd(), "compiler.exe")

    try:
        process = subprocess.Popen(
            exe_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output, error = process.communicate(code)
        output_text.configure(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, output if output else error)
        output_text.configure(state="disabled")

    except Exception as e:
        output_text.configure(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, str(e))
        output_text.configure(state="disabled")


# ------------- MAIN WINDOW -------------
window = tk.Tk()
window.title("LexiCore – Compiler Design Project")
window.geometry("950x650")
window.configure(bg=BG_COLOR)

# Center the window a bit nicer
window.update_idletasks()
x = (window.winfo_screenwidth() // 2) - (950 // 2)
y = (window.winfo_screenheight() // 2) - (650 // 2)
window.geometry(f"950x650+{x}+{y}")

# ------------- STYLE CONFIG -------------
style = ttk.Style(window)
style.theme_use("clam")  # better base theme

style.configure(
    "Card.TFrame",
    background=CARD_COLOR,
    relief="flat"
)
style.configure(
    "Heading.TLabel",
    background=BG_COLOR,
    foreground=TEXT_PRIMARY,
    font=("Segoe UI", 16, "bold")
)
style.configure(
    "Subheading.TLabel",
    background=CARD_COLOR,
    foreground=TEXT_SECONDARY,
    font=("Segoe UI", 11)
)
style.configure(
    "Section.TLabel",
    background=CARD_COLOR,
    foreground=TEXT_PRIMARY,
    font=("Segoe UI", 12, "bold")
)
style.configure(
    "Accent.TButton",
    background=BUTTON_BG,
    foreground=BUTTON_FG,
    font=("Segoe UI", 11, "bold"),
    borderwidth=0,
    focusthickness=3,
    focuscolor=ACCENT
)
style.map(
    "Accent.TButton",
    background=[("active", "#0ea5e9")],
    foreground=[("disabled", "#2e5bb4")]
)

# ------------- LAYOUT FRAMES -------------
# Main wrapper
main_frame = ttk.Frame(window, style="Card.TFrame", padding=20)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Title & subtitle area
header_frame = ttk.Frame(main_frame, style="Card.TFrame")
header_frame.pack(fill="x", pady=(0, 15))

title_label = ttk.Label(
    header_frame,
    text="LexiCore",
    style="Heading.TLabel"
)
title_label.pack(side="left")

subtitle_label = ttk.Label(
    header_frame,
    text="Analyze and test your C source code in a clean, modern interface.",
    style="Subheading.TLabel"
)
subtitle_label.pack(side="left", padx=(15, 0))

# Split into two panels: input (left) and output (right)
content_frame = ttk.Frame(main_frame, style="Card.TFrame")
content_frame.pack(fill="both", expand=True)

content_frame.columnconfigure(0, weight=1)
content_frame.columnconfigure(1, weight=1)
content_frame.rowconfigure(0, weight=1)

# ------------- LEFT PANEL: INPUT -------------
input_frame = ttk.Frame(content_frame, style="Card.TFrame", padding=(15, 15, 8, 15))
input_frame.grid(row=0, column=0, sticky="nsew")

input_label = ttk.Label(
    input_frame,
    text="C Source Code",
    style="Section.TLabel"
)
input_label.pack(anchor="w", pady=(0, 8))

input_helper = ttk.Label(
    input_frame,
    text="Paste or type your C program here, then click Analyze.",
    style="Subheading.TLabel"
)
input_helper.pack(anchor="w", pady=(0, 10))

input_text = scrolledtext.ScrolledText(
    input_frame,
    height=18,
    font=("Consolas", 11),
    bg="#020617",
    fg=TEXT_PRIMARY,
    insertbackground=ACCENT,
    relief="flat",
    borderwidth=0
)
input_text.pack(fill="both", expand=True)

# ------------- CENTER BUTTON AREA -------------
button_frame = ttk.Frame(main_frame, style="Card.TFrame")
button_frame.pack(pady=15)

analyze_button = ttk.Button(
    button_frame,
    text="► Analyze Code",
    style="Accent.TButton",
    command=analyze_code
)
analyze_button.pack(ipadx=15, ipady=4)

# ------------- RIGHT PANEL: OUTPUT -------------
output_frame = ttk.Frame(content_frame, style="Card.TFrame", padding=(8, 15, 15, 15))
output_frame.grid(row=0, column=1, sticky="nsew")

output_label = ttk.Label(
    output_frame,
    text="Compiler Output",
    style="Section.TLabel"
)
output_label.pack(anchor="w", pady=(0, 8))

output_helper = ttk.Label(
    output_frame,
    text="Diagnostics and messages from compiler.exe will appear here.",
    style="Subheading.TLabel"
)
output_helper.pack(anchor="w", pady=(0, 10))

output_text = scrolledtext.ScrolledText(
    output_frame,
    height=18,
    font=("Consolas", 11),
    bg="#020617",
    fg=TEXT_PRIMARY,
    insertbackground=ACCENT,
    relief="flat",
    borderwidth=0
)
output_text.pack(fill="both", expand=True)
output_text.configure(state="disabled")

window.mainloop()
