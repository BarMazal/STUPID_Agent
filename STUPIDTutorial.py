import os
import sys

def clear_screen():
    # Helper to clear terminal screen for a clean, premium console experience
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("=" * 80)
    print(f" {title:^78} ")
    print("=" * 80)

def main_menu():
    clear_screen()
    print_header("🤖 Welcome to the STUPID Workspace Interactive Tutorial 🤖")
    print(
        "STUPID (Semantic Text Understanding & Paper Ingestion Dashboard)\n"
        "lets you explore and filter fields of interest (named 'Branches') in academic literature.\n\n"
        "This interactive tutorial collects your requirements to build a personalized\n"
        "step-by-step instruction guide for operating the workspace.\n"
    )
    print("Which path would you like to explore?")
    print("  [1] Adding a new field of interest (branch) to the pipeline")
    print("  [2] Configuring search keywords or semantic rules for an existing branch")
    print("  [3] Renaming an existing branch")
    print("  [4] Deleting a branch (and understanding backup archives)")
    print("  [5] Managing custom taxonomy categories")
    print("  [6] Resetting configuration to factory defaults")
    print("  [7] Daily crawling & ingestion sweeps (full vs limited)")
    print("  [8] Running specific pipeline components")
    print("  [9] Configuring search sites/sources (globally or branch-specific)")
    print("  [10] Visualizing paper attributes and metadata (--show_attributes)")
    print("  [Enter] Exit Tutorial")
    print("-" * 80)
    
    choice = input("⚡ Selection: ").strip()
    return choice

def path_add_branch():
    clear_screen()
    print_header("📍 PATH 1: ADDING A NEW FIELD OF INTEREST")
    print(
        "To start tracking new research subjects, you must define a 'Branch' in the system.\n"
        "You can configure this branch manually or let local AI assist you.\n"
    )
    print("How would you like to define your branch?")
    print("  [1] Manually define the branch name, keywords, and rules")
    print("  [2] Give a human language explanation using AI-assist")
    print("  [Enter] Go back to Main Menu")
    print("-" * 80)
    
    sub_choice = input("⚡ Selection: ").strip()
    if sub_choice == "1":
        clear_screen()
        print_header("🔧 MANUAL BRANCH CONFIGURATION")
        print("Please provide the details below (or press Enter for defaults):")
        
        branch_name = input("\n👉 Enter branch name (snake_case, e.g., deep_learning):\n 👉 ").strip().lower().replace(" ", "_")
        if not branch_name:
            branch_name = "new_research_branch"
            
        print("\nCrawler search keywords are used to scrape matching papers from ArXiv / DuckDuckGo.")
        keywords_str = input("👉 Enter crawler search phrases (comma-separated, e.g., neural networks, transformer models):\n 👉 ").strip()
        if not keywords_str:
            keywords_str = "neural networks, transformer models"
            
        print(
            "\nSemantic rules govern how the local AI Evaluator assesses paper relevance.\n"
            "Note: These do NOT have to be Boolean expressions! You can write plain prose describing what you want."
        )
        print("Example: \"I'm looking for a paper that achieves a significant jump in results of MOTA, but does use special HW or only one specific dataset.\"")
        semantic_rule = input("👉 Enter your semantic rule:\n 👉 ").strip()
        if not semantic_rule:
            semantic_rule = "I'm looking for papers discussing optimization techniques in deep neural networks."
            
        clear_screen()
        print_header("📋 YOUR PERSONALIZED WALKTHROUGH GUIDE (MANUAL PATH)")
        print(
            f"Here is your step-by-step roadmap to manually register and configure your brand new\n"
            f"'{branch_name}' research pipeline branch:\n"
        )
        print("So to achieve this, run the following command in your PowerShell terminal:")
        print("  👉 python STUPIDConsoleUI.py --configure")
        print("\nYou will see the Root Menu showing all active branches. Select the Add option:")
        print("  👉 Write: A")
        print(f"  👉 Then write: {branch_name}")
        print("\nYou will see the new branch registered in the list. Select it to edit:")
        print("  👉 Write: E <num>  (replace <num> with the index number of your new branch)")
        print("\nYou will see the branch edit submenu. For your choice of 'manual insertion', select search keywords:")
        print("  👉 Write: 1")
        print("  👉 Write: A  (to add a new phrase)")
        print("  👉 Write the crawling keywords you entered:")
        for kw in [k.strip() for k in keywords_str.split(",") if k.strip()]:
            print(f"     ➔ \"{kw}\"")
        print("  👉 Press Enter to go back up to the Edit Branch menu.")
        print("\nNow, select semantic requirement rules to set your NLP filters:")
        print("  👉 Write: 2")
        print("  👉 Write: A  (to add a new rule)")
        print("  👉 Write the custom semantic rule you entered:")
        print(f"     👉 \"{semantic_rule}\"")
        print("  👉 Press Enter to go back up to the Edit Branch menu.")
        print("\nFinally, go back to the root menu and run the processing pipeline:")
        print("  👉 Press Enter to return to the parent ROOT menu.")
        print("  👉 Write: E <num> (open the branch page again)")
        print("  👉 Write: 5  (Run Branch Pipeline)")
        print("  👉 Write: 1  (End-to-End Analysis: Crawl ➔ Extract ➔ Evaluate ➔ Visualize)")
        print("=" * 80)
        input("\n[Press Enter to return to main menu]")

    elif sub_choice == "2":
        clear_screen()
        print_header("🧠 AI-ASSISTED BRANCH CONFIGURATION")
        print(
            "AI-Assist lets you write a short summary of your research interest in natural language.\n"
            "The local AI model will autonomously design the branch schema for you.\n"
        )
        idea = input("👉 Describe your research idea or topic in plain English:\n 👉 ").strip()
        if not idea:
            idea = "I want to track papers about multi-object tracking utilizing vision-language models like CLIP."
            
        clear_screen()
        print_header("📋 YOUR PERSONALIZED WALKTHROUGH GUIDE (AI-ASSIST PATH)")
        print(
            "Here is the roadmap to automatically register your branch using natural language:\n"
        )
        print("So to achieve this, run the following command in your PowerShell terminal:")
        print("  👉 python STUPIDConsoleUI.py --configure")
        print("\nYou will see the ROOT VIEW. Select the AI Assist option:")
        print("  👉 Write: AI")
        print("\nYou will see the prompt: 'Describe your research vision, problem domain, or target concept'.")
        print("  👉 Paste your description:")
        print(f"     👉 \"{idea}\"")
        print("\nYou will see the local AI process your input and print an architectural decision summary.")
        print("It automatically designs a branch name, crawling search queries, and semantic requirements.")
        print("\nTo confirm and spawn the branch:")
        print("  👉 Write: y")
        print("  👉 The system will instantly register and commit the new branch to Configuration/targets_config.json!")
        print("=" * 80)
        input("\n[Press Enter to return to main menu]")

