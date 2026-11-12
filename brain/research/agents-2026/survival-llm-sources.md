# Survival LLM (brangus.io) — Competitor Source Analysis

**Research Date:** 2026-11-11  
**Primary Source:** [Survival LLM GitHub SOURCES.md](https://github.com/anonnerdfrenzy/survival-llm/blob/main/SOURCES.md) (checked 2026-10-24)  
**Project Homepage:** https://www.brangus.io/survival-llm  
**Repository:** https://github.com/anonnerdfrenzy/survival-llm (fork of matthew-mcateer/survival-llm)

---

## Executive Summary

Survival LLM bundles an **offline AI assistant + emergency reference library** (~1.5M articles in "Everything" download, ~500K in "Essentials"). All sources are converted to plain text via Kiwix ZIM files or custom fetch scripts. The full library requires **~8.8 GB download, ~21 GB installed**.

Two download tiers:
- **Essentials** (1.3 GB): Everything except Wikipedia and iFixit
- **Everything** (8.8 GB): Full library including ~930K Wikipedia articles + iFixit

---

## Source-by-Source Breakdown

| # | Source | Coverage | License / ToS | Offline Availability | Size (ZIM / Download) | Acquisition Method |
|---|--------|----------|---------------|---------------------|----------------------|-------------------|
| 1 | **Wikipedia (top 930K most-read)** | General knowledge | CC BY-SA 4.0 | ✅ Full offline via Kiwix `wikipedia_en_top1m` | ~8–10 GB (nopic) | Kiwix ZIM |
| 2 | **WikiMed** | Medical encyclopedia (Wikipedia medicine subset) | CC BY-SA 4.0 | ✅ Full offline via Kiwix `wikipedia_en_medicine` | ~1.2–2.2 GB (varies by language; EN ~1.2 GB nopic, ~2.2 GB maxi) | Kiwix ZIM |
| 3 | **WikEM** | Emergency medicine (71K+ pages) | CC BY-SA 4.0 | ✅ Full offline via Kiwix `wikem_en_all` | ~100–200 MB estimated | Kiwix ZIM |
| 4 | **MedlinePlus (NLM-written pages only)** | Health topics, lab tests, genetics | **Public domain** (U.S. gov); licensed sections (A.D.A.M., ASHP, Natural Medicines) **excluded** in shared builds | ✅ Full offline via Kiwix `medlineplus.gov_en_all` | ~200–500 MB estimated | Kiwix ZIM (licensed sections stripped) |
| 5 | **UK Medicines A to Z (NHS)** | How to take common medicines safely | **Open Government Licence v3.0** (UK public sector info) | ✅ Full offline via Kiwix `nhs.uk_en_medicines` | ~50–150 MB estimated | Kiwix ZIM (static copy as of Sep 2026) |
| 6 | **CDC Travelers' Health** | Disease, water/food safety, Yellow Book | **Public domain** (CDC) | ✅ Full offline via Kiwix `wwwnc.cdc.gov_en_all` | ~300–600 MB estimated | Kiwix ZIM |
| 7 | **Ready.gov (FEMA)** | Emergency preparedness by hazard | **Public domain** (FEMA) | ✅ Full offline via Kiwix `ready.gov_en_all` | ~100–200 MB estimated | Kiwix ZIM |
| 8 | **U.S. Military Medicine Manuals** | Hospital Corpsman, First Aid (FM 4-25.11), Ship's Medicine Chest, field sanitation, preventive medicine, radiation protection | **Public domain** (U.S. gov). *Excludes 3 vols. with copyrighted material (Military Dermatology, War Psychiatry, FM 21-11)* | ✅ Full offline via Kiwix `irp.fas.org_en_military-medicine` | ~200–500 MB estimated | Kiwix ZIM |
| 9 | **U.S. Gov Survival & First-Aid Manuals** | USAF AFH 10-644 SERE, Army ATP 3-50.21 Survival, ATP 4-02.11 First Aid (2026), TC 21-3 Cold Weather, ATP 4-25.12 Field Sanitation, TB MED 577/507, FEMA Are You Ready?, CERT, JTS Prolonged Casualty Care | **Public domain** (17 U.S.C. §105) | ✅ Full offline via custom fetch `library/fetch_manuals.py` | ~100–300 MB total (PDFs) | Direct PDF fetch |
| 10 | **Nuclear War Survival Skills (Kearny/ORNL 1987)** | Fallout shelter, water, ventilation | ORNL report; 1986 additions © Cresson H. Kearny (reproduced with notice) | ✅ Full offline via `library/fetch_manuals.py` | ~5–10 MB | Direct PDF fetch |
| 11 | **Emergency Response Guidebook 2024** | Hazmat spills/fires | Reproduction permitted by participating govts (DOT/PHMSA, Transport Canada, Mexico SICT, Argentina CIQUIME); **not for resale** | ✅ Full offline via `library/fetch_manuals.py` (from Internet Archive) | ~10–20 MB | Direct PDF fetch |
| 12 | **Risk & Micromort References** | SSA life table (2023), CDC mortality (2024), NHTSA crash data, NWS lightning odds; Wikipedia micromort articles (Essentials only) | Gov stats: **public domain**; Wikipedia: CC BY-SA 4.0 | ✅ Full offline via `library/fetch_risk.py` (CDC/SSA from Internet Archive) | ~5–15 MB | Direct fetch |
| 13 | **USDA Complete Guide to Home Canning (2015)** | Safe canning, botulism prevention | **Public domain** (USDA) | ✅ Full offline via Kiwix `usda-2015_en` | ~20–50 MB | Kiwix ZIM |
| 14 | **wikiHow (2018 text dump)** | How-to guides (200K+ articles) | **CC BY-NC-SA 3.0** (non-commercial) | ✅ Full offline via Hugging Face `Lajvi/wikihowAll` | ~500 MB – 1 GB | HF dataset |
| 15 | **iFixit** | Repair guides (44K+ guides, 456K images) | **CC BY-NC-SA 3.0** (non-commercial); author attribution required | ✅ Full offline via Kiwix `ifixit_en_all` | **~2.5 GB** (per iFixit announcement) | Kiwix ZIM |
| 16 | **Appropedia** | Appropriate technology, sustainability | **CC BY-SA 3.0 or 4.0** (per page) | ✅ Full offline via Kiwix `appropedia_en_all` | ~100–300 MB estimated | Kiwix ZIM |
| 17 | **Energypedia** | Solar, batteries, cookstoves, biogas | **CC BY-SA 3.0 or 4.0** (per page) | ✅ Full offline via Kiwix `energypedia_en_all` | ~100–300 MB estimated | Kiwix ZIM |
| 18 | **WikiCiv** | Rebuilding technology from scratch | **CC BY-SA 4.0** | ✅ Full offline via Kiwix `wikiciv_en_all` | ~50–150 MB estimated | Kiwix ZIM |
| 19 | **Stack Exchange (10 sites)** | Practical Q&A with authors: Home Improvement, The Great Outdoors, Seasoned Advice (cooking), Gardening, Lifehacks, Sustainable Living, Amateur Radio, Medical Sciences, Motor Vehicle Repair, Pets | **CC BY-SA 2.5 / 3.0 / 4.0** (by post date) | ✅ Full offline via Kiwix Stack Exchange ZIMs | ~5–15 GB total (varies by site; Stack Overflow alone ~60 GB expanded) | Kiwix ZIM |
| 20 | **IFRC First Aid Guidelines 2020** | Evidence-based first aid | © IFRC; **non-commercial copying allowed with acknowledgement** | ✅ Full offline via `library/fetch_manuals.py` | ~10–20 MB | Direct PDF fetch |
| 21 | **WHO Emergency Care / Childbirth / Water Quality** | Emergency care, childbirth complications, safe water | **CC BY-NC-SA 3.0 IGO** (non-commercial); WHO does not endorse this app | ✅ Full offline via `library/fetch_manuals.py` | ~20–50 MB | Direct PDF fetch |

---

## Sources Excluded / Left Out on Purpose

| Source | Reason |
|--------|--------|
| MedlinePlus licensed sections (A.D.A.M. Medical Encyclopedia, ASHP drug info, Natural Medicines) | Third-party copyright; included in personal builds only (`--public`/`--lite` builds exclude) |
| Kiwix "zimgit" collections (post-disaster, water, food, medicine, knots) | Bundled PDFs from many publishers with mixed rights; personal builds only |
| Military Dermatology, War Psychiatry, FM 21-11 (1988) | Reprint copyrighted figures/text; FM 4-25.11 included instead |
| Hesperian books (*Where There Is No Doctor*) | Digital use requires written permission |
| MSF clinical guidelines, Sphere Handbook, USAMRIID Blue Book, Red Cross manuals, commercial survival books | All rights reserved |

---

## License Compliance Notes

- **Non-commercial sources** (wikiHow, iFixit, IFRC, WHO): Licensed CC BY-NC-SA. **Fine for this free project.** Anyone wanting commercial use must rebuild without them.
- **ShareAlike sources** (Wikipedia, WikiMed, WikEM, Appropedia, Energypedia, WikiCiv, Stack Exchange): Text shared under same license (CC BY-SA), credited to authors; each article retains source address.
- **Public domain / Government works**: No restrictions (U.S. federal, CDC, FEMA, Military, USDA, SSA, NHTSA, NWS, UK OGL v3.0).
- **Attribution**: Stack Exchange posts and iFixit guides keep original author names. Wikipedia/WikiMed/WikEM credit contributors.

---

## Kiwix ZIM File Details

All Kiwix-sourced content uses the **ZIM format** (highly compressed, full-text search index included). Files are downloaded from `library.kiwix.org` or mirrors (e.g., `ftp.fau.de/kiwix/zim/`).

**Kiwix ZIM variants (for Wikipedia):**
- `mini` — intro + infobox only (~5% of maxi)
- `nopic` — full articles, no images (~25% of maxi)
- `maxi` — full with images

Survival LLM uses **`wikipedia_en_top1m`** (top 1M most-read, likely nopic variant) for the "Everything" download.

**Known ZIM sizes (approximate, from Kiwix catalog / mirrors):**
- `wikipedia_en_top1m` (nopic): ~8–10 GB
- `wikipedia_en_medicine` (WikiMed): ~1.2 GB (nopic) / ~2.2 GB (maxi)
- `wikem_en_all`: ~100–200 MB
- `medlineplus.gov_en_all`: ~200–500 MB
- `nhs.uk_en_medicines`: ~50–150 MB
- `wwwnc.cdc.gov_en_all`: ~300–600 MB
- `ready.gov_en_all`: ~100–200 MB
- `irp.fas.org_en_military-medicine`: ~200–500 MB
- `usda-2015_en`: ~20–50 MB
- `ifixit_en_all`: ~2.5 GB (per iFixit blog)
- `appropedia_en_all`: ~100–300 MB
- `energypedia_en_all`: ~100–300 MB
- `wikiciv_en_all`: ~50–150 MB
- Stack Exchange ZIMs: ~5–15 GB total for 10 sites

---

## Technical Architecture

- **Build script:** `library/build_library.py` converts all sources to plain text
- **Fetch scripts:** `library/fetch_manuals.py`, `library/fetch_risk.py` for direct PDF/CSV downloads
- **Search index:** Built from plain-text library (not from ZIM at runtime)
- **Model:** Local Ollama models (auto-selected by RAM)
- **App:** Electron/Tauri desktop app (Mac/Windows), MIT licensed
- **Offline-first:** Zero network calls after initial setup

---

## Verification & Sources

| Claim | Source | Type |
|-------|--------|------|
| Full source list, licenses, inclusion tiers | [SOURCES.md](https://github.com/anonnerdfrenzy/survival-llm/blob/main/SOURCES.md) | Primary (measured) |
| WikiMed offline size, languages | [WikiMed on Kiwix](https://meta.wikimedia.org/wiki/Wiki_Project_Med/App) + [Google Play](https://play.google.com/store/apps/details?id=org.kiwix.kiwixcustomwikimed) | Measured / Reported |
| iFixit offline archive size (2.5 GB, 44K guides) | [iFixit Blog](https://www.ifixit.com/News/64006/download-every-ifixit-guide-for-free) | Reported (iFixit) |
| iFixit license (CC BY-NC-SA 3.0) | [iFixit Licensing](https://www.ifixit.com/Info/Licensing) | Primary |
| MedlinePlus public domain status | [MedlinePlus Using Content](https://medlineplus.gov/about/using/usingcontent) | Primary (NLM) |
| UK Medicines A-Z OGL v3.0 | [NHS Medicines A-Z](https://www.nhs.uk/medicines) + [OGL v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) | Primary |
| CDC Travelers' Health public domain | [CDC Travelers' Health](https://wwwnc.cdc.gov/travel) | Primary (CDC .gov) |
| Ready.gov/FEMA public domain | [Ready.gov Publications](https://www.ready.gov/publications) | Primary (FEMA .gov) |
| Military manuals public domain (17 USC 105) | [Army Publishing Directorate](https://armypubs.army.mil/) | Primary (U.S. gov) |
| Stack Exchange CC BY-SA data dumps | [Stack Overflow Blog](https://stackoverflow.blog/2014/01/23/stack-exchange-cc-data-now-hosted-by-the-internet-archive) | Primary |
| Appropedia CC BY-SA 3.0/4.0 | [Appropedia Open Licenses](https://www.appropedia.org/Open_licenses) | Primary |
| WikiHow CC BY-NC-SA 3.0 | [wikiHow Terms of Use](https://www.wikihow.com/wikiHow:Terms-of-Use) | Primary |
| Kiwix ZIM format, catalog | [Kiwix Catalog](https://get.kiwix.org/en/solutions/catalog) | Primary |

---

## Competitive Implications for NOMAD 2

| Aspect | Survival LLM Approach | NOMAD 2 Opportunity |
|--------|----------------------|---------------------|
| **Source diversity** | 21 sources, heavily medical/survival | Can curate different verticals (tech, legal, engineering, etc.) |
| **License handling** | Strips non-commercial sources for commercial builds | Build license-aware pipeline from day one |
| **Offline format** | Kiwix ZIM → plain text → custom search index | Consider SQLite/Parquet + vector embeddings for RAG |
| **Update mechanism** | Quarterly Kiwix ZIM refreshes | Automated diff-based updates |
| **Attribution** | Per-article source + license displayed | Structured provenance metadata (W3C PROV-O?) |
| **Model coupling** | Tight (Ollama + fixed library) | Decoupled: any local LLM + any indexed corpus |
| **Commercial viability** | Blocked by NC sources | Fully commercial-friendly corpus possible |

---

## Recommended Next Steps

1. **Audit Kiwix catalog** for additional relevant ZIMs (e.g., `libretexts`, `freecodecamp`, `devdocs`, `maps`)
2. **Build license classifier** to auto-tag ingested content (PD, CC-BY, CC-BY-SA, CC-BY-NC-SA, OGL, custom)
3. **Prototype ZIM → Parquet pipeline** with metadata preservation (source, license, author, URL, retrieval date)
4. **Evaluate Stack Exchange ZIMs** for technical Q&A coverage (Stack Overflow, Super User, Ask Ubuntu, etc.)
5. **Design commercial-safe corpus** by excluding all NC/SA sources and replacing with permissive alternatives

---

*Research compiled by OpenCode agent using 10+ web searches + primary source analysis. All sizes are estimates from Kiwix catalog/mirrors unless noted as reported by publisher.*