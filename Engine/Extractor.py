import os
import re
import json
from datetime import datetime
from pypdf import PdfReader

class FileBundleExtractor:
    def __init__(self, storage_root: str = "./downloaded_research"):
        self.storage_root = storage_root
        self.session_extractions = []

    def _print_extractor_progress(self, current, max_val):
        import sys
        progress_str = f"   ⏳ Progress: Extracting {current}/{max_val}"
        sys.stdout.write(f"\r{progress_str:<80}")
        sys.stdout.flush()

    def _log(self, message: str):
        import sys
        sys.stdout.write(f"\r{message:<80}\n")
        if hasattr(self, 'max_to_extract') and hasattr(self, 'extracted_in_session'):
            self._print_extractor_progress(self.extracted_in_session, self.max_to_extract)

    def _clean_text(self, text: str) -> str:
        """Fixes dual-column line breaks and formatting artifacts."""
        # Clean surrogate characters and invalid unicode points
        text = text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        # Merge hyphenated words broken across line wraps (e.g., track- \n ing -> tracking)
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
        # Normalize double spacing and structural breaks into a single continuous stream
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Opens a local PDF and extracts text page-by-page."""
        try:
            reader = PdfReader(pdf_path)
            extracted_text = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text.append(page_text)
            
            raw_full_text = "\n".join(extracted_text)
            return self._clean_text(raw_full_text)
        except Exception as e:
            print(f"   ❌ Failed to parse PDF pages: {e}")
            return ""

    def write_sidecar_bundle(self, target_path: str, file_base_name: str, clean_text: str):
        """Generates matching .txt and .json tracking cards side-by-side with the PDF."""
        txt_path = os.path.join(target_path, f"{file_base_name}.txt")
        json_path = os.path.join(target_path, f"{file_base_name}_meta.json")

        # Step A: Write the normalized text summary file if it doesn't exist or is empty
        if not os.path.exists(txt_path) or os.path.getsize(txt_path) == 0:
            with open(txt_path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(clean_text)
            self._log(f"   💾 Generated plain text sidecar: {file_base_name}.txt")

        # Step B: Write the companion structured json tracking card if it doesn't exist
        if not os.path.exists(json_path):
            # Generate a human-readable title variant from the filename string tokens
            formatted_title = file_base_name.replace("_", " ")
            
            # Baseline taxonomy tracking blueprint layout for the future AI pipeline
            meta_payload = {
                "document_id": file_base_name,
                "document_title": formatted_title,
                "processed_timestamp": datetime.now().isoformat(),
                "evaluated_under_version": 0,  # <-- NEW: Defaults to 0 (unevaluated)
                "file_metrics": {
                    "character_count": len(clean_text),
                    "estimated_words": len(clean_text.split())
                },
                "agent_relevance_eval": {
                    "is_evaluated": False,
                    "is_relevant": False,
                    "confidence_score": 0.0,
                    "reasoning_summary": "",
                    "short_summary": ""
                },
                "semantic_tags": {
                    "innovation_focus": [],
                    "methodology_branch": [],
                    "hardware_targets": []
                }
            }
            
            with open(json_path, "w", encoding="utf-8", errors="ignore") as f:
                json.dump(meta_payload, f, indent=4, ensure_ascii=False)
            self._log(f"   📋 Generated structured metadata card: {file_base_name}_meta.json")

    def process_all_targets(self, target_branch: str = None, limit: int = None, prioritized_pdfs: list = None):
        """Scans folder structure, processing new PDFs into complete sidecar bundles."""
        if not os.path.exists(self.storage_root):
            import sys
            sys.stdout.write(f"\r⚠️ Storage path missing. Run your Crawler.py file first.\n")
            sys.stdout.flush()
            return

        import sys
        sys.stdout.write("📖 Scanning repositories to generate file bundle sidecars...\n")
        sys.stdout.flush()
        
        self.session_extractions = []
        self.extracted_in_session = 0
        
        # Helper to check if a pdf needs extraction
        def needs_extraction(pdf_path):
            base_name, _ = os.path.splitext(os.path.basename(pdf_path))
            txt_path = os.path.join(os.path.dirname(pdf_path), f"{base_name}.txt")
            json_path = os.path.join(os.path.dirname(pdf_path), f"{base_name}_meta.json")
            txt_exists = os.path.exists(txt_path) and os.path.getsize(txt_path) > 0
            return not (txt_exists and os.path.exists(json_path))

        # Deduplicate and prioritize tasks
        task_seen = set()
        ordered_tasks = []
        
        # Phase 1: Prioritized downloads
        if prioritized_pdfs:
            self._log("🔗 Chaining: Prioritizing newly downloaded files from this session...")
            for branch, pdf_path in prioritized_pdfs:
                if target_branch and branch.lower() != target_branch.lower().strip():
                    continue
                if os.path.exists(pdf_path) and needs_extraction(pdf_path):
                    if pdf_path not in task_seen:
                        task_seen.add(pdf_path)
                        ordered_tasks.append((branch, pdf_path))
                        
        # Phase 2: Other scanned PDFs
        for target_name in os.listdir(self.storage_root):
            if target_branch and target_name.lower() != target_branch.lower().strip():
                continue
            target_path = os.path.join(self.storage_root, target_name)
            if os.path.isdir(target_path):
                pdf_files = [f for f in os.listdir(target_path) if f.lower().endswith(".pdf")]
                for file_name in pdf_files:
                    full_pdf_path = os.path.join(target_path, file_name)
                    if needs_extraction(full_pdf_path) and full_pdf_path not in task_seen:
                        task_seen.add(full_pdf_path)
                        ordered_tasks.append((target_name, full_pdf_path))
        # Sort tasks by modification time descending (newest first)
        ordered_tasks.sort(key=lambda t: os.path.getmtime(t[1]) if os.path.exists(t[1]) else 0, reverse=True)
        total_to_process = len(ordered_tasks)
        if limit is not None:
            self.max_to_extract = min(total_to_process, limit)
        else:
            self.max_to_extract = total_to_process

        if self.max_to_extract > 0:
            self._print_extractor_progress(0, self.max_to_extract)
            
        for branch, pdf_path in ordered_tasks:
            if self.extracted_in_session >= self.max_to_extract:
                break
                
            file_name = os.path.basename(pdf_path)
            base_name, _ = os.path.splitext(file_name)
            target_path = os.path.dirname(pdf_path)
            
            self._log(f"   🔍 Reading payload binary: {file_name[:40]}...")
            clean_content = self.extract_text_from_pdf(pdf_path)
            if clean_content:
                self.write_sidecar_bundle(target_path, base_name, clean_content)
                self.session_extractions.append((branch, file_name))
                self.extracted_in_session += 1
                
            self._print_extractor_progress(self.extracted_in_session, self.max_to_extract)
            
        if self.max_to_extract > 0:
            sys.stdout.write("\n")
            sys.stdout.flush()

        # Logging
        if self.session_extractions:
            import datetime
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, "extractor.log")
            now = datetime.datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"[{date_str}]\n")
                extractions_by_branch = {}
                for branch, file_name in self.session_extractions:
                    if branch not in extractions_by_branch:
                        extractions_by_branch[branch] = []
                    extractions_by_branch[branch].append(file_name)
                
                for branch, files in extractions_by_branch.items():
                    f.write(f"\t[{time_str}] Branch: {branch}\n")
                    for fn in files:
                        f.write(f"\t[{time_str}]   - Extracted: {fn}\n")
                f.write("\n")

# =====================================================================
# RUN BUNDLE SYSTEM TRIGGER
# =====================================================================
if __name__ == "__main__":
    extractor = FileBundleExtractor()
    extractor.process_all_targets()
    print("\n🏁 Sidecar bundle sync complete. Storage environment updated.")
