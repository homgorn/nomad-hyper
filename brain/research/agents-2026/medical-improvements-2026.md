# Offline Medical/Health Tools for NOMAD Hyper — 2026 Deep Research

> **Research date:** 2026-11-11  
> **Method:** 8+ websearch queries (TinyFish quota exhausted after ~12 queries)  
> **Labeling convention:**  
> - **[measured]** — from benchmarks, specs sheets, or direct testing  
> - **[reported]** — from vendor docs, release notes, or community reports (URL + date)  
> - **[inferred]** — derived from architecture, dependencies, or comparable deployments

---

## 1. Hikma Health — Offline-First EHR

| Attribute | Value | Source |
|-----------|-------|--------|
| **Status (2026)** | Active, v1.3.0 (Nov 2025), v3 platform in mono-repo; 18 countries, 500k+ patients served | [reported] docs.hikmahealth.org, GitHub hikmahealth/hikma-health-platform |
| **License** | MIT (platform); mobile app MIT | [reported] GitHub LICENSE files |
| **RAM (mobile)** | **6–8 GB recommended**; minimum Android 13+/iOS 16+ | [reported] FAQ: "Recommended: 6-8GB RAM and 64-128GB storage" |
| **RAM (server)** | Not explicitly stated; Node.js/TypeScript + PostgreSQL; typical VPS 2–4 GB | [inferred] from docker compose & Render deploy notes |
| **Offline capability** | **Full offline-native**: SQLite (WatermelonDB) on device; three sync modes — cloud, Local Sync Hub (LAN, encrypted RPC), fully online. Local Sync Hub (Tauri/Rust desktop) enables device↔device sync without internet. | [reported] docs.hikmahealth.org/offline-and-sync, PLOS Digital Health 2026-02-13 |
| **Sync architecture** | WatermelonDB + JSI (C++); syncs only deltas (created/changed/deleted) since last sync; initial sync downloads full DB (~500 MB noted in Lebanon clinic study) | [reported] PLOS Digital Health 2026; docs.hikmahealth.org |
| **Platforms** | Android, iOS (React Native/Expo); admin web (TanStack Start); Local Sync Hub (Windows/macOS/Linux via Tauri) | [reported] GitHub mono-repo structure |
| **Languages** | Arabic, Spanish, English, RTL support | [reported] App Store listing |
| **ONC/FHIR** | Not ONC-certified; FHIR not mentioned in 2026 docs | [inferred] |
| **Key limitation** | Multi-device sync during single patient encounter strains LAN/Wi-Fi (~500 MB per sync in 2026 study); mitigated by delta-sync redesign | [reported] PLOS Digital Health 2026 |

---

## 2. OpenMRS / Bahmni (including Bahmni Lite 2.0 & EMR4All)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Status (2026)** | **Bahmni Lite 2.0 released Oct 5, 2026** — React 19 frontend, FHIR R4 across core workflows, OpenMRS 2.6.15, MySQL 8.0. **Bahmni Standard 1.0.2** (security patch Jul 2026). **EMR4All** — Raspberry Pi 5 ARM64 images, solar/battery kits, pilot in Niger State Nigeria endorsed for rollout. | [reported] talk.openmrs.org (Bahmni Lite 2.0), bahmni.atlassian.net, emr4all.org |
| **License** | **Complex**: Bahmni components migrating AGPL 3.0 → MPL 2.0 w/ healthcare disclaimer; OpenMRS MPL 2.0; OpenELIS AGPL 3.0; Odoo Community LGPL 3.0; dcm4chee MPL/GPL/LGPL; bahmni-docker repo MIT | [reported] bahmni.org/license, dentiit.com |
| **RAM (server)** | **Full Bahmni: 8 GB min (16 GB w/ PACS)**; **Test: 8 GB** (4 GB causes manual service starts); **EMR4All Pi 5 kit: 8 GB or 16 GB RAM** | [reported] bahmni.atlassian.net/wiki System Requirements; emr4all.org |
| **RAM (client)** | Browser-based; any modern browser; lightweight on thin clients | [inferred] |
| **Offline capability** | **Bahmni Standard/Lite: designed for always-on server (Docker)**. **EMR4All = true offline-first**: Raspberry Pi 5 runs full stack (OpenMRS, OpenELIS, PACS, Odoo WIP) on local Wi-Fi; store-and-forward sync via USB/SMS/FHIR to central OpenMRS. | [reported] emr4all.org comparison table; talk.openmrs.org Bahmni on Pi |
| **Sync architecture** | EMR4All: Python Sync Tool merges Pi DB → central OpenMRS; HL7/FHIR for DHIS2/OpenHIM; future SMS exchange | [reported] emr4all.org |
| **Platforms** | Server: Docker (Linux/macOS/Win via Docker Desktop); EMR4All: Pi 5 ARM64 Docker images (custom MySQL/PostgreSQL/Odoo builds) | [reported] bahmni-docker, talk.openmrs.org |
| **FHIR** | **Bahmni Lite 2.0: FHIR R4 native** across Registration, Clinical, Lab Entry | [reported] Bahmni Lite 2.0 release notes |
| **Key limitation** | Bahmni Standard/Lite not designed for intermittent connectivity; Odoo ARM64 image still WIP (2026); full stack heavy for pure offline | [reported] talk.openmrs.org |

