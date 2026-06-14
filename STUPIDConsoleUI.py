import os
import sys

# Reconfigure stdout/stderr error handling to ignore/replace non-encodable chars in non-UTF-8 terminals
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(errors='ignore')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(errors='ignore')
    except Exception:
        pass

# Inject Engine folder into Python path so that components can import each other
sys.path.append(os.path.join(os.path.dirname(__file__), 'Engine'))

from Configurator import ConfigurationLogicController
from Selector import HierarchicalQueryEngine
from ArticlesAgent import GrandMasterOrchestrator

class HierarchicalConsoleUI:
    def __init__(self, limit=None, show_attributes=False, filter_str="", combine_tags=True):
        self.configurator = ConfigurationLogicController()
        self.selector = HierarchicalQueryEngine(combine_tags=combine_tags)
        self.current_state = "TOP"
        self.active_branch_context = None
        self.limit = limit
        self.show_attributes = show_attributes
        self.filter_str = filter_str
        self.combine_tags = combine_tags

    def run_master_loop(self):
        """The core central switchboard driver loop handling nested navigational menu panels."""
        print("🤖 Welcome to the Collaborative STUPID Intelligent Workspace Shell 🤖")
        print("=" * 80)
        while True:
            if self.current_state == "TOP": 
                self._handle_top_state()
            elif self.current_state == "EditBranch": 
                self._handle_edit_branch_state()
            elif self.current_state == "ListKP": 
                self._handle_list_kp_state()
            elif self.current_state == "ListSem": 
                self._handle_list_sem_state()
            elif self.current_state == "ListSrc":
                self._handle_list_src_state()
            elif self.current_state == "EXIT": 
                break

    # =====================================================================
    # 🎛️ STATE PANEL 1: ROOT VIEW
    # =====================================================================
    def _handle_top_state(self):
        branches = self.configurator.get_all_branches()
        print(f"\n📍 LOCATION: ROOT VIEW ({len(branches)} Branches Active)")
        print("-" * 60)
        for idx, b in enumerate(branches):
            print(f"  [{idx + 1}] Branch: {b['name'].upper()} (v{b['criteria_version']})")
        print("\n📝 COMMANDS: [A] Add Branch | [E <num>] Edit Branch | [M] Manage Categories | [S] Manage Global Sources | [F] Reset Factory Settings | [AI] AI Assist | [H] Help | [Enter] Exit")
        
        cmd = input("\n⚡ Operational choice: ").strip()
        if cmd.lower() == 's':
            self._handle_manage_global_sources()
            return
        elif cmd == "":
            self.current_state = "EXIT"
            return
            
        if cmd.lower() == 'h':
            self._print_root_help()
            return
            
        if cmd.lower() == 'ai':
            idea = input("\n💡 Describe your research vision, problem domain, or target concept:\n 👉 ")
            res = self.configurator.generate_assist_suggestions("ROOT_STRATEGY", idea)
            strategy = res.get("recommended_strategy", "CREATE_NEW")
            
            if "halted" in res.get("architectural_rationale", "").lower():
                print("❌ Configuration generation aborted.")
                return

            print(f"\n📊 ARCHITECTURAL DECISION: Strategy Chosen ➔ [{strategy}]")
            print(f"   └─ Rationale: {res.get('architectural_rationale')}")
            print(f"   └─ Target Rule Generated: \"{res.get('suggested_semantic_rule')}\"")
            print(f"   └─ Target Crawler Keywords: {res.get('suggested_phrases')}")
            
            if strategy == "ENHANCE":
                target_b = res.get("target_branch_name", "")
                adopt = input(f"Option: Merge new keywords and update rule for [{target_b.upper()}]? (y/N): ")
                if adopt.lower().strip() == 'y':
                    self.configurator.commit_requirement(target_b, res.get('suggested_semantic_rule', ''))
                    for phrase in res.get('suggested_phrases', []):
                        self.configurator.commit_phrase(target_b, phrase)
                    print(f"✅ Branch [{target_b.upper()}] expanded successfully.")
            else:
                suggested_name = res.get("suggested_branch_name", "new_research_track")
                adopt = input(f"Option: Spawn brand new pipeline lane named '{suggested_name}'? (y/N): ")
                if adopt.lower().strip() == 'y':
                    self.configurator.commit_new_branch(suggested_name, res.get('suggested_semantic_rule', ''))
                    for phrase in res.get('suggested_phrases', []):
                        self.configurator.commit_phrase(suggested_name, phrase)
                    print(f"🚀 Research lane [{suggested_name.upper()}] spawned!")

        elif cmd.lower() == 'a':
            name = input(" 👉 Enter new branch name: ")
            if name.strip():
                self.configurator.commit_new_branch(name)
                print("✨ Branch committed.")
        elif cmd.lower().startswith('e '):
            try:
                idx = int(cmd.split(' ')[-1]) - 1
                if 0 <= idx < len(branches):
                    self.active_branch_context = branches[idx]["name"]
                    self.current_state = "EditBranch"
            except Exception: 
                print("❌ Invalid choice index.")
        elif cmd.lower() == 'm':
            self._handle_manage_categories()
        elif cmd.lower() == 'f':
            confirm = input("\n🤔 Are you sure you want to reset all configurations (branches, categories, vocabularies) to factory defaults? (y/N): ").strip().lower()
            if confirm == 'y':
                self.configurator.reset_to_factory_settings()
                print("✅ System reset to factory defaults successfully.")

    def _handle_manage_categories(self):
        while True:
            cats = self.configurator.get_categories()
            print(f"\n📍 LOCATION: ROOT ➔ CATEGORY MANAGEMENT")
            print("-" * 60)
            print("Active Taxonomy Categories:")
            for idx, cat in enumerate(cats):
                source_label = "System" if cat.get("source") == "system" else "Custom/AI"
                desc = cat.get("description", "No description provided.")
                print(f"  [{idx + 1}] {cat['label']} (Key: {cat['key']}, Type: {source_label})")
                print(f"      └─ Path: {' ➔ '.join(cat['path'])} | Description: {desc}")
            print("\n📝 COMMANDS: [A] Add Custom Category | [D <num>] Delete Custom Category | [Enter] Go Back")
            
            choice = input("\n⚡ Selection: ").strip()
            if choice == "":
                break
            if choice.lower() == 'a':
                key = input("👉 Enter new category key (lowercase, e.g. hardware): ").strip()
                if not key:
                    print("❌ Category key cannot be empty.")
                    continue
                label = input("👉 Enter user-friendly display label (e.g. Hardware Target): ").strip()
                if not label:
                    print("❌ Display label cannot be empty.")
                    continue
                desc = input("👉 Enter description for the AI filtering prompt: ").strip()
                if self.configurator.add_custom_category(key, label, desc):
                    print(f"✅ Custom category '{label}' added successfully.")
                else:
                    print(f"❌ Failed to add category. Key might already exist.")
            elif choice.lower().startswith('d '):
                try:
                    idx = int(choice.split(' ')[-1]) - 1
                    if 0 <= idx < len(cats):
                        cat = cats[idx]
                        if cat.get("source") == "system":
                            print("❌ System categories cannot be deleted.")
                        else:
                            confirm = input(f"🤔 Are you sure you want to delete category '{cat['label']}'? (y/N): ").strip().lower()
                            if confirm == 'y':
                                if self.configurator.remove_custom_category(cat['key']):
                                    print(f"✅ Category '{cat['label']}' removed.")
                                else:
                                    print("❌ Failed to remove category.")
                    else:
                        print("❌ Invalid category index.")
                except Exception:
                    print("❌ Invalid command format.")

    def _handle_run_pipeline(self, branch_name):
        print(f"\n🚀 PIPELINE RUNNER SWITCHBOARD FOR BRANCH: [{branch_name.upper()}]")
        print("-" * 60)
        print("  [1] End-to-End Analysis (Crawl ➔ Extract ➔ AI Evaluate ➔ Visualizer) [C,E,V,Z]")
        print("  [2] Crawl Only (Sync new papers from web/conferences) [C]")
        print("  [3] Text Extraction Only (Convert downloaded PDFs to text) [E]")
        print("  [4] AI Evaluation Only (Apply/update semantic tags using local LLM) [V]")
        print("  [5] Interactive Tree Visualizer Only (Browse/query tagged documents) [Z]")
        print("  [6] Custom Steps (Manually enter comma-separated sequence, e.g. C,E,V)")
        print("  [Enter] Return to Main Menu")
        
        choice = input("\n⚡ Selection: ").strip()
        if not choice:
            return
            
        steps = []
        if choice == '1':
            steps = ["C", "E", "V", "Z"]
        elif choice == '2':
            steps = ["C"]
        elif choice == '3':
            steps = ["E"]
        elif choice == '4':
            steps = ["V"]
        elif choice == '5':
            steps = ["Z"]
        elif choice == '6':
            custom = input("👉 Enter pipeline tokens (C, E, V, S, Z): ").strip()
            steps = [s.strip().upper() for s in custom.split(",") if s.strip()]
        else:
            print("❌ Invalid selection.")
            return

        if not steps:
            return

        limit = self.limit
        is_data_run = any(step in ["C", "E", "V"] for step in steps)
        if limit is None and is_data_run:
            limit_prompt = input("👉 Limit operations per block (integer, or press Enter for no limit): ").strip()
            limit = int(limit_prompt) if limit_prompt.isdigit() else None

        try:
            orchestrator = GrandMasterOrchestrator()
            orchestrator.config_path = self.configurator.config_path
            orchestrator.storage_root = self.selector.storage_root
            orchestrator.run_pipeline(steps, target_branch=branch_name, limit=limit, show_attributes=self.show_attributes, filter_str=self.filter_str, combine_tags=self.combine_tags)
        except Exception as e:
            print(f"❌ Error during pipeline execution: {e}")

    # =====================================================================
    # 🎛️ STATE PANEL 2: EDIT BRANCH MANAGER
    # =====================================================================
    def _handle_edit_branch_state(self):
        b = self.configurator.get_branch_by_name(self.active_branch_context)
        if not b: 
            self.current_state = "TOP"
            return
        print(f"\n📍 LOCATION: ROOT ➔ [{b['name'].upper()}]")
        print("-" * 60)
        print("  [1] List / Modify Search Keywords & Phrases")
        print("  [2] List / Modify Semantic Requirement Logic Rules")
        print("  [3] Rename this Branch Track")
        print("  [4] Delete this Entire Branch Pipeline Track")
        print("  [5] Run Branch Pipeline")
        print("  [6] List / Modify Targeted Search Sites (Sources)")
        print("  [H] Help / Examples")
        print("  [Enter] Go back up to Parent Root Menu")
        
        choice = input("\n⚡ Selection: ").strip()
        if choice == "":
            self.current_state = "TOP"
            self.active_branch_context = None
            return
            
        if choice == "1": 
            self.current_state = "ListKP"
        elif choice == "2": 
            self.current_state = "ListSem"
        elif choice == "6":
            self.current_state = "ListSrc"
        elif choice == "3":
            new_name = input(" 👉 Enter new name for this branch: ").strip().lower().replace(" ", "_")
            if new_name:
                if self.configurator.rename_branch(b['name'], new_name):
                    print(f"✅ Branch successfully renamed to '{new_name}'.")
                    self.active_branch_context = new_name
                else:
                    print("❌ Collision error: A branch with that name already exists.")
            else:
                print("❌ Name cannot be empty.")
        elif choice == "4":
            if input(f"💥 Permanent wipe [{b['name'].upper()}]? (y/N): ").lower() == 'y':
                self.configurator.delete_branch_by_name(b['name'])
                self.current_state = "TOP"
                self.active_branch_context = None
        elif choice == "5":
            self._handle_run_pipeline(b['name'])
        elif choice.lower() == "h":
            self._print_edit_branch_help(b['name'])

    # =====================================================================
    # 🎛️ STATE PANEL 3: KEYWORDS & PHRASES LIST
    # =====================================================================
    def _handle_list_kp_state(self):
        b = self.configurator.get_branch_by_name(self.active_branch_context)
        phrases = b.get("search_phrases", [])
        print(f"\n📍 LOCATION: ROOT ➔ [{b['name'].upper()}] ➔ CRAWL PHRASES")
        print("-" * 60)
        for idx, p in enumerate(phrases): 
            print(f"  [{idx + 1}] String: \"{p}\"")
        print("\n📝 COMMANDS: [A] Add Phrase | [U <num>] Update | [D <num>] Delete | [AI] AI Assist | [H] Help | [Enter] Go Up")
        
        cmd = input("\n⚡ Selection: ").strip()
        if cmd == "":
            self.current_state = "EditBranch"
            return
            
        if cmd.lower() == 'a':
            phrase = input(" 👉 Enter search string: ").strip()
            if phrase:
                self.configurator.commit_phrase(b['name'], phrase)
                print("✅ Added.")
        elif cmd.lower().startswith('u '):
            try:
                idx = int(cmd.split(' ')[-1]) - 1
                if 0 <= idx < len(phrases):
                    old_phrase = phrases[idx]
                    new_phrase = input(f" 👉 Enter replacement string for \"{old_phrase}\": ").strip()
                    if new_phrase:
                        self.configurator.update_phrase(b['name'], old_phrase, new_phrase)
                        print("✅ Keyword phrase updated.")
                else:
                    print("❌ Index out of range.")
            except Exception:
                print("❌ Invalid command parameter.")
        elif cmd.lower().startswith('d '):
            try:
                idx = int(cmd.split(' ')[-1]) - 1
                if 0 <= idx < len(phrases):
                    phrase_to_del = phrases[idx]
                    self.configurator.delete_phrase(b['name'], phrase_to_del)
                    print(f"✅ Deleted phrase: \"{phrase_to_del}\"")
                else:
                    print("❌ Index out of range.")
            except Exception:
                print("❌ Invalid command parameter.")
        elif cmd.lower() == 'ai':
            idea = input("\n💡 What specific angle are you hunting for on the web?\n 👉 ")
            res = self.configurator.generate_assist_suggestions("KEYWORDS", idea)
            print(f"\n✨ Isolated Keyword Suggestions: {res.get('suggested_phrases')}")
            for p in res.get('suggested_phrases', []):
                if input(f"   ➕ Map phrase '{p}' to crawler? (Y/n): ").lower() != 'n':
                    self.configurator.commit_phrase(b['name'], p)
                    print("✅ Added phrase.")
        elif cmd.lower() == 'h':
            self._print_keywords_help()

    # =====================================================================
    # 🎛️ STATE PANEL 4: SEMANTIC RULES VIEW
    # =====================================================================
    def _handle_list_sem_state(self):
        b = self.configurator.get_branch_by_name(self.active_branch_context)
        reqs = self.configurator.get_semantic_requirements(b['name'])
        print(f"\n📍 LOCATION: ROOT ➔ [{b['name'].upper()}] ➔ SEMANTIC RULES")
        print("-" * 60)
        for idx, r in enumerate(reqs):
            print(f"  [{idx + 1}] Rule: \"{r}\"")
        print("\n📝 COMMANDS: [A] Add Rule | [U <num>] Update | [D <num>] Delete | [AI] AI Assist | [S] AI Suggest Rule | [H] Help | [Enter] Go Up")
        
        cmd = input("\n⚡ Selection: ").strip()
        if cmd == "":
            self.current_state = "EditBranch"
            return
            
        if cmd.lower() == 'a':
            rule = input(" 👉 Enter new semantic rule: ").strip()
            if rule:
                self.configurator.add_semantic_requirement(b['name'], rule)
                print("✅ Semantic rule added.")
        elif cmd.lower().startswith('u '):
            try:
                idx = int(cmd.split(' ')[-1]) - 1
                if 0 <= idx < len(reqs):
                    old_rule = reqs[idx]
                    new_rule = input(f" 👉 Enter replacement rule: ").strip()
                    if new_rule:
                        self.configurator.update_semantic_requirement(b['name'], idx, new_rule)
                        print("✅ Rule updated.")
                else:
                    print("❌ Index out of range.")
            except Exception:
                print("❌ Invalid command parameter.")
        elif cmd.lower().startswith('d '):
            try:
                idx = int(cmd.split(' ')[-1]) - 1
                if 0 <= idx < len(reqs):
                    self.configurator.delete_semantic_requirement(b['name'], idx)
                    print("✅ Rule deleted.")
                else:
                    print("❌ Index out of range.")
            except Exception:
                print("❌ Invalid command parameter.")
        elif cmd.lower() == 'ai':
            idea = input("\n💡 Describe your filtering or selection rules in plain language:\n 👉 ")
            res = self.configurator.generate_assist_suggestions("SEMANTIC_RULE", idea)
            rule = res.get('suggested_semantic_rule')
            print(f"\n✨ Suggested Rule Expression: \"{rule}\"")
            if input(" ➕ Map this rule to active branch requirements? (Y/n): ").lower() != 'n':
                self.configurator.add_semantic_requirement(b['name'], rule)
                print("✅ Rule added.")
        elif cmd.lower() == 's':
            phrases = b.get("search_phrases", [])
            existing_rules = reqs
            article_snippets = []
            branch_dir = os.path.join("./downloaded_research", b['name'])
            if os.path.exists(branch_dir) and os.path.isdir(branch_dir):
                files = [f for f in os.listdir(branch_dir) if f.endswith("_meta.json")]
                for f in files[:5]:
                    try:
                        with open(os.path.join(branch_dir, f), "r", encoding="utf-8") as file:
                            card = json.load(file)
                            title = card.get("document_title", "")
                            summary = card.get("agent_relevance_eval", {}).get("reasoning_summary", "")
                            if title:
                                article_snippets.append(f"Title: {title} | AI Summary: {summary}")
                    except Exception:
                        pass
            
            print("\n💡 Consulting AI Architect to formulate a complementary semantic rule based on branch context...")
            res = self.configurator.generate_semantic_rule_suggestion(b['name'], phrases, existing_rules, article_snippets)
            rule = res.get('suggested_semantic_rule')
            rationale = res.get('architectural_rationale', 'No rationale provided.')
            if rule:
                print(f"\n💡 AI RATIONALE: {rationale}")
                print(f"✨ Suggested Rule Expression: \"{rule}\"")
                if input(" ➕ Map this rule to active branch requirements? (Y/n): ").lower() != 'n':
                    self.configurator.add_semantic_requirement(b['name'], rule)
                    print("✅ Rule added.")
            else:
                print("❌ Failed to get suggestions from local AI model.")
        elif cmd.lower() == 'h':
            self._print_semantic_rules_help()

    def _handle_manage_global_sources(self):
        while True:
            sources = self.configurator.get_global_sources()
            print(f"\n📍 LOCATION: ROOT ➔ GLOBAL SOURCES")
            print("-" * 60)
            print("Active Global Ingestion Sources:")
            for idx, src in enumerate(sources):
                print(f"  [{idx + 1}] Site/Domain: {src}")
            print("\n📝 COMMANDS: [A] Add Global Source | [D <num>] Delete Global Source | [Enter] Go Back")
            
            choice = input("\n⚡ Selection: ").strip()
            if choice == "":
                break
            if choice.lower() == 'a':
                source = input("👉 Enter new global search site/domain (e.g. spie.org): ").strip().lower()
                if not source:
                    print("❌ Source name cannot be empty.")
                    continue
                if self.configurator.add_global_source(source):
                    print(f"✅ Global source '{source}' added successfully.")
                else:
                    print(f"❌ Global source '{source}' already exists.")
            elif choice.lower().startswith('d '):
                try:
                    idx = int(choice.split(' ')[-1]) - 1
                    if 0 <= idx < len(sources):
                        source_to_del = sources[idx]
                        confirm = input(f"🤔 Are you sure you want to delete global source '{source_to_del}'? (y/N): ").strip().lower()
                        if confirm == 'y':
                            if self.configurator.remove_global_source(source_to_del):
                                print(f"✅ Global source '{source_to_del}' removed.")
                            else:
                                print("❌ Failed to remove global source.")
                    else:
                        print("❌ Invalid source index.")
                except Exception:
                    print("❌ Invalid command format.")

    def _handle_list_src_state(self):
        b = self.configurator.get_branch_by_name(self.active_branch_context)
        sources = b.get("sources", [])
        print(f"\n📍 LOCATION: ROOT ➔ [{b['name'].upper()}] ➔ TARGETED SOURCES")
        print("-" * 60)
        for idx, src in enumerate(sources): 
            print(f"  [{idx + 1}] Site/Domain: \"{src}\"")
        print("\n📝 COMMANDS: [A] Add Source | [D <num>] Delete Source | [Enter] Go Up")
        
        cmd = input("\n⚡ Selection: ").strip()
        if cmd == "":
            self.current_state = "EditBranch"
            return
            
        if cmd.lower() == 'a':
            source = input(" 👉 Enter targeted search site/domain (e.g., spie.org): ").strip().lower()
            if source:
                self.configurator.add_source_to_branch(b['name'], source)
                print("✅ Targeted source added.")
        elif cmd.lower().startswith('d '):
            try:
                idx = int(cmd.split(' ')[-1]) - 1
                if 0 <= idx < len(sources):
                    src_to_del = sources[idx]
                    self.configurator.delete_source_from_branch(b['name'], src_to_del)
                    print(f"✅ Deleted targeted source: \"{src_to_del}\"")
                else:
                    print("❌ Index out of range.")
            except Exception:
                print("❌ Invalid command parameter.")

    # =====================================================================
    # 🗃️ COGNITIVE HELPERS & EXAMPLES
    # =====================================================================
    def _print_root_help(self):
        print("\n📖 HELP: ROOT VIEW MENU")
        print("=" * 60)
        print("This is the main dashboard of the STUPID pipeline. Here you manage your research target lanes.")
        print("  - [A] Add Branch: Prompts you to add a new research branch folder/track manually.")
        print("  - [E <num>]: Selects branch number <num> to view/edit keywords, rules, rename or delete it.")
        print("  - [M] Manage Categories: Manage dynamic taxonomy categories, allowing custom tags/fields.")
        print("  - [S] Manage Global Sources: Add/remove search sites executed across all branches.")
        print("  - [F] Reset Factory Settings: Wipes existing configurations and restores default branch configurations,")
        print("        vocabularies, and dynamic categories.")
        print("  - [AI] AI Assist: Type a research topic or general idea, and the local LLM will automatically")
        print("        create a new branch or enhance an existing one with suggested phrases and rules.")
        print("=" * 60)
        input("\n[Press Enter to continue]")

    def _print_edit_branch_help(self, branch_name):
        print(f"\n📖 HELP: EDIT BRANCH [{branch_name.upper()}]")
        print("=" * 60)
        print("Here you configure the settings specific to the selected branch:")
        print("  - [1] Search Keywords & Phrases: The crawler queries these words across DuckDuckGo")
        print("        and ArXiv to harvest PDF documents. Add specific search queries here.")
        print("  - [2] Semantic Requirement Rules: The rules/expressions that the local LLM checks")
        print("        against the text of the papers to evaluate relevance and tag key topics.")
        print("  - [3] Rename Branch: Modifies the branch identifier name and automatically renames")
        print("        its folders on disk to prevent orphaned files.")
        print("  - [4] Delete Branch: Erases this configuration lane entirely from the ledger.")
        print("  - [5] Run Branch Pipeline: Opens execution switchboard options (End-to-End, Crawl, ")
        print("        AI Evaluate, Visualizer) to process files specifically for this branch.")
        print("  - [6] List / Modify Targeted Search Sites (Sources): Restrict or extend crawling searches")
        print("        for this branch specifically to targeted domains.")
        print("=" * 60)
        input("\n[Press Enter to continue]")

    def _print_keywords_help(self):
        print("\n📖 HELP: SEARCH KEYWORDS & PHRASES")
        print("=" * 60)
        print("These keyword strings are executed by the Crawler to download matching scientific papers.")
        print("  - [A] Add Phrase: Manually type in a new keyword query (e.g. 'multi object tracking GPU').")
        print("  - [U <num>]: Update and overwrite the phrase at index <num> with new text.")
        print("  - [D <num>]: Delete the phrase at index <num> from the crawler list.")
        print("  - [AI] AI Assist: Enter an angle or sub-topic, and the local LLM will generate multiple")
        print("        crawling keyword variants and suggest adding them to your list.")
        print("=" * 60)
        input("\n[Press Enter to continue]")

    def _print_semantic_rules_help(self):
        print("\n📖 HELP: SEMANTIC REQUIREMENT RULES")
        print("=" * 60)
        print("These are expressions the local AI Evaluator checks against each paper's text to determine")
        print("relevance, tag innovations, and methodology. They do not have to be Boolean, though Boolean")
        print("expressions using AND, OR, NOT, and parentheses are supported.")
        print("\nExamples of valid rules:")
        print("  - Boolean rules: (Cooking Techniques) AND (Image Processing Algorithms)")
        print("  - Plain English rules: Focus on papers discussing accelerator performance under load")
        print("  - Negative rules: NOT (autonomous driving datasets)")
        print("\nAvailable options:")
        print("  - [A] Add Rule: Enter a new semantic criteria rule to be evaluated.")
        print("  - [U <num>]: Update/edit the rule text at index <num>.")
        print("  - [D <num>]: Delete the rule at index <num> from the active evaluation list.")
        print("  - [AI] AI Assist: Explain your complex evaluation constraints in plain prose, and the")
        print("        AI will translate them into structured logic expressions.")
        print("  - [S] AI Suggest Rule: Automatically formulate a complementary semantic rule based on")
        print("        existing branch context (phrases, current rules, and downloaded articles sample).")
        print("=" * 60)
        input("\n[Press Enter to continue]")

