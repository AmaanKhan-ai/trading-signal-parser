import tkinter as tk
import json

from parser import parse_trade
from rules import apply_rules
from utils import get_time_cst
from kafka_producer import send_to_kafka


def process_trade():
    text = input_box.get("1.0", tk.END).strip()

    if not text:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "⚠️ Please enter a trading message.")
        return

    try:
        data = parse_trade(text)
        data = apply_rules(data)
        

        send_to_kafka(data)

        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, json.dumps(data, indent=4))

    except Exception as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"❌ Error:\n{e}")


# ---------------- UI SETUP ---------------- #

root = tk.Tk()
root.title("Trading Signal Processor")
root.geometry("760x560")
root.configure(bg="#0f172a")

# Fonts
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_LABEL = ("Segoe UI", 13, "bold")
FONT_TEXT_INPUT = ("Segoe UI", 12)
FONT_TEXT_OUTPUT = ("Consolas", 13)

# Colors
BG_MAIN = "#0f172a"
ACCENT = "#38bdf8"
TEXT_LIGHT = "#e5e7eb"
INPUT_BG = "#f8fafc"
INPUT_FG = "#020617"
OUTPUT_BG = "#020617"
OUTPUT_FG = "#e5e7eb"
BUTTON_BG = "#22c55e"

# Title
tk.Label(
    root,
    text="📊 Trading Signal Parser Bot",
    bg=BG_MAIN,
    fg=ACCENT,
    font=FONT_TITLE
).pack(pady=16)

# Input Label
tk.Label(
    root,
    text="Enter Trading Message",
    bg=BG_MAIN,
    fg=TEXT_LIGHT,
    font=FONT_LABEL
).pack(anchor="w", padx=40)

# Input Box (LIGHT)
input_box = tk.Text(
    root,
    height=5,
    bg=INPUT_BG,
    fg=INPUT_FG,
    insertbackground="black",
    font=FONT_TEXT_INPUT,
    relief="flat"
)
input_box.pack(padx=40, pady=8, fill=tk.X)

# Process Button
tk.Button(
    root,
    text="🚀 Process Signal",
    bg=BUTTON_BG,
    fg="black",
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    padx=14,
    pady=8,
    command=process_trade
).pack(pady=14)

# Output Label
tk.Label(
    root,
    text="Processed Output",
    bg=BG_MAIN,
    fg=TEXT_LIGHT,
    font=FONT_LABEL
).pack(anchor="w", padx=40)

# Output Box (BIGGER FONT)
output_box = tk.Text(
    root,
    height=12,
    bg=OUTPUT_BG,
    fg=OUTPUT_FG,
    insertbackground="white",
    font=FONT_TEXT_OUTPUT,
    relief="flat"
)
output_box.pack(padx=40, pady=8, fill=tk.X)

root.mainloop()