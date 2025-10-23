# IS601 - Midterm Project: Python Calculator App

This is a command line Python calculator application that features a wide range of mathematical operations and automatically preserves the user's history with undo and redo functionality. 

# 🧮 Usage Guide
Here is the usage. Enter one of the operation keywords:

- `add`
- `subtract`
- `multiply`
- `divide`
- `power`
- `root`
- `modulus`
- `percentage`
- `int_division`
- `abs_diff`

Then enter the first number, followed by the second number. 

The Calculator preserves a history of the performed operations, and the user may undo and redo operations, which will be removed or re-added to the history. The calculator also has a dynamic help menu, which automatically adds new operations to the help menu once they've been added to the operations class. Beyond the operation commands, the other available commands are: 

- `history` - Show calculation history
- `clear` - Clear calculation history
- `undo` - Undo the last calculation
- `redo` - Redo the last undone calculation
- `save` - Save calculation history to file
- `load` - Load calculation history from file
- `help` - View the calculator documentation 
- `exit` - Exit the calculator

# 📦 Project Setup

---

# 🧩 Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```
---

# Running the Project

```bash
python main.py
```
--- 

# Configuration Setup
The application includes `.env` file for configuring the environment variables in the applicaton. The `.env.` file should include these parameters.

- Base Directories:

`CALCULATOR_LOG_DIR: Directory for log files.`
`CALCULATOR_HISTORY_DIR: Directory for history files.`

- History Settings:

`CALCULATOR_MAX_HISTORY_SIZE: Maximum number of history entries.`
`CALCULATOR_AUTO_SAVE: Whether to auto-save history (true or false).` 

- Calculation Settings:

`CALCULATOR_PRECISION: Number of decimal places for calculations.`
`CALCULATOR_MAX_INPUT_VALUE: Maximum allowed input value.`
`CALCULATOR_DEFAULT_ENCODING: Default encoding for file operations.`

--- 

# Testing Instructions 

The application includes testing suites for all of the classes and functions. You can run `pytest tests/ --cov=app --cov-report=term-missing` to observe the testing coverage for the app. 

--- 

# CI/CD Information

GitHub actions includes the workflow that tests the process of installing the necessary dependencies for the application and running pytest on its classes and functions. 