def path_configure_branch():
    clear_screen()
    print_header("📍 PATH 2: CONFIGURING AN EXISTING BRANCH")
    print(
        "You can configure keywords, rules, and sources for an active research branch.\n"
    )
    branch_name = input("👉 Enter the name of the branch to modify (e.g. object_tracking):\n 👉 ").strip().lower().replace(" ", "_")
    if not branch_name:
        branch_name = "object_tracking"
        
    keyword_update = input("\n👉 Enter a new keyword or rule you want to add (e.g. deep learning):\n 👉 ").strip()
    if not keyword_update:
        keyword_update = "deep learning"

    clear_screen()
    print_header(f"📋 YOUR PERSONALIZED WALKTHROUGH GUIDE (MODIFYING '{branch_name.upper()}')")
    print(
        f"Here is how to modify settings for the branch '{branch_name}':\n"
    )
    print("Step 1: Launch the configuration manager")
    print("   👉 python STUPIDConsoleUI.py --configure")
    print("\nStep 2: Enter the Edit Menu for this branch")
    print(f"   - Find the index number next to '{branch_name.upper()}' (e.g., let's say it is 1).")
    print("   - Type: E 1")
    print("\nStep 3: Modify crawler keywords")
    print("   - Type: 1  (List / Modify Search Keywords & Phrases)")
    print("   - Type: A  (Add Phrase)")
    print(f"   - Write: {keyword_update}")
    print("   - Press Enter to return to the edit menu.")
    print("\nStep 4: Modify semantic requirements")
    print("   - Type: 2  (List / Modify Semantic Requirement Logic Rules)")
    print("   - Type: A  (Add Rule)")
    print(f"   - Write: {keyword_update}")
    print("   - Press Enter to return to the edit menu.")
    print("\n🌐 NOTE ON TARGETED SOURCES:")
    print("   To configure search sites/sources for this branch specifically, select Option [6] (List / Modify Targeted Search Sites (Sources))")
    print("   inside the Edit Branch menu.")
    print("   For detailed guidelines, check option [9] on the main menu.")
    print("=" * 80)
    input("\n[Press Enter to return to main menu]")

