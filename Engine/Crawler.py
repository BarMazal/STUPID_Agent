# import os
# import re
# import json
# import requests
# import arxiv
# from ddgs import DDGS

# class DataDrivenIngestionEngine:
#     def __init__(self, config_path: str = "./targets_config.json", output_root: str = "./downloaded_research"):
#         self.config_path = config_path
#         self.output_root = output_root
#         os.makedirs(self.output_root, exist_ok=True)
#         self.headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#         }
#         self.config = self._load_config()

#     # =====================================================================
#     # 📑 INTERNAL CONFIGURATION REGISTRY API (CRUD Operations)
#     # =====================================================================
#     def _load_config(self) -> dict:
#         """Reads settings tracking document from disk or generates baseline fallbacks."""
#         if os.path.exists(self.config_path):
#             with open(self.config_path, "r", encoding="utf-8") as f:
#                 return json.load(f)
#         return {"global_sources": ["arxiv", "duckduckgo"], "branches": []}

#     def _save_config(self):
#         """Flushes configuration modifications directly back to disk storage."""
#         with open(self.config_path, "w", encoding="utf-8") as f:
#             json.dump(self.config, f, indent=4)

#     def add_branch(self, name: str, search_phrases: list = None, sources: list = None):
#         """API Feature: Appends a completely new research track to the ecosystem."""
#         name_clean = name.strip().lower().replace(" ", "_")
#         if any(b["name"] == name_clean for b in self.config["branches"]):
#             print(f"ℹ️ Target branch [{name_clean.upper()}] already exists.")
#             return
        
#         new_branch = {
#             "name": name_clean,
#             "search_phrases": search_phrases if search_phrases else [],
#             "sources": sources if sources else []
#         }
#         self.config["branches"].append(new_branch)
#         self._save_config()
#         print(f"✨ Successfully added branch track: [{name_clean.upper()}]")

#     def add_phrase_to_branch(self, branch_name: str, phrase: str):
#         """API Feature: Enhances search footprint by adding key phrases to a branch."""
#         for b in self.config["branches"]:
#             if b["name"] == branch_name.lower():
#                 if phrase not in b["search_phrases"]:
#                     b["search_phrases"].append(phrase)
#                     self._save_config()
#                     print(f"➕ Added search phrase '{phrase}' to branch [{branch_name.upper()}]")
#                 return
#         print(f"❌ Branch [{branch_name}] not found.")

#     def add_source_to_branch(self, branch_name: str, source: str):
#         """API Feature: Registers a target crawler engine to a specific branch."""
#         for b in self.config["branches"]:
#             if b["name"] == branch_name.lower():
#                 if source not in b["sources"]:
#                     b["sources"].append(source)
#                     self._save_config()
#                     print(f"➕ Source endpoint '{source}' mapped to branch [{branch_name.upper()}]")
#                 return
#         print(f"❌ Branch [{branch_name}] not found.")

#     def remove_phrase_from_branch(self, branch_name: str, phrase: str):
#         """API Feature: Removes an active search phrase from a target domain track."""
#         for b in self.config["branches"]:
#             if b["name"] == branch_name.lower():
#                 if phrase in b["search_phrases"]:
#                     b["search_phrases"].remove(phrase)
#                     self._save_config()
#                     print(f"🗑️ Removed search phrase '{phrase}' from branch [{branch_name.upper()}]")
#                 return
#         print(f"❌ Branch [{branch_name}] not found.")

#     def delete_branch(self, branch_name: str):
#         """API Feature: Completely deletes an entire research track from the registry."""
#         clean_name = branch_name.lower().strip()
#         initial_count = len(self.config["branches"])
        
#         # Keep every branch EXCEPT the one we want to eliminate
#         self.config["branches"] = [b for b in self.config["branches"] if b["name"] != clean_name]
        
