# import os
# import sys
# import argparse
# import json

# # Import your underlying components dynamically
# try:
#     from Crawler import DataDrivenIngestionEngine
#     from Extractor import FileBundleExtractor
#     from Evaluator import DataDrivenEvaluator
#     from Selector import HierarchicalQueryEngine
#     from Visualizer import TerminalConsoleUI
# except ImportError as e:
#     print(f"❌ Initialization Error: Critical pipeline script missing in namespace. {e}")
#     sys.exit(1)

# class GrandMasterOrchestrator:
#     def __init__(self):
#         # Baseline internal default infrastructure paths
#         self.config_path = "./targets_config.json"
#         self.storage_root = "./downloaded_research"

#     def _verify_pipeline_integrity(self, tasks: list) -> bool:
#         """Data Integrity Guardrail: Prevents state corruption by analyzing task dependencies."""
#         # Map shorthand characters to formal system names for clean display logs
#         name_map = {"C": "Crawler", "E": "Extractor", "V": "Evaluator", "S": "Selector", "Z": "Visualizer"}
        
#         # Check 1: Running Selector or Visualizer directly after a Crawler sync without Extractor/Evaluator
#         if "C" in tasks and "Z" in tasks:
#             if "E" not in tasks or "V" not in tasks:
#                 print("\n⚠️  PIPELINE INTEGRITY WARNING ⚠️")
#                 print(" 👉 You are running [Crawler] and [Visualizer] but SKIPPING [Extractor] or [Evaluator].")
#                 print(" 👉 Newly crawled PDFs will NOT show up in your visual tree because they lack text sidecars and AI tags!")
#                 confirm = input(" 🤔 Are you absolutely sure you want to proceed with this incomplete data state? (y/N): ")
#                 if confirm.lower().strip() != 'y':
#                     return False
#         return True

#     def run_pipeline(self, execution_steps: list):
#         """Sequentially triggers the component classes based on validated array tokens."""
#         if not self._verify_pipeline_integrity(execution_steps):
#             print("🛑 Pipeline execution aborted by the user.")
#             return

#         print("\n🚀 Initializing Grand Master Pipeline Sweep Sequence...")
#         print("=" * 90)

#         # 1. RUN CRAWLER
#         if "C" in execution_steps:
#             print("\n[STEP 1/5] 🛠️ Launching Ingestion Engine (Crawler)...")
#             crawler = DataDrivenIngestionEngine(config_path=self.config_path, output_root=self.storage_root)
#             crawler.execute_daily_sync()

#         # 2. RUN EXTRACTOR
#         if "E" in execution_steps:
#             print("\n[STEP 2/5] 🛠️ Launching Sidecar Text Processor (Extractor)...")
#             extractor = FileBundleExtractor(storage_root=self.storage_root)
#             extractor.process_all_targets()

#         # 3. RUN EVALUATOR
#         if "V" in execution_steps:
#             print("\n[STEP 3/5] 🛠️ Launching Cognitive Reasoning Layer (Evaluator)...")
#             evaluator = DataDrivenEvaluator(config_path=self.config_path, storage_root=self.storage_root)
#             evaluator.evaluate_all_new_sidecars()

#         # 4. RUN SELECTOR & VISUALIZER
#         # If Visualizer is checked, it handles Selector's data queries natively via composition
#         if "Z" in execution_steps:
#             print("\n[STEP 4/5] 🛠️ Launching Hierarchy Engine & Console Presentation Interface (Visualizer)...")
#             selector_engine = HierarchicalQueryEngine(storage_root=self.storage_root)
#             ui_shell = TerminalConsoleUI(selector_engine)
#             ui_shell.run_loop()
#         elif "S" in execution_steps:
#             print("\n[STEP 5/5] 🛠️ Launching Data-Only Hierarchy Split Parser (Selector)...")
#             selector_engine = HierarchicalQueryEngine(storage_root=self.storage_root)
#             records = selector_engine.load_all_metadata_records()
#             print(f"   📊 Selector silently parsed {len(records)} metadata records. Zero UI bound.")

#         print("\n🏁 Grand Master Pipeline run segment completed successfully.")

#     def launch_interactive_wizard(self):
#         """Interactive Shell Option: Guides users through settings step-by-step with examples."""
#         print("\n🧙‍♂️ Welcome to the MT-ARA Interactive Orchestration Wizard 🧙‍♂️")
#         print("=" * 90)
        
#         print(f"Current Config Path Target: {self.config_path}")
#         print(f"Current Storage Repository Destination: {self.storage_root}")
#         change_paths = input("📝 Do you want to modify these default system path destinations? (y/N): ")
        
#         if change_paths.lower().strip() == 'y':
#             custom_config = input("   👉 Enter target JSON config file path: ")
#             custom_storage = input("   👉 Enter data storage root folder path: ")
#             if custom_config.strip(): self.config_path = custom_config.strip()
#             if custom_storage.strip(): self.storage_root = custom_storage.strip()