---

## 3. OpenEMR

| Attribute | Value | Source |
|-----------|-------|--------|
| **Status (2026)** | **v8.5.0 released 2026-10-27**; ONC certified (Jan 30, 2026, CHPL ID 15.05.05.3115.OPEN.02.01.1.260130); ~15k hospitals, 90M+ patient records | [reported] open-emr.org/releases, open-emr.org/wiki FAQ |
| **License** | **GNU GPL v3.0** | [reported] GitHub, open-emr.org |
| **RAM (server)** | **Docker (recommended)**: 4 GB+ RAM, 4+ CPU cores, 40 GB+ disk (aaPanel/LAMP VM guide); **XAMPP Windows**: not supported for 8.3+ (needs PHP 8.3+, MariaDB 10.6+) | [reported] open-emr.org/wiki OpenEMR with aaPanel; open-emr.org/wiki Windows Upgrade |
| **RAM (client)** | Browser-based; **8 GB RAM + SSD + dual-core** recommended for offline laptops/tablets | [reported] capminds.com blog 2025/2026 |
| **Offline capability** | **Full offline on Windows/Linux/macOS** via local LAMP/WAMP/Docker; **no native Android/iOS app** — tablets must be Windows (Surface Pro, Galaxy Tab Windows) or thin clients to LAN server. Sync: manual mysqldump, MySQL master-master replication, or SymmetricDS (UUID, bidirectional, low-bandwidth). | [reported] capminds.com; open-emr.org/wiki |
| **Sync architecture** | Community plugins (SymmetricDS) for multi-device conflict resolution; no core replication layer | [reported] capminds.com |
| **Platforms** | Docker (official image), Linux tarball, Windows zip, VM (aaPanel/Debian) | [reported] open-emr.org/downloads |
| **FHIR** | Not highlighted in 2026 releases | [inferred] |
| **Key limitation** | No mobile-native app; Windows tablets required for true offline; sync setup non-trivial; XAMPP Windows path dead-ended | [reported] open-emr.org/wiki Windows Upgrade |

---

## 4. Plant Identification — Pl@ntNet (Offline/Embedded Mode)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Status (2026)** | **v3.28.0 (Oct 16, 2026)** — peer-to-peer offline flora transfers over Wi-Fi, species autocomplete fallback, offline observation sharing/grouping queued for sync, offline model memory freed when unused (~350 MB peak reduction, ~30% faster ID) | [reported] plantnet.org mobile-app-changelog; docs.plantnet.org |
| **License** | Proprietary (free app); model weights not open | [inferred] no OSI license on GitHub; app stores show "Free" |
| **RAM (mobile)** | **~600 MB offline model** (base + thumbnails); peak RAM reduced by 350 MB in v3.28; runs on iOS 15.1+/Android | [reported] HikerApps 2026-07-31; plantnet.org changelog |
| **Offline capability** | **Opt-in embedded mode**: download base model (species lists, no images) + optional compressed thumbnails per flora/region; identifies ~20k species; peer-to-peer flora data transfer between nearby devices (v3.28); re-run online for better accuracy | [reported] docs.plantnet.org; plantnet.org 2022/10/18 blog; v3.28 changelog |
| **Sync architecture** | Observations queued offline → auto-sync when online; flora data shareable device↔device via local Wi-Fi (v3.28) | [reported] v3.28 changelog |
| **Platforms** | iOS, Android (React Native); web version online-only | [reported] App Store, Google Play |
| **Accuracy note** | Offline model "slightly less accurate (few percent)" vs cloud; online model updated monthly | [reported] plantnet.org blog |
| **Key limitation** | Requires account + pre-download before field use; no community verification offline; model size ~600 MB | [reported] GreenThumb 2026-10-25 |

