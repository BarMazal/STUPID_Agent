# STUPID Search Resources & Methods Reference

## Overview

The STUPID pipeline ingests academic papers through two mechanisms:

1. **General Search** (DuckDuckGo fallback): Sends search phrases to DuckDuckGo, optionally scoped to a domain with `site:`. Universal but limited by DDG's indexing and result caps.
2. **Dedicated Fetcher**: Custom scraper per source that directly hits the target site's API or proceedings pages for complete, reliable coverage.

---

## Source Routing Logic

In `Engine/Crawler.py:execute_daily_sync()`, each source name is routed through a switch:

```
source == "arxiv"          → fetch_from_arxiv()
source == "cvf"            → fetch_from_cvf()
source == "imagesensors.org" → fetch_from_imagesensors_org()
source == "duckduckgo"     → fetch_from_general_web(scope="duckduckgo")
source == <anything else>  → fetch_from_general_web(scope=source)  [site: scoped]
```

Active sources per branch = union of `global_sources` + branch-specific `sources`.

---

## Implemented Sources

| Source Name | Type | Coverage | Method | Status |
|---|---|---|---|---|
| `arxiv` | Dedicated | Preprints (all fields) | arXiv API (`arxiv` Python lib), query by keyword, sorted by submit date | ✅ Implemented |
| `cvf` | Dedicated | CVF conferences: CVPR, ICCV, ECCV, WACV | Scrapes `openaccess.thecvf.com/<ConfYear>` proceedings pages, keyword-matches paper titles, downloads PDF links | ✅ Implemented |
| `imagesensors.org` | Dedicated | Image Sensor Society workshops | Scrapes past-workshops-library page, keyword-matches anchor text, follows `.pdf` links | ✅ Implemented |
| `duckduckgo` | General | Entire web | DDGS text search with `filetype:pdf` filter | ✅ Implemented |
| `<any domain>` | General (fallback) | Any site (DDG-indexed) | DDGS text search with `site:<domain>` + `filetype:pdf` filter | ✅ Implemented |

---

## Planned Sources

| Source Name | Type | Coverage | Proposed Method | Status |
|---|---|---|---|---|
| `openreview` | Dedicated | NeurIPS, ICLR, ICML, TMLR | OpenReview REST API (`/search/notes`), filter by venue, download PDF from `pdf` field | ⬜ Not implemented |
| `pmlr` | Dedicated | ICML, AISTATS, COLT, etc. | Scrape `proceedings.mlr.press`, match volume pages, extract PDF links | ⬜ Not implemented |
| `semanticscholar` | Dedicated | Cross-domain aggregator | Semantic Scholar API (`/graph/v1/paper`), follow open access PDF URLs | ⬜ Not implemented |
| `openalex` | Dedicated | Cross-domain aggregator | OpenAlex API (`/works`), filter by open access, follow PDF links | ⬜ Not implemented |
| `eurographics` | Dedicated | Eurographics, SIGGRAPH | Scrape `eg.org` / `portals.cis.fcu.edu.tw` proceedings, extract PDFs | ⬜ Not implemented |
| `ieee_open` | Dedicated | IEEE open-access papers | IEEE Xplore API, filter by open access flag | ⬜ Not implemented |
| `acm_dl` | Dedicated | ACM Digital Library open access | ACM API, filter by open access, download PDFs | ⬜ Not implemented |
| `pubmed` | Dedicated | Biomedical / life sciences | PubMed E-utilities API, filter by free full text, download from PMC | ⬜ Not implemented |
| `core` | Dedicated | Open access aggregator (theses + papers) | Core.ac.uk API, filter by full text available | ⬜ Not implemented |

---

## General vs. Dedicated: When to Use Which

| | General (`duckduckgo` / `site:`) | Dedicated Fetcher |
|---|---|---|
| **Setup effort** | None — just add domain string | Requires writing `fetch_from_<source>()` + routing entry |
| **Coverage** | Limited to what DDG indexed | Complete, from the source's own listings |
| **Reliability** | Subject to DDG rate limits, result caps | Direct access, predictable |
| **Freshness** | Days-to-weeks DDG indexing lag | Immediate — scrapes live pages |
| **PDF accuracy** | May hit abstract/landing pages | Lands on actual PDF URLs |
| **Best for** | Broad discovery, niche/unknown sites | Known, high-value, structured sources |

---

## How to Add a New Dedicated Fetcher

1. **Implement** `fetch_from_<source>()` in `Engine/Crawler.py` (follow `fetch_from_cvf` or `fetch_from_imagesensors_org` as template)
2. **Register** in the routing switch inside `execute_daily_sync()` (line ~496):
   ```python
   elif source == "<source_name>":
       self.fetch_from_<source>(phrase, target_dir)
   ```
3. **Configure** the source via CLI: `python STUPIDConsoleUI.py --configure` → `[S] Manage Global Sources` or branch-level `[6] Targeted Sources`



The current codebase has 4 source types:

Source	Type	Coverage
arxiv	Dedicated	Preprints
cvf	Dedicated (just added)	CVPR, ICCV, ECCV, WACV
imagesensors.org	Dedicated	ISWS workshops
duckduckgo	General	Everything
<any domain>	Fallback	DDG site: scoped
Major sources worth dedicated fetchers (structured proceedings, free PDFs, or APIs):

Target	Source	Notes
OpenReview.net	NeurIPS, ICLR, ICML, ICLR	REST API, full text often available
PMLR	ICML, AISTATS, COLT	Free PDFs, clean site structure
Semantic Scholar	Aggregator	Free API, links to open PDFs
OpenAlex	Aggregator	Free API, successor to Microsoft Academic
Eurographics	Eurographics, SIGGRAPH	Free PDFs, proceedings pages
IEEE Open Access	Selected journals/confs	Free subset, has API
ACM DL	SIGGRAPH, PLDI, etc.	Some open access, has API
PubMed Central	Biomedical	Free full-text API
Core.ac.uk	Open access aggregator	Free API, thesis + papers
Most impactful next picks: OpenReview (NeurIPS/ICLR are top-tier ML venues not on CVF) and PMLR (ICML proceedings). Both are free, well-structured, and complement the existing CVF+arXiv coverage.

Done. Two changes in Engine/Crawler.py:

New fetch_from_cvf method (line ~405) — scrapes CVF proceedings pages for CVPR/ICCV/ECCV, keyword-matches paper titles, downloads PDFs directly
Routing entry (line ~497) — "cvf" source triggers the dedicated scraper
To use both, add them as global sources:
python STUPIDConsoleUI.py --configure

Then at root: [S] Manage Global Sources > [A]:

Add cvf — triggers the dedicated scraper (CVPR/ICCV/ECCV, direct PDF, no DDG limits)
Add openaccess.thecvf.com — triggers DDG site-scoped search (broad CVF coverage, catches edge cases)
Together they cover the full spectrum: the scraper gets you complete, year-filtered proceedings; DDG catches anything the scraper might miss (supplementary material, posters, late-breaking papers not on the main proceedings listing).