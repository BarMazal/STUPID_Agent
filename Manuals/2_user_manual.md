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

### 🎛️ 3.1 All Command Line Flags Reference

The command-line interface supports the following arguments:

| Flag | Parameter | Description |
| :--- | :--- | :--- |
| **`--configure`** | None | Launches the interactive configuration loop to manage branches, search keywords, categories, and evaluation rules. |
| **`--run`** | Optional steps (e.g. `C,E`) | Executes the pipeline. Can specify a list of tokens (`C`,`E`,`V`,`S`,`Z`). If no components are specified, defaults to the entire pipeline (`C,E,V,Z`). |
| **`--interactive`** | None | Launches the step-by-step interactive orchestrator wizard (CLI questions instead of flags). |
| **`--limit`** | Integer (e.g. `10`) | Limits the number of operations per pipeline block (e.g., maximum crawled papers, text extractions, or evaluations). |
| **`--show_attributes`**| None | Include and display extracted attributes/categories (e.g. Year, Affiliation) under the paper cards inside the generated HTML tree view. |
| **`--silent`** | None | Runs the pipeline unattended without prompting (for overnight runs/automated tasks). Automatically bypasses integrity warnings and extends Ollama loading timeouts. |
| **`--visualize`** | String (e.g. `branch`) | Sets the default grouping sequence for the visualizer output when running in silent mode. |
| **`--min-year`** | Integer (e.g. `2026`) | Restricts paper crawling to publications from or after this year (applied to arXiv date filters and DuckDuckGo queries). |
| **`--filter`** | String (e.g. `israeli_involvement=Yes`) | Pre-applies filter conditions to visualizer records. Supports case-insensitive partial matching. |
| **`--no-combine-tags`**| None | Disables combined tag grouping (list-valued fields will duplicate papers under each tag rather than merging them into a compound name). |
| **`--branch`** | String (e.g. `bci_gaming`) | Restricts the pipeline execution only to this target branch. Prevents limits from applying to and downloading papers from other branches. |

---

### 📋 3.2 Main Workflow and Execution Examples

#### Flow A: Complete End-to-End Automated Overnight Sweep
Use this flow to run the pipeline unattended overnight. It downloads publications from 2026 onwards, runs AI evaluations, and builds the visualizer tree automatically:
```powershell
.venv\Scripts\python.exe STUPIDConsoleUI.py --run --silent --min-year 2026 --show_attributes --visualize branch,innovation,institute
```
*   **Result**: Zero human inputs required. Any Ollama timeout delays auto-extend. The final tree is written directly to `Visualizations/tree.html` and a timestamped copy, categorized by branch, innovation focus, and author institution.

#### Flow B: Skip Crawler (Resume / Local Processing)
If you have already downloaded PDF papers (or want to skip downloading fresh ones) and want to parse the text, run AI evaluations, and visualizer:
```powershell
.venv\Scripts\python.exe STUPIDConsoleUI.py --run E,V,Z --silent --show_attributes --visualize branch,innovation,institute
```
*   **Result**: Skips the crawler step (`C`), parsing any newly discovered PDFs in the storage root, runs LLM categorization, and renders the updated HTML tree view.

#### Flow C: Fast Targeted Crawl Only (Dry-Run / Scraping Limit)
To quickly ingest a limited set of papers after 2025 without triggering any extraction or local AI models:
```powershell
.venv\Scripts\python.exe STUPIDConsoleUI.py --run C --limit 3 --min-year 2026
```
*   **Result**: Downloads up to 3 papers matching branch criteria published from/after 2026, saving the raw PDFs inside `./downloaded_research/<branch_name>`.

#### Flow D: AI Evaluation Sweep Only
If you extracted several text files and want to trigger the offline LLM tagger:
```powershell
.venv\Scripts\python.exe STUPIDConsoleUI.py --run V --limit 5
```
*   **Result**: Evaluates up to 5 un-analyzed sidecars on disk.