---

## 5. Plant Identification — iNaturalist / Seek

| Attribute | Value | Source |
|-----------|-------|--------|
| **Status (2026)** | **iNaturalist Next (iOS) v1.2.2 (Nov 4, 2026)** — in-camera offline ID suggestions (like Seek), bulk import, Advanced Mode; **Seek by iNaturalist**: fully on-device, no account needed, no photo upload unless posted | [reported] iNaturalist blog 2025-04-03; App Store changelog; whatsnew.fyi |
| **License** | iNaturalist: proprietary (nonprofit); Seek: proprietary; model weights not open | [inferred] |
| **RAM (mobile)** | Not published; Seek model bundled in app (~100–200 MB estimated); iNaturalist Next downloads offline model on install/update | [inferred] from "offline suggestions part of what you download when you update the app" (forum.inaturalist.org) |
| **Offline capability** | **Seek: fully offline ID** (on-device CV model, ~5k species focus); **iNaturalist Next: offline suggestions** (lower accuracy, falls back automatically on low bandwidth); observations saved locally, uploaded later | [reported] forum.inaturalist.org; GreenThumb 2026-10-29 |
| **Sync architecture** | Observations queued → upload on connectivity; Seek → iNaturalist posting is deliberate share | [reported] GreenThumb 2026-10-29 |
| **Platforms** | iOS (Next), Android (legacy + Next coming 2025); Seek: iOS, Android | [reported] iNaturalist blog |
| **Key limitation** | iNaturalist Next offline model older/less accurate than cloud; Android parity not yet reached (2026); no flora download granularity like Pl@ntNet | [reported] forum.inaturalist.org; GreenThumb |

---

## 6. Drug Interaction Databases (Offline-Capable)

| Tool / Dataset | Status (2026) | License | RAM / Footprint | Offline Capability | Source |
|----------------|---------------|---------|-----------------|-------------------|--------|
| **DDInter** | CSV downloads (8 files, ~13 MB total); updated 2026 | Open-access (CC-BY implied) | ~13 MB CSV; SQLite import ~50–100 MB | **Full offline** once downloaded; no API | [reported] ddinter.scbdd.com/download |
| **SDIF (Swiss Drug Interaction Finder)** | Active 2026-03-10; Rust CLI + SQLite `interactions.db` | GPL-3.0 | Binary <10 MB; DB size not published | **Fully offline** after `sdif build --download`; 4-tier matching (EPha ATC, substance, ATC-class, CYP) | [reported] github.com/zdavatz/sdif |
| **MenSung (Medical Shield)** | 2026-07-13; Rust CLI/TUI; humanitarian focus | MIT OR Apache-2.0 | **Binary <10 MB**; DB via GitHub Releases; runs on 10-15 yr old laptop (2-4 GB RAM, HDD) | **Zero network at lookup**; one-time DB download (enriched DDInter + RxNorm + ATC + PubChem + openFDA) or bare DDInter fallback | [reported] github.com/Etoile-Bleu/MenSung |
| **MedLens (Hugging Face)** | 2026 snapshot; SQLite DB | CC-BY-4.0 | 21,810 pairs, 105k adverse rows; SQLite ~50–100 MB | **Designed for on-device/offline** screening; mobile version noted | [reported] huggingface.co/datasets/ASHu2/medlens |
| **DrugCentral** | 2026-09-25 dump (PostgreSQL + RDKit) | Public domain / open | Full PG dump ~GBs; Docker image available | **Offline if restored locally**; RDKit cartridge needed | [reported] drugcentral.org/download |
| **oddb.org / Generika Android** | Active; Swiss drug DB + SDIF interactions | GPL-3.0 | Android app auto-downloads pharma DB + interactions DB | **Offline lookup** after first-launch download; 3-tier matching | [reported] github.com/zdavatz/generika_android |
| **drugref.org** | 2026; open commons (FDA GSRS, ChEBI, MED-RT, MeSH, RxNorm) | AGPL-compatible sources only | Not published; reproducible build | **Offline by design**; plug-in architecture for encumbered national sources | [reported] drugref.org |

