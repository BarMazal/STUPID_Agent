# # # # import os
# # # # import json
# # # # import requests

# # # # class ConfigurationLogicController:
# # # #     def __init__(self, config_path: str = "./targets_config.json", ollama_url: str = "http://localhost:11434", model_name: str = "deepseek-r1:14b"):
# # # #         self.config_path = config_path
# # # #         self.ollama_url = ollama_url
# # # #         self.model_name = model_name
# # # #         self.config = self._load_config()

# # # #     def _load_config(self) -> dict:
# # # #         if os.path.exists(self.config_path):
# # # #             with open(self.config_path, "r", encoding="utf-8") as f:
# # # #                 return json.load(f)
# # # #         return {"global_sources": ["arxiv", "duckduckgo"], "branches": []}

# # # #     def _save_config(self):
# # # #         with open(self.config_path, "w", encoding="utf-8") as f:
# # # #             json.dump(self.config, f, indent=4)

# # # #     def get_all_branches(self) -> list:
# # # #         return self.config.get("branches", [])

# # # #     def get_branch_by_name(self, name: str) -> dict:
# # # #         for b in self.config.get("branches", []):
# # # #             if b["name"] == name.lower().strip():
# # # #                 return b
# # # #         return None

# # # #     # =====================================================================
# # # #     # 🧠 COGNITIVE REASONING LAYER (AI CHANGE GUARDRAIL)
# # # #     # =====================================================================
# # # #     def reason_over_change(self, proposed_action: str, target_context: str, data_payload: str) -> dict:
# # # #         """Connects to local AI to analyze if user configuration changes are redundant or broken."""
# # # #         system_prompt = "You are a senior data architect. Analyze the proposed workspace schema modification for inefficiencies or gaps. You must respond in strict JSON only."
        
# # # #         user_prompt = f"""Review this proposed configuration update for an academic research pipeline.
        
# # # # CURRENT SYSTEM SCHEMA MATRIX:
# # # # {json.dumps(self.config, indent=2)}

# # # # PROPOSED ACTION OPERATION: {proposed_action} (Target: {target_context})
# # # # PROPOSED NEW VALUE INPUT: "{data_payload}"

# # # # TASK:
# # # # Determine if this change causes inefficiencies (like duplicating an existing branch or creating an unstable, overly broad rule). 
# # # # If it is completely fine, set "is_issue" to false. 
# # # # If there is an overlap or design gap, set "is_issue" to true, write a clear warning, and provide choices.

# # # # YOU MUST RETURN EXACTLY THIS JSON:
# # # # {{
# # # #     "is_issue": true or false,
# # # #     "warning_message": "Clear explanation of the inefficiency or structural gap.",
# # # #     "suggested_fix": "Description of the best architectural solution.",
# # # #     "action_choices": [
# # # #         {{"key": "1", "label": "Keep it anyway (Force Override)"}},
# # # #         {{"key": "2", "label": "Apply the suggested fix instead"}}
# # # #     ]
# # # # }}"""
# # # #         try:
# # # #             response = requests.post(
# # # #                 f"{self.ollama_url}/api/generate",
# # # #                 json={
# # # #                     "model": self.model_name,
# # # #                     "system": system_prompt,
# # # #                     "prompt": user_prompt,
# # # #                     "format": "json",
# # # #                     "stream": False,
# # # #                     "options": {"temperature": 0.0}
# # # #                 },
# # # #                 timeout=45
# # # #             )
# # # #             if response.status_code == 200:
# # # #                 text = response.json().get("response", "{}")
# # # #                 if "</think>" in text: text = text.split("</think>")[-1].strip()
# # # #                 return json.loads(text)
# # # #         except Exception:
# # # #             pass
# # # #         return {"is_issue": False} # Fallback safety slip if offline

# # # #     # =====================================================================
# # # #     # MUTATION EXECUTORS (Only fired after user approval gates clear)
# # # #     # =====================================================================
# # # #     def commit_new_branch(self, name: str, requirement: str = ""):
# # # #         clean_name = name.strip().lower().replace(" ", "_")
# # # #         new_branch = {
# # # #             "name": clean_name,
# # # #             "criteria_version": 1,
# # # #             "search_phrases": [],
# # # #             "sources": [],
# # # #             "semantic_requirement": requirement.strip()
# # # #         }
# # # #         self.config["branches"].append(new_branch)
# # # #         self._save_config()

# # # #     def commit_phrase(self, branch_name: str, phrase: str):
# # # #         b = self.get_branch_by_name(branch_name)
# # # #         if b and phrase.strip() not in b["search_phrases"]:
# # # #             b["search_phrases"].append(phrase.strip())
# # # #             self._save_config()

# # # #     def commit_requirement(self, branch_name: str, requirement: str):
# # # #         b = self.get_branch_by_name(branch_name)
# # # #         if b:
# # # #             b["semantic_requirement"] = requirement.strip()
# # # #             b["criteria_version"] = b.get("criteria_version", 1) + 1
# # # #             self._save_config()

# # # #     def delete_branch_by_name(self, branch_name: str):
# # # #         self.config["branches"] = [b for b in self.config["branches"] if b["name"] != branch_name.lower().strip()]
# # # #         self._save_config()

# # # import os
# # # import json
# # # import requests

# # # class ConfigurationLogicController:
# # #     def __init__(self, config_path: str = "./targets_config.json", ollama_url: str = "http://localhost:11434", model_name: str = "deepseek-r1:14b"):
# # #         self.config_path = config_path
# # #         self.ollama_url = ollama_url
# # #         self.model_name = model_name
# # #         self.config = self._load_config()

# # #     def _load_config(self) -> dict:
# # #         if os.path.exists(self.config_path):
# # #             with open(self.config_path, "r", encoding="utf-8") as f:
# # #                 return json.load(f)
# # #         return {"global_sources": ["arxiv", "duckduckgo"], "branches": []}

# # #     def _save_config(self):
# # #         with open(self.config_path, "w", encoding="utf-8") as f:
# # #             json.dump(self.config, f, indent=4)

