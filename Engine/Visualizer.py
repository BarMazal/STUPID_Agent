from Selector import HierarchicalQueryEngine

class TerminalConsoleUI:
    def __init__(self, engine: HierarchicalQueryEngine, show_attributes: bool = False):
        self.engine = engine
        self.show_attributes = show_attributes

    def render_tree_to_console(self, node: dict, indent: str = ""):
        """Visually loops through the engine's data dictionary to format tree lines on screen."""
        if node["type"] == "leaf_cluster":
            if not node["papers"]:
                print(f"{indent}  🍃 (Empty Cluster)")
                return
            for paper in node["papers"]:
                clean_title = paper['title'].replace("_", " ").strip()
                print(f"{indent}  📄 [{paper['id'][:25]}...] ➔ {clean_title}")
                print(f"{indent}     └─ AI Digest: {paper['summary'][:110]}...")
            return

        print(f"{indent}🌿 [Grouped Level: {node['split_by_field'].upper()}]")
        for branch_value, child_node in node["branches"].items():
            print(f"{indent} └── 🔀 Filter Category: \"{branch_value}\"")
            self.render_tree_to_console(child_node, indent + "     ")

    def save_tree_to_html(self, tree: dict, conditions: list, filter_str: str = ""):
        path_str = " ➔ ".join(conditions).upper()
        filter_badge = f'<span style="margin-left: 10px; opacity: 0.8;">(Filters: {filter_str})</span>' if filter_str else ""
        
        def format_attribute_val(val) -> str:
            if isinstance(val, list):
                return ", ".join(str(v) for v in val) if val else "None"
            if isinstance(val, bool):
                return "Yes" if val else "No"
            return str(val) if val is not None else "None"
            
        def _build_html_tree(node: dict) -> str:
            import os
            if node["type"] == "leaf_cluster":
                html = '<div class="leaf-container">'
                if not node["papers"]:
                    html += '<div class="empty-cluster">🍃 (Empty Cluster)</div>'
                else:
                    for paper in node["papers"]:
                        clean_title = paper['title'].replace("_", " ").strip()
                        branch = paper['branch']
                        pid = paper['id']
                        
                        pdf_rel = f"../downloaded_research/{branch}/{pid}.pdf"
                        txt_rel = f"../downloaded_research/{branch}/{pid}.txt"
                        json_rel = f"../downloaded_research/{branch}/{pid}_meta.json"
                        
                        storage_root = getattr(self.engine, 'storage_root', './downloaded_research')
                        pdf_path = os.path.join(storage_root, branch, f"{pid}.pdf")
                        txt_path = os.path.join(storage_root, branch, f"{pid}.txt")
                        json_path = os.path.join(storage_root, branch, f"{pid}_meta.json")
                        
                        links_html = []
                        if os.path.exists(pdf_path):
                            links_html.append(f'<a href="{pdf_rel}" target="_blank" class="file-link">📕 PDF</a>')
                        if os.path.exists(txt_path):
                            links_html.append(f'<a href="{txt_rel}" target="_blank" class="file-link">📝 TXT</a>')
                        if os.path.exists(json_path):
                            links_html.append(f'<a href="{json_rel}" target="_blank" class="file-link">⚙️ JSON</a>')
                        
                        links_str = ""
                        if links_html:
                            links_str = f'<span class="file-links">{" ".join(links_html)}</span>'
                            
                        attr_html = ""
                        if self.show_attributes and paper.get("attributes"):
                            items_html = []
                            for attr_name, attr_val in paper["attributes"].items():
                                formatted_val = format_attribute_val(attr_val)
                                items_html.append(f'<div class="attribute-item"><span class="attribute-key">{attr_name}:</span> <span class="attribute-value">{formatted_val}</span></div>')
                            attr_html = f"""
                            <div class="paper-attributes">
                                {"".join(items_html)}
                            </div>
                            """
                            
                        html += f"""
                        <div class="paper-card">
                            <div class="paper-title">📄 {clean_title}</div>
                            <div class="paper-meta">
                                <span>ID: {pid[:25]}...</span>
                                {links_str}
                            </div>
                            <div class="paper-digest"><strong>AI Digest:</strong> {paper['summary']}</div>
                            {attr_html}
                        </div>
                        """
                html += '</div>'
                return html

            split_field = node['split_by_field'].upper()
            html = '<div class="node-container">'
            for branch_value, child_node in node["branches"].items():
                html += f"""
                <details open>
                    <summary>
                        <span class="folder-icon">🌿</span>
                        <span class="group-label">[{split_field}]</span>
                        <span class="branch-val">"{branch_value}"</span>
                    </summary>
                    {_build_html_tree(child_node)}
                </details>
                """
            html += '</div>'
            return html

        tree_html = _build_html_tree(tree)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Research Tree Visualizer</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            --card-bg: rgba(255, 255, 255, 0.03);
            --card-border: rgba(255, 255, 255, 0.06);
            --accent-color: #818cf8;
            --accent-hover: #6366f1;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-digest: #cbd5e1;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Outfit', sans-serif;
            background: var(--bg-gradient);
            color: var(--text-main);
            min-height: 100vh;
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        
        .container {{
            width: 100%;
            max-width: 900px;
            background: rgba(255, 255, 255, 0.01);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        }}
        
        header {{
            margin-bottom: 30px;
            text-align: center;
        }}
        
        h1 {{
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(to right, #a5b4fc, #818cf8, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: var(--text-muted);
            font-size: 1rem;
            margin-bottom: 20px;
        }}
        
        .path-badge {{
            display: inline-block;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: var(--accent-color);
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        
        .controls {{
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-bottom: 25px;
        }}
        
        button {{
            font-family: 'Outfit', sans-serif;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-main);
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }}
        
        button:hover {{
            background: var(--accent-hover);
            border-color: var(--accent-hover);
            transform: translateY(-1px);
        }}
        
        button:active {{
            transform: translateY(1px);
        }}
        
        .tree-root {{
            background: rgba(0, 0, 0, 0.2);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }}
        
        details {{
            margin-left: 20px;
            margin-top: 10px;
            transition: all 0.3s ease;
        }}
        
        summary {{
            list-style: none;
            cursor: pointer;
            padding: 8px 12px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        
        summary::-webkit-details-marker {{
            display: none;
        }}
        
        summary:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.15);
        }}
        
        .folder-icon {{
            font-size: 1.1rem;
        }}
        
        .group-label {{
            color: var(--text-muted);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .branch-val {{
            color: var(--accent-color);
        }}
        
        .leaf-container {{
            margin-left: 25px;
            padding-left: 10px;
            border-left: 1px dashed rgba(255, 255, 255, 0.1);
        }}
        
        .paper-card {{
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            transition: all 0.25s ease;
        }}
        
        .paper-card:hover {{
            transform: translateX(4px);
            background: rgba(255, 255, 255, 0.03);
            border-color: rgba(99, 102, 241, 0.25);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }}
        
        .paper-title {{
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 5px;
        }}
        
        .paper-meta {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }}
        
        .file-links {{
            display: inline-flex;
            gap: 6px;
        }}
        
        .file-link {{
            text-decoration: none;
            color: var(--accent-color);
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}
        
        .file-link:hover {{
            background: var(--accent-hover);
            border-color: var(--accent-hover);
            color: #ffffff;
            transform: translateY(-1px);
        }}
        
        .file-link:active {{
            transform: translateY(1px);
        }}
        
        .paper-digest {{
            font-size: 0.9rem;
            color: var(--text-digest);
            line-height: 1.5;
            border-left: 3px solid var(--accent-color);
            padding-left: 10px;
        }}
        
        .empty-cluster {{
            color: var(--text-muted);
            font-style: italic;
            padding: 10px;
            font-size: 0.9rem;
        }}
        
        .paper-attributes {{
            margin-top: 12px;
            padding: 10px 14px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        
        .attribute-item {{
            display: flex;
            align-items: baseline;
            gap: 8px;
            font-size: 0.82rem;
            line-height: 1.4;
        }}
        
        .attribute-key {{
            color: var(--text-muted);
            font-weight: 600;
            min-width: 120px;
            flex-shrink: 0;
        }}
        
        .attribute-value {{
            color: var(--accent-color);
            word-break: break-word;
        }}
        
        /* Custom details animation/indicator */
        details > summary::after {{
            content: '▼';
            margin-left: auto;
            font-size: 0.7rem;
            color: var(--text-muted);
            transition: transform 0.2s ease;
        }}
        
        details[open] > summary::after {{
            transform: rotate(180deg);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>STUPID Research Tree</h1>
            <div class="subtitle">Interactive Multi-Tenant Synthesized Literature View</div>
            <div class="path-badge">Path: {path_str}{filter_badge}</div>
        </header>
        
        <div class="controls">
            <button onclick="expandAll()">Expand All</button>
            <button onclick="collapseAll()">Collapse All</button>
        </div>
        
        <div class="tree-root">
            {tree_html}
        </div>
    </div>
    
    <script>
        function expandAll() {{
            document.querySelectorAll('details').forEach(el => el.open = true);
        }}
        
        function collapseAll() {{
            document.querySelectorAll('details').forEach(el => el.open = false);
        }}
    </script>
</body>
</html>"""
        
        import os
        import datetime
        visualizations_dir = "./Visualizations"
        try:
            os.makedirs(visualizations_dir, exist_ok=True)
            
            # Save the latest tree.html
            latest_file = os.path.join(visualizations_dir, "tree.html")
            with open(latest_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"🌐 Saved interactive HTML tree view to '{latest_file}'")
            
            # Save timestamped copy for history
            slug = "_".join(conditions).replace(" ", "_").lower() if conditions else "root"
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            timestamped_file = os.path.join(visualizations_dir, f"tree_{slug}_{timestamp}.html")
            with open(timestamped_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"🌐 Saved history HTML tree view copy to '{timestamped_file}'")
        except Exception as e:
            print(f"⚠️ Failed to write HTML tree view: {e}")

    def _print_visualizer_progress(self, current, max_val, task_name):
        import sys
        progress_str = f"   ⏳ Progress: {task_name} {current}/{max_val}"
        sys.stdout.write(f"\r{progress_str:<80}")
        sys.stdout.flush()

    def filter_records(self, records: list, filter_str: str) -> list:
        if not filter_str.strip():
            return records
        
        conditions = []
        for part in filter_str.split(","):
            if "=" in part:
                k, v = part.split("=", 1)
                conditions.append((k.strip().lower(), v.strip()))
        
        if not conditions:
            return records
            
        filtered = []
        total = len(records)
        self._print_visualizer_progress(0, total, "Filtering")
        for idx, r in enumerate(records):
            match = True
            for k, v in conditions:
                val = self.engine._get_nested_value(r, k)
                if isinstance(val, bool):
                    bool_v = v.lower() in ["true", "yes", "1"]
                    if val != bool_v:
                        match = False
                        break
                elif isinstance(val, list):
                    val_lower = [str(item).lower().strip() for item in val]
                    if v.lower().strip() not in val_lower:
                        match = False
                        break
                else:
                    if str(val).lower().strip() != v.lower().strip():
                        match = False
                        break
            if match:
                filtered.append(r)
            self._print_visualizer_progress(idx + 1, total, "Filtering")
            
        import sys
        sys.stdout.write("\n")
        sys.stdout.flush()
        return filtered

    def show_filter_help(self, records: list):
        print("\n📖 VISUALIZER FILTER ASSISTANT")
        print("=" * 60)
        print("Filter syntax: key=value, key2=value2 (comma-separated, case-insensitive)")
        print("Keys can be any of the active taxonomy keywords (e.g., relevant, branch, innovation).")
        
        # 1. Show branch names
        branches = sorted(list({r.get("_branch_lineage") for r in records if r.get("_branch_lineage")}))
        print(f"\n📂 Available branches for 'branch=':")
        print(f"   [ {', '.join(branches)} ]")
        
        # 2. Show Boolean keys
        print("\n⚖️ Boolean keys (use '=true' or '=false'):")
        print("   relevant")
        
        # 3. Extract a sample of active vocabulary tags across records
        categories = self.engine.config.get("categories", [])
        ai_keys = [cat["key"] for cat in categories if cat.get("source") == "ai"]
        
        if ai_keys:
            print("\n🏷️ Sample of active tags in database:")
            for key in ai_keys:
                tags = set()
                for r in records:
                    val = self.engine._get_nested_value(r, key)
                    if isinstance(val, list):
                        for item in val:
                            if item: tags.add(item)
                    elif isinstance(val, str) and val:
                        tags.add(val)
                if tags:
                    sorted_tags = sorted(list(tags))[:10]  # Show top 10 tags
                    more_suffix = "..." if len(tags) > 10 else ""
                    print(f"   - {key}=: [ {', '.join(sorted_tags)}{more_suffix} ]")
        print("=" * 60 + "\n")

    def run_loop(self):
        print("📊 Initializing Hierarchical Search Tree Query Engine...")
        records = self.engine.load_all_metadata_records()
        
        if not records:
            print("⚠️ Data index tracking records empty. Run your pipeline steps first.")
            return
            
        print(f"📊 Successfully loaded and indexed {len(records)} active records from disk.")

        while True:
            try:
                config = self.engine.load_config()
                categories = config.get("categories", [
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
                valid_keywords = [cat["key"].lower().strip() for cat in categories]
                keywords_str = " | ".join(valid_keywords)
                print(f"\nAvailable taxonomy keywords: [ {keywords_str} ]")
                user_input = input("🔍 Enter hierarchy condition sequence (comma-separated tags), 'help' for options, or 'exit': ")
                cleaned_input = user_input.strip().lower()
                if cleaned_input == 'exit':
                    print("👋 Exiting Query Shell Workspace.")
                    break
                if cleaned_input in ['help', 'h', '?']:
                    print("\n📖 HIERARCHY SEQUENCE & FILTERING HELP")
                    print("=" * 60)
                    print("1. HIERARCHY SEQUENCE:")
                    print("   Enter a comma-separated list of active taxonomy keywords to group papers by.")
                    print("   Example: branch, relevant, innovation")
                    print(f"   Available keywords: [ {keywords_str} ]")
                    print("\n2. FILTERING OPTIONS:")
                    self.show_filter_help(records)
                    continue
                if not user_input.strip():
                    continue

                conditions_sequence = [c.strip().lower() for c in user_input.split(",") if c.strip()]
                
                if any(kw not in valid_keywords for kw in conditions_sequence):
                    print("❌ Error: Invalid keyword entered. Type 'help' to see active keywords and syntax.")
                    continue

                print(f"\nComputing split mapping for path: { ' ➔ '.join(conditions_sequence) }")
                print("=" * 90)
                
                while True:
                    filter_input = input("🎯 Enter filter conditions (e.g. relevant=true, branch=ccd_sensors), 'help' for options, or press Enter: ").strip()
                    if filter_input.lower() in ["help", "?", "h"]:
                        self.show_filter_help(records)
                        continue
                    break
                filtered_records = self.filter_records(records, filter_input)
                print(f"📊 Filtered dataset: {len(filtered_records)} of {len(records)} records matching filters.")
                
                # Fetch raw data payload from the pure Selector module
                compiled_tree = self.engine.build_query_tree(filtered_records, conditions_sequence)
                
                # Parse and visually display the data structure locally
                self.render_tree_to_console(compiled_tree)
                self.save_tree_to_html(compiled_tree, conditions_sequence, filter_input)
                print("=" * 90 + "\n")
                
            except KeyboardInterrupt:
                print("\n👋 Exiting Query Shell Workspace.")
                break

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Standalone visualizer parser.")
    parser.add_argument("--show_attributes", action="store_true", help="Show attributes in leaves")
    args = parser.parse_known_args()[0]
    
    # Instantiate the pure data processor module
    core_engine = HierarchicalQueryEngine()
    
    # Inject the processor instance directly into your visual presentation layout wrapper
    ui_shell = TerminalConsoleUI(core_engine, show_attributes=args.show_attributes)
    ui_shell.run_loop()
