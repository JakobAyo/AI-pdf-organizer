
# AI-Invoice-Organizer
📋 Table of Contents

- [Setup](#Setup)
- [How to use the App](#how-to-use-the-app)

## Setup
### 1. Clone the Repository (Optional)

If you haven’t already, clone the repo:
```bash
git clone https://github.com/JakobAyo/AI-pdf-organizer.git
cd project
```
---

### 2. Run ```setup.bat``` (Installs Dependencies)

Double-click setup.bat or run it in Command Prompt:
```bash
setup.bat
```

This will:

Create a Python virtual environment (venv).

Install all required dependencies (pip install -r requirements.txt).

(If setup.bat fails, run it as Administrator.)

---
### 3. Get a Gemini API Key

Go to Google AI Studio (Gemini API).

Sign in and generate an API key.

Copy the key.

### 4. Paste the API Key in ```.env```

Open .env in a text editor (create one if missing).

Add your key like this:
plaintext

GEMINI_API_KEY=your-api-key-here

(Do not share this key!)

---

### 5. Run the Application

Start the app with:
```bash
python app.py
```

Follow any on-screen instructions.

---
# How to use the App
### 1. Select Invoices Folder
![Image](https://github.com/user-attachments/assets/c1bc8a9a-8d04-4489-adab-b6b837571607)
First click on the ```Select Invoices Folder``` Button

Browse and select the folder containing your PDF invoices

### 2. Generate Category Suggestions
![Image](https://github.com/user-attachments/assets/63bc0588-02f9-418f-b75a-de8b72d07ef1)
Click on the ```Suggest Categories``` Button

The App will:
- Process invoices in batches
- Send requests to the Gemini API
- Generate logical categories

When complete, click ```Continue``` to proceed

### 3. Review and Refine Categories
You'll see the AI-generated categories:
![Image](https://github.com/user-attachments/assets/825c8736-85a6-45aa-a53c-7befe296870f)

To improve results:
1. Select any unsatisfactory categories
2. Click ```Resuggest Categories```
    - The API will regenerate new categories to replace your selections

### 4. Organize Your Invoices
Click ```Organize Invoices``` to:
- Create new folders for each categorya
- Automatically move invoices to their appropriate folders

### 5. Use the Lookup Table
The system will open an advanced search interface:
![Image](https://github.com/user-attachments/assets/3a61207b-0edc-46a6-b4a1-1bbb9532b62e)

**Features include**:
- Multiple filter options
- Full-text search capabilities
- Quick navigation through organized invoices