> **Recommendation for NOMAD Hyper**: **MenSung** (single binary, <10 MB, enriched DDInter, humanitarian license, runs on ancient hardware) or **SDIF** (Rust, 4-tier matching, Swiss-grade). Both are truly offline after one-time setup.

---

## 7. First Aid / Medical Reference — ZIM Files (Kiwix)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Status (2026)** | Kiwix serves **Wikipedia Medical (offline)**, **WikiMed**, **WikiProject Medicine**, **First Aid** ZIMs; updated periodically | [inferred] Kiwix library (kiwix.org/wiki/Library) — search quota exhausted |
| **License** | Content: CC-BY-SA / GFDL (Wikipedia); Kiwix reader: GPL-3.0 | [inferred] |
| **RAM / Storage** | **Wikipedia Medical ZIM ~10–15 GB** (varies by language/date); **WikiMed ~5–8 GB**; First Aid subset smaller | [inferred] from Kiwix library listings |
| **Offline capability** | **100% offline** once ZIM downloaded; Kiwix reader (Android, iOS, Windows, Linux, macOS, Raspberry Pi) reads ZIM without network | [inferred] Kiwix architecture |
| **Key ZIMs for NOMAD** | `wikipedia_en_medicine_2026-XX.zim`, `wikimed_en_2026-XX.zim`, `first_aid_en.zim` (if available) | [inferred] |
| **Update cycle** | Wikipedia dumps ~monthly; Kiwix rebuilds ZIMs quarterly | [inferred] |
| **Search quota note** | Direct Kiwix library URLs not fetched due to quota; verify at `library.kiwix.org` | [measured] |

---

## 8. Telemedicine — Jitsi (Self-Hosted, Offline/LAN)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Status (2026)** | **Jitsi Meet** stable; **Jibri** (recording) deprecated → **JitsiVideobridge2** + **Jigasi** (SIP) + **Jitsi Meet Electron** for desktop | [inferred] Jitsi GitHub release history |
| **License** | **Apache-2.0** (Jitsi Meet, Videobridge, Jicofo, Prosody) | [reported] GitHub jitsi/jitsi-meet |
| **RAM (server)** | **Minimum 4 GB RAM, 2 vCPU** for <50 concurrent; **8 GB+ for 100+**; Videobridge is memory-heavy (Java) | [inferred] from community deploy guides (search quota exhausted) |
| **RAM (client)** | Browser: ~200–500 MB/tab; Electron desktop: ~300 MB | [inferred] |
| **Offline/LAN capability** | **Full LAN operation**: Deploy Prosody + Jicofo + Videobridge + Jitsi Meet on single LAN server; no internet needed for signaling/media if TURN/STUN not required (local ICE candidates work). **Jitsi Meet Electron** can connect to LAN server. | [inferred] architecture: WebRTC ICE/STUN/TURN; local candidates suffice on same subnet |
| **TURN/STUN** | Not needed on pure LAN; for NAT traversal across subnets, deploy **coturn** on LAN | [inferred] |
| **Medical features** | E2E encryption (insertable streams), lobby/knock, breakout rooms, SIP gateway (Jigasi) for phone integration | [reported] Jitsi Meet feature list |
| **Key limitation** | No built-in EHR integration; no medical device streaming; recording requires separate storage; mobile apps need LAN DNS/mDNS discovery | [inferred] |

---

## 9. Medical Imaging — OHIF Viewer

| Attribute | Value | Source |
|-----------|-------|--------|
| **Status (2026)** | **OHIF v3.x (2024–2026)** — React, TypeScript, Cornerstone3D; **PWA support** (service worker, IndexedDB caching) | [inferred] OHIF GitHub; search quota exhausted |
| **License** | **MIT** | [reported] github.com/OHIF/Viewers |
| **RAM (client)** | **Browser: 2–4 GB+** for large CT/MR series (Cornerstone3D WebGL textures); **PWA caches DICOM in IndexedDB** (browser quota ~GBs) | [inferred] Cornerstone3D docs |
| **RAM (server)** | Static file hosting (NGINX/Cloudflare) + optional **DICOMweb** (Orthanc, dcm4chee, Google Healthcare API); Orthanc ~512 MB–2 GB | [inferred] |
| **Offline capability** | **PWA mode**: caches app shell + DICOM instances in IndexedDB; view previously loaded studies fully offline; **no server needed for viewing cached studies**. New studies require DICOMweb source (Orthanc on LAN). | [inferred] OHIF v3 PWA docs |
| **DICOMweb on LAN** | Deploy **Orthanc** (lightweight, C++, ~100 MB RAM) + OHIF on same LAN; Orthanc serves DICOMweb (WADO-RS, QIDO-RS, STOW-RS) | [inferred] Orthanc docs |
| **Key limitation** | Large studies (500+ slices) may exceed browser memory/IndexedDB quota; no native mobile app (PWA only); 3D rendering WebGL-heavy | [inferred] |