# # #     def get_all_branches(self) -> list:
# # #         return self.config.get("branches", [])

# # #     def get_branch_by_name(self, name: str) -> dict:
# # #         for b in self.config.get("branches", []):
# # #             if b["name"] == name.lower().strip():
# # #                 return b
# # #         return None

# # #     # =====================================================================
# # #     # 🧠 COGNITIVE STRATEGIC GENERATOR (THE DECISION MAKER)
# # #     # =====================================================================
# # #     def generate_assist_suggestions(self, context_tier: str, user_idea: str) -> dict:
# # #         """
# # #         Analyzes the user's free-form idea against the current system configuration matrix.
# # #         Autonomously decides whether to ENHANCE an existing branch or SPAWN a new one.
# # #         """
# # #         system_prompt = (
# # #             "You are an enterprise AI data architect. You must evaluate the user's semantic intent "
# # #             "against the existing database configuration and choose the most efficient integration path. "
# # #             "Respond in strict JSON only."
# # #         )
        
# # #         user_prompt = f"""Analyze this high-level research intent paragraph. Determine if we should ENHANCE an existing branch or SPAWN a brand new one.
        
# # # CURRENT REGISTERED ACTIVE BRANCHES:
# # # {json.dumps(self.config.get("branches", []), indent=2)}

# # # USER INTENT PROSE:
# # # "{user_idea}"

# # # CONTEXT CONSTRAINT: {context_tier}

# # # TASK DIRECTION:
# # # 1. Review the existing branches. If the user's idea heavily overlaps with an existing branch, set "recommended_strategy" to "ENHANCE", specify that branch's name in "target_branch_name", and provide updated keywords and rules to merge into it.
# # # 2. If the idea is novel and does not map to current lines, set "recommended_strategy" to "CREATE_NEW", choose a clean snake_case "suggested_branch_name", and generate complete keywords and rules.

# # # YOU MUST RETURN EXACTLY THIS JSON STRUCTURE:
# # # {{
# # #     "recommended_strategy": "ENHANCE" or "CREATE_NEW",
# # #     "architectural_rationale": "Clear logical explanation of why a new branch is needed OR why it overlaps with an existing name.",
# # #     "target_branch_name": "name_of_existing_branch_if_enhancing_or_empty_string",
# # #     "suggested_branch_name": "clean_snake_case_name_for_new_branch_or_empty_string",
# # #     "suggested_phrases": ["phrase_variation1", "phrase_variation2", "phrase_variation3"],
# # #     "suggested_semantic_rule": "Clean Boolean logic string rule using AND, OR, NOT matching their target intent"
# # # }}"""
# # #         try:
# # #             response = requests.post(
# # #                 f"{self.ollama_url}/api/generate",
# # #                 json={
# # #                     "model": self.model_name,
# # #                     "system": system_prompt,
# # #                     "prompt": user_prompt,
# # #                     "format": "json",
# # #                     "stream": False,
# # #                     "options": {"temperature": 0.1} # Low temperature enforces structural adherence
# # #                 },
# # #                 timeout=45
# # #             )
# # #             if response.status_code == 200:
# # #                 t = response.json().get("response", "{}")
# # #                 if "</think>" in t: 
# # #                     t = t.split("</think>")[-1].strip()
# # #                 return json.loads(t)
# # #         except Exception as e:
# # #             print(f"   ⚠️ AI Inference handshake drop: {e}")
# # #         return {
# # #             "recommended_strategy": "CREATE_NEW",
# # #             "architectural_rationale": "Direct fallback routing.",
# # #             "target_branch_name": "",
# # #             "suggested_branch_name": "research_lane",
# # #             "suggested_phrases": [user_idea[:30]],
# # #             "suggested_semantic_rule": user_idea[:50]
# # #         }

# # #     # =====================================================================
# # #     # CONTEXT COMMIT ACTIONS
# # #     # =====================================================================
# # #     def commit_new_branch(self, name: str, requirement: str = ""):
# # #         clean_name = name.strip().lower().replace(" ", "_")
# # #         if not any(b["name"] == clean_name for b in self.config["branches"]):
# # #             self.config["branches"].append({
# # #                 "name": clean_name,
# # #                 "criteria_version": 1,
# # #                 "search_phrases": [],
# # #                 "sources": [],
# # #                 "semantic_requirement": requirement.strip()
# # #             })
# # #             self._save_config()

# # #     def commit_phrase(self, branch_name: str, phrase: str):
# # #         b = self.get_branch_by_name(branch_name)
# # #         if b and phrase.strip() not in b["search_phrases"]:
# # #             b["search_phrases"].append(phrase.strip())
# # #             self._save_config()

# # #     def commit_requirement(self, branch_name: str, requirement: str):
# # #         b = self.get_branch_by_name(branch_name)
# # #         if b:
# # #             b["semantic_requirement"] = requirement.strip()
# # #             b["criteria_version"] = b.get("criteria_version", 1) + 1
# # #             self._save_config()

# # #     def delete_branch_by_name(self, branch_name: str):
# # #         self.config["branches"] = [b for b in self.config["branches"] if b["name"] != branch_name.lower().strip()]
# # #         self._save_config()

# # import os
# # import json
# # import re
# # import requests
# # import time
# # import sys

# # class ConfigurationLogicController:
# #     def __init__(self, config_path: str = "./targets_config.json", ollama_url: str = "http://localhost:11434", model_name: str = "deepseek-r1:14b"):
# #         self.config_path = config_path
# #         self.ollama_url = ollama_url
# #         self.model_name = model_name
# #         self.config = self._load_config()

# #     def _load_config(self) -> dict:
# #         if os.path.exists(self.config_path):
# #             with open(self.config_path, "r", encoding="utf-8") as f:
# #                 return json.load(f)
# #         return {"global_sources": ["arxiv", "duckduckgo"], "branches": []}

# #     def _save_config(self):
# #         with open(self.config_path, "w", encoding="utf-8") as f:
# #             json.dump(self.config, f, indent=4)