def path_rename_branch():
    clear_screen()
    print_header("📍 PATH 3: RENAMING AN EXISTING BRANCH")
    old_name = input("👉 Enter the current branch name (e.g., ccd_sensors):\n 👉 ").strip().lower().replace(" ", "_")
    if not old_name:
        old_name = "ccd_sensors"
        
    new_name = input("👉 Enter the new name for this branch (e.g., multi_ccd_or_cmos_sensors):\n 👉 ").strip().lower().replace(" ", "_")
    if not new_name:
        new_name = "multi_ccd_or_cmos_sensors"

    clear_screen()
    print_header(f"📋 YOUR PERSONALIZED WALKTHROUGH GUIDE (RENAMING '{old_name.upper()}')")
    print(
        f"To safely rename your branch track from '{old_name}' to '{new_name}':\n"
    )
    print("Step 1: Launch the configuration manager")
    print("   👉 python STUPIDConsoleUI.py --configure")
    print("\nStep 2: Go to the edit menu")
    print(f"   - Find the index number next to '{old_name.upper()}' (e.g., let's say it is 3).")
    print("   - Type: E 3")
    print("\nStep 3: Rename the branch")
    print("   - Type: 3")
    print(f"   - When prompted, enter the new name: {new_name}")
    print("\n📦 WHAT HAPPENS UNDER THE HOOD:")
    print("   - The ledger 'Configuration/targets_config.json' is updated with the new name.")
    print(f"   - The active downloaded papers directory './downloaded_research/{old_name}' is automatically")
    print(f"     moved to a backup directory: './Archive/renamed_branches/{old_name}_renamed_to_{new_name}_[timestamp]'.")
    print(f"     This preserves your old evaluations and lets the system start a fresh directory loop.")
    print("=" * 80)
    input("\n[Press Enter to return to main menu]")

def path_delete_branch():
    clear_screen()
    print_header("📍 PATH 4: DELETING A BRANCH")
    branch_name = input("👉 Enter the name of the branch to delete:\n 👉 ").strip().lower().replace(" ", "_")
    if not branch_name:
        branch_name = "cooking_image_processing_analogy"

    clear_screen()
    print_header(f"📋 YOUR PERSONALIZED WALKTHROUGH GUIDE (DELETING '{branch_name.upper()}')")
    print(
        f"To erase '{branch_name}' from the active pipeline:\n"
    )
    print("Step 1: Launch the configuration manager")
    print("   👉 python STUPIDConsoleUI.py --configure")
    print("\nStep 2: Go to the edit menu")
    print(f"   - Find the index number next to '{branch_name.upper()}' (e.g., let's say it is 4).")
    print("   - Type: E 4")
    print("\nStep 3: Trigger wipe")
    print("   - Type: 4")
    print(f"   - Confirm the permanent wipe: y")
    print("\n📦 DATA ARCHIVE PROTECTION:")
    print(f"   - To prevent accidental deletion of your research, the active directory")
    print(f"     './downloaded_research/{branch_name}' is not deleted.")
    print(f"     It is moved to: './Archive/deleted_branches/{branch_name}_[timestamp]'.")
    print("=" * 80)
    input("\n[Press Enter to return to main menu]")

def path_manage_categories():
    clear_screen()
    print_header("📍 PATH 5: MANAGING CUSTOM TAXONOMY CATEGORIES")
    cat_label = input("👉 Enter display label for the new classification category (e.g., Hardware Target):\n 👉 ").strip()
    if not cat_label:
        cat_label = "Hardware Target"
        
    cat_key = input("👉 Enter category key in lowercase (e.g., hardware):\n 👉 ").strip().lower().replace(" ", "_")
    if not cat_key:
        cat_key = "hardware"
        
    cat_desc = input("👉 Enter category description for the AI filtering prompt:\n 👉 ").strip()
    if not cat_desc:
        cat_desc = "hardware targets such as FPGAs, GPUs, ASICs, or edge compute platforms"

    clear_screen()
    print_header("📋 YOUR PERSONALIZED WALKTHROUGH GUIDE (MANAGING TAXONOMY)")
    print(
        "To customize classification categories evaluated by the local AI:\n"
    )
    print("Step 1: Open Category Manager")
    print("   - Run: python STUPIDConsoleUI.py --configure")
    print("   - At the ROOT menu, type: M  (Manage Categories)")
    print("\nStep 2: Register a custom category")
    print("   - Type: A  (Add Custom Category)")
    print(f"   - Category key: {cat_key}")
    print(f"   - User-friendly label: {cat_label}")
    print(f"   - Description: {cat_desc}")
    print("\n💡 SYSTEM VS CUSTOM CATEGORIES:")
    print("   - System-wide categories (like 'Relevance' or 'Branch Lineage') are locked and cannot be deleted.")
    print("   - Custom categories can be deleted from the same menu by typing: D <num>.")
    print("=" * 80)
    input("\n[Press Enter to return to main menu]")

