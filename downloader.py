import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import sys

ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # "blue", "dark-blue", "green"

class ReelsDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Facebook Reels Downloader")
        self.geometry("800x600")
        self.resizable(True, True)

        # Header
        self.label = ctk.CTkLabel(self, text="Batch Download Facebook Reels", font=("Segoe UI", 20, "bold"))
        self.label.pack(pady=(20, 10))

        # Output folder
        self.folder_frame = ctk.CTkFrame(self)
        self.folder_frame.pack(fill="x", padx=30, pady=10)

        self.entry_folder = ctk.CTkEntry(self.folder_frame, placeholder_text="Output folder (optional)")
        self.entry_folder.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_browse = ctk.CTkButton(self.folder_frame, text="Browse", width=100, command=self.choose_folder)
        self.btn_browse.pack(side="right")

        # Info
        ctk.CTkLabel(self, text="Using links.txt in the current folder", text_color="gray").pack(pady=(0, 15))

        # Start button
        self.btn_start = ctk.CTkButton(self, text="START DOWNLOAD", width=300, height=50,
                                       font=("Segoe UI", 16, "bold"), command=self.start_download_thread)
        self.btn_start.pack(pady=10)

        # Log area
        self.text_log = ctk.CTkTextbox(self, height=300, font=("Consolas", 11))
        self.text_log.pack(padx=30, pady=10, fill="both", expand=True)

        # Footer - appearance switch
        self.switch_var = ctk.StringVar(value="System")
        self.switch = ctk.CTkSwitch(self, text="Dark / Light / System", variable=self.switch_var,
                                    onvalue="Dark", offvalue="Light", command=self.change_appearance)
        self.switch.pack(pady=10)

    def change_appearance(self):
        mode = self.switch_var.get()
        if mode == "System":
            ctk.set_appearance_mode("System")
        else:
            ctk.set_appearance_mode(mode)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_folder.delete(0, "end")
            self.entry_folder.insert(0, folder)

    def log(self, message):
        self.text_log.insert("end", message + "\n")
        self.text_log.see("end")
        self.update()

    def run_download(self):
        self.btn_start.configure(state="disabled")
        self.text_log.delete("1.0", "end")
        self.log("Starting batch download...\n")

        txt_file = "links.txt"
        if not os.path.isfile(txt_file):
            messagebox.showerror("Error", f"{txt_file} not found!")
            self.btn_start.configure(state="normal")
            return

        output_folder = self.entry_folder.get().strip()
        if output_folder:
            try:
                os.chdir(output_folder)
                self.log(f"Changed output directory to: {output_folder}")
            except Exception as e:
                self.log(f"Folder change failed: {e}")

        command = [
            "yt-dlp",
            "-a", txt_file,
            "-f", "bv*+ba/b",
            "--merge-output-format", "mp4",
            "-o", "%(title)s - %(id)s.%(ext)s",
            "--no-playlist",
            "--retries", "10",
            "--fragment-retries", "10"
        ]

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            for line in iter(process.stdout.readline, ''):
                self.log(line.strip())

            process.stdout.close()
            return_code = process.wait()

            if return_code == 0:
                self.log("\nSuccess ✓ All downloads finished.")
            else:
                self.log(f"\nFinished with error code {return_code}")

        except FileNotFoundError:
            self.log("Error: yt-dlp not found. Install it with: pip install yt-dlp")
        except Exception as e:
            self.log(f"Error: {str(e)}")

        finally:
            self.btn_start.configure(state="normal")

    def start_download_thread(self):
        threading.Thread(target=self.run_download, daemon=True).start()


if __name__ == "__main__":
    app = ReelsDownloader()
    app.mainloop()