if __name__ == "__main__":
    import argparse
    import json
    
    parser = argparse.ArgumentParser(
        description="STUPID: Semantic Text Understanding & Paper Ingestion Dashboard Console UI."
    )
    
    # Standalone boolean flag for configuring
    parser.add_argument(
        "--configure", action="store_true",
        help="Launches the interactive configuration loop to manage branches, keywords, and rules."
    )
    
    # Optional pipeline run step token argument (nargs='?' matches --run alone as const='ALL' or --run C,E as value)
    parser.add_argument(
        "--run", nargs="?", const="ALL", type=str,
        help="Executes the processing pipeline. Can specify components (e.g. C,E,V). If no components are specified, runs the entire pipeline."
    )
    
    parser.add_argument(
        "--interactive", action="store_true",
        help="Launches the step-by-step interactive orchestrator wizard."
    )
    
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Limits the number of operations per pipeline block (e.g. max downloads, max extractions, max evaluations)."
    )
    
    parser.add_argument(
        "--show_attributes", action="store_true",
        help="Include and display extracted attributes/categories and their values in the leaf paper cards."
    )
    
    parser.add_argument(
        "--silent", action="store_true", default=False,
        help="Runs the pipeline unattended without prompting for user confirmation or input."
    )
    
    parser.add_argument(
        "--visualize", type=str, default="branch",
        help="Hierarchy sequence for visualizer when running in silent mode (e.g., 'branch,relevant')."
    )
    
    parser.add_argument(
        "--min-year", type=int, default=None,
        help="Filter downloads to publications from or after this year (e.g., 2026)."
    )

    parser.add_argument(
        "--filter", type=str, default="",
        help="Initial query criteria filter to apply to the visualizer tree (e.g. 'israeli_involvement=Yes')."
    )

    parser.add_argument(
        "--no-combine-tags", action="store_true", default=False,
        help="Disable combined tag grouping (leaves will duplicate under multiple branches)."
    )

    parser.add_argument(
        "--branch", type=str, default=None,
        help="Restricts the pipeline execution only to this target branch (e.g. 'bci_gaming')."
    )
    
    # If executed with zero arguments, print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    args, unknown = parser.parse_known_args()
    
    try:
        # Track config state before configuration begins
        initial_config = None
        config_path = "./Configuration/targets_config.json"
        try:
            config_controller = ConfigurationLogicController(config_path=config_path)
            initial_config = config_controller.config
        except Exception:
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        initial_config = json.load(f)
                except Exception:
                    pass

        # 1. Execute Configuration UI if requested
        if args.configure:
            ui = HierarchicalConsoleUI(limit=args.limit, show_attributes=args.show_attributes, filter_str=args.filter, combine_tags=not args.no_combine_tags)
            ui.run_master_loop()

        # Track config state after configuration exits
        final_config = None
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    final_config = json.load(f)
            except Exception:
                pass

        config_changed = (initial_config != final_config)

        # 2. Execute Pipeline Run if requested
        if args.run is not None:
            # Determine run steps
            if args.run.upper() == "ALL" or not args.run.strip():
                run_steps = ["C", "E", "V", "Z"]
            else:
                run_steps = [step.strip().upper() for step in args.run.split(",") if step.strip()]
                
            # Invalidation Gate: Warning if configuration changed but only running a subset of components
            if config_changed and run_steps and not args.silent:
                is_full_run = (set(run_steps) == {"C", "E", "V", "Z"} or set(run_steps) == {"C", "E", "V", "S"})
                if not is_full_run:
                    print("\n⚠️  CONFIGURATION CHANGE DETECTED ⚠️")
                    print(f" 👉 You modified the configuration, but requested to run only a subset: {run_steps}")
                    print(" 👉 To prevent incomplete or inconsistent data states, it is highly recommended to run all components (C, E, V, Z).")
                    confirm = input(" 🤔 Would you like to run all components instead? (Y/n): ").strip().lower()
                    if confirm != 'n':
                        run_steps = ["C", "E", "V", "Z"]
                        print("🚀 Adjusting execution plan to run all components.")

            if run_steps:
                orchestrator = GrandMasterOrchestrator()
                orchestrator.run_pipeline(
                    run_steps, 
                    target_branch=args.branch,
                    limit=args.limit, 
                    show_attributes=args.show_attributes, 
                    silent=args.silent, 
                    visualize=args.visualize,
                    min_year=args.min_year,
                    filter_str=args.filter,
                    combine_tags=not args.no_combine_tags
                )
                
        # 3. Execute Interactive Wizard if requested
        elif args.interactive:
            orchestrator = GrandMasterOrchestrator()
            orchestrator.launch_interactive_wizard()
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user (Ctrl+C). Exiting STUPID Console UI.")
        sys.exit(0)