#         print("\n📋 Select which components you would like to execute during this runtime sweep:")
#         print("   [C] Crawler    - Harvests missing document binaries from web/conferences")
#         print("   [E] Extractor  - Parses full-text summaries and structures sidecar triads")
#         print("   [V] Evaluator  - Triggers offline AI model to process text and apply taxonomy tags")
#         print("   [S] Selector   - Evaluates pure parent-child tree dictionary partitions (Data Only)")
#         print("   [Z] Visualizer - Launches interactive terminal shell to browse tree nodes visually")
        
#         print("\n💡 Processing Configuration Examples:")
#         print("   - Type 'C,E,V,Z' to run a complete, end-to-end data harvesting and analysis sweep.")
#         print("   - Type 'C' to only scrape new files safely without running local AI models.")
#         print("   - Type 'Z' to quickly open up your query shell workspace to read existing data.")
        
#         user_selection = input("\n🔍 Enter components to run (comma-separated abbreviations): ")
#         user_input_split = user_selection.split(",")
#         parsed_steps = [s.strip().upper() for s in user_input_split if s.strip()]
        
#         # Guard against bad inputs
#         valid_tokens = ["C", "E", "V", "S", "Z"]
#         if any(t not in valid_tokens for t in parsed_steps):
#             print("❌ Invalid component token entered. Aborting wizard interface.")
#             return

#         self.run_pipeline(parsed_steps)

# # =====================================================================
# # Command Line Interface (CLI) Parsing Entry Point
# # =====================================================================
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="ArticleAgent: Grand Master Multi-Tenant Research Pipeline Controller Wrapper.")
    
#     # Configuration override flags
#     parser.add_argument("--configure", nargs=2, metavar=('COMPONENT', 'CONF_PATH'), action='append',
#                         help="Overrides storage parameters. Usage: --configure Crawler ./custom_vault/ or --configure Selector ./custom.json")
    
#     # Operational execution flags
#     parser.add_argument("--run", type=str, help="Executes strict pipeline sequences using tokens (C,E,V,S,Z). Example: --run C,E")
#     parser.add_argument("--interactive", action="store_true", help="Launches step-by-step interactive questionnaire prompt panel.")

#     args = parser.parse_args()
#     orchestrator = GrandMasterOrchestrator()

#     # Apply configuration parameters if passed via CLI flags
#     if args.configure:
#         for comp_target, custom_val in args.configure:
#             if comp_target.lower() == "crawler":
#                 orchestrator.storage_root = custom_val
#                 print(f"⚙️ CLI Override: Crawler storage destination reassigned to '{custom_val}'")
#             elif comp_target.lower() == "selector":
#                 orchestrator.config_path = custom_val
#                 print(f"⚙️ CLI Override: JSON configuration ledger path reassigned to '{custom_val}'")

#     # Route execution based on flags
#     if args.interactive:
#         orchestrator.launch_interactive_wizard()
#     elif args.run:
#         steps = [step.strip().upper() for step in args.run.split(",") if step.strip()]
#         orchestrator.run_pipeline(steps)
#     else:
#         # Default behavior if executed completely without parameters
#         parser.print_help()


import os
import sys
import argparse
import json

# Import your underlying components dynamically
try:
    from Crawler import DataDrivenIngestionEngine
    from Extractor import FileBundleExtractor
    from Evaluator import LocalAIEvaluator  # FIXED: Matches current class name
    from Selector import HierarchicalQueryEngine
    from Visualizer import TerminalConsoleUI
except ImportError as e:
    print(f"❌ Initialization Error: Critical pipeline script missing in namespace. {e}")
    sys.exit(1)