def path_factory_reset():
    clear_screen()
    print_header("📍 PATH 6: RESETTING CONFIGURATION TO FACTORY DEFAULTS")
    print(
        "To clear custom setups, restore default taxonomy categories (such as Publication Year\n"
        "and Research Institution), and start with an empty branch ledger:\n"
    )
    print("Step 1: Execute Factory Reset")
    print("   - Run: python STUPIDConsoleUI.py --configure")
    print("   - At the ROOT menu, type: F  (Reset Factory Settings)")
    print("   - Confirm the operation: y")
    print("\n⚠️ WARNING DETAILS:")
    print("   - This completely overwrites 'Configuration/targets_config.json' with original defaults.")
    print("   - Custom categories and all branches are wiped from the configuration ledger.")
    print("   - Local directories under './downloaded_research/' are left untouched to prevent data loss.")
    print("=" * 80)
    input("\n[Press Enter to return to main menu]")

def path_daily_crawling():
    clear_screen()
    print_header("📍 PATH 7: DAILY CRAWLING & INGESTION SWEEPS")
    print(
        "Ingestion sweeps fetch new scientific papers, extract their text content, run them\n"
        "through the local AI model for semantic evaluation, and open the tree browser.\n"
    )
    print("How would you like to run the daily sweep?")
    print("  [1] Full Ingestion Sweep (All new papers matching all branches)")
    print("  [2] Limited Ingestion Sweep (Cap the number of operations per pipeline block)")
    print("  [Enter] Go back to Main Menu")
    print("-" * 80)
    
    sub_choice = input("⚡ Selection: ").strip()
    if sub_choice == "1":
        clear_screen()
        print_header("📋 YOUR PERSONALIZED WALKTHROUGH GUIDE (FULL RUN)")
        print(
            "To run a complete pipeline sweep without going through the interactive menus:\n"
        )
        print("So to achieve this, run this shorthand command directly in your PowerShell terminal:")
        print("  👉 python STUPIDConsoleUI.py --run C,E,V,Z")
        print("\nYou will see the console log output for each step. Under the hood, this triggers:")
        print("   - [C] Crawler: Connects to online databases and downloads matching PDFs.")
        print("   - [E] Extractor: Converts all newly downloaded PDFs to structured plain text.")
        print("   - [V] Evaluator: Sends the text to the local LLM to assess your semantic rules.")
        print("   - [Z] Visualizer: Launches the interactive tree explorer UI.")
        print("=" * 80)
        input("\n[Press Enter to return to main menu]")
        
    elif sub_choice == "2":
        clear_screen()
        print_header("⚙️ LIMITED RUN Sweep Settings")
        limit_val = input("\n👉 Enter the maximum number of operations per block (e.g. 1 or 3):\n 👉 ").strip()
        if not limit_val.isdigit():
            limit_val = "3"
            
        clear_screen()
        print_header("📋 YOUR PERSONALIZED WALKTHROUGH GUIDE (LIMITED RUN)")
        print(
            f"To run the pipeline capped at a maximum of {limit_val} operations per block:\n"
        )
        print("So to achieve this, run this command in your PowerShell terminal:")
        print(f"  👉 python STUPIDConsoleUI.py --run C,E,V,Z --limit {limit_val}")
        print("\nYou will see the operations limited at each phase:")
        print(f"   - Crawler: Downloads a maximum of {limit_val} new papers per branch.")
        print(f"   - Extractor: Processes up to {limit_val} files (prioritizing this session's downloads first).")
        print(f"   - Evaluator: Evaluates up to {limit_val} documents using the local LLM.")
        print("=" * 80)
        input("\n[Press Enter to return to main menu]")