#### Flow E: Silent HTML Tree Visualizer Update Only
To regenerate the HTML representation of current records on disk with custom grouping sequence without launching any prompt shell:
```powershell
.venv\Scripts\python.exe STUPIDConsoleUI.py --run Z --silent --show_attributes --visualize branch,relevant,pub_year
```

#### Flow F: Extracting and Filtering Israeli Associations Silently
To silently filter all papers to those involving Israeli organizations and output a clean visualizer tree:
```powershell
.venv\Scripts\python.exe STUPIDConsoleUI.py --run Z --silent --filter "israeli_involvement=Yes" --show_attributes
```

#### Flow G: Visualizing without Tag Combinations (Original Splitting Behavior)
To prevent categories from merging into a single sorted branch (like `"EEG, fMRI"`) and instead list the paper separately under each tag category:
```powershell
.venv\Scripts\python.exe STUPIDConsoleUI.py --run Z --silent --filter "israeli_involvement=Yes" --no-combine-tags --show_attributes
```

#### Flow H: Running a Full Ingestion Sweep Restricted to a Target Branch
To run the full pipeline (`C,E,V,Z`) only on a specific branch (e.g., `bci_gaming`) with a cap of 5 papers, preventing other branches from fetching or processing:
```powershell
.venv\Scripts\python.exe STUPIDConsoleUI.py --run C,E,V,Z --branch "bci_gaming" --limit 5 --show_attributes
```

---

## 🔍 4. Interactive Visualizer Shell (`--run Z`)

If running without `--silent`, the Visualizer launches an interactive hierarchy retrieval console.

### 4.1 Step 1: Define Hierarchy Sequence
Enter a comma-separated list of active taxonomy keywords to group papers by (in order from parent to nested child).
*   **Available keywords**: `branch`, `relevant`, `pub_year`, `institute`, `innovation`, `methodology`, `israeli_involvement`, `sectors`
*   **Example Input**: `branch, pub_year, relevant`
*   **Upfront Help**: Type `help`, `h`, or `?` at the sequence prompt to view a guide explaining sequence syntax, active database branches, Boolean variables, and dynamic tag lists.

### 4.2 Step 2: Define Filter Conditions
You will be prompted to enter optional filters.
*   **Syntax**: Comma-separated equations of format `key=value` (applied using **AND** constraints).
*   **Case-Insensitive Substring Match**: Filters are case-insensitive and match partial values or substrings.
    *   *Example*: `israeli_involvement=Yes` will match papers with metadata tags like `"Yes: Tel Aviv University"` or `"Yes: Sheba Medical Center"`.
    *   *Example*: `institute=Technion` will match `"Technion - Israel Institute of Technology"`.
*   **Available Filter Keys**: Any of the categories configured in `targets_config.json` (e.g., `branch`, `relevant`, `pub_year`, `institute`, `innovation`, `methodology`, `israeli_involvement`, `sectors`).
*   **Default**: Press **Enter** to skip (or use the CLI pre-set filter defined with `--filter`).
*   **Tag Grouping Behavior**: By default, list-valued fields (e.g. `methodology`, `innovation`) are grouped into a single merged category name (e.g. `"EEG, fMRI"`). If you run the command with the `--no-combine-tags` flag, papers are split and repeated under each tag bucket separately.

### 4.3 Step 3: Browse Results
The program will:
1.  Partition your records recursively and output an indented tree structure to the terminal window.
2.  Compile and export a styled dark-glassmorphism HTML page to [Visualizations/tree.html](file:///h:/projects/STUPID_Agent/Visualizations/tree.html) (representing the latest run), as well as a timestamped historical copy.
3.  Open the HTML file in your browser to inspect papers, read AI summaries, view attributes, and click links to open raw source `📕 PDF` files, processed `📝 TXT` drafts, or `⚙️ JSON` meta cards.