# #     def get_all_branches(self) -> list:
# #         return self.config.get("branches", [])

# #     def get_branch_by_name(self, name: str) -> dict:
# #         for b in self.config.get("branches", []):
# #             if b["name"] == name.lower().strip():
# #                 return b
# #         return None

# #     # =====================================================================
# #     # 🧠 ADVANCED NON-BLOCKING STREAMING ENGINE (ANIMATION + TIMEOUT CONTROLLER)
# #     # =====================================================================
# #     def _stream_ollama_with_ui_controls(self, system: str, prompt: str, time_window_seconds: int = 45) -> dict:
# #         """Streams tokens, renders a locked loading animation, and manages user timeout gates."""
# #         payload = {
# #             "model": self.model_name,
# #             "system": system,
# #             "prompt": prompt,
# #             "format": "json",
# #             "stream": True,  # CRITICAL: Enables continuous text token delivery
# #             "options": {"temperature": 0.1, "num_ctx": 4096}
# #         }

# #         accumulated_text = ""
# #         animation_cycle = [".  ", ".. ", "..."]
# #         cycle_idx = 0
        
# #         # Start stopwatch variables
# #         start_time = time.time()
# #         last_anim_time = time.time()
        
# #         try:
# #             # Open direct binary streaming channel to the local server
# #             with requests.post(f"{self.ollama_url}/api/generate", json=payload, stream=True, timeout=10) as response:
# #                 if response.status_code != 200:
# #                     return {}

# #                 # Read JSON packets line-by-line as the background model fires them
# #                 for line in response.iter_lines():
# #                     if not line:
# #                         continue
                        
# #                     packet = json.loads(line.decode('utf-8'))
# #                     accumulated_text += packet.get("response", "")
                    
# #                     # Update local elapsed execution clock
# #                     now = time.time()
# #                     elapsed = now - start_time
                    
# #                     # Render the locked animation every 400 milliseconds
# #                     if now - last_anim_time > 0.4:
# #                         anim = animation_cycle[cycle_idx]
# #                         cycle_idx = (cycle_idx + 1) % len(animation_cycle)
# #                         # \r forces the cursor to return to start of line, writing over the previous text dots
# #                         sys.stdout.write(f"\r🧠 Thinking{anim} (Elapsed: {int(elapsed)}s)  ")
# #                         sys.stdout.flush()
# #                         last_anim_time = now

# #                     # TIMEOUT CHECKPOINT FILTER
# #                     if elapsed > time_window_seconds:
# #                         # Clean up the animation characters on screen
# #                         sys.stdout.write("\r" + " " * 50 + "\r")
# #                         sys.stdout.flush()
                        
# #                         print(f"\n⚠️  TIMEOUT GATE EXCEEDED: The local model has been reasoning for {int(elapsed)} seconds.")
# #                         print(" 👉 Your hardware needs more time to complete this strategic mapping analysis.")
# #                         choice = input(" 🤔 Do you want to let the AI think for another window? (Y/n): ").strip().lower()
                        
# #                         if choice == 'n':
# #                             print("🛑 Connection broken by user request. Terminating server task inference slot...")
# #                             return {} # Aborts stream, requests library closes network socket automatically
# #                         else:
# #                             print("🚀 Window expanded. Continuing token synthesis sequence...")
# #                             start_time = time.time() # Reset clock window for next loop cycle
# #                             last_anim_time = time.time()

# #                 # Clean up final animation line text artifacts upon smooth collection exit
# #                 sys.stdout.write("\r" + " " * 50 + "\r")
# #                 sys.stdout.flush()

# #                 # Robust check for DeepSeek thought tags if present
# #                 clean_json = accumulated_text
# #                 if "</think>" in clean_json:
# #                     clean_json = clean_json.split("</think>")[-1].strip()
                    
# #                 # Fix loose trailing block formatting errors common to streamed strings
# #                 clean_json = clean_json.strip()
# #                 return json.loads(clean_json)

# #         except Exception as e:
# #             sys.stdout.write("\r" + " " * 50 + "\r")
# #             sys.stdout.flush()
# #             # print(f"DEBUG Error caught inside streaming context channel: {e}")
# #             return {}

# #     # =====================================================================
# #     # STRATEGIC EXECUTIONS
# #     # =====================================================================
# #     def generate_assist_suggestions(self, context_tier: str, user_idea: str) -> dict:
# #         system = "You are an enterprise AI data architect. Choose the most efficient integration path. Respond in strict JSON only."
# #         prompt = f"""Analyze this research intent paragraph. Determine if we should ENHANCE an existing branch or SPAWN a brand new one.
        
# # CURRENT SCHEMA MATRIX:
# # {json.dumps(self.config.get("branches", []), indent=2)}

# # USER INTENT PROSE:
# # "{user_idea}"

# # CONTEXT CONSTRAINT: {context_tier}

# # YOU MUST RETURN EXACTLY THIS JSON STRUCTURE:
# # {{
# #     "recommended_strategy": "ENHANCE" or "CREATE_NEW",
# #     "architectural_rationale": "Reasoning data text...",
# #     "target_branch_name": "existing_branch_name_or_empty_string",
# #     "suggested_branch_name": "clean_snake_case_name_for_new_branch_or_empty_string",
# #     "suggested_phrases": ["phrase1", "phrase2"],
# #     "suggested_semantic_rule": "Boolean expression"
# # }}"""
# #         # Call our advanced custom streaming method instead of a static post call!
# #         res = self._stream_ollama_with_ui_controls(system, prompt, time_window_seconds=30)
        
# #         if not res:
# #             # Safe internal configuration fallback block if completely aborted
# #             return {
# #                 "recommended_strategy": "CREATE_NEW",
# #                 "architectural_rationale": "Inference stream was halted or timed out.",
# #                 "target_branch_name": "",
# #                 "suggested_branch_name": "research_lane",
# #                 "suggested_phrases": [user_idea[:30]],
# #                 "suggested_semantic_rule": user_idea[:50]
# #             }
# #         return res

