# 🧜 Mermaid Studio

**A professional, real-time editor for creating, previewing, and exporting Mermaid.js diagrams.**

## 🚀 Overview

Mermaid Studio is a streamlined web application designed to simplify the creation of technical diagrams. By providing a side-by-side interface, users can write Mermaid syntax and see their flowcharts, sequence diagrams, and Gantt charts render instantly in a high-fidelity preview pane.

The project addresses the need for a persistent, local-first diagramming tool. Built with Streamlit, it manages a local library of diagrams, allowing users to save their progress automatically and return to their work at any time without losing data.

## ✨ Key Features

- ⚡ **Real-time Rendering**: Instant visual feedback as you type your Mermaid code using a high-performance integrated editor.
- 💾 **Auto-Save Storage**: A built-in JSON-based storage system that automatically preserves your titles and code changes.
- 🖼️ **Industrial Export**: Export your diagrams directly to high-resolution PNG files or copy them to your clipboard for use in reports and presentations.
- 🗂️ **Project Management**: A centralized dashboard to create, list, and manage multiple diagram projects seamlessly.
- 🎨 **Monokai Theme**: A polished, developer-friendly code editing experience powered by Streamlit Ace.

## 🛠️ Tech Stack

- **Frontend/Backend**: Streamlit
- **Editor**: Streamlit Ace (Monokai Theme)
- **Rendering Engine**: Mermaid.js (v10 via CDN)
- **Data Persistence**: JSON File System
- **Language**: Python 3.x

## 📦 Installation

Follow these steps to set up Mermaid Studio on your local machine:

**1. Clone the repository:**
```bash
git clone https://github.com/EF361/mermaid_editor.git
cd mermaid_editor

```

**2. Create and activate a virtual environment:**

*Windows:*

```bash
python -m venv venv
.\venv\Scripts\activate

```

*Mac/Linux:*

```bash
python3 -m venv venv
source venv/bin/activate

```

**3. Install dependencies:**

```bash
pip install -r requirements.txt

```

## 🏃‍♂️ How to Run

To launch the application, execute the following command in your terminal:

```bash
streamlit run app.py

```

Once running, you can access the application at:
`http://localhost:8501`

## 📖 Usage Guide

1. **Create a Diagram**: Click the **"➕ New"** button on the home dashboard to generate a new workspace.
2. **Edit Code**: Use the **Code** editor on the left to input your Mermaid syntax (e.g., `flowchart TD`).
3. **Preview & Refine**: Monitor the **Preview** pane on the right to see your changes update in real-time.
4. **Export Your Work**: Use the toolbar in the top-right of the preview window to download the diagram as a PNG or copy it to your clipboard.
5. **Manage Library**: Click the **"Back"** button to return to the dashboard and view your saved diagrams.

## 📂 Project Structure

```text
mermaid_editor/
├── app.py              # Main entry point and dashboard UI
├── components.py       # Custom Mermaid.js rendering component
├── storage.py          # Logic for JSON-based file persistence
├── requirements.txt    # Project dependencies
├── .gitignore          # Version control exclusion rules
├── diagrams/           # Local storage directory for saved JSON files
└── pages/
    └── editor.py       # Real-time editor and preview interface

```