#         if len(self.config["branches"]) < initial_count:
#             self._save_config()
#             print(f"💥 Completely deleted branch track: [{clean_name.upper()}] from JSON registry.")
#         else:
#             print(f"❌ Branch [{clean_name}] could not be found to delete.")

#     # =====================================================================
#     # 📥 NETWORK HARVESTING ENGINE PIPELINES
#     # =====================================================================
#     def _sanitize_filename(self, text: str) -> str:
#         clean = re.sub(r'[^a-zA-Z0-9_\- ]', '', text)[:50].strip()
#         return clean.replace(" ", "_") if clean else "web_document"

#     def _download_pdf(self, url: str, target_folder: str, file_title: str) -> bool:
#         try:
#             safe_name = f"{self._sanitize_filename(file_title)}.pdf"
#             dest_path = os.path.join(target_folder, safe_name)
            
#             if os.path.exists(dest_path):
#                 print(f"   ⏩ Document already exists on disk: {safe_name}")
#                 return True

#             response = requests.get(url, headers=self.headers, timeout=15, stream=True)
#             content_type = response.headers.get("Content-Type", "").lower()
            
#             if response.status_code == 200 and "application/pdf" in content_type:
#                 with open(dest_path, "wb") as f:
#                     for chunk in response.iter_content(chunk_size=8192):
#                         f.write(chunk)
#                 print(f"   💾 Downloaded Successfully: {safe_name}")
#                 return True
#             return False
#         except Exception:
#             return False

#     def fetch_from_arxiv(self, subject: str, target_folder: str, max_results: int = 3):
#         """Engine 1: Official library wrapper interface to secure canonical query syntax."""
#         print(f"📡 Querying arXiv API wrapper for: '{subject}'")
        
#         # Format query according to canonical parenthesized grouping syntax rules
#         words = [w.strip() for w in subject.split() if w.strip()]
#         grouped_query = f"all:({' AND '.join(words)})"
        
#         try:
#             # Native client instantiation handles rate-limiting and query serialization
#             client = arxiv.Client()
#             search = arxiv.Search(
#                 query=grouped_query,
#                 max_results=max_results,
#                 sort_by=arxiv.SortCriterion.SubmittedDate,
#                 sort_order=arxiv.SortOrder.Descending
#             )
            
#             results = list(client.results(search))
#             if not results:
#                 return

#             for paper in results:
#                 # Stream the direct PDF attachment link down to the folder location
#                 if paper.pdf_url:
#                     self._download_pdf(paper.pdf_url, target_folder, paper.title)
#         except Exception as e:
#             print(f"   ❌ arXiv client failed to parse stream: {e}")

#     # def fetch_from_general_web(self, subject: str, target_folder: str, max_results: int = 3):
#     #     query_str = f"{subject} filetype:pdf"
#     #     print(f"🌐 Querying General Web (DDGS) for expanded query: '{query_str}'")
#     #     try:
#     #         with DDGS() as ddgs:
#     #             results = list(ddgs.text(query_str, max_results=max_results))
#     #         for res in results:
#     #             url = res.get("href", "")
#     #             title = res.get("title", "web_document")
#     #             if url:
#     #                 self._download_pdf(url, target_folder, title)
#     #     except Exception as e:
#     #         print(f"❌ General web crawler failure: {e}")

#     # # =====================================================================
#     # # 🚀 ORCHESTRATION PIPELINE SYNC ENGINE
#     # # =====================================================================
#     # def execute_daily_sync(self):
#     #     global_sources = self.config.get("global_sources", [])
#     #     branches = self.config.get("branches", [])

#     #     if not branches:
#     #         print("⚠️ Ingestion schema lookup empty. Register active branch entities first.")
#     #         return

#     #     for branch in branches:
#     #         name = branch["name"]
#     #         phrases = branch["search_phrases"]
#     #         active_sources = list(set(global_sources + branch.get("sources", [])))
            
