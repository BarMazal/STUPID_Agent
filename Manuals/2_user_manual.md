# 📖 STUPID Unified User Manual: Configuration and Execution

Welcome to the **STUPID (Semantic Text Understanding & Paper Ingestion Dashboard)** master control workspace. This manual guides you through using the unified console UI to configure target branches, execute pipeline runs, and query indexed research trees.

---

## 🛠️ 1. Master Pipeline Shorthand Reference Table

When orchestrating tasks via the Command Line Interface (CLI) or the Interactive Wizard, use these capitalized single-character execution tokens:

| Token | Component Name | Underlying Script | Primary Core Responsibility |
| :---: | :--- | :--- | :--- |
| **`C`** | **Crawler** | `Engine/Crawler.py` | Harvests missing raw `.pdf` files from web, APIs, and targeted conferences. |
| **`E`** | **Extractor** | `Engine/Extractor.py` | Extracts full text from PDFs and builds three-file folder sidecar bundles. |
| **`V`** | **Evaluator** | `Engine/Evaluator.py` | Connects to local AI model to run Boolean logic and apply taxonomy tags. |
| **`S`** | **Selector** | `Engine/Selector.py` | Processes metadata tags recursively into tree arrays (Pure Data Layer). |
| **`Z`** | **Visualizer** | `Engine/Visualizer.py` | Launches interactive shell console to browse target tree nodes visually. |

---

## ⚙️ 2. Centralized Interactive Configuration Shell (`--configure`)

Modifying how the agent harvests or evaluates research is entirely data-driven and can be configured through the interactive loop. To launch it, run:
```powershell
.venv\Scripts\python.exe STUPIDConsoleUI.py --configure
```

### 🌎 2.1 Root View Options
When the console UI launches, you are in the **ROOT VIEW**. From here, you have the following controls:
*   **`[A] Add Branch`**: Spawn a brand new research branch track (e.g., `metalenses` or `ccd_sensors`).
*   **`[E <num>] Edit Branch`**: Select an existing branch to enter its nested submenu.
*   **`[M] Manage Categories`**: Manage dynamic taxonomy categories (e.g. `pub_year`, `institute`). You can add or delete custom categories. System-defined categories (`branch`, `relevant`) are locked and cannot be deleted.
*   **`[S] Manage Global Sources`**: Configure global search indices (such as `arxiv` or `duckduckgo`) queried universally by the Crawler.
*   **`[F] Reset Factory Settings`**: Restore default branches, global sources, default categories, and initial vocabularies (discarding custom configurations).

### 📂 2.2 Edit Branch Submenu
Within the Edit Branch menu, you can configure target branch parameters:
*   **`[1] Manage Search Phrases`**: List, add, update, or delete search query keywords used by the Crawler.
*   **`[2] Manage Semantic Requirements`**: Add, update, or delete Boolean rule strings (e.g., `(Multi-Object Tracking) AND (Fast GPU OR temporal embeddings)`) used by the AI Evaluator.
*   **`[3] Rename this Branch Track`**: Modifies the branch name in `targets_config.json`, bumps the branch criteria version, and archives the old folder to `./Archive/renamed_branches/<old_name>_renamed_to_<new_name>_<timestamp>`.
*   **`[4] Delete this Entire Branch Track`**: Removes the branch from the configuration ledger and archives its folder under `./Archive/deleted_branches/<branch_name>_<timestamp>`.

---

## 🚀 3. Executing the Processing Pipeline (`--run`)

You can execute the entire pipeline end-to-end or trigger specific stages.

### 📋 3.1 CLI Execution Examples
*   **Full End-to-End Run (Crawl ➔ Extract ➔ Evaluate ➔ Visualizer)**:
    ```powershell
    .venv\Scripts\python.exe STUPIDConsoleUI.py --run
    ```
*   **Crawl and Extract Text Only**:
    ```powershell
    .venv\Scripts\python.exe STUPIDConsoleUI.py --run C,E
    ```
*   **AI Evaluation Only**:
    ```powershell
    .venv\Scripts\python.exe STUPIDConsoleUI.py --run V
    ```
*   **Launch Visualizer Query Shell Directly**:
    ```powershell
    .venv\Scripts\python.exe STUPIDConsoleUI.py --run Z
    ```

### 🎛️ 3.2 Execution Option Flags
*   **`--limit [num]`**: Limits the number of documents processed per block stage. For example, `--run C,E,V --limit 2` will crawl up to 2 papers, extract up to 2 papers, and evaluate up to 2 papers.
*   **`--show_attributes`**: Enables printing dynamic category attributes (like Publication Year and Research Institution) under the paper cards inside the generated HTML tree view.
*   **`--interactive`**: Guides you through selecting pipeline stages step-by-step with natural prompt questions.

---

## 🔍 4. Interactive Visualizer Shell (`--run Z`)

The Visualizer creates a dynamic hierarchy retrieval console interface.

### 4.1 Step 1: Define Hierarchy Sequence
Enter a comma-separated list of active taxonomy keywords to group papers by (in order from parent to nested child).
*   **Available keywords**: `branch`, `relevant`, `pub_year`, `institute`, `innovation`, `methodology`, `distributed`
*   **Example Input**: `branch, pub_year, relevant`
*   **Upfront Help**: Type `help`, `h`, or `?` at the sequence prompt to view a guide explaining sequence syntax, active database branches, Boolean variables, and dynamic tag lists.

### 4.2 Step 2: Define Filter Conditions
You will be prompted to enter optional filters.
*   **Syntax**: Comma-separated equations of format `key=value` (applied using **AND** constraints).
*   **Example Input**: `relevant=true, branch=object_tracking`
*   **Default**: Press **Enter** to skip and visualize the entire collection.

### 4.3 Step 3: Browse Results
The program will:
1.  Partition your records recursively and output an indented tree structure to the terminal window.
2.  Compile and export a styled dark-glassmorphism HTML page to [Visualizations/tree.html](file:///c:/Projects/Agents/ArticleBrowser/Visualizations/tree.html) (representing the latest run), as well as a timestamped historical copy.
3.  Open the HTML file in your browser to inspect papers, read AI summaries, view attributes, and click links to open raw source `📕 PDF` files, processed `📝 TXT` drafts, or `⚙️ JSON` meta cards.
