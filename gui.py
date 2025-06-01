import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import db
from db import export_to_csv  # updated to accept file_path


class EmployWeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EmployWe Onboarding")
        self.geometry("950x500")
        self.configure(bg="#f0f2f5")
        db.connect_db()
        self.icon = None

        self.setup_widgets()

    def setup_widgets(self):
        # Add Employee Form
        form_frame = tk.LabelFrame(self, text="Add Employee", padx=10, pady=10, bg="#ffffff")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        tk.Label(form_frame, text="Username:", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(form_frame, width=25)
        self.username_entry.grid(row=0, column=1, pady=2)

        tk.Label(form_frame, text="Password:", bg="#ffffff").grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(form_frame, show="*", width=25)
        self.password_entry.grid(row=1, column=1, pady=2)

        tk.Label(form_frame, text="Email:", bg="#ffffff").grid(row=2, column=0, sticky="w")
        self.email_entry = tk.Entry(form_frame, width=25)
        self.email_entry.grid(row=2, column=1, pady=2)

        tk.Label(form_frame, text="Role:", bg="#ffffff").grid(row=3, column=0, sticky="w")
        self.role_entry = tk.Entry(form_frame, width=25)
        self.role_entry.grid(row=3, column=1, pady=2)

        self.submit_btn = tk.Button(form_frame, text=" Submit", command=self.add_employee, bg="#4caf50", fg="white")
        self.submit_btn.grid(row=4, column=0, pady=10)

        self.clear_btn = tk.Button(form_frame, text=" Clear", command=self.clear_form, bg="#9e9e9e", fg="white")
        self.clear_btn.grid(row=4, column=1)

        ToolTip(self.submit_btn, "Add employee to database")
        ToolTip(self.clear_btn, "Clear form fields")

        # View Employees Section
        table_frame = tk.LabelFrame(self, text="Employees", padx=10, pady=10, bg="#ffffff")
        table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        search_frame = tk.Frame(table_frame, bg="#ffffff")
        search_frame.grid(row=0, column=0, sticky="w", pady=(0, 10))

        tk.Label(search_frame, text="Search:", bg="#ffffff").grid(row=0, column=0)
        self.search_entry = tk.Entry(search_frame, width=25)
        self.search_entry.grid(row=0, column=1, padx=5)

        search_btn = tk.Button(search_frame, text="Search", command=self.search_employees, bg="#2196f3", fg="white")
        search_btn.grid(row=0, column=2)

        clear_btn = tk.Button(search_frame, text="Clear", command=self.load_employees, bg="#9e9e9e", fg="white")
        clear_btn.grid(row=0, column=3, padx=5)

        export_btn = tk.Button(search_frame, text="Export to CSV", command=self.export_to_csv, bg="#3f51b5", fg="white")
        export_btn.grid(row=0, column=4)

        ToolTip(search_btn, "Search by username, email, or role")
        ToolTip(clear_btn, "Clear search and reload")
        ToolTip(export_btn, "Export employee data to CSV")

        self.columns = ["id", "username", "email", "role"]
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col.title(), command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=150)

        self.tree.grid(row=1, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Status bar
        self.status_label = tk.Label(self, text="", bd=1, relief="sunken", anchor="w", bg="#eeeeee")
        self.status_label.grid(row=1, column=0, columnspan=2, sticky="we")

        self.load_employees()

    def set_status(self, message):
        self.status_label.config(text=message)

    def clear_form(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.role_entry.delete(0, tk.END)
        self.set_status("Form cleared.")

    def add_employee(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        email = self.email_entry.get().strip()
        role = self.role_entry.get().strip()

        if not all([username, password, email, role]):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            db.add_employee(username, password, email, role)
            self.set_status(f"Employee '{username}' added successfully.")
            self.clear_form()
            self.load_employees()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.set_status(str(e))

    def load_employees(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for emp in db.get_all_employees():
            self.tree.insert("", "end", values=emp)
        self.set_status("Employee list loaded.")

    def search_employees(self):
        keyword = self.search_entry.get().strip()
        results = db.search_employees(keyword)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for emp in results:
            self.tree.insert("", "end", values=emp)
        self.set_status(f"{len(results)} results found.")

    def sort_column(self, col, reverse):
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try:
            data.sort(key=lambda t: int(t[0]) if col == "id" else t[0].lower(), reverse=reverse)
        except Exception:
            data.sort(reverse=reverse)

        for i, (val, k) in enumerate(data):
            self.tree.move(k, "", i)

        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Employee Data As"
        )
        if not file_path:
            self.set_status("Export cancelled.")
            return

        try:
            export_to_csv(file_path)
            self.set_status(f"Employees exported to '{file_path}'.")
        except Exception as e:
            self.set_status(f"Export failed: {e}")


# Tooltip helper class
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, _):
        if self.tipwindow:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + cy + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "9", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, _):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


if __name__ == "__main__":
    app = EmployWeApp()
    app.mainloop()
