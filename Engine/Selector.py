# import os
# import json

# class HierarchicalQueryEngine:
#     def __init__(self, storage_root: str = "./downloaded_research"):
#         self.storage_root = storage_root

#     def load_all_metadata_records(self) -> list:
#         """Traverses the workspace directory and loads every processed AI metadata card."""
#         all_records = []
#         if not os.path.exists(self.storage_root):
#             return []

#         for target_name in os.listdir(self.storage_root):
#             target_path = os.path.join(self.storage_root, target_name)
#             if os.path.isdir(target_path):
#                 for file_name in os.listdir(target_path):
#                     if file_name.lower().endswith("_meta.json"):
#                         json_path = os.path.join(target_path, file_name)
#                         try:
#                             with open(json_path, "r", encoding="utf-8") as f:
#                                 record = json.load(f)
#                                 record["_branch_lineage"] = target_name
#                                 all_records.append(record)
#                         except Exception:
#                             continue
#         return all_records

#     def _get_nested_value(self, record: dict, field_path: str):
#         """Extracts deep properties or tag arrays using simple keyword shortcuts."""
#         field_map = {
#             "branch": ["_branch_lineage"],
#             "relevant": ["agent_relevance_eval", "is_relevant"],
#             "innovation": ["semantic_tags", "innovation_focus"],
#             "methodology": ["semantic_tags", "methodology_branch"]
#         }
        
#         lookup_path = field_map.get(field_path.lower().strip(), [field_path])
        
#         current_data = record
#         for key in lookup_path:
#             if isinstance(current_data, dict) and key in current_data:
#                 current_data = current_data[key]
#             else:
#                 return None
#         return current_data

#     def build_query_tree(self, records: list, conditions: list, current_depth: int = 0) -> dict:
#         """
#         Recursively splits records down into a conditional clustering tree matrix.
#         RETURNS: A standard Python nested dictionary. Zero print statements.
#         """
#         if current_depth >= len(conditions):
#             return {
#                 "type": "leaf_cluster",
#                 "papers_count": len(records),
#                 "papers": [
#                     {
#                         "id": r.get("document_id"),
#                         "title": r.get("document_title"),
#                         "summary": r.get("agent_relevance_eval", {}).get("reasoning_summary", "No summary logs available.")
#                     } for r in records
#                 ]
#             }

#         current_field = conditions[current_depth]
#         grouped_buckets = {}

#         for r in records:
#             field_value = self._get_nested_value(r, current_field)
            
#             if isinstance(field_value, list):
#                 if not field_value:
#                     field_value = ["Unassigned/None"]
#                 values_to_loop = field_value
#             else:
#                 if field_value is None:
#                     field_value = "Unassigned/None"
#                 values_to_loop = [field_value]

#             for val in values_to_loop:
#                 stringified_val = str(val)
#                 if stringified_val not in grouped_buckets:
#                     grouped_buckets[stringified_val] = []
#                 grouped_buckets[stringified_val].append(r)

#         node_branches = {}
#         for bucket_key, bucket_records in grouped_buckets.items():
#             node_branches[bucket_key] = self.build_query_tree(bucket_records, conditions, current_depth + 1)

#         return {
#             "type": "conditional_node",
#             "split_by_field": current_field,
#             "branches": node_branches
#         }
import os
import json

class HierarchicalQueryEngine:
    def __init__(self, storage_root: str = "./downloaded_research", config_path: str = "./Configuration/targets_config.json"):
        self.storage_root = storage_root
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> dict:
        try:
            from Configurator import ConfigurationLogicController
            controller = ConfigurationLogicController(config_path=self.config_path)
            return controller.config
        except Exception:
            if os.path.exists(self.config_path):
                try:
                    with open(self.config_path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    pass
            return {}

    def _print_selector_progress(self, current, max_val):
        import sys
        progress_str = f"   ⏳ Progress: Loading records {current}/{max_val}"
        sys.stdout.write(f"\r{progress_str:<80}")
        sys.stdout.flush()

    def load_all_metadata_records(self) -> list:
        all_records = []
        if not os.path.exists(self.storage_root):
            return []

        # Pre-scan to count total meta files
        meta_files = []
        for target_name in os.listdir(self.storage_root):
            target_path = os.path.join(self.storage_root, target_name)
            if os.path.isdir(target_path):
                for file_name in os.listdir(target_path):
                    if file_name.lower().endswith("_meta.json"):
                        meta_files.append((target_name, os.path.join(target_path, file_name)))

        total_files = len(meta_files)
        if total_files > 0:
            self._print_selector_progress(0, total_files)

        for idx, (target_name, json_path) in enumerate(meta_files):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    record = json.load(f)
                    record["_branch_lineage"] = target_name
                    all_records.append(record)
            except Exception:
                continue
            self._print_selector_progress(idx + 1, total_files)

        if total_files > 0:
            import sys
            sys.stdout.write("\n")
            sys.stdout.flush()

        return all_records

    def _get_nested_value(self, record: dict, field_path: str):
        categories = [
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
        if hasattr(self, 'config') and self.config and "categories" in self.config:
            categories = self.config["categories"]

        field_map = {}
        for cat in categories:
            field_map[cat["key"].lower().strip()] = cat["path"]
        
        lookup_path = field_map.get(field_path.lower().strip(), [field_path])
        current_data = record
        for key in lookup_path:
            if isinstance(current_data, dict) and key in current_data:
                current_data = current_data[key]
            else:
                return None
        return current_data

    def build_query_tree(self, records: list, conditions: list, current_depth: int = 0) -> dict:
        if current_depth == 0:
            self.config = self.load_config()
        if current_depth >= len(conditions):
            return {
                "type": "leaf_cluster", "papers_count": len(records),
                "papers": [
                    {
                        "id": r.get("document_id"), "title": r.get("document_title"),
                        "branch": r.get("_branch_lineage"),
                        "summary": r.get("agent_relevance_eval", {}).get("short_summary") or r.get("agent_relevance_eval", {}).get("reasoning_summary") or "No log summary.",
                        "attributes": {
                            cat["label"]: self._get_nested_value(r, cat["key"])
                            for cat in (self.config.get("categories", []) if hasattr(self, 'config') and self.config else [])
                        }
                    } for r in records
                ]
            }

        current_field = conditions[current_depth]
        grouped_buckets = {}

        for r in records:
            field_value = self._get_nested_value(r, current_field)
            if isinstance(field_value, list):
                if not field_value: field_value = ["Unassigned/None"]
                values_to_loop = field_value
            else:
                if field_value is None: field_value = "Unassigned/None"
                values_to_loop = [field_value]

            for val in values_to_loop:
                stringified_val = str(val)
                if stringified_val not in grouped_buckets:
                    grouped_buckets[stringified_val] = []
                grouped_buckets[stringified_val].append(r)

        node_branches = {}
        for bucket_key, bucket_records in grouped_buckets.items():
            node_branches[bucket_key] = self.build_query_tree(bucket_records, conditions, current_depth + 1)

        return {"type": "conditional_node", "split_by_field": current_field, "branches": node_branches}
