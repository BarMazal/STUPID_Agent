# import os
# import json
# import requests

# class LocalAIEvaluator:
#     def __init__(self, config_path: str = "./targets_config.json", storage_root: str = "./downloaded_research", model_name: str = "llama3:8b", ollama_url: str = "http://localhost:11434"):
#         self.config_path = config_path
#         self.storage_root = storage_root
#         self.model_name = model_name
#         self.ollama_url = ollama_url

#     def _get_branch_criteria(self, branch_name: str) -> str:
#         """Dynamically provides natural language evaluation rules based on the active branch context."""
#         criteria_matrix = {
#             "object_tracking": "We are specifically searching for papers dealing with Multi-Object Tracking (MOT), tracking-by-detection, or end-to-end models. Pay special attention to papers introducing innovations in temporal embeddings, cross-check embeddings, or motion models to reduce ID switches.",
#             "metalenses": "We want papers focused on metalens engineering, flat optics, subwavelength structures, and optical metasurfaces. Look for solutions regarding metalens bars, material choices, sensors, or changing operating wavelengths.",
#             "ccd_sensors": "We are tracking methodologies regarding Charge-Coupled Device (CCD) architectures, Bayer patterns, 3CMOS prism beam splitters, and algorithmic solutions to demographic artifacts or sensor limitations."
#         }
#         return criteria_matrix.get(branch_name.lower(), "Evaluate if this document is a valid scientific or engineering research paper.")

#     def evaluate_document(self, text_content: str, criteria: str) -> dict:
#         """Executes an isolated reasoning loop using a local LLM to extract structured taxonomies."""
#         # Restrict window (first 6000 characters) to prevent token window crashes on local systems
#         sample_text = text_content[:6000]
        
#         system_prompt = "You are an expert academic research filtering agent. You must output raw JSON only matching the schema exactly. No markdown blocks, no conversational text."
#         user_prompt = f"""Evaluate if this research paper fits our strict research criteria.
        
# CRITERIA GOAL:
# {criteria}

# DOCUMENT DATA TEXT SOURCE:
# {sample_text}

# You MUST return exactly this JSON layout: {{
#     "is_relevant": true or false,
#     "confidence_score": 0.0 to 1.0,
#     "reasoning_summary": "A concise single-sentence explanation of why it passes or fails your evaluation filter.",
#     "innovation_focus": ["Tag1", "Tag2"],
#     "methodology_branch": ["Tag1", "Tag2"]
# }}"""

#         try:
#             # Connect directly via Ollama's local HTTP API endpoint
#             response = requests.post(
#                 f"{self.ollama_url}/api/generate",
#                 json={
#                     "model": self.model_name,
#                     "system": system_prompt,
#                     "prompt": user_prompt,
#                     "format": "json",
#                     "stream": False,
#                     "options": {"temperature": 0.0} # Zero guarantees absolute repeatable accuracy
#                 },
#                 timeout=90
#             )
            
#             if response.status_code == 200:
#                 raw_response_text = response.json().get("response", "{}")
#                 return json.loads(raw_response_text)
#             return {}
#         except Exception as e:
#             print(f"      ❌ Local AI model engine connectivity hurdle: {e}")
#             return {}

#     def evaluate_all_new_sidecars(self):
#         """Scans the sidecar layout and updates unevaluated json cards dynamically on disk."""
#         if not os.path.exists(self.storage_root):
#             print("⚠️ Storage target footprint empty. Run your extraction script first.")
#             return

#         print(f"🧠 Connecting to local Ollama engine container using model instance: [{self.model_name}]...")
        
#         for target_name in os.listdir(self.storage_root):
#             target_path = os.path.join(self.storage_root, target_name)
            
#             if os.path.isdir(target_path):
#                 branch_criteria = self._get_branch_criteria(target_name)
#                 meta_files = [f for f in os.listdir(target_path) if f.lower().endswith("_meta.json")]
                
#                 if not meta_files:
#                     continue
                    
#                 print(f"\n🤖 Processing branch lane evaluation filters: [{target_name.upper()}]")
                
#                 for meta_name in meta_files:
#                     json_path = os.path.join(target_path, meta_name)
#                     base_name = meta_name.replace("_meta.json", "")
#                     txt_path = os.path.join(target_path, f"{base_name}.txt")
                    
#                     if not os.path.exists(txt_path):
#                         continue

#                     with open(json_path, "r", encoding="utf-8") as f:
#                         meta_card = json.load(f)

