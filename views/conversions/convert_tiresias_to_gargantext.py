import re
import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def segment_abstract(
    title, abstract, source, author, year, month, day, char_limit=2000
):
    min_chars = 1000
    max_chars = 4000
    char_limit = max(min_chars, min(char_limit, max_chars))

    abstract = abstract.replace("�", "").replace("", "").strip()
    if not abstract:
        return []

    segments = []
    start = 0
    count = 1

    while start < len(abstract):
        end = start + char_limit

        if end < len(abstract):
            match = re.search(r",\s", abstract[end:])
            if match:
                end += match.start() + 1
            else:
                end = min(start + max_chars, len(abstract))

        if end < len(abstract) and abstract[end - 1] == ",":
            end -= 1

        segment_text = abstract[start:end].strip()
        if segment_text:
            segment_title = (
                title
                if count == 1 and end >= len(abstract)
                else f"{title} : Part {count}"
            )
            segments.append(
                {
                    "PUBLICATION DAY": day,
                    "PUBLICATION MONTH": month,
                    "PUBLICATION YEAR": year,
                    "SOURCE": source,
                    "AUTHORS": author,
                    "TITLE": segment_title,
                    "ABSTRACT": segment_text,
                }
            )
            count += 1

        start = end

    return segments


class ViewConvertTiresiasToGargantext:
    def __init__(self, parent):
        self.parent = parent
        self.window_title = tk.Label(
            self.parent, text="Factiva to Gargantext", font=("Helvetica", 12, "bold")
        )
        self.window_title.pack(fill=tk.X)

        self.frame1 = tk.Frame(self.parent)
        self.frame1.pack(anchor=tk.W, padx=5, pady=2)

        self.csv_entry = tk.Entry(self.frame1, width=52)
        self.csv_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.bn_csv = tk.Button(
            self.frame1, text="Select files", command=self.sel_files
        )
        self.bn_csv.pack(side=tk.RIGHT, padx=5)

        self.frame2 = tk.Frame(self.parent)
        self.frame2.pack(anchor=tk.W, padx=5, pady=2)

        self.dir_entry = tk.Entry(self.frame2, width=52)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.bn_dir = tk.Button(
            self.frame2, text="Select directory", command=self.sel_dir
        )
        self.bn_dir.pack(side=tk.RIGHT, padx=5)

        self.frame3 = tk.Frame(self.parent)
        self.frame3.pack(anchor=tk.W, padx=5, pady=2)

        self.bn_convert = tk.Button(self.frame3, text="Convert", command=self.convert)
        self.bn_convert.pack(side=tk.RIGHT, padx=5)

        self.frame4 = tk.Frame(self.parent)
        self.frame4.pack(anchor=tk.W, padx=5, pady=2)

        self.char_limit_label = tk.Label(self.frame4, text="Number of characters:")
        self.char_limit_label.pack(side=tk.LEFT, padx=5)

        self.char_limit = tk.Entry(self.frame4, width=10)
        self.char_limit.insert(0, "1000")
        self.char_limit.pack(side=tk.LEFT, padx=5)

        self.char_limit.bind("<FocusOut>", self.validate_input)

        self.char_limit_unit = tk.Label(self.frame4, text="(between 1000 and 4000)")
        self.char_limit_unit.pack(side=tk.LEFT, padx=5)

        self.frame5 = tk.Frame(self.parent)
        self.frame5.pack(anchor=tk.W, padx=5, pady=2)

        self.progressbar = ttk.Progressbar(
            self.frame5, orient="horizontal", length=100, mode="determinate"
        )
        self.progressbar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.progress_label = tk.Label(self.frame5, text="0%")
        self.progress_label.pack(side=tk.RIGHT, padx=5)

    def validate_input(self, P):
        value = self.char_limit.get()

        try:
            value = int(value)
            if value < 1000 or value > 4000:
                raise ValueError("Value out of range")
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a number between 1000 and 4000.",
            )
            self.char_limit.delete(0, tk.END)
            self.char_limit.insert(0, "1000")

    def sel_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select one or more files",
            initialdir=os.path.expanduser("~"),
            filetypes=[("CSV Files", "*.csv")],
        )
        if file_paths:
            self.csv_entry.delete(0, tk.END)
            self.csv_entry.insert(0, "; ".join(file_paths))

    def sel_dir(self):
        dir_path = filedialog.askdirectory(
            title="Select a directory", initialdir=os.path.expanduser("~")
        )
        if dir_path:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, dir_path)

    def convert(self):
        file_paths = self.csv_entry.get()
        output_dir = self.dir_entry.get()
        char_limit = self.char_limit.get()

        if (
            not file_paths
            or not output_dir
            or not char_limit.isdigit()
            or int(char_limit) < 1
        ):
            messagebox.showerror(
                "Error", "Please select a file, directory, and valid number of parts!"
            )
            return

        char_limit = int(char_limit)
        file_paths = file_paths.split("; ")

        for i, file_path in enumerate(file_paths):
            try:
                with open(file_path, "r", encoding="utf8") as infile:
                    reader = csv.reader(infile, delimiter=";")
                    converted_data = []
                    next(reader)  # Skip header

                    for row in reader:
                        if len(row) > 1:
                            title = row[2].strip()
                            source = row[7].strip()
                            publication_info = row[6].strip()
                            abstract = row[14].strip()
                            authors = row[3].strip()

                            publication_parts = publication_info.split("/")
                            if len(publication_parts) == 3:
                                publication_year = publication_parts[2]
                                publication_month = publication_parts[1]
                                publication_day = publication_parts[0]
                            else:
                                publication_year = publication_month = (
                                    publication_day
                                ) = ""

                            segmented = segment_abstract(
                                title,
                                abstract,
                                source,
                                authors,
                                publication_year,
                                publication_month,
                                publication_day,
                                char_limit,
                            )
                            converted_data.extend(segmented)

                output_file = os.path.join(
                    output_dir,
                    f"gargantext_{os.path.basename(file_path).replace('.csv', '.tsv')}",
                )
                with open(output_file, "w", encoding="utf-8", newline="") as outfile:
                    fieldnames = [
                        "publication day",
                        "publication month",
                        "publication year",
                        "source",
                        "authors",
                        "title",
                        "abstract",
                    ]
                    writer = csv.DictWriter(
                        outfile,
                        fieldnames=[f.upper() for f in fieldnames],
                        delimiter="\t",
                    )
                    writer.writeheader()
                    for row in converted_data:
                        writer.writerow(row)

                progress = ((i + 1) / len(file_paths)) * 100
                self.progressbar["value"] = progress
                self.progress_label["text"] = f"{int(progress)}%"

                messagebox.showinfo(
                    "Success", f"Conversion complete! Saved to {output_file}"
                )

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                self.progressbar["value"] = 0
                self.progress_label["text"] = "0%"