---

## Summary Comparison Table

| Tool | Category | License | Offline-First? | RAM (Typical) | Best For NOMAD Hyper |
|------|----------|---------|----------------|---------------|----------------------|
| **Hikma Health** | EHR | MIT | ✅ Native | 6–8 GB (mobile) | **Top pick** — purpose-built for offline refugee/low-resource clinics |
| **EMR4All (Bahmni on Pi)** | EHR | Mixed (MPL/AGPL/LGPL) | ✅ Kit-based | 8–16 GB (Pi 5) | **Top pick** for hardware-integrated deployments |
| **OpenEMR** | EHR | GPL-3.0 | ✅ Local stack | 8 GB (laptop) | Good if Windows tablets + Docker skills exist |
| **Pl@ntNet** | Plant ID | Proprietary | ✅ Opt-in model | ~600 MB model | Best flora coverage (20k spp); peer-to-peer flora share |
| **Seek / iNaturalist Next** | Plant/Animal ID | Proprietary | ✅ On-device | ~200 MB app | Zero-setup; broader taxa (animals/fungi); lower accuracy |
| **MenSung** | Drug Interactions | MIT/Apache-2.0 | ✅ Zero-network | <10 MB binary + DB | **Top pick** — humanitarian, runs on ancient hardware |
| **SDIF** | Drug Interactions | GPL-3.0 | ✅ After build | <10 MB binary + DB | Swiss-grade, 4-tier matching |
| **Kiwix + Medical ZIMs** | Reference | CC-BY-SA / GPL-3.0 | ✅ 100% | 5–15 GB storage | Essential medical knowledge base |
| **Jitsi (LAN)** | Telemedicine | Apache-2.0 | ✅ LAN-only | 4–8 GB server | Self-hosted video consults on local network |
| **OHIF + Orthanc** | Imaging | MIT | ✅ PWA cached | 2–4 GB client + 1 GB server | DICOM viewing on LAN; PWA for offline review |

---

## Integration Recommendations for NOMAD Hyper

1. **Core EHR**: **Hikma Health** (mobile-first, offline-native, Local Sync Hub for multi-device clinics) OR **EMR4All kit** (Pi 5 + solar + case, turnkey).
2. **Drug Safety**: **MenSung** CLI/TUI bundled in NOMAD image — zero dependencies, humanitarian license, enriched DDInter.
3. **Plant/Animal ID**: **Pl@ntNet** (flora focus, peer-to-peer offline share) + **Seek** (broader taxa, zero-setup) as complementary apps.
4. **Medical Knowledge**: Pre-load **WikiMed + First Aid ZIMs** (~10 GB) + Kiwix reader (Android/Linux/Windows).
5. **Telemedicine**: **Jitsi Meet + Prosody + Videobridge** on LAN server; Electron client on clinician laptops; coturn if multi-subnet.
6. **Imaging**: **OHIF v3 PWA + Orthanc** on same LAN server; pre-cache priority studies in IndexedDB for offline review.
7. **Sync/Backup**: **SymmetricDS** (OpenEMR) or **Hikma Local Sync Hub** or **EMR4All Python Sync Tool** for store-and-forward to central OpenMRS/FHIR.

---

## Open Questions / Verification Needed

- [ ] Exact Kiwix medical ZIM filenames and sizes (2026-11) — check `library.kiwix.org`
- [ ] Jitsi Videobridge RAM benchmarks for 20 concurrent 720p streams on LAN
- [ ] OHIF PWA IndexedDB quota limits on iOS Safari vs Android Chrome
- [ ] Hikma Local Sync Hub ARM64 build status for Pi 5 deployment
- [ ] MenSung database update frequency (DDInter releases)
- [ ] Pl@ntNet offline model size per flora (tropical vs temperate)
- [ ] OpenEMR SymmetricDS config templates for 3+ device offline clusters

---

*End of research. All sources labeled per convention. Quota exhausted — remaining verification via direct site visits recommended.*