def path_specific_component():
    clear_screen()
    print_header("📍 PATH 8: RUNNING SPECIFIC PIPELINE COMPONENTS")
    print(
        "Sometimes you only want to run a single step of the pipeline. For example,\n"
        "if you manually copied PDFs to a folder and only want to run text extraction and AI evaluation.\n"
    )
    print("Which component would you like to run?")
    print("  [C] Crawler (Download files from the web)")
    print("  [E] Extractor (Convert PDFs to plain text)")
    print("  [V] Evaluator (AI Relevance and Taxonomy Tagging)")
    print("  [Z] Visualizer (Interactive Tree Browser)")
    print("  [Enter] Go back to Main Menu")
    print("-" * 80)
    
    comp_choice = input("⚡ Component selection: ").strip().upper()
    if comp_choice in ["C", "E", "V", "Z"]:
        comp_names = {
            "C": "Crawler",
            "E": "Extractor",
            "V": "Evaluator (AI Relevance)",
            "Z": "Visualizer (Tree Browser)"
        }
        
        clear_screen()
        print_header(f"📋 YOUR PERSONALIZED WALKTHROUGH GUIDE ({comp_names[comp_choice].upper()})")
        print(
            f"To run only the {comp_names[comp_choice]} component:\n"
        )
        print("So to achieve this, run this CLI command in your PowerShell terminal:")
        print(f"  👉 python STUPIDConsoleUI.py --run {comp_choice}")
        
        if comp_choice in ["V", "Z"]:
            print("\n⚠️  DATA INTEGRITY GUARDRAIL NOTE:")
            print("   If you have modified target configurations or added new branches, running")
            print("   a downstream component (like Evaluator or Visualizer) alone might cause incomplete")
            print("   or inconsistent data states. The UI will detect this configuration shift and show:")
            print("   '⚠️ CONFIGURATION CHANGE DETECTED'")
            print("   It will ask you if you'd like to perform a full run (C,E,V,Z) instead to stay safe.")
        print("=" * 80)
        input("\n[Press Enter to return to main menu]")

def path_configure_sources():
    clear_screen()
    print_header("📍 PATH 9: CONFIGURING SEARCH SITES/SOURCES")
    print(
        "The Crawler retrieves academic documents by querying search engines or databases.\n"
        "You can target specific domains globally or restrict them to a specific branch.\n"
    )
    print("Which source configuration path would you like to explore?")
    print("  [1] Add a target search site to a specific branch (Site-Scoped Crawls)")
    print("  [2] Configure global search sites (Used across all branches)")
    print("  [Enter] Go back to Main Menu")
    print("-" * 80)
    
    sub_choice = input("⚡ Selection: ").strip()
    if sub_choice == "1":
        clear_screen()
        print_header("🌐 BRANCH-SPECIFIC SOURCES CONFIGURATION")
        branch_name = input("👉 Enter branch name to configure (e.g. metalenses):\n 👉 ").strip().lower().replace(" ", "_")
        if not branch_name:
            branch_name = "metalenses"
            
        site_domain = input("👉 Enter the search site/domain you want to target (e.g. spie.org):\n 👉 ").strip().lower()
        if not site_domain:
            site_domain = "spie.org"
            
        clear_screen()
        print_header(f"📋 WALKTHROUGH: BRANCH SOURCES ('{branch_name.upper()}')")
        print(
            f"To restrict or extend searches for '{branch_name}' to the site '{site_domain}':\n"
        )
        print("Step 1: Launch the configuration manager")
        print("   👉 python STUPIDConsoleUI.py --configure")
        print("\nStep 2: Enter the Edit Menu for this branch")
        print(f"   - Find the index number next to '{branch_name.upper()}' (e.g., let's say it is 1).")
        print("   - Type: E 1")
        print("\nStep 3: Add targeted search site")
        print("   - Type: 6  (List / Modify Targeted Search Sites (Sources))")
        print("   - Type: A  (Add Source)")
        print(f"   - Write: {site_domain}")
        print("\n💡 HOW THE CRAWLER EXECUTES THIS UNDER THE HOOD:")
        print(f"   When running crawls for '{branch_name}':")
        print("   - If the source is 'arxiv', the Crawler targets the arXiv academic API.")
        print("   - If the source is 'duckduckgo', it searches the open web via DuckDuckGo.")
        print("   - If the source is 'imagesensors.org', it runs a custom scraper targeting past workshops.")
        print(f"   - For other sites (like '{site_domain}'), it automatically runs site-scoped DuckDuckGo scans:")
        print(f"     👉 Search Query: \"[your keyword] filetype:pdf site:{site_domain}\"")
        print("=" * 80)
        input("\n[Press Enter to return to main menu]")

    elif sub_choice == "2":
        clear_screen()
        print_header("🌐 GLOBAL SOURCES CONFIGURATION")
        global_site = input("👉 Enter global search site to add or remove (e.g. arxiv, duckduckgo, or spie.org):\n 👉 ").strip().lower()
        if not global_site:
            global_site = "arxiv"
            
        clear_screen()
        print_header("📋 WALKTHROUGH: GLOBAL SEARCH SITES")
        print(
            "Global search sites are queried for every active branch in the system.\n"
        )
        print("Step 1: Launch the configuration manager")
        print("   👉 python STUPIDConsoleUI.py --configure")
        print("\nStep 2: Open Global Sources Management")
        print("   - At the ROOT view, type: S  (Manage Global Sources)")
        print("\nStep 3: Manage your global sources")
        print("   - Type: A  (Add Global Source) and write the domain name, or")
        print("   - Type: D <num> (Delete Global Source) to remove a source.")
        print("\n💡 DESIGN PRINCIPLE:")
        print("   The Crawler scans the union of global sources and branch-specific sources.")
        print("   If 'arxiv' is listed in global_sources, arXiv will be crawled for all branches.")
        print("=" * 80)
        input("\n[Press Enter to return to main menu]")