class GrandMasterOrchestrator:
    def __init__(self):
        self.config_path = "./Configuration/targets_config.json"
        self.storage_root = "./downloaded_research"

    def _verify_pipeline_integrity(self, tasks: list) -> bool:
        """Data Integrity Guardrail: Prevents state corruption by analyzing task dependencies."""
        if "C" in tasks and "Z" in tasks:
            if "E" not in tasks or "V" not in tasks:
                print("\n⚠️  PIPELINE INTEGRITY WARNING ⚠️")
                print(" 👉 You are running [Crawler] and [Visualizer] but SKIPPING [Extractor] or [Evaluator].")
                print(" 👉 Newly crawled PDFs will NOT show up in your visual tree because they lack text sidecars and AI tags!")
                confirm = input(" 🤔 Are you absolutely sure you want to proceed with this incomplete data state? (y/N): ")
                if confirm.lower().strip() != 'y':
                    return False
        return True

    def run_pipeline(self, execution_steps: list, target_branch: str = None, limit: int = None, show_attributes: bool = False):
        """Sequentially triggers the component classes based on validated array tokens."""
        if not self._verify_pipeline_integrity(execution_steps):
            print("🛑 Pipeline execution aborted by the user.")
            return

        print("\n🚀 Initializing Grand Master Pipeline Sweep Sequence...")
        print("=" * 90)

        new_pdfs = None
        # 1. RUN CRAWLER
        if "C" in execution_steps:
            print("\n[STEP 1/5] 🛠️ Launching Ingestion Engine (Crawler)...")
            crawler = DataDrivenIngestionEngine(config_path=self.config_path, output_root=self.storage_root)
            crawler.execute_daily_sync(target_branch=target_branch, limit=limit)
            new_pdfs = []
            for branch, title, url in crawler.session_downloads:
                safe_name = f"{crawler._sanitize_filename(title)}.pdf"
                pdf_path = os.path.join(self.storage_root, branch, safe_name)
                new_pdfs.append((branch, pdf_path))

        new_metas = None
        # 2. RUN EXTRACTOR
        if "E" in execution_steps:
            print("\n[STEP 2/5] 🛠️ Launching Sidecar Text Processor (Extractor)...")
            extractor = FileBundleExtractor(storage_root=self.storage_root)
            extractor.process_all_targets(target_branch=target_branch, limit=limit, prioritized_pdfs=new_pdfs)
            new_metas = []
            for branch, file_name in extractor.session_extractions:
                base_name, _ = os.path.splitext(file_name)
                meta_path = os.path.join(self.storage_root, branch, f"{base_name}_meta.json")
                new_metas.append((branch, meta_path))

        # 3. RUN EVALUATOR
        if "V" in execution_steps:
            print("\n[STEP 3/5] 🛠️ Launching Cognitive Reasoning Layer (Evaluator)...")
            evaluator = LocalAIEvaluator(config_path=self.config_path, storage_root=self.storage_root)
            evaluator.evaluate_all_new_sidecars(target_branch=target_branch, limit=limit, prioritized_metas=new_metas)

        # 4. RUN SELECTOR & VISUALIZER
        if "Z" in execution_steps:
            print("\n[STEP 4/5] 🛠️ Launching Hierarchy Engine & Console Presentation Interface (Visualizer)...")
            selector_engine = HierarchicalQueryEngine(storage_root=self.storage_root)
            ui_shell = TerminalConsoleUI(selector_engine, show_attributes=show_attributes)
            ui_shell.run_loop()
        elif "S" in execution_steps:
            print("\n[STEP 5/5] 🛠️ Launching Data-Only Hierarchy Split Parser (Selector)...")
            selector_engine = HierarchicalQueryEngine(storage_root=self.storage_root)
            records = selector_engine.load_all_metadata_records()
            print(f"   📊 Selector silently parsed {len(records)} metadata records. Zero UI bound.")

        print("\n🏁 Grand Master Pipeline run segment completed successfully.")

    def launch_interactive_wizard(self):
        """Interactive Shell Option: Guides users through settings step-by-step with examples."""
        print("\n🧙‍♂️ Welcome to the STUPID Interactive Orchestration Wizard 🧙‍♂️")
        print("=" * 90)
        
        print(f"Current Config Path Target: {self.config_path}")
        print(f"Current Storage Repository Destination: {self.storage_root}")
        change_paths = input("📝 Do you want to modify these default system path destinations? (y/N): ")
        
        if change_paths.lower().strip() == 'y':
            custom_config = input("   👉 Enter target JSON config file path: ")
            custom_storage = input("   👉 Enter data storage root folder path: ")
            if custom_config.strip(): self.config_path = custom_config.strip()
            if custom_storage.strip(): self.storage_root = custom_storage.strip()

        print("\n📋 Select which components you would like to execute during this runtime sweep:")
        print("   [C] Crawler    - Harvests missing document binaries from web/conferences")
        print("   [E] Extractor  - Parses full-text summaries and structures sidecar triads")
        print("   [V] Evaluator  - Triggers offline AI model to process text and apply taxonomy tags")
        print("   [S] Selector   - Evaluates pure parent-child tree dictionary partitions (Data Only)")
        print("   [Z] Visualizer - Launches interactive terminal shell to browse tree nodes visually")
        
        print("\n💡 Processing Configuration Examples:")
        print("   - Type 'C,E,V,Z' to run a complete, end-to-end data harvesting and analysis sweep.")
        print("   - Type 'C' to only scrape new files safely without running local AI models.")
        print("   - Type 'Z' to quickly open up your query shell workspace to read existing data.")
        
        user_selection = input("\n🔍 Enter components to run (comma-separated abbreviations): ")
        
        user_input_split = user_selection.split(",")
        parsed_steps = [s.strip().upper() for s in user_input_split if s.strip()]
        
        valid_tokens = ["C", "E", "V", "S", "Z"]
        if any(t not in valid_tokens for t in parsed_steps):
            print("❌ Invalid component token entered. Aborting wizard interface.")
            return

        limit_input = input("\n👉 Enter execution limit per block (integer, or press Enter for no limit): ").strip()
        user_limit = int(limit_input) if limit_input.isdigit() else None

        self.run_pipeline(parsed_steps, limit=user_limit)

# =====================================================================
# Command Line Interface (CLI) Parsing Entry Point
# =====================================================================
if __name__ == "__main__":
    print("🛑 Direct execution of ArticlesAgent.py is restricted.")
    print("👉 Please run the application using an active UI component (such as STUPIDConsoleUI.py).")
    sys.exit(0)