# #     def commit_new_branch(self, name: str, requirement: str = ""):
# #         clean_name = name.strip().lower().replace(" ", "_")
# #         if not any(b["name"] == clean_name for b in self.config["branches"]):
# #             self.config["branches"].append({
# #                 "name": clean_name, "criteria_version": 1, "search_phrases": [], "sources": [], "semantic_requirement": requirement.strip()
# #             })
# #             self._save_config()

# #     def commit_phrase(self, branch_name: str, phrase: str):
# #         b = self.get_branch_by_name(branch_name)
# #         if b and phrase.strip() not in b["search_phrases"]:
# #             b["search_phrases"].append(phrase.strip())
# #             self._save_config()

# #     def commit_requirement(self, branch_name: str, requirement: str):
# #         b = self.get_branch_by_name(branch_name)
# #         if b:
# #             b["semantic_requirement"] = requirement.strip()
# #             b["criteria_version"] = b.get("criteria_version", 1) + 1
# #             self._save_config()

# #     def delete_branch_by_name(self, branch_name: str):
# #         self.config["branches"] = [b for b in self.config["branches"] if b["name"] != branch_name.lower().strip()]
# #         self._save_config()

# import os
# import json
# import re
# import requests
# import time
# import sys

# class ConfigurationLogicController:
#     def __init__(self, config_path: str = "./targets_config.json", ollama_url: str = "http://localhost:11434", model_name: str = "deepseek-r1:14b"):
#         self.config_path = config_path
#         self.ollama_url = ollama_url
#         self.model_name = model_name
#         self.config = self._load_config()

#     def _load_config(self) -> dict:
#         if os.path.exists(self.config_path):
#             with open(self.config_path, "r", encoding="utf-8") as f:
#                 return json.load(f)
#         return {"global_sources": ["arxiv", "duckduckgo"], "branches": []}

#     def _save_config(self):
#         with open(self.config_path, "w", encoding="utf-8") as f:
#             json.dump(self.config, f, indent=4)

#     def get_all_branches(self) -> list:
#         return self.config.get("branches", [])

#     def get_branch_by_name(self, name: str) -> dict:
#         for b in self.config.get("branches", []):
#             if b["name"] == name.lower().strip():
#                 return b
#         return None

#     # =====================================================================
#     # 🧠 FIXED BYTE-STREAM CLOCK ENGINE (FORCES UNBUFFERED CONSOLE FLUSHING)
#     # =====================================================================
#     def _stream_ollama_with_ui_controls(self, system: str, prompt: str, time_window_seconds: int = 30) -> dict:
#         """Streams byte-by-byte to bypass OS buffering, rendering a live clock and dots."""
#         payload = {
#             "model": self.model_name,
#             "system": system,
#             "prompt": prompt,
#             "stream": True,
#             "options": {"temperature": 0.1, "num_ctx": 4096}
#         }

#         accumulated_bytes = bytearray()
#         animation_cycle = [".  ", ".. ", "..."]
#         cycle_idx = 0
        
#         start_time = time.time()
#         last_anim_time = time.time()
        
#         print() # Initial visual space
        
#         try:
#             # Open binary stream to the local background server
#             with requests.post(f"{self.ollama_url}/api/generate", json=payload, stream=True, timeout=30) as response:
#                 if response.status_code != 200:
#                     return {}

#                 # CRITICAL FIX: Read exactly 1 single byte at a time to force immediate console ticks
#                 for chunk in response.iter_content(chunk_size=1):
#                     if not chunk:
#                         continue
                        
#                     accumulated_bytes.extend(chunk)
                    
#                     now = time.time()
#                     elapsed = now - start_time
                    
#                     # Force render the clock to the console screen every 300 milliseconds
#                     if now - last_anim_time > 0.3:
#                         anim = animation_cycle[cycle_idx]
#                         cycle_idx = (cycle_idx + 1) % len(animation_cycle)
                        
#                         # Calculate hours, minutes, and seconds from the elapsed clock float
#                         hours = int(elapsed // 3600)
#                         minutes = int((elapsed % 3600) // 60)
#                         seconds = int(elapsed % 60)
                        
#                         # Format structural clock string: (00h 00m 00s)
#                         time_string = f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
                        
#                         # \r drops cursor to index 0, writing cleanly over previous output segments
#                         sys.stdout.write(f"\r🧠 Thinking{anim} ({time_string})   ")
#                         sys.stdout.flush() # Forces terminal to clear internal buffers instantly
#                         last_anim_time = now

#                     # TIMEOUT CONTROL CHECKPOINT
#                     if elapsed > time_window_seconds:
#                         # Clear active animation trace fields
#                         sys.stdout.write("\r" + " " * 60 + "\r")
#                         sys.stdout.flush()
                        
#                         print(f"\n⚠️  TIMEOUT LIMIT REACHED: The local model has been calculating for {int(elapsed)}s.")
#                         print(" 👉 Your hardware needs more time to complete this strategic mapping analysis.")
#                         choice = input(" 🤔 Do you want to let the AI continue thinking? (Y/n): ").strip().lower()
                        
#                         if choice == 'n':
#                             print("🛑 Stream aborted by user request.")
#                             return {}
#                         else:
#                             print("🚀 Allocation window extended. Continuing token tracking sync...")
#                             start_time = time.time()  # Reset stopwatch variables
#                             last_anim_time = time.time()

#                 # Clean up the console line tracking dots upon successful loop completion
#                 sys.stdout.write("\r" + " " * 60 + "\r")
#                 sys.stdout.flush()

#                 # Decode the entire collected array back into a standard Python string
#                 full_text_response = ""
                
#                 # Split raw data stream boundaries cleanly by line ends
#                 raw_lines = accumulated_bytes.decode('utf-8', errors='ignore').split('\n')
#                 for line in raw_lines:
#                     if line.strip():
#                         try:
#                             packet = json.loads(line)
#                             full_text_response += packet.get("response", "")
#                         except Exception:
#                             continue