#                     # IDEMPOTENT GUARD: Skip if already processed by the agent
#                     # if meta_card.get("agent_relevance_eval", {}).get("is_evaluated", False):
#                     #     print(f"   ⏩ Record already parsed by AI model: {base_name[:40]}...")
#                     #     continue
#                     if meta_card.get("agent_relevance_eval", {}).get("is_evaluated", False) is True:
#                         print(f"   ⏩ Record already parsed by AI model: {base_name[:40]}...")
#                         continue

#                     print(f"   🧠 Model analyzing content logic for: {base_name[:40]}...")
                    
#                     with open(txt_path, "r", encoding="utf-8") as f:
#                         raw_doc_text = f.read()

#                     ai_verdict = self.evaluate_document(raw_doc_text, branch_criteria)

#                     if not ai_verdict:
#                         print("      ⚠️ Model returned empty payload, skipping execution slot.")
#                         continue

#                     # Update the ledger entry mapping schema directly
#                     meta_card["agent_relevance_eval"] = {
#                         "is_evaluated": True,
#                         "is_relevant": ai_verdict.get("is_relevant", False),
#                         "confidence_score": ai_verdict.get("confidence_score", 0.0),
#                         "reasoning_summary": ai_verdict.get("reasoning_summary", "")
#                     }
#                     meta_card["semantic_tags"] = {
#                         "innovation_focus": ai_verdict.get("innovation_focus", []),
#                         "methodology_branch": ai_verdict.get("methodology_branch", []),
#                         "hardware_targets": meta_card.get("semantic_tags", {}).get("hardware_targets", [])
#                     }

#                     with open(json_path, "w", encoding="utf-8") as f:
#                         json.dump(meta_card, f, indent=4, ensure_ascii=False)
                    
#                     status_emoji = "✅ MATCH" if ai_verdict.get("is_relevant") else "❌ REJECT"
#                     print(f"      {status_emoji} ({ai_verdict.get('confidence_score')}): {ai_verdict.get('reasoning_summary')}")

# if __name__ == "__main__":
#     evaluator = LocalAIEvaluator(model_name="deepseek-r1:14b")
#     evaluator.evaluate_all_new_sidecars()
#     print("\n🏁 AI semantic processing complete. Metadata tracking indexes updated.")

import os
import json
import requests
import sys
import time

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

def safe_write(text: str):
    try:
        sys.stdout.write(text)
        sys.stdout.flush()
    except UnicodeEncodeError:
        try:
            # Fall back to ASCII characters only, removing/ignoring others
            cleaned_text = text.encode('ascii', errors='ignore').decode('ascii')
            sys.stdout.write(cleaned_text)
            sys.stdout.flush()
        except Exception:
            pass
    except Exception:
        pass

