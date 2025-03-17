import os
import tempfile
import zipfile
import shutil
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk


class ViewConvertEncodeDecode:
    def __init__(self, parent):
        self.parent = parent

        self.choose_files = tk.StringVar()
        self.choose_dir = tk.StringVar()
        self.encoding_from = tk.StringVar(value="utf-8")
        self.encoding_to = tk.StringVar(value="latin-1")

        self.window_title = tk.Label(
            self.parent, text="Encode/Decode", font=("Helvetica", 12, "bold")
        )
        self.window_title.pack(fill=tk.X)

        self.frame1 = tk.Frame(self.parent)
        self.frame1.pack(anchor=tk.W, padx=5, pady=2)

        self.csv_entry = tk.Entry(self.frame1, textvariable=self.choose_files, width=52)
        self.csv_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.bn_csv = tk.Button(
            self.frame1, text="Select files", command=self.sel_files
        )
        self.bn_csv.pack(side=tk.RIGHT, padx=5)

        self.frame2 = tk.Frame(self.parent)
        self.frame2.pack(anchor=tk.W, padx=5, pady=2)

        self.dir_entry = tk.Entry(self.frame2, textvariable=self.choose_dir, width=52)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.bn_dir = tk.Button(
            self.frame2, text="Select directory", command=self.sel_dir
        )
        self.bn_dir.pack(side=tk.RIGHT, padx=5)

        self.frame3 = tk.Frame(self.parent)
        self.frame3.pack(anchor=tk.W, padx=5, pady=5)

        tk.Label(self.frame3, text="From Encoding:").pack(side=tk.LEFT, padx=5)
        self.combo_from = ttk.Combobox(
            self.frame3,
            textvariable=self.encoding_from,
            values=["utf-8", "latin-1", "windows-1252", "ascii"],
            state="readonly",
            width=12,
        )
        self.combo_from.pack(side=tk.LEFT, padx=5)

        tk.Label(self.frame3, text="To Encoding:").pack(side=tk.LEFT, padx=5)
        self.combo_to = ttk.Combobox(
            self.frame3,
            textvariable=self.encoding_to,
            values=["utf-8", "latin-1", "windows-1252", "ascii"],
            state="readonly",
            width=12,
        )
        self.combo_to.pack(side=tk.LEFT, padx=5)

        self.bn_convert = tk.Button(self.frame3, text="Convert", command=self.convert)
        self.bn_convert.pack(side=tk.RIGHT, padx=5)

        self.frame4 = tk.Frame(self.parent)
        self.frame4.pack(anchor=tk.W, padx=5, pady=2)

        self.output = tk.StringVar()
        self.output_label = tk.Label(self.frame4, textvariable=self.output)
        self.output_label.pack(fill=tk.X, padx=5)

    def sel_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select one or more files",
            initialdir=os.path.expanduser("~"),
            filetypes=[
                ("All Files", "*.*"),
                ("TXT Files", "*.txt"),
                ("TXT Files", "*.srt"),
                ("CTX Files", "*.ctx"),
                ("ZIP Files", "*.zip"),
            ],
        )
        if file_paths:
            self.choose_files.set("; ".join(file_paths))

    def sel_dir(self):
        dir_path = filedialog.askdirectory(
            title="Select a directory", initialdir=os.path.expanduser("~")
        )
        if dir_path:
            self.choose_dir.set(dir_path)

    def extract_zip(self, zip_path):
        """Extracts a ZIP file to a temporary folder and returns the extracted files."""
        extract_dir = os.path.join(os.path.dirname(zip_path), "temp_extracted")
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        extracted_files = [
            os.path.join(extract_dir, f) for f in os.listdir(extract_dir)
        ]
        return extracted_files, extract_dir

    def create_zip(self, files, output_dir):
        """Creates a ZIP archive with all converted files."""
        zip_path = os.path.join(output_dir, "converted_files.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                zipf.write(file, os.path.basename(file))
        return zip_path

    def convert(self):
        selected_files = self.choose_files.get().split("; ")
        selected_dir = self.choose_dir.get()
        from_encoding = self.encoding_from.get()
        to_encoding = self.encoding_to.get()

        if not selected_files or selected_files == [""]:
            messagebox.showerror("Error", "No files selected!")
            return

        if not selected_dir:
            messagebox.showerror("Error", "No output directory selected!")
            return

        converted_files = []
        extracted_dirs = []

        temp_dir = tempfile.mkdtemp()

        for file_path in selected_files:
            if file_path.endswith(".zip"):
                extracted_files, extract_dir = self.extract_zip(file_path)
                extracted_dirs.append(extract_dir)
                selected_files.extend(extracted_files)
                continue

        for file_path in selected_files:
            if file_path.endswith(".zip"):
                continue

            try:
                with open(file_path, "r", encoding=from_encoding) as f:
                    content = f.read().lstrip("\ufeff")

                file_name = os.path.basename(file_path)
                output_path = os.path.join(temp_dir, file_name)

                with open(output_path, "w", encoding=to_encoding) as f:
                    f.write(content)

                converted_files.append(output_path)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert {file_path}: {e}")

        for extract_dir in extracted_dirs:
            shutil.rmtree(extract_dir)

        if converted_files:
            zip_path = self.create_zip(converted_files, selected_dir)

            shutil.rmtree(temp_dir)

            messagebox.showinfo("Success", f"Files converted and saved in:\n{zip_path}")
        else:
            messagebox.showwarning("Warning", "No files were converted.")