#                 # Parse reasoning tokens out of DeepSeek payloads if present
#                 if "</think>" in full_text_response:
#                     full_text_response = full_text_response.split("</think>")[-1].strip()

#                 # Locate the marked JSON string content block using regex matches
#                 match = re.search(r'<JSON_START>(.*?)</JSON_START>', full_text_response, re.DOTALL)
#                 if match:
#                     return json.loads(match.group(1).strip())
#                 else:
#                     json_match = re.search(r'\{.*\}', full_text_response, re.DOTALL)
#                     if json_match:
#                         return json.loads(json_match.group(0))
                        
#         except Exception as e:
#             sys.stdout.write("\r" + " " * 60 + "\r")
#             sys.stdout.flush()
#             print(f"\n❌ Network pipeline stream anomaly: {e}")
            
#         return {}

#     # =====================================================================
#     # STRATEGIC EXECUTIONS
#     # =====================================================================
#     def generate_assist_suggestions(self, context_tier: str, user_idea: str) -> dict:
#         system = (
#             "You are an enterprise AI data architect. Choose the most efficient integration path. "
#             "You MUST wrap your final output variables inside structural text tags exactly like this: "
#             "<JSON_START> {\"your_json_keys\": ...} </JSON_START>"
#         )
        
#         prompt = f"""Analyze this research intent paragraph against our active branch collection layout.
# Determine if we should ENHANCE an existing branch or SPAWN a brand new one.

# CURRENT REGISTERED ACTIVE BRANCHES:
# {json.dumps(self.config.get("branches", []), indent=2)}

# USER INTENT PROSE:
# "{user_idea}"

# CONTEXT CONSTRAINT: {context_tier}

# YOU MUST RETURN EXACTLY THIS JSON STRUCTURE WRAPPED INSIDE THE REQUESTED TEXT TAG MAPS:
# <JSON_START>
# {{
#     "recommended_strategy": "ENHANCE" or "CREATE_NEW",
#     "architectural_rationale": "Clear context explanation string...",
#     "target_branch_name": "existing_branch_name_if_enhancing_or_empty_string",
#     "suggested_branch_name": "clean_snake_case_name_for_new_branch_or_empty_string",
#     "suggested_phrases": ["phrase1", "phrase2", "phrase3"],
#     "suggested_semantic_rule": "Clean Boolean logic string rule using AND, OR, NOT matching their intent"
# }}
# </JSON_START>"""

#         # Set the internal checking timeout gate window to 25 seconds for clear human verification
#         res = self._stream_ollama_with_ui_controls(system, prompt, time_window_seconds=25)
        
#         if not res:
#             return {
#                 "recommended_strategy": "CREATE_NEW",
#                 "architectural_rationale": "Inference streaming pipeline was halted or timed out.",
#                 "target_branch_name": "",
#                 "suggested_branch_name": "research_lane",
#                 "suggested_phrases": [user_idea[:30]],
#                 "suggested_semantic_rule": user_idea[:50]
#             }
#         return res

#     def commit_new_branch(self, name: str, requirement: str = ""):
#         clean_name = name.strip().lower().replace(" ", "_")
#         if not any(b["name"] == clean_name for b in self.config["branches"]):
#             self.config["branches"].append({
#                 "name": clean_name, "criteria_version": 1, "search_phrases": [], "sources": [], "semantic_requirement": requirement.strip()
#             })
#             self._save_config()

#     def commit_phrase(self, branch_name: str, phrase: str):
#         b = self.get_branch_by_name(branch_name)
#         if b and phrase.strip() not in b["search_phrases"]:
#             b["search_phrases"].append(phrase.strip())
#             self._save_config()

#     def commit_requirement(self, branch_name: str, requirement: str):
#         b = self.get_branch_by_name(branch_name)
#         if b:
#             b["semantic_requirement"] = requirement.strip()
#             b["criteria_version"] = b.get("criteria_version", 1) + 1
#             self._save_config()

#     def delete_branch_by_name(self, branch_name: str):
#         self.config["branches"] = [b for b in self.config["branches"] if b["name"] != branch_name.lower().strip()]
#         self._save_config()

import os
import json
import re
import requests
import time
import sys
import shutil

