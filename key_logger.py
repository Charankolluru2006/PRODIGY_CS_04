import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import json
import csv

# =========================================================
# ADVANCED KEYBOARD ACTIVITY MONITOR
# Educational / Ethical Demonstration Only
# =========================================================

LOG_FILE = "key_log.txt"
JSON_FILE = "key_log.json"
CSV_FILE = "key_log.csv"

key_count = {}
session_logs = []


# =========================================================
# LOG KEY EVENTS
# =========================================================

def log_key(event):

    key = event.keysym

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    log_entry = {
        "timestamp": timestamp,
        "key": key
    }

    session_logs.append(log_entry)

    # Update key frequency
    if key in key_count:
        key_count[key] += 1

    else:
        key_count[key] = 1

    # Save to TXT
    with open(LOG_FILE, "a") as file:

        file.write(
            f"[{timestamp}] Key Pressed: {key}\n"
        )

    # Display in GUI
    display.insert(
        tk.END,
        f"[{timestamp}] Key Pressed: {key}\n"
    )

    display.see(tk.END)

    # Update statistics
    update_stats()


# =========================================================
# UPDATE STATISTICS
# =========================================================

def update_stats():

    total = sum(key_count.values())

    stats_text = (
        f"Total Keys Pressed: {total}\n"
        f"Unique Keys: {len(key_count)}\n"
    )

    stats_box.config(state="normal")
    stats_box.delete(1.0, tk.END)
    stats_box.insert(tk.END, stats_text)

    stats_box.config(state="disabled")


# =========================================================
# EXPORT JSON
# =========================================================

def export_json():

    with open(JSON_FILE, "w") as file:

        json.dump(
            session_logs,
            file,
            indent=4
        )

    messagebox.showinfo(
        "Export Complete",
        f"Logs exported to {JSON_FILE}"
    )


# =========================================================
# EXPORT CSV
# =========================================================

def export_csv():

    with open(
        CSV_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Timestamp",
            "Key"
        ])

        for entry in session_logs:

            writer.writerow([
                entry["timestamp"],
                entry["key"]
            ])

    messagebox.showinfo(
        "Export Complete",
        f"Logs exported to {CSV_FILE}"
    )


# =========================================================
# CLEAR LOGS
# =========================================================

def clear_logs():

    display.delete(1.0, tk.END)

    stats_box.config(state="normal")
    stats_box.delete(1.0, tk.END)
    stats_box.config(state="disabled")

    session_logs.clear()
    key_count.clear()

    open(LOG_FILE, "w").close()

    messagebox.showinfo(
        "Logs Cleared",
        "All session logs removed"
    )


# =========================================================
# SAVE DISPLAY CONTENT
# =========================================================

def save_display():

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if file_path:

        content = display.get(
            1.0,
            tk.END
        )

        with open(file_path, "w") as file:
            file.write(content)

        messagebox.showinfo(
            "Saved",
            "Log file saved successfully"
        )


# =========================================================
# GUI SETUP
# =========================================================

root = tk.Tk()

root.title(
    "Advanced Keyboard Activity Monitor"
)

root.geometry("900x600")

title = tk.Label(
    root,
    text="Educational Keyboard Activity Monitor",
    font=("Arial", 18, "bold")
)

title.pack(pady=10)

info = tk.Label(
    root,
    text=(
        "This application logs keys ONLY "
        "inside this window."
    ),
    font=("Arial", 11)
)

info.pack()

# =========================================================
# DISPLAY AREA
# =========================================================

display = tk.Text(
    root,
    width=100,
    height=20
)

display.pack(pady=10)

# =========================================================
# STATISTICS BOX
# =========================================================

stats_box = tk.Text(
    root,
    width=40,
    height=5,
    state="disabled"
)

stats_box.pack(pady=5)

# =========================================================
# BUTTONS
# =========================================================

button_frame = tk.Frame(root)

button_frame.pack(pady=10)

save_btn = tk.Button(
    button_frame,
    text="Save TXT",
    command=save_display,
    width=15
)

save_btn.grid(row=0, column=0, padx=5)

json_btn = tk.Button(
    button_frame,
    text="Export JSON",
    command=export_json,
    width=15
)

json_btn.grid(row=0, column=1, padx=5)

csv_btn = tk.Button(
    button_frame,
    text="Export CSV",
    command=export_csv,
    width=15
)

csv_btn.grid(row=0, column=2, padx=5)

clear_btn = tk.Button(
    button_frame,
    text="Clear Logs",
    command=clear_logs,
    width=15
)

clear_btn.grid(row=0, column=3, padx=5)

# =========================================================
# KEY EVENT BINDING
# =========================================================

root.bind("<Key>", log_key)

# =========================================================
# START APPLICATION
# =========================================================

root.mainloop()