#     #         print(f"\n🚀 Initiating Synchronization Sequence for Target Branch: [{name.upper()}]")
#     #         target_dir = os.path.join(self.output_root, name)
#     #         os.makedirs(target_dir, exist_ok=True)

#     #         for phrase in phrases:
#     #             print(f" 🔍 Processing Phrase Token: '{phrase}'")
                
#     #             if "arxiv" in active_sources:
#     #                 self.fetch_from_arxiv(phrase, target_dir)
#     #             if "duckduckgo" in active_sources:
#     #                 self.fetch_from_general_web(phrase, target_dir)

#     def fetch_from_general_web(self, subject: str, target_folder: str, source_scope: str = "duckduckgo", max_results: int = 3):
#         """Engine 2: General Web Search Engine Crawler with dynamic conference/site scoping logic."""
        
#         # Base query format
#         query_str = f"{subject} filetype:pdf"
        
#         # Dynamic Scoping Logic: If the source string is a custom website URL, scope the search to that site!
#         if source_scope != "duckduckgo" and source_scope != "arxiv":
#             # Sanitize url to act as a clean site filter (e.g., '://thecvf.com')
#             clean_domain = source_scope.strip().lower().replace("http://", "").replace("https://", "")
#             query_str += f" site:{clean_domain}"
#             print(f"🌐 Querying Scoped Conference Engine ({clean_domain}) for: '{subject}'")
#         else:
#             print(f"🌐 Querying Broad Web (DDGS) for: '{query_str}'")
        
#         try:
#             with DDGS() as ddgs:
#                 results = list(ddgs.text(query_str, max_results=max_results))
            
#             if not results:
#                 return

#             for res in results:
#                 url = res.get("href", "")
#                 title = res.get("title", "web_document")
#                 if url:
#                     self._download_pdf(url, target_folder, title)
#         except Exception as e:
#             print(f"❌ Web crawler engine failure for scope [{source_scope}]: {e}")

#     # # =====================================================================
#     # # 🚀 ORCHESTRATION PIPELINE SYNC ENGINE
#     # # =====================================================================
#     def execute_daily_sync(self):
#         """Loops through branches dynamically based on JSON config properties."""
#         global_sources = self.config.get("global_sources", [])
#         branches = self.config.get("branches", [])

#         if not branches:
#             print("⚠️ Ingestion schema lookup empty. Register active branch entities first.")
#             return

#         for branch in branches:
#             name = branch["name"]
#             phrases = branch["search_phrases"]
#             active_sources = list(set(global_sources + branch.get("sources", [])))
            
#             print(f"\n🚀 Initiating Synchronization Sequence for Target Branch: [{name.upper()}]")
#             target_dir = os.path.join(self.output_root, name)
#             os.makedirs(target_dir, exist_ok=True)

#             for phrase in phrases:
#                 print(f" 🔍 Processing Phrase Token: '{phrase}'")
                
#                 # Check arXiv if registered
#                 if "arxiv" in active_sources:
#                     self.fetch_from_arxiv(phrase, target_dir)
                
#                 # Loop through web targets, feeding the source scope name directly into the crawler engine
#                 for source in active_sources:
#                     if source != "arxiv":
#                         self.fetch_from_general_web(phrase, target_dir, source_scope=source)


# # =====================================================================
# # INTERFACE DEMONSTRATION LOOP
# # =====================================================================
# if __name__ == "__main__":
#     engine = DataDrivenIngestionEngine()
#     engine.execute_daily_sync()
#     print("\n🏁 Integration sync complete. Shared data arrays cleanly matched.")

import os
import re
import json
import xml.etree.ElementTree as ET
import requests
import time
import arxiv
import urllib.parse
import sys
from bs4 import BeautifulSoup
from ddgs import DDGS

