# 📖 STUPID Workspace Environment Bringup Manual

This manual provides detailed instructions to initialize the workspace environment, configure dependencies, and deploy the local AI model daemon after cloning the repository.

---

## 💻 1. System Requirements

*   **Operating System**: Windows 10/11 (PowerShell 5.1+ is required for the automated setup script).
*   **Python**: Python 3.10 or higher.
*   **Hardware**: Dedicated GPU (Nvidia recommended) to support the offline local AI model (`deepseek-r1:14b`).
*   **Network Ports**: Local port `11434` must be open and available for the Ollama server listener.

---

## ⚡ 2. Option A: Automated Bringup (Recommended)

An automated script [setup.ps1](file:///c:/Projects/Agents/ArticleBrowser/setup.ps1) is included at the root of the repository to automate environment creation and dependency setup on Windows.

### 🚀 Step-by-Step Execution
1. Open a **PowerShell** terminal window and navigate to the project directory:
   ```powershell
   cd c:\Projects\Agents\ArticleBrowser
   ```
2. Execute the setup script with the bypass policy:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\setup.ps1
   ```
3. **What the Script Accomplishes**:
   * **Python Check**: Verifies Python 3.10+ is active.
   * **Virtual Environment**: Dynamically creates a `.venv` directory if not present.
   * **Package Dependencies**: Installs and upgrades all Python packages listed in `requirements.txt`.
   * **Ollama Installation**: Checks if Ollama is installed. If missing, it downloads `OllamaSetup.exe` to a temporary directory, launches the installer, and cleans up the executable after completion.
   * **Ollama Service**: Ensures the background Ollama daemon is running.
   * **Model Download**: Automatically pulls the `deepseek-r1:14b` model locally.

---

## 🛠️ 3. Option B: Manual Bringup (Alternative)

If you prefer to configure the workspace step-by-step manually, run the following sequence:

### Step 1: Create and Activate Virtual Environment
Open a PowerShell terminal in the project directory:
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1
```

### Step 2: Install Package Dependencies
Upgrade pip and install all required python packages:
```powershell
# Upgrade package installer
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Install and Start Ollama
1. Download the Ollama for Windows installer from the official repository: `https://ollama.com`.
2. Run the setup wizard to install the Ollama application. This starts a background service daemon bound securely to local network port `11434`.

### Step 4: Pull AI Model Weights
Open a new terminal window and pull the required model:
```bash
ollama pull deepseek-r1:14b
```
To verify the model is pulled successfully:
```bash
ollama list
```

---

## 🔍 4. Verification and Connectivity Check
After finishing either bringup method, verify that python can communicate with the local AI engine. Run:
```powershell
.venv\Scripts\python.exe -c "import requests; print(requests.get('http://localhost:11434').text)"
```
Expected output:
```text
Ollama is running
```