def path_visualize_attributes():
    clear_screen()
    print_header("📍 PATH 10: VISUALIZING PAPER ATTRIBUTES AND METADATA")
    print(
        "By default, the Visualizer outputs the paper's title and short summary.\n"
        "You can enable the '--show_attributes' option to list all dynamic classification\n"
        "categories extracted during the pipeline and their parsed values on each card.\n"
    )
    print("How would you like to run the visualizer with attributes?")
    print("  [1] Through the console orchestrator (STUPIDConsoleUI.py)")
    print("  [2] Directly as a standalone visualizer tool (Engine/Visualizer.py)")
    print("  [Enter] Go back to Main Menu")
    print("-" * 80)
    
    sub_choice = input("⚡ Selection: ").strip()
    if sub_choice == "1":
        clear_screen()
        print_header("📋 WALKTHROUGH: ORCHESTRATOR VISUALIZATION WITH ATTRIBUTES")
        print(
            "To generate the literature tree containing detailed classification attributes:\n"
        )
        print("Run the console UI using the visualizer token 'Z' and '--show_attributes':")
        print("  👉 python STUPIDConsoleUI.py --run Z --show_attributes")
        print("\nNote: You can combine this flag with other pipeline steps too:")
        print("  👉 python STUPIDConsoleUI.py --run C,E,V,Z --show_attributes")
        print("\nThis will output the tree configuration to Visualizations/tree.html,")
        print("including a styled attributes card detailing Branch Lineage, Relevance,")
        print("and any custom taxonomy categories defined via the categories menu.")
        print("=" * 80)
        input("\n[Press Enter to return to main menu]")
    elif sub_choice == "2":
        clear_screen()
        print_header("📋 WALKTHROUGH: STANDALONE RUN WITH ATTRIBUTES")
        print(
            "To launch the visualizer independently, run it from the Engine/ directory:"
        )
        print("  👉 python Engine/Visualizer.py --show_attributes")
        print("\nThis will initialize the query tree loop and embed the detailed attributes")
        print("metadata dynamically inside the generated interactive HTML files.")
        print("=" * 80)
        input("\n[Press Enter to return to main menu]")


def run_tutorial():
    while True:
        choice = main_menu()
        if choice == "":
            print("\n👋 Thank you for using the STUPID Interactive Tutorial. Goodbye!\n")
            break
        elif choice == "1":
            path_add_branch()
        elif choice == "2":
            path_configure_branch()
        elif choice == "3":
            path_rename_branch()
        elif choice == "4":
            path_delete_branch()
        elif choice == "5":
            path_manage_categories()
        elif choice == "6":
            path_factory_reset()
        elif choice == "7":
            path_daily_crawling()
        elif choice == "8":
            path_specific_component()
        elif choice == "9":
            path_configure_sources()
        elif choice == "10":
            path_visualize_attributes()

if __name__ == "__main__":
    try:
        run_tutorial()
    except KeyboardInterrupt:
        print("\n\n👋 Tutorial interrupted. Goodbye!\n")