class DataDrivenIngestionEngine:
    def __init__(self, config_path: str = "./Configuration/targets_config.json", output_root: str = "./downloaded_research", min_year: int = None):
        self.config_path = config_path
        self.output_root = output_root
        os.makedirs(self.output_root, exist_ok=True)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.config = self._load_config()
        self.limit = None
        self.downloaded_in_session = 0
        self.session_downloads = []
        self.min_year = min_year

    def _load_config(self) -> dict:
        try:
            from Configurator import ConfigurationLogicController
            controller = ConfigurationLogicController(config_path=self.config_path)
            return controller.config
        except Exception:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {"global_sources": ["arxiv", "duckduckgo"], "branches": []}

    def _print_crawler_progress(self):
        if self.limit is not None:
            progress_str = f"   ⏳ Progress: Fetched paper {self.downloaded_in_session}/{self.limit}"
        else:
            progress_str = f"   ⏳ Progress: Fetched paper {self.downloaded_in_session}"
        sys.stdout.write(f"\r{progress_str:<80}")
        sys.stdout.flush()

    def _log(self, message: str):
        sys.stdout.write(f"\r{message:<80}\n")
        self._print_crawler_progress()

    def _sanitize_filename(self, text: str) -> str:
        clean = re.sub(r'[^a-zA-Z0-9_\- ]', '', text)[:50].strip()
        return clean.replace(" ", "_") if clean else "web_document"

    def _download_pdf(self, url: str, target_folder: str, file_title: str) -> bool:
        if self.limit is not None and self.downloaded_in_session >= self.limit:
            return False
        try:
            safe_name = f"{self._sanitize_filename(file_title)}.pdf"
            dest_path = os.path.join(target_folder, safe_name)
            
            if os.path.exists(dest_path):
                self._log(f"   ⏩ Document already exists on disk: {safe_name}")
                return True

            response = requests.get(url, headers=self.headers, timeout=15, stream=True)
            content_type = response.headers.get("Content-Type", "").lower()
            
            if response.status_code == 200 and "application/pdf" in content_type:
                with open(dest_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                branch_name = os.path.basename(target_folder)
                self.session_downloads.append((branch_name, file_title, url))
                self.downloaded_in_session += 1
                self._log(f"   💾 Downloaded Successfully: {safe_name}")
                return True
            return False
        except Exception:
            return False

    # =====================================================================
    # 📡 CORE SOURCE ENGINES
    # =====================================================================
    def fetch_from_arxiv(self, subject: str, target_folder: str, max_results: int = 3):
        """Engine 1: Canonical Academic Archive Wrapper Layer."""
        self._log(f"📡 Querying arXiv API wrapper for: '{subject}'")
        words = [w.strip() for w in subject.split() if w.strip()]
        grouped_query = f"all:({' AND '.join(words)})"
        
        try:
            client = arxiv.Client()
            search = arxiv.Search(
                query=grouped_query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            results = list(client.results(search))
            for paper in results:
                if self.min_year is not None and paper.published.year < self.min_year:
                    self._log(f"   ⏩ Skipping older preprint ({paper.published.year}): {paper.title[:40]}...")
                    continue
                if paper.pdf_url:
                    self._download_pdf(paper.pdf_url, target_folder, paper.title)
        except Exception as e:
            self._log(f"   ❌ arXiv client failed to parse stream: {e}")

    def fetch_from_general_web(self, subject: str, target_folder: str, source_scope: str = "duckduckgo", max_results: int = 3):
        """Engine 2: Flexible General Web Scoper with Dynamic Fallback Site Constraints."""
        query_str = f"{subject} filetype:pdf"
        if self.min_year is not None:
            query_str = f"{subject} {self.min_year} filetype:pdf"
        
        # Generic Fallback Logic: If source is an unidentified website domain, force site scoping
        if source_scope not in ["duckduckgo", "arxiv", "imagesensors.org"]:
            clean_domain = source_scope.strip().lower().replace("http://", "").replace("https://", "")
            query_str += f" site:{clean_domain}"
            self._log(f"🌐 Querying Scoped Fallback Search Engine ({clean_domain}) for: '{subject}'")
        else:
            self._log(f"🌐 Querying Open Web (DDGS) for: '{query_str}'")
        
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query_str, max_results=max_results))
            if not results:
                return
            for res in results:
                url = res.get("href", "")
                title = res.get("title", "web_document")
                if url:
                    self._download_pdf(url, target_folder, title)
        except Exception as e:
            self._log(f"❌ Web crawler fallback engine failure for scope [{source_scope}]: {e}")

    # =====================================================================
    # 🛠️ CUSTOM TARGET SCRAPER FUNCTION (DEDICATED CHANNEL EXAMPLE)
    # =====================================================================
    def fetch_from_imagesensors_org(self, subject: str, target_folder: str, max_results: int = 2):
        """Engine 3: Specialized Scraper for Image Sensor Society Workshop Library records."""
        # Target url pointing directly to their online library resource index page
        target_url = "https://imagesensors.org/past-workshops-library/" # Link to image sensor society past library page
        self._log(f"🕸️ Running Specialized Custom Scraper targeting index endpoint: [{target_url}]...")
        
        try:
            response = requests.get(target_url, headers=self.headers, timeout=20)
            if response.status_code != 200:
                return
                
            soup = BeautifulSoup(response.text, 'html.parser')
            # Scrape and locate all hyperlinked anchor tags across the page DOM
            links_found = soup.find_all('a', href=True)
            
            download_count = 0
            # Break subject into individual phrase tokens to perform local text search matching
            keywords = [k.lower() for k in subject.split()]
            
            for link in links_found:
                if download_count >= max_results:
                    break
                    
                href_url = link['href']
                link_text = link.text.lower()
                
                # Check if link references a direct PDF file attachment resource
                if href_url.lower().endswith('.pdf'):
                    # Check if the page anchor text or file URL string mentions our keywords
                    if any(kw in link_text or kw in href_url.lower() for kw in keywords):
                        # Construct absolute URL path context if link is relative
                        if not href_url.startswith('http'):
                            href_url = urllib.parse.urljoin(target_url, href_url)
                            
                        self._log(f"   🎯 Custom Scraper intercepted matching record text: '{link.text[:40]}...'")
                        success = self._download_pdf(href_url, target_folder, link.text)
                        if success:
                            download_count += 1
        except Exception as e:
            self._log(f"   ❌ Specialized custom scraper failed: {e}")

    # =====================================================================
    # 🛠️ CVF / CVPR DEDICATED SCRAPER
    # =====================================================================
    def fetch_from_cvf(self, subject: str, target_folder: str, max_results: int = 5):
        """Engine 4: Scrapes CVF openaccess proceedings for matching papers."""
        conferences = ["CVPR2026", "CVPR2025", "CVPR2024", "CVPR2023", "ICCV2025", "ICCV2023", "ECCV2024", "ECCV2022"]
        keywords = [k.lower() for k in subject.split() if len(k) > 2]
        if not keywords:
            return

        download_count = 0
        for conf in conferences:
            if download_count >= max_results:
                break

            proceedings_url = f"https://openaccess.thecvf.com/{conf}"
            self._log(f"🕸️ Scraping CVF proceedings [{conf}] for: '{subject}'")

            try:
                resp = requests.get(proceedings_url, headers=self.headers, timeout=20)
                if resp.status_code != 200:
                    continue

                soup = BeautifulSoup(resp.text, 'html.parser')
                paper_blocks = soup.find_all('div', class_='papertitle')

                for block in paper_blocks:
                    if download_count >= max_results:
                        break

                    title_el = block.find('a', class_='title')
                    if not title_el:
                        continue

                    title = title_el.get_text(strip=True)
                    if not any(kw in title.lower() for kw in keywords):
                        continue

                    pdf_link = block.find('a', string=lambda t: t and 'pdf' in t.lower())
                    if not pdf_link or not pdf_link.get('href'):
                        continue

                    pdf_url = pdf_link['href']
                    if not pdf_url.startswith('http'):
                        pdf_url = urllib.parse.urljoin(proceedings_url, pdf_url)

                    self._log(f"   🎯 CVF match: '{title[:50]}...'")
                    success = self._download_pdf(pdf_url, target_folder, title)
                    if success:
                        download_count += 1

            except Exception as e:
                self._log(f"   ❌ CVF scraper failed for {conf}: {e}")

    # =====================================================================
    # 🚀 PIPELINE MASTER CONTROLLER ORCHESTRATOR
    # =====================================================================
    def execute_daily_sync(self, target_branch: str = None, limit: int = None):
        self.limit = limit
        self.downloaded_in_session = 0
        self.session_downloads = []

        global_sources = self.config.get("global_sources", [])
        branches = self.config.get("branches", [])

        if target_branch:
            target_branch = target_branch.lower().strip()
            branches = [b for b in branches if b["name"] == target_branch]

        if not branches:
            sys.stdout.write(f"\r⚠️ No active branches found matching filter: '{target_branch}'\n")
            sys.stdout.flush()
            return

        self._print_crawler_progress()

        for branch in branches:
            if self.limit is not None and self.downloaded_in_session >= self.limit:
                break
            name = branch["name"]
            phrases = branch["search_phrases"]
            active_sources = list(set(global_sources + branch.get("sources", [])))
            
            self._log(f"\n🚀 Starting Synchronization for Target Branch: [{name.upper()}]")
            target_dir = os.path.join(self.output_root, name)
            os.makedirs(target_dir, exist_ok=True)

            for phrase in phrases:
                if self.limit is not None and self.downloaded_in_session >= self.limit:
                    break
                self._log(f" 🔍 Processing Phrase Token: '{phrase}'")
                
                # Path A: Standard arXiv ecosystem check
                if "arxiv" in active_sources:
                    self.fetch_from_arxiv(phrase, target_dir)
                
                # Path B: Route sources through switch structures
                for source in active_sources:
                    if self.limit is not None and self.downloaded_in_session >= self.limit:
                        break
                    if source == "arxiv":
                        continue
                        
                    # 1. SPECIFIC CUSTOM FUNCTION ROUTING SWITCH
                    if source == "imagesensors.org":
                        self.fetch_from_imagesensors_org(phrase, target_dir)
                    elif source == "cvf":
                        self.fetch_from_cvf(phrase, target_dir)
                    # 2. STANDARD DUCKDUCKGO ROUTING SWITCH
                    elif source == "duckduckgo":
                        self.fetch_from_general_web(phrase, target_dir, source_scope="duckduckgo")
                    # 3. GENERIC FALLBACK SITE-SCOPING ROUTING SWITCH
                    else:
                        self.fetch_from_general_web(phrase, target_dir, source_scope=source)

        if self.downloaded_in_session > 0 or self.limit is not None:
            sys.stdout.write("\n")
            sys.stdout.flush()

        # Logging
        if self.session_downloads:
            import datetime
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, "crawler.log")
            now = datetime.datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"[{date_str}]\n")
                downloads_by_branch = {}
                for branch, title, url in self.session_downloads:
                    if branch not in downloads_by_branch:
                        downloads_by_branch[branch] = []
                    downloads_by_branch[branch].append((title, url))
                
                for branch, items in downloads_by_branch.items():
                    f.write(f"\t[{time_str}] Branch: {branch}\n")
                    for title, url in items:
                        f.write(f"\t[{time_str}]   - Downloaded: {title} (URL: {url})\n")
                f.write("\n")

if __name__ == "__main__":
    engine = DataDrivenIngestionEngine()
    engine.execute_daily_sync()
    print("\n🏁 Custom integration sweep verified. Pipeline up-to-date.")