class ConfigurationLogicController:
    def __init__(self, config_path: str = "./Configuration/targets_config.json", ollama_url: str = "http://localhost:11434", model_name: str = "deepseek-r1:14b"):
        self.config_path = config_path
        self.ollama_url = ollama_url
        self.model_name = model_name
        self.config = self._load_config()

    def _load_config(self) -> dict:
        config_dir = os.path.dirname(self.config_path)
        if config_dir:
            os.makedirs(config_dir, exist_ok=True)
            
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                if isinstance(loaded, dict) and "categories" in loaded:
                    existing_keys = {c["key"] for c in loaded["categories"] if "key" in c}
                    default_cats = [
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
                    ]
                    modified = False
                    for default_cat in default_cats:
                        if default_cat["key"] not in existing_keys:
                            loaded["categories"].append(default_cat)
                            modified = True
                    if modified:
                        with open(self.config_path, "w", encoding="utf-8") as f:
                            json.dump(loaded, f, indent=4, ensure_ascii=False)
                return loaded
            except Exception:
                pass
                
        default_config = {
            "global_sources": ["arxiv", "duckduckgo"],
            "categories": [
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
            ],
            "branches": []
        }
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        return default_config

    def _save_config(self):
        config_dir = os.path.dirname(self.config_path)
        if config_dir:
            os.makedirs(config_dir, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def get_all_branches(self) -> list:
        return self.config.get("branches", [])

    def get_branch_by_name(self, name: str) -> dict:
        for b in self.config.get("branches", []):
            if b["name"] == name.lower().strip():
                return b
        return None

    # def _stream_ollama_with_ui_controls(self, system: str, prompt: str, time_window_seconds: int = 30) -> dict:
    #     payload = {
    #         "model": self.model_name,
    #         "system": system,
    #         "prompt": prompt,
    #         "stream": True,
    #         "options": {"temperature": 0.1, "num_ctx": 4096}
    #     }

    #     full_text_response = ""
    #     animation_cycle = [".  ", ".. ", "..."]
    #     cycle_idx = 0
        
    #     start_time = time.time()
    #     last_anim_time = time.time()
        
    #     print()
        
    #     try:
    #         with requests.post(f"{self.ollama_url}/api/generate", json=payload, stream=True, timeout=30) as response:
    #             if response.status_code != 200:
    #                 return {}

    #             for line in response.iter_lines():
    #                 if not line:
    #                     continue
                        
    #                 packet = json.loads(line.decode('utf-8'))
    #                 token = packet.get("response", "")
    #                 full_text_response += token
                    
    #                 now = time.time()
    #                 elapsed = now - start_time
                    
    #                 if now - last_anim_time > 0.3:
    #                     anim = animation_cycle[cycle_idx]
    #                     cycle_idx = (cycle_idx + 1) % len(animation_cycle)
                        
    #                     hours = int(elapsed // 3600)
    #                     minutes = int((elapsed % 3600) // 60)
    #                     seconds = int(elapsed % 60)
    #                     time_string = f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
                        
    #                     sys.stdout.write(f"\r🧠 Thinking{anim} ({time_string})   ")
    #                     sys.stdout.flush()
    #                     last_anim_time = now

    #                 if elapsed > time_window_seconds:
    #                     sys.stdout.write("\r" + " " * 60 + "\r")
    #                     sys.stdout.flush()
                        
    #                     print(f"\n⚠️ TIMEOUT LIMIT REACHED: AI has been reasoning for {int(elapsed)} seconds.")
    #                     choice = input(" 🤔 Do you want to let the AI continue thinking? (Y/n): ").strip().lower()
                        
    #                     if choice == 'n':
    #                         return {}
    #                     else:
    #                         start_time = time.time()
    #                         last_anim_time = time.time()

    #             sys.stdout.write("\r" + " " * 60 + "\r")
    #             sys.stdout.flush()

    #             if "</think>" in full_text_response:
    #                 full_text_response = full_text_response.split("</think>")[-1].strip()

    #             match = re.search(r'<JSON_START>(.*?)</JSON_START>', full_text_response, re.DOTALL)
    #             if match:
    #                 return json.loads(match.group(1).strip())
    #             else:
    #                 json_match = re.search(r'\{.*\}', full_text_response, re.DOTALL)
    #                 if json_match:
    #                     return json.loads(json_match.group(0))
                        
    #     except Exception:
    #         pass
            
    #     return {}

    def _stream_ollama_with_ui_controls(self, system: str, prompt: str, time_window_seconds: int = 120) -> dict:
        """Launches the stopwatch instantly and accumulates time continuously across window extensions."""
        payload = {
            "model": self.model_name,
            "system": system,
            "prompt": prompt,
            "stream": True,
            "options": {"temperature": 0.1, "num_ctx": 4096}
        }

        full_text_response = ""
        animation_cycle = [".  ", ".. ", "..."]
        cycle_idx = 0
        
        # Absolute start time to ensure the clock never resets
        absolute_start_time = time.time()
        # Track total elapsed time accumulated across extensions
        accumulated_elapsed_time = 0.0
        
        last_anim_time = time.time()
        current_window_start = time.time()
        
        print()  # Visual layout buffer space
        
        # Immediately print the initial thinking status
        sys.stdout.write("\r🧠 Thinking. (00h 00m 00s)   ")
        sys.stdout.flush()
        
        try:
            # 1. Establish the network stream connection
            response_stream = requests.post(f"{self.ollama_url}/api/generate", json=payload, stream=True, timeout=30)
            if response_stream.status_code != 200:
                print(f"❌ Connection error: Status code {response_stream.status_code}")
                return {}

            # 2. Extract lines from response stream
            lines_iterator = response_stream.iter_lines()
            
            # Continuous processing loop
            while True:
                now = time.time()
                
                # Calculate absolute continuous elapsed time string format
                total_elapsed = (now - absolute_start_time) + accumulated_elapsed_time
                hours = int(total_elapsed // 3600)
                minutes = int((total_elapsed % 3600) // 60)
                seconds = int(total_elapsed % 60)
                time_string = f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
                
                # Calculate current temporary window check duration
                current_window_duration = now - current_window_start
                
                # INSTANT REFRESH: Force render animation frames even while network line data is empty
                if now - last_anim_time > 0.3:
                    anim = animation_cycle[cycle_idx]
                    cycle_idx = (cycle_idx + 1) % len(animation_cycle)
                    sys.stdout.write(f"\r🧠 Thinking{anim} ({time_string})   ")
                    sys.stdout.flush()
                    last_anim_time = now

                # TIMEOUT REASONING WINDOW FILTER GATES
                if current_window_duration > time_window_seconds:
                    sys.stdout.write("\r" + " " * 60 + "\r")
                    sys.stdout.flush()
                    
                    print(f"\n⚠️  TIMEOUT GATE EXCEEDED: The model has been processing for {int(total_elapsed)} seconds.")
                    print(" 👉 Your hardware needs more time to compile this multi-tenant layout matrix.")
                    choice = input(" 🤔 Do you want to extend this reasoning session? (Y/n): ").strip().lower()
                    
                    if choice == 'n':
                        print("🛑 Session aborted by user command input request.")
                        response_stream.close()
                        return {}
                    else:
                        print("🚀 Window limits extended. Continuing token tracking sequence...")
                        # Reset temporary current window clock, but maintain the absolute running time tracking
                        current_window_start = time.time()
                        last_anim_time = time.time()
                        continue

                # Non-blocking fetch for the next incoming data segment line chunk
                try:
                    # Capture next line element from generator sequence stream
                    line = next(lines_iterator, None)
                    if line:
                        packet = json.loads(line.decode('utf-8'))
                        token = packet.get("response", "")
                        full_text_response += token
                    else:
                        # If line is None, the model has finished sending packets cleanly
                        break
                except StopIteration:
                    break
                except Exception:
                    # Safe loop cycle continuation step to prioritize animation renders if stream temporarily buffers
                    time.sleep(0.05)

            # Clear trailing console traces when loop completes smoothly
            sys.stdout.write("\r" + " " * 60 + "\r")
            sys.stdout.flush()

            if "</think>" in full_text_response:
                full_text_response = full_text_response.split("</think>")[-1].strip()

            match = re.search(r'<JSON_START>(.*?)</JSON_START>', full_text_response, re.DOTALL)
            if match:
                return json.loads(match.group(1).strip())
            else:
                json_match = re.search(r'\{.*\}', full_text_response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(0))
                        
        except Exception as e:
            sys.stdout.write("\r" + " " * 60 + "\r")
            sys.stdout.flush()
            print(f"\n❌ Pipeline streaming anomaly: {e}")
            
        return {}


    def generate_assist_suggestions(self, context_tier: str, user_idea: str) -> dict:
        system = "You are an enterprise AI data architect. Choose the most efficient integration path. You MUST wrap your final output variable dictionary inside structural text tags exactly like this: <JSON_START> {\"your_json_keys\": ...} </JSON_START>"
        prompt = f"Analyze this research intent paragraph against our active branch collection layout mapping list.\nDetermine if we should ENHANCE an existing branch or SPAWN a brand new one.\n\nCURRENT REGISTERED ACTIVE BRANCHES:\n{json.dumps(self.config.get('branches', []), indent=2)}\n\nUSER INTENT PROSE:\n\"{user_idea}\"\n\nCONTEXT CONSTRAINT: {context_tier}\n\nYOU MUST RETURN EXACTLY THIS JSON STRUCTURE WRAPPED INSIDE THE REQUESTED TEXT TAG MAPS:\n<JSON_START>\n{{\n    \"recommended_strategy\": \"ENHANCE\" or \"CREATE_NEW\",\n    \"architectural_rationale\": \"Context explanation...\",\n    \"target_branch_name\": \"existing_branch_name_or_empty_string\",\n    \"suggested_branch_name\": \"clean_snake_case_name_or_empty_string\",\n    \"suggested_phrases\": [\"phrase1\", \"phrase2\"],\n    \"suggested_semantic_rule\": \"Boolean expression\"\n}}\n</JSON_START>"

        res = self._stream_ollama_with_ui_controls(system, prompt, time_window_seconds=120)
        if not res:
            return {
                "recommended_strategy": "CREATE_NEW", "architectural_rationale": "Timeout fallback.", "target_branch_name": "",
                "suggested_branch_name": "research_lane", "suggested_phrases": [user_idea[:30]], "suggested_semantic_rule": user_idea[:50]
            }
        return res

    def generate_semantic_rule_suggestion(self, branch_name: str, existing_phrases: list, existing_rules: list, article_snippets: list) -> dict:
        system = "You are a principal research assistant. Suggest a new, high-quality, complementary semantic rule. You MUST wrap your final output variable dictionary inside structural text tags exactly like this: <JSON_START> {\"suggested_semantic_rule\": ..., \"architectural_rationale\": ...} </JSON_START>"
        
        prompt = f"""We are managing a research branch called "{branch_name}".
        
ACTIVE SEARCH KEYWORDS:
{json.dumps(existing_phrases, indent=2)}

EXISTING SEMANTIC RULES:
{json.dumps(existing_rules, indent=2)}

SAMPLE OF DOWNLOADED ARTICLES IN THIS BRANCH:
{json.dumps(article_snippets, indent=2)}

TASK:
Analyze the branch's keywords, current rules, and sample articles. Formulate a single new semantic requirement rule (e.g. Boolean logic or plain language description) that refines or extends the filtering focus. Do not repeat existing rules.

YOU MUST RETURN EXACTLY THIS JSON STRUCTURE WRAPPED INSIDE THE REQUESTED TEXT TAG MAPS:
<JSON_START>
{{
    "suggested_semantic_rule": "The formulated new rule string.",
    "architectural_rationale": "Brief explanation of why this rule is suggested based on the context."
}}
</JSON_START>"""

        res = self._stream_ollama_with_ui_controls(system, prompt, time_window_seconds=120)
        return res

    def commit_new_branch(self, name: str, requirement: str = ""):
        clean_name = name.strip().lower().replace(" ", "_")
        if not any(b["name"] == clean_name for b in self.config["branches"]):
            self.config["branches"].append({
                "name": clean_name, "criteria_version": 1, "search_phrases": [], "sources": [], "semantic_requirement": requirement.strip()
            })
            self._save_config()

    def commit_phrase(self, branch_name: str, phrase: str):
        b = self.get_branch_by_name(branch_name)
        if b and phrase.strip() and (phrase.strip() not in b["search_phrases"]):
            b["search_phrases"].append(phrase.strip())
            self._save_config()

    def commit_requirement(self, branch_name: str, requirement: str):
        b = self.get_branch_by_name(branch_name)
        if b:
            b["semantic_requirement"] = requirement.strip()
            b["criteria_version"] = b.get("criteria_version", 1) + 1
            self._save_config()

    def delete_branch_by_name(self, branch_name: str):
        branch_name_clean = branch_name.lower().strip()
        self.config["branches"] = [b for b in self.config["branches"] if b["name"] != branch_name_clean]
        self._save_config()
        
        # Option A: Archive deleted branch directory
        old_dir = os.path.join("./downloaded_research", branch_name_clean)
        if os.path.exists(old_dir) and os.path.isdir(old_dir):
            archive_parent = "./Archive/deleted_branches"
            os.makedirs(archive_parent, exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            archive_dir = os.path.join(archive_parent, f"{branch_name_clean}_{timestamp}")
            try:
                shutil.move(old_dir, archive_dir)
                print(f"📦 Archived deleted branch directory to: '{archive_dir}'")
            except Exception as e:
                print(f"⚠️ Failed to archive deleted branch directory: {e}")

    def rename_branch(self, old_name: str, new_name: str) -> bool:
        old_name = old_name.lower().strip()
        new_name = new_name.lower().strip().replace(" ", "_")
        if not new_name:
            return False
        if any(b["name"] == new_name for b in self.config["branches"]):
            return False
        b = self.get_branch_by_name(old_name)
        if b:
            b["name"] = new_name
            b["criteria_version"] = b.get("criteria_version", 1) + 1
            self._save_config()
            old_dir = os.path.join("./downloaded_research", old_name)
            new_dir = os.path.join("./downloaded_research", new_name)
            if os.path.exists(old_dir) and os.path.isdir(old_dir):
                # Option A: Archive old directory state under renamed_branches backup (moves it off the active path)
                archive_parent = "./Archive/renamed_branches"
                os.makedirs(archive_parent, exist_ok=True)
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                archive_dir = os.path.join(archive_parent, f"{old_name}_renamed_to_{new_name}_{timestamp}")
                try:
                    shutil.move(old_dir, archive_dir)
                    print(f"📦 Archived renamed branch directory backup to: '{archive_dir}'")
                except Exception as e:
                    print(f"⚠️ Failed to archive renaming branch backup: {e}")
            return True
        return False

    def delete_phrase(self, branch_name: str, phrase: str) -> bool:
        b = self.get_branch_by_name(branch_name)
        if b and phrase in b.get("search_phrases", []):
            b["search_phrases"].remove(phrase)
            self._save_config()
            return True
        return False

    def update_phrase(self, branch_name: str, old_phrase: str, new_phrase: str) -> bool:
        b = self.get_branch_by_name(branch_name)
        if b and old_phrase in b.get("search_phrases", []):
            idx = b["search_phrases"].index(old_phrase)
            b["search_phrases"][idx] = new_phrase.strip()
            self._save_config()
            return True
        return False

    def get_semantic_requirements(self, branch_name: str) -> list:
        b = self.get_branch_by_name(branch_name)
        if b:
            if "semantic_requirements" not in b:
                b["semantic_requirements"] = []
                if b.get("semantic_requirement"):
                    b["semantic_requirements"].append(b["semantic_requirement"])
            return b["semantic_requirements"]
        return []

    def add_semantic_requirement(self, branch_name: str, requirement: str) -> bool:
        b = self.get_branch_by_name(branch_name)
        if b:
            # Trigger get list to initialize it if needed
            reqs = self.get_semantic_requirements(branch_name)
            reqs.append(requirement.strip())
            b["semantic_requirements"] = reqs
            b["criteria_version"] = b.get("criteria_version", 1) + 1
            self._save_config()
            return True
        return False

    def update_semantic_requirement(self, branch_name: str, index: int, new_requirement: str) -> bool:
        b = self.get_branch_by_name(branch_name)
        if b:
            reqs = self.get_semantic_requirements(branch_name)
            if 0 <= index < len(reqs):
                reqs[index] = new_requirement.strip()
                b["semantic_requirements"] = reqs
                b["criteria_version"] = b.get("criteria_version", 1) + 1
                self._save_config()
                return True
        return False

    def delete_semantic_requirement(self, branch_name: str, index: int) -> bool:
        b = self.get_branch_by_name(branch_name)
        if b:
            reqs = self.get_semantic_requirements(branch_name)
            if 0 <= index < len(reqs):
                del reqs[index]
                b["semantic_requirements"] = reqs
                b["criteria_version"] = b.get("criteria_version", 1) + 1
                self._save_config()
                return True
        return False

    def reset_to_factory_settings(self) -> dict:
        default_config = {
            "global_sources": ["arxiv", "duckduckgo"],
            "categories": [
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
            ],
            "branches": []
        }
        self.config = default_config
        self._save_config()
        return default_config

    def get_categories(self) -> list:
        if "categories" not in self.config:
            self.config["categories"] = [
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
            ]
            self._save_config()
        return self.config["categories"]

    def add_custom_category(self, key: str, label: str, description: str) -> bool:
        key = key.lower().strip().replace(" ", "_")
        if not key:
            return False
        cats = self.get_categories()
        if any(c["key"] == key for c in cats):
            return False
        new_cat = {
            "key": key,
            "label": label.strip(),
            "source": "ai",
            "path": ["semantic_tags", key],
            "description": description.strip()
        }
        cats.append(new_cat)
        self._save_config()
        return True

    def remove_custom_category(self, key: str) -> bool:
        key = key.lower().strip()
        cats = self.get_categories()
        target = next((c for c in cats if c["key"] == key), None)
        if target and target.get("source") != "system":
            self.config["categories"] = [c for c in cats if c["key"] != key]
            self._save_config()
            return True
        return False

    def get_global_sources(self) -> list:
        if "global_sources" not in self.config:
            self.config["global_sources"] = ["arxiv", "duckduckgo"]
            self._save_config()
        return self.config["global_sources"]

    def add_global_source(self, source: str) -> bool:
        source = source.strip().lower()
        if not source:
            return False
        sources = self.get_global_sources()
        if source not in sources:
            sources.append(source)
            self._save_config()
            return True
        return False

    def remove_global_source(self, source: str) -> bool:
        source = source.strip().lower()
        sources = self.get_global_sources()
        if source in sources:
            sources.remove(source)
            self._save_config()
            return True
        return False

    def add_source_to_branch(self, branch_name: str, source: str) -> bool:
        b = self.get_branch_by_name(branch_name)
        if b:
            if "sources" not in b:
                b["sources"] = []
            source = source.strip().lower()
            if source and source not in b["sources"]:
                b["sources"].append(source)
                self._save_config()
                return True
        return False

    def delete_source_from_branch(self, branch_name: str, source: str) -> bool:
        b = self.get_branch_by_name(branch_name)
        if b and "sources" in b:
            source = source.strip().lower()
            if source in b["sources"]:
                b["sources"].remove(source)
                self._save_config()
                return True
        return False


