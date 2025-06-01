# EmployWe Onboarding App

**EmployWe** is a lightweight, user-friendly desktop application designed to help HR personnel and managers manage employee onboarding seamlessly. It allows you to add, view, search, sort, and export employee records with an intuitive graphical interface.

---

## 🧰 Features

- ✅ Add New Employees (with email and role)
- ✅ Password Hashing using bcrypt for security
- ✅ Email Validation and Duplicate Username Checks
- ✅ Real-time Search (by username, email, or role)
- ✅ Sortable Table Columns
- ✅ Export Employee List to CSV
- ✅ Status Bar Notifications
- ✅ Modernized Color Scheme
- ✅ Tooltips on Buttons for Better UX
- ✅ Built-in Local SQLite Database (No external setup needed)

---

## 🛠️ Technologies Used

| Technology     | Purpose                                |
|----------------|----------------------------------------|
| `Python 3`     | Main programming language              |
| `Tkinter`      | GUI framework for building the app     |
| `SQLite`       | Embedded database to store records     |
| `bcrypt`       | Secure password hashing                |
| `PIL (Pillow)` | Image processing for icon support      |
| `csv`          | Exporting data to CSV                  |
| `re`           | Regular expressions for email validation |

---

## 📦 Project Structure
employwe/

├── db.py # Handles database operations.

├── gui.py # Graphical user interface logic.

├── main.py # Application entry point.

├── employees_export.csv (generated on export).

├── icon.ico # App icon (optional).

├── README.md # Project documentation.

---

## 🚀 How to Run the App

### 1. Clone this Repository

```bash
git clone https://github.com/YourUsername/EmployWe.git
cd EmployWe
```

### 2. Install Dependencies
```
pip install bcrypt pillow
```
### 3. Run the Application
```
python main.py
```

---

## 🛠️ Build as Executable (Optional)
```
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

## 📄 License
  - This project is licensed under the MIT License

## 🙋‍♂️ Author
Joseph Maina

## 📸 Screenshot
![1](https://github.com/user-attachments/assets/afc23d3c-62a5-48bd-bd88-8cc5403cfb95)


## 🌐 Contributions

---

### ✅ What You Should Do Now:
1. Save this as `README.md` in your project folder.
2. Optionally add a screenshot in a `/screenshots` folder and reference it (or remove that section).
3. Commit & push:
```bash
git add README.md
git commit -m "Add detailed project README"
git push origin main

