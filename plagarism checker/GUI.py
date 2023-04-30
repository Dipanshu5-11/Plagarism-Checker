import csv
import tkinter as tk


def read_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


class CSVViewer:
    def __init__(self, csv_file, heading_text):
        self.csv_file = csv_file
        self.data = read_csv(csv_file)

        # Create the main frame
        self.main_frame = tk.Frame(root, bg='#f2f2f2', bd=2, relief=tk.GROOVE)
        self.main_frame.pack(padx=10, pady=10, side=tk.LEFT)

        # Create the heading
        heading = tk.Label(self.main_frame, text=heading_text, font='Helvetica 18 bold', bg='#f2f2f2')
        heading.pack()

        # Create the table frame
        self.table_frame = tk.Frame(self.main_frame, bg='#f2f2f2')
        self.table_frame.pack(padx=10, pady=10)

        # Create the table headers
        for col, header in enumerate(self.data[0]):
            header_label = tk.Label(self.table_frame, text=header, bg='#4d4d4d', fg='white', font='Helvetica 12 bold', padx=5, pady=5)
            header_label.grid(row=0, column=col, sticky='we')

        # Create the table rows
        for row, data in enumerate(self.data[1:], start=1):
            row_color = '#f2f2f2' if row % 2 == 0 else 'white'
            for col, cell in enumerate(data):
                cell_label = tk.Label(self.table_frame, text=cell, bg=row_color, font='Helvetica 12', padx=5, pady=5)
                cell_label.grid(row=row, column=col, sticky='we')

        # Configure column weights
        for col in range(len(self.data[0])):
            self.table_frame.columnconfigure(col, weight=1)

    def run(self):
        self.main_frame.mainloop()


# Create the main window
root = tk.Tk()
root.title('CSV Viewer')

# Create the CSV viewer objects for each file
csv_viewer1 = CSVViewer('plagiarism_results123.csv', 'Plagiarism Results')
csv_viewer2 = CSVViewer('grammar_errors123.csv', 'Grammar Errors')

# Pack the CSV viewer frames horizontally
csv_viewer1.main_frame.pack(side=tk.LEFT, padx=10, pady=10)
csv_viewer2.main_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Run the CSV viewers
csv_viewer1.run()
csv_viewer2.run()

# Run the main window
root.mainloop()
