# 📝 TailPad

**TailPad** is a lightweight, cross-platform log viewer and editor built with PyQt5. Designed for developers and testers who need to monitor and edit large or constantly updating text files — like `logs.txt` from long-running processes.

> Think of it as "Notepad with a tail -ing superpower."

---

## ✨ Features

- 📂 Open and edit plain text files  
- 🔁 Watch a file for live updates (like `tail -f`)  
- 🌙 Toggle between Light and Dark themes  
- 🔍 Adjustable font size (monospaced for better log viewing)  
- 💾 Save and "Save As" support  
- 📌 Auto-scrolls to the bottom on update (log-following mode)  
- 🪟 Native `.exe` and `.app` builds (see [Releases](#-downloads))  

---

## 🚀 Installation (Run from Source)

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/tailpad.git
cd tailpad
```

### 2. Install Dependencies

Make sure Python 3.7+ is installed, then:

```bash
pip install PyQt5
```

### 3. Run the App

```bash
python tailpad.py
```

> You’ll see a resizable notepad with a toolbar, file selection, watcher checkbox, font control, and theme toggle.

---

## 📦 Packaging Instructions

Use `pyinstaller` to generate standalone binaries:

```bash
pip install pyinstaller
```

### 🪟 Windows

```bash
pyinstaller tailpad.py --onefile --windowed --icon=logo.ico --add-data "logo.ico;."
```

### 🍎 macOS

```bash
pyinstaller tailpad.py --onefile --windowed --icon=logo.icns --add-data "logo.icns:."
```

Binaries will be available in the `dist/` folder.

---

## 📁 Folder Structure

```
tailpad/
├── tailpad.py          # Main application
├── logo.ico            # App icon for Windows
├── logo.icns           # App icon for macOS (optional)
├── dist/               # Contains generated .exe and .app
└── README.md
```

---

## 📥 Downloads

You can directly download ready-to-use binaries from the [`dist/`](./dist) folder:

- [TailPad for Windows (EXE)](./dist/TailPad.exe)
- [TailPad for macOS (APP)](./dist/TailPad.app)

> No installation required — just download and run.

---

## 🔧 Tips

- ✅ Ensure your log files are UTF-8 encoded for best results.  
- ⚠️ The Watcher checks for file changes every 5 seconds.  
- 📃 Use it for monitoring test logs, app output, Locust reports, and more.

---

## 🧑‍💻 Author

Developed by [Aakash](https://github.com/aakzsh)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