class LocalAIEvaluator:
    def __init__(self, config_path: str = "./Configuration/targets_config.json", storage_root: str = "./downloaded_research", model_name: str = "deepseek-r1:14b", ollama_url: str = "http://localhost:11434", silent: bool = False):
        self.config_path = config_path
        self.storage_root = storage_root
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.config = self._load_config()
        self.session_evaluations = []
        self.silent = silent

    def _print_evaluator_progress(self, current, max_val):
        import sys
        progress_str = f"   ⏳ Progress: Evaluating {current}/{max_val}"
        safe_write(f"\r{progress_str:<80}")

    def _log(self, message: str):
        import sys
        safe_write(f"\r{message:<80}\n")
        if hasattr(self, 'max_to_evaluate') and hasattr(self, 'evaluated_in_session'):
            self._print_evaluator_progress(self.evaluated_in_session, self.max_to_evaluate)

    def _load_config(self) -> dict:
        """Reads the centralized tracking configuration document from disk."""
        try:
            from Configurator import ConfigurationLogicController
            controller = ConfigurationLogicController(config_path=self.config_path)
            return controller.config
        except Exception:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {"branches": []}

    def _save_config(self):
        """Saves the tracking configuration document back to disk."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def _get_branch_by_name(self, name: str) -> dict:
        """Helper to find branch dictionary from config."""
        for b in self.config.get("branches", []):
            if b["name"] == name.lower().strip():
                return b
        return None

    def _get_branch_requirement_from_json(self, branch_name: str) -> str:
        """Extracts the semantic requirement expression for the active branch."""
        for branch in self.config.get("branches", []):
            if branch["name"] == branch_name.lower():
                reqs = branch.get("semantic_requirements", [])
                if reqs:
                    return " AND ".join([f"({r})" for r in reqs])
                return branch.get("semantic_requirement", "Evaluate if this document is a valid scientific research paper.")
        return "Evaluate if this document is a valid scientific research paper."

    def _get_branch_version_from_json(self, branch_name: str) -> int:
        """Extracts the criteria version tracking number for the active branch."""
        for branch in self.config.get("branches", []):
            if branch["name"] == branch_name.lower():
                return branch.get("criteria_version", 1)
        return 1

    def evaluate_document(self, text_content: str, criteria_expression: str, categories: list = None, branch_vocab: list = None) -> dict:
        """Executes the local LLM reasoning cycle to evaluate boolean constraints."""
        sample_text = text_content[:6000]
        system_prompt = "You are an expert filtering agent. Output raw JSON matching schema exactly. No conversational text."
        
        if categories is None:
            categories = self.config.get("categories", [
                {
                    "key": "pub_year",
                    "label": "Publication Year",
                    "source": "ai",
                    "path": ["semantic_tags", "pub_year"],
                    "description": "extract the 4-digit publication year of the paper (e.g. 2024, 2021). If not found, return ['Unassigned/None']",
                    "key_search": ["published in", "publication year", "year of publication", "accepted in", "conference year"],
                    "semantic_rules": ["Extract the publication year of the research paper.", "Verify that the year is a 4-digit calendar year (e.g. 2024, 2020)."]
                },
                {
                    "key": "institute",
                    "label": "Research Institution",
                    "source": "ai",
                    "path": ["semantic_tags", "institute"],
                    "description": "extract the primary research group, university, or corporate lab affiliation of the authors (e.g. Stanford University, MIT, Google DeepMind). If not found, return ['Unassigned/None']",
                    "key_search": ["university", "institute", "department", "laboratory", "school of", "author affiliation", "research group"],
                    "semantic_rules": ["Extract the author affiliations or research institutions.", "Look for keywords indicating corporate research labs, universities, or academic institutions."]
                },
                {"key": "innovation", "label": "Innovation Focus", "source": "ai", "path": ["semantic_tags", "innovation_focus"], "description": "innovation focus tags"},
                {"key": "methodology", "label": "Methodology Branch", "source": "ai", "path": ["semantic_tags", "methodology_branch"], "description": "methodology tags"}
            ])
        if branch_vocab is None:
            branch_vocab = []
            
        ai_categories = [c for c in categories if c.get("source") == "ai"]
        
        vocab_instruction = ""
        if branch_vocab:
            vocab_instruction = f"\nVOCABULARY CONSTRAINTS:\nFor the categorization lists, try to first match and use tags from this existing vocabulary if appropriate. If a new tag is necessary to accurately capture the content, you may output a new tag.\nExisting Vocabulary: {json.dumps(branch_vocab)}\n"

        categories_instruction = ""
        for cat in ai_categories:
            field_name = cat["path"][-1]
            desc = cat.get("description", "")
            key_search = cat.get("key_search", [])
            rules = cat.get("semantic_rules", [])
            
            cat_desc = f"- {field_name}: {desc}"
            if key_search:
                cat_desc += f"\n  Search Keywords: {', '.join(key_search)}"
            if rules:
                cat_desc += f"\n  Semantic Extraction Rules:\n    " + "\n    ".join([f"* {r}" for r in rules])
            categories_instruction += cat_desc + "\n"

        schema_format = "{\n"
        schema_format += '    "is_relevant": true or false,\n'
        schema_format += '    "confidence_score": 0.0 to 1.0,\n'
        schema_format += '    "reasoning_summary": " concise single-sentence explanation of why it passes/fails the criteria ",\n'
        schema_format += '    "short_summary": " a comprehensive 3-8 sentences summary of the paper\'s core goals, methods, and results ",\n'
        for cat in ai_categories:
            field_name = cat["path"][-1]
            schema_format += f'    "{field_name}": ["Tag1", "Tag2"],\n'
        schema_format = schema_format.rstrip(",\n") + "\n}"

        user_prompt = (
            f"CRITERIA GOAL EXPR:\n{criteria_expression}\n\n"
            f"CATEGORY EXTRACTION GUIDELINES:\n{categories_instruction}\n"
            f"DOCUMENT DATA:\n{sample_text}\n"
            f"{vocab_instruction}\n"
            f"Return JSON layout exactly like this:\n{schema_format}"
        )

        # Immediately print the initial thinking status
        safe_write("\r      🧠 Thinking. (00h 00m 00s)   ")

        payload = {
            "model": self.model_name,
            "system": system_prompt,
            "prompt": user_prompt,
            "format": "json",
            "stream": True,
            "options": {"temperature": 0.0}
        }

        full_text_response = ""
        animation_cycle = [".  ", ".. ", "..."]
        cycle_idx = 0
        
        absolute_start_time = time.time()
        accumulated_elapsed_time = 0.0
        
        last_anim_time = time.time()
        current_window_start = time.time()
        time_window_seconds = 600 #120 # 2 minutes global timeout
        
        try:
            response_stream = requests.post(f"{self.ollama_url}/api/generate", json=payload, stream=True, timeout=time_window_seconds)
            if response_stream.status_code != 200:
                safe_write(f"\r      ❌ Connection error: Status code {response_stream.status_code}\n")
                return {}

            lines_iterator = response_stream.iter_lines()
            
            while True:
                now = time.time()
                total_elapsed = (now - absolute_start_time) + accumulated_elapsed_time
                hours = int(total_elapsed // 3600)
                minutes = int((total_elapsed % 3600) // 60)
                seconds = int(total_elapsed % 60)
                time_string = f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
                
                current_window_duration = now - current_window_start
                
                if now - last_anim_time > 0.3:
                    anim = animation_cycle[cycle_idx]
                    cycle_idx = (cycle_idx + 1) % len(animation_cycle)
                    safe_write(f"\r      🧠 Thinking{anim} ({time_string})   ")
                    last_anim_time = now

                if current_window_duration > time_window_seconds:
                    safe_write("\r" + " " * 60 + "\r")
                    
                    if getattr(self, 'silent', False):
                        safe_write(f"\n      🚀 Window limits automatically extended in silent mode ({int(total_elapsed)}s). Continuing token tracking sequence...\n")
                        current_window_start = time.time()
                        last_anim_time = time.time()
                        continue

                    print(f"\n      ⚠️  TIMEOUT GATE EXCEEDED: The model has been processing for {int(total_elapsed)} seconds.")
                    choice = input("      🤔 Do you want to extend this reasoning session? (Y/n): ").strip().lower()
                    
                    if choice == 'n':
                        print("      🛑 Session aborted by user command input request.")
                        response_stream.close()
                        return {}
                    else:
                        print("      🚀 Window limits extended. Continuing token tracking sequence...")
                        current_window_start = time.time()
                        last_anim_time = time.time()
                        continue

                try:
                    line = next(lines_iterator, None)
                    if line:
                        packet = json.loads(line.decode('utf-8'))
                        token = packet.get("response", "")
                        full_text_response += token
                    else:
                        break
                except StopIteration:
                    break
                except Exception:
                    time.sleep(0.05)

            safe_write("\r" + " " * 60 + "\r")

            if "</think>" in full_text_response:
                full_text_response = full_text_response.split("</think>")[-1].strip()

            full_text_response = full_text_response.strip()
            return json.loads(full_text_response)

        except Exception as e:
            safe_write("\r" + " " * 60 + "\r")
            # Log the actual exception safely so it's not silently ignored!
            try:
                err_msg = str(e).encode('ascii', errors='ignore').decode('ascii')
                print(f"\n❌ Pipeline streaming anomaly: {err_msg}")
            except Exception:
                pass
            return {}

    def evaluate_all_new_sidecars(self, target_branch: str = None, limit: int = None, prioritized_metas: list = None):
        if not os.path.exists(self.storage_root):
            import sys
            safe_write(f"\r⚠️ Storage target footprint empty.\n")
            return

        import sys
        safe_write(f"🧠 AI Evaluation Layer active using model instance: [{self.model_name}]...\n")
        
        self.config = self._load_config()  # Ensure latest config is loaded
        
        categories = self.config.get("categories", [
            {"key": "branch", "label": "Branch Lineage", "source": "system", "path": ["_branch_lineage"]},
            {"key": "relevant", "label": "Relevance", "source": "system", "path": ["agent_relevance_eval", "is_relevant"]},
            {
                "key": "pub_year",
                "label": "Publication Year",
                "source": "ai",
                "path": ["semantic_tags", "pub_year"],
                "description": "extract the 4-digit publication year of the paper (e.g. 2024, 2021). If not found, return ['Unassigned/None']",
                "key_search": ["published in", "publication year", "year of publication", "accepted in", "conference year"],
                "semantic_rules": ["Extract the publication year of the research paper.", "Verify that the year is a 4-digit calendar year (e.g. 2024, 2020)."]
            },
            {
                "key": "institute",
                "label": "Research Institution",
                "source": "ai",
                "path": ["semantic_tags", "institute"],
                "description": "extract the primary research group, university, or corporate lab affiliation of the authors (e.g. Stanford University, MIT, Google DeepMind). If not found, return ['Unassigned/None']",
                "key_search": ["university", "institute", "department", "laboratory", "school of", "author affiliation", "research group"],
                "semantic_rules": ["Extract the author affiliations or research institutions.", "Look for keywords indicating corporate research labs, universities, or academic institutions."]
            },
            {"key": "innovation", "label": "Innovation Focus", "source": "ai", "path": ["semantic_tags", "innovation_focus"], "description": "innovation focus tags"},
            {"key": "methodology", "label": "Methodology Branch", "source": "ai", "path": ["semantic_tags", "methodology_branch"], "description": "methodology tags"}
        ])
        ai_categories = [c for c in categories if c.get("source") == "ai"]
        
        self.session_evaluations = []
        self.evaluated_in_session = 0
        
        # Helper to check if a json card needs evaluation
        def check_needs_evaluation(branch_name, json_path):
            if not os.path.exists(json_path):
                return False, None
            base_name = os.path.basename(json_path).replace("_meta.json", "")
            txt_path = os.path.join(os.path.dirname(json_path), f"{base_name}.txt")
            if not os.path.exists(txt_path):
                return False, None
                
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    meta_card = json.load(f)
            except Exception:
                return False, None
                
            active_version = self._get_branch_version_from_json(branch_name)
            saved_version = meta_card.get("evaluated_under_version", 0)
            is_eval = meta_card.get("agent_relevance_eval", {}).get("is_evaluated", False)
            
            missing_cats = []
            for cat in ai_categories:
                field_name = cat["path"][-1]
                if "semantic_tags" not in meta_card or field_name not in meta_card["semantic_tags"]:
                    missing_cats.append(cat["key"])
                    
            if not is_eval:
                return True, "Unevaluated sidecar file"
            if saved_version != active_version:
                return True, f"Criteria mismatch (File: v{saved_version} vs Config: v{active_version})"
            if missing_cats:
                return True, f"Missing dynamic categories: {', '.join(missing_cats)}"
                
            return False, None

        # Deduplicate and prioritize tasks
        task_seen = set()
        ordered_tasks = []
        
        # 1. Prioritized
        if prioritized_metas:
            for branch, meta_path in prioritized_metas:
                if target_branch and branch.lower() != target_branch.lower().strip():
                    continue
                needs_eval, reason = check_needs_evaluation(branch, meta_path)
                if needs_eval and meta_path not in task_seen:
                    task_seen.add(meta_path)
                    ordered_tasks.append((branch, meta_path, reason))
                    
        # 2. Scanned
        if os.path.exists(self.storage_root):
            for target_name in os.listdir(self.storage_root):
                if target_branch and target_name.lower() != target_branch.lower().strip():
                    continue
                target_path = os.path.join(self.storage_root, target_name)
                if os.path.isdir(target_path):
                    meta_files = [f for f in os.listdir(target_path) if f.lower().endswith("_meta.json")]
                    for meta_name in meta_files:
                        full_path = os.path.join(target_path, meta_name)
                        needs_eval, reason = check_needs_evaluation(target_name, full_path)
                        if needs_eval and full_path not in task_seen:
                            task_seen.add(full_path)
                            ordered_tasks.append((target_name, full_path, reason))

        # Sort tasks by associated PDF modification time descending (newest first)
        def get_mtime(task_item):
            meta_path = task_item[1]
            base_name = os.path.basename(meta_path).replace("_meta.json", "")
            pdf_path = os.path.join(os.path.dirname(meta_path), f"{base_name}.pdf")
            if os.path.exists(pdf_path):
                return os.path.getmtime(pdf_path)
            if os.path.exists(meta_path):
                return os.path.getmtime(meta_path)
            return 0

        ordered_tasks.sort(key=get_mtime, reverse=True)

        total_to_process = len(ordered_tasks)
        if limit is not None:
            self.max_to_evaluate = min(total_to_process, limit)
        else:
            self.max_to_evaluate = total_to_process

        if self.max_to_evaluate > 0:
            self._print_evaluator_progress(0, self.max_to_evaluate)
            
        for branch, meta_path, reason in ordered_tasks:
            if self.evaluated_in_session >= self.max_to_evaluate:
                break
                
            file_name = os.path.basename(meta_path)
            base_name = file_name.replace("_meta.json", "")
            target_path = os.path.dirname(meta_path)
            txt_path = os.path.join(target_path, f"{base_name}.txt")
            
            self._log(f"   🧠 Model analyzing constraints for: {base_name[:40]}... (Reason: {reason})")
            
            with open(txt_path, "r", encoding="utf-8") as f:
                raw_doc_text = f.read()
                
            boolean_criteria = self._get_branch_requirement_from_json(branch)
            active_version = self._get_branch_version_from_json(branch)
            branch_obj = self._get_branch_by_name(branch)
            branch_vocab = branch_obj.get("vocabulary", []) if branch_obj else []
            
            ai_verdict = self.evaluate_document(raw_doc_text, boolean_criteria, categories=categories, branch_vocab=branch_vocab)
            if not ai_verdict:
                self._log(f"      ⚠️ MODEL ERROR: Local LLM failed to output valid JSON structure. Skipping file.")
                self._print_evaluator_progress(self.evaluated_in_session, self.max_to_evaluate)
                continue
                
            with open(meta_path, "r", encoding="utf-8") as f:
                meta_card = json.load(f)
                
            meta_card["evaluated_under_version"] = active_version
            meta_card["agent_relevance_eval"] = {
                "is_evaluated": True,
                "is_relevant": ai_verdict.get("is_relevant", False),
                "confidence_score": ai_verdict.get("confidence_score", 0.0),
                "reasoning_summary": ai_verdict.get("reasoning_summary", ""),
                "short_summary": ai_verdict.get("short_summary", "")
            }
            
            if "semantic_tags" not in meta_card:
                meta_card["semantic_tags"] = {}
                
            for cat in ai_categories:
                field_name = cat["path"][-1]
                meta_card["semantic_tags"][field_name] = ai_verdict.get(field_name, [])
                
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta_card, f, indent=4, ensure_ascii=False)
                
            self.session_evaluations.append((branch, base_name, reason))
            self.evaluated_in_session += 1
            
            if branch_obj:
                if "vocabulary" not in branch_obj:
                    branch_obj["vocabulary"] = []
                branch_vocab = branch_obj["vocabulary"]
                existing_vocab_lower = {v.lower().strip() for v in branch_vocab}
                added_any = False
                for cat in ai_categories:
                    field_name = cat["path"][-1]
                    tags = ai_verdict.get(field_name, [])
                    if isinstance(tags, list):
                        for tag in tags:
                            if isinstance(tag, str):
                                cleaned = tag.strip()
                                if cleaned and cleaned.lower() not in existing_vocab_lower:
                                    branch_vocab.append(cleaned)
                                    existing_vocab_lower.add(cleaned.lower())
                                    added_any = True
                if added_any:
                    self._save_config()
                    self._log(f"      🆕 Updated branch vocabulary in config with new tags: {branch_vocab}")
                    
            status_emoji = "✅ MATCH" if ai_verdict.get("is_relevant") else "❌ REJECT"
            self._log(f"      {status_emoji} ({ai_verdict.get('confidence_score', 0.0)}): {ai_verdict.get('reasoning_summary', '')}")
            
            self._print_evaluator_progress(self.evaluated_in_session, self.max_to_evaluate)
            
        if self.max_to_evaluate > 0:
            safe_write("\n")

        # Logging
        if self.session_evaluations:
            import datetime
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, "evaluator.log")
            now = datetime.datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"[{date_str}]\n")
                evals_by_branch = {}
                for branch, base_name, reason in self.session_evaluations:
                    if branch not in evals_by_branch:
                        evals_by_branch[branch] = []
                    evals_by_branch[branch].append((base_name, reason))
                
                for branch, items in evals_by_branch.items():
                    f.write(f"\t[{time_str}] Branch: {branch}\n")
                    for base_name, reason in items:
                        f.write(f"\t[{time_str}]   - Evaluated: {base_name} (Reason: {reason})\n")
                f.write("\n")

if __name__ == "__main__":
    evaluator = LocalAIEvaluator(model_name="deepseek-r1:14b")
    evaluator.evaluate_all_new_sidecars()
    print("\n🏁 AI semantic processing complete. Metadata tracking indexes updated.")
