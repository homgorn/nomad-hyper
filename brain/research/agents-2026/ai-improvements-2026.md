# AI Models/Tools Released in 2026 That Can Improve NOMAD Hyper

**Research Date:** 2026-11-11  
**Scope:** Small edge models, RAG improvements, embedding models, vision models for plant/medical ID, code repair models  
**Method:** 8+ websearch queries, primary sources prioritized  
**Labeling:** **Measured** (benchmark numbers from papers/vendor evals) / **Reported** (vendor claims, press releases) / **Inferred** (analysis based on architecture/specs)

---

## 1. Small Models for Edge Deployment

### 1.1 Needle 2 (Cactus Compute) — **Measured/Reported**

| Attribute | Detail |
|-----------|--------|
| **Release** | 2026-08-10 (v2.0.0); 6 point releases in 6 days |
| **Parameters** | 45M |
| **Size** | 14 MB binary (CQ2-bit quantized) |
| **RAM** | ~28 MB session (256-token sliding window with pinned tool KV sinks) |
| **Architecture** | Simple Attention Network: Hadamard MLP, GQA, engram KV memory, multi-lane hyper-connections |
| **License** | MIT (source) / Apache-2.0 (weights) |
| **Platforms** | macOS, Linux, Windows, Android, iOS, watchOS, tvOS, WebAssembly (x86-64, ARM64, ARMv7, RISC-V) |
| **Tool-calling benchmarks (BFCL v4 single-turn, 3,641 rows)** | Simple 40.8, Python simple 61.2, Java 29.0, JS 32.0, Multiple 57.0, Parallel 30.0, Parallel multiple 22.5, Live simple 36.8 |
| **Well-formed rate** | 93.4% overall |
| **Mobile Actions accuracy** | 63.7% (vs LFM2.5 230M 69.1%, FunctionGemma 270M, Apple FM) |
| **Key differentiator** | Quantization-aware training from pretrain through post-train (Cactus Quants); confidence scoring + empty-call refusal for edge→cloud escalation; grammar-constrained decoding via declared schemas |
| **Python package** | `cactus-needle` (PyPI), weights on Hugging Face (Cactus-Compute/needle2) |
| **Production note** | Very young (first PyPI release 2026-08-10); pin exact version; 16 open issues, 10 open PRs as of 2026-08-16 |

**Relevance to NOMAD Hyper:** Ultra-lightweight agentic tool-calling for on-device NOMAD agents (wearables, phones, robots). Confidence gating enables graceful cloud fallback. Apache-2.0 license allows commercial embedding.

---

### 1.2 Gemma 4 Family (Google DeepMind) — **Measured/Reported**

| Variant | Params | Context | Modalities | Target Hardware | Key Benchmarks (Measured) |
|---------|--------|---------|------------|-----------------|---------------------------|
| **E2B** | 2B eff. | 128K | Text, vision, **audio** | Phones, Raspberry Pi, Jetson Nano, browser (WebGPU) | Arena Elo 1365; MMMLU 60.0%; MMMU Pro 44.2%; AIME 2026 20.8%; LiveCodeBench v6 29.1% |
| **E4B** | 4B eff. | 128K | Text, vision, **audio** | Same as E2B | Arena Elo 1442 (thinking); MMMLU 82.6%; MMMU Pro 73.8%; AIME 88.3%; LiveCodeBench 77.1% |
| **12B** | 12B dense | 256K | Text, vision, **audio** (encoder-free) | Laptops with 16GB VRAM/unified memory | Near-26B MoE performance; encoder-free multimodal reduces latency |
| **26B MoE** | 26B (A4B) | 256K | Text, vision | High-throughput server / desktop GPU | Arena Elo 1442; MMMLU 82.6%; MMMU Pro 73.8%; GPQA Diamond 82.3% |
| **31B** | 31B dense | 256K | Text, vision | Single 80GB H100 | Arena Elo 1451 (thinking); MMMLU 85.2%; MMMU Pro 76.9%; AIME 89.2%; LiveCodeBench 80.0% |

**Key 2026 releases:**
- **2026-03-31:** Initial Gemma 4 (E2B, E4B, 31B, 26B A4B) — Apache 2.0
- **2026-04-16:** Multi-Token Prediction (MTP) drafters for E2B, E4B, 31B, 26B A4B
- **2026-06-03:** Gemma 4 12B Unified (encoder-free multimodal, native audio)
- **2026-06-05:** QAT checkpoints (Q4_0 + mobile-specialized quantization for E2B/E4B)
- **2026-10-06:** EmbeddingGemma 2 (740M, multimodal — see §3)

**Edge deployment stack:** `litert-lm` CLI (Linux, macOS, Raspberry Pi), Google AI Edge Gallery app, Transformers.js (browser), MLX (Apple Silicon), llama.cpp, Ollama, vLLM, SGLang, Unsloth for fine-tuning.

**Relevance to NOMAD Hyper:** E2B/E4B are the strongest Apache-2.0 models for on-device multimodal agents with audio input. QAT mobile quantization enables <500MB RAM footprint. Gemma Skills repository provides agentic skill primitives.

---

### 1.3 Phi-4 Family (Microsoft) — **Measured/Reported**

| Variant | Params | Context | Modalities | Key Benchmarks (Measured) |
|---------|--------|---------|------------|---------------------------|
| **Phi-4** | 14B | 16K | Text | MMLU 84.8%, MATH 80.4%, HumanEval 82.6% |
| **Phi-4-mini** | 3.8B | 128K | Text | Strong long-context; function calling, instruction following |
| **Phi-4-multimodal** | 5.6B | 128K | Speech, vision, text (mixture-of-LoRAs) | Unified speech/vision/text |
| **Phi-4-reasoning** | 14B | 32K | Text | Enhanced reasoning traces |
| **Phi-4-reasoning-plus** | 14B | 32K | Text | Further reasoning improvement |
| **Phi-4-mini-reasoning** | 3.8B | 128K | Text | Mini reasoning |
| **Phi-4-reasoning-vision** | 15B | — | Vision + reasoning | Matches/exceeds larger VLMs on scientific/mathematical multimodal reasoning; excels at computer use |

**Key 2026 releases:**
- **2026-03-04:** Phi-4-reasoning-vision-15B (mid-fusion: SigLIP-2 vision encoder + Phi-4-Reasoning backbone; mixed reasoning/non-reasoning training with `<nothink>` token)
- **2026-05-07:** Phi-4 family on Microsoft Foundry (MIT license)
- **Pricing (Azure AI Foundry, 2026-11-05):** Phi-4 $0.125/$0.50 per 1M in/out; Phi-4-mini $0.075/$0.30; Phi-4-multimodal text/image $0.08/$0.32, audio $4/$0.32

**Relevance to NOMAD Hyper:** Phi-4-mini (3.8B, 128K context) is deployable on phone-class edge (NPU). Phi-4-multimodal enables speech+vision NOMAD agents. MIT license = commercial friendly. Phi-4-reasoning-vision for medical/plant visual reasoning.

---

### 1.4 Qwen 3.5 Small Models (Alibaba) — **Measured**

| Variant | Params | Context | License | Key Benchmarks (Measured) |
|---------|--------|---------|---------|---------------------------|
| **Qwen3.5-0.8B** | 0.8B | 262K (YaRN >1M) | Apache 2.0 | BFCL-V4: 25.3 |
| **Qwen3.5-2B** | 2B | 262K | Apache 2.0 | BFCL-V4: 43.6 |
| **Qwen3.5-4B** | 4B | 262K | Apache 2.0 | BFCL-V4: 50.3; MMLU-Pro 79.1; GPQA Diamond 76.2; MMMU-Pro 66.3; MathVision 74.6 |
| **Qwen3.5-9B** | 9B | 262K | Apache 2.0 | **BFCL-V4: 66.1**; **MMLU-Pro 82.5**; **GPQA Diamond 81.7**; **MMMU-Pro 70.1**; **MathVision 78.9**; beats GPT-OSS-120B & Qwen3-30B on all listed |

**Architecture:** Hybrid Gated DeltaNet; native 262K context, extensible to 1M+ via YaRN.

**Release:** 2026-03-02 (four models simultaneously). All on Hugging Face & ModelScope.

**Relevance to NOMAD Hyper:** Qwen3.5-4B/9B are best-in-class Apache-2.0 tool-calling (BFCL) and vision models for edge. 9B fits 16GB GPU at 4-bit; 4B fits 8GB.

---

### 1.5 Other Notable 2026 Edge Models

| Model | Params | Release | License | Notes |
|-------|--------|---------|---------|-------|
| **Gemma 3n** (E2B/E4B) | 2B/4B eff. | 2025-06-26 | Gemma license | Predecessor to Gemma 4 edge; still relevant for deployed base |
| **FunctionGemma** | 270M | 2025-12-18 | Apache 2.0 | Tool-calling specialist; benchmark baseline for Needle 2 |
| **LFM2.5** | 230M | 2026 | Liquid AI | Needle 2 competitor on Mobile Actions |
| **Apple FM** | — | 2026 | Proprietary | On-device only; Needle 2 benchmark baseline |
| **Ministral 3 8B** | 8B | 2026 | Apache 2.0 | Vision on modest hardware (VDF AI 2026-10-06) |
| **Llama 3.2 3B** | 3B | 2025 | Llama license | Only 3B footprint option (non-Apache) |
| **Granite 4.2 8B** | 8B | 2026 | Apache 2.0 | Tool calling/agents (VDF AI 2026-10-06) |

---

### 1.6 Edge Deployment Reality Check (2026) — **Measured/Inferred**

- **Phone-class edge (NPU):** 1.5B–3B is the deployable SLM size (Scixa 2026-09-08). Fine-tuned Qwen2.5-3B (Q4_K_M) closes ~70% of quality gap to frontier LLMs *on edge workloads*.
- **Tokens/sec benchmarks (Presenc AI 2026-10-02):**
  - RTX 5090: 290–300 tps (Llama 2 7B Q4_0, llama.cpp); 150 tps (Llama 3.1 8B, Ollama)
  - DGX Spark: 38 tps (Llama 3.1 8B); 4.4 tps (Llama 3.1 70B dense); 60.6 tps (gpt-oss 120B MoE)
  - M5 Max: ~120 tps (Llama 2 7B); better memory bandwidth (460–614 GB/s) than DGX Spark (273 GB/s) for dense models
- **Interactive threshold:** >30 tps (chat); 8–30 tps (batch); <8 tps (impractical)
- **Thermal warning:** Test under worst-case thermal conditions, not lab benchmarks (Scixa 2026)
- **QLoRA anomaly:** QLoRA reduces memory but *increases adaptation energy up to 7×* for small models (ACL Industry 2026) — challenges QAT assumptions

---

## 2. RAG Improvements: Graph RAG & Agentic Retrieval

### 2.1 Key 2026 Papers & Frameworks — **Measured** (from paper benchmarks)

| Framework | Venue | Key Innovation | Measured Gains |
|-----------|-------|----------------|----------------|
| **T²RAG** (Triplet-Driven) | ACL 2026 Findings | Graph-free atomic triplets; LLM decomposes questions into searchable triplets with placeholders; iterative resolution | +11% avg across 6 datasets; -45% retrieval cost vs Graph RAG & multi-round RAG |
| **SPARKLE** | ACL 2026 Long | Structured plug-and-play agentic retrieval policy; 3 agents (Retrieval Decision, Query Formulation, Knowledge Integration); dynamic KG chains at reasoning time | +9.17% in-domain, +2.85% out-of-domain vs adaptive RAG baselines |
| **VecTree-RAG** | arXiv 2026-07-25 | Vector search (corpus-level) + reasoning-guided tree traversal (section-level evidence) for scientific QA | QASPER: 0.800 LLM-judge correctness (vs 0.046–0.071 evidence-page precision for baselines); LitQA2: 0.925 accuracy; MOSAIC: 0.547 composite |
| **MemGraphRAG** | KDD 2026 | Memory-based multi-agent graph construction; universal high-quality graph constructor improving HippoRAG, MS-GraphRAG, etc. | HippoRAG 51.07→51.78; MS-GraphRAG consistent improvements across datasets |
| **Entity-Event RAG (E²RAG)** | EACL 2026 | Dual-graph (entity + event subgraphs) with bipartite mapping; preserves temporal/causal consistency | Addresses KG-RAG collapse of entity mentions into single nodes |
| **Is GraphRAG Needed?** | ACL 2026 GEM Workshop | 9 standardized RAG scenarios; context engineering for GraphRAG/Agentic RAG; 19–53% token reduction; identifies retrieval-generation gap | Expanded retrieval ≠ proportional generation quality; retrieval metrics overstate benefits |

### 2.2 Industry Analysis — **Reported**

- **Airbyte (2026-03-23, updated 2026-11-05):** Graph RAG improves F1 by 92% on "how" questions requiring multi-hop reasoning; hybrid patterns (subgraph + text-to-graph-query + hybrid) cover different query types; start with domain-specific pilot (1–2 entity types).
- **Airbyte Graph RAG for Agentic Retrieval:** Three problems with vector-only RAG: (1) cannot follow multi-hop paths, (2) loses relationships, (3) no auditability ("embedding was close" ≠ compliance answer).

### 2.3 Practical Takeaways for NOMAD Hyper — **Inferred**

1. **Don't default to Graph RAG** — use the "Is GraphRAG Needed?" framework to evaluate 9 scenarios first. Many NOMAD queries may be single-hop (vector RAG sufficient).
2. **Agentic retrieval policies (SPARKLE)** — implement structured decision agents for when/what/how to retrieve, especially for multi-step plant/medical diagnosis.
3. **VecTree-RAG pattern** — for NOMAD's plant/medical knowledge base: vector search over document/section summaries + tree traversal for evidence localization.
4. **Context engineering** — 19–53% token reduction via structured representations + agentic loop design critical for edge context windows (128K–256K).
5. **Temporal-causal graphs (E²RAG)** — essential for longitudinal plant growth / medical history tracking.

---

## 3. Embedding Models (2026 Releases)

### 3.1 Major 2026 Releases — **Measured/Reported**

| Model | Params | Context | Modalities | License | Key Specs / Benchmarks |
|-------|--------|---------|------------|---------|------------------------|
| **EmbeddingGemma 2** | 740M (270M text encoder) | 8,192 | Text, code, images, video, audio | Apache 2.0 | Matryoshka: 128–3,072 dims; quantized Pixel 11 Pro: ~191MB RAM (text), ~567MB (full multimodal); unified embedding space |
| **Cohere Embed 5** (Pro/Fast) | — | 128K | Text, images, mixed (PDF pages) | Proprietary (API/Model Vault) | Matryoshka: 256–2048 dims; float/int8/binary; 100+ languages; shared embedding space Pro↔Fast; Embed 5 Fast beats EmbeddingGemma 2 on 95% of 163 datasets (Cohere claim) |
| **Nemotron 3.5 Embed** (1B/8B) | 1.55B / 8.38B | 32,768 | Text, images (page images, tables, charts) | OpenMDW-1.1 | 1B distilled from 8B (95.4% teacher score); ViDoRe v3.1: 8B=61.17 nDCG@10 (#1 dense), 1B=58.38; 34 langs text, 18 langs image; NVFP4 quantized variant |
| **Qwen3-Embedding-8B** | 8B | 32K | Text, code, multilingual | Apache 2.0 | MTEB Multilingual 70.58 (Jun 2025 release); configurable output dims |
| **Voyage Code 4** | — | 32K | Code | Proprietary | CoIR benchmark for code retrieval; 32K context for long files |
| **Gemini Embedding 2** | — | 8,192 | Text, images, audio, video, PDF | Proprietary (API) | Matryoshka 128–3,072 dims; stable release 2026-04-22 |
| **BGE-M3** | — | 8,192 | Dense + sparse + multi-vector (ColBERT) | MIT | 1,024 dense; mature tooling; predates Qwen3/Harrier |
| **Perplexity pplx-embed-v2-late** | 0.6B / 9B | 32K | Late-interaction | MIT | Released Oct 2026 |
| **UltraBERT-Embed-150M** | 150M | 32K | English | — | DMIS Lab, Oct 2026 |

### 3.2 Embedding Model Selection Guidance — **Inferred**

| Use Case | Recommended Primary | Comparison / Fallback |
|----------|---------------------|------------------------|
| **On-device multimodal RAG (NOMAD edge)** | EmbeddingGemma 2 (740M, Apache 2.0, 191MB RAM text) | Nemotron 3.5 Embed 1B (OpenMDW-1.1, 32K context, multimodal) |
| **Enterprise document RAG (PDFs, tables, charts)** | Cohere Embed 5 Pro (index) + Fast (query) | Nemotron 3.5 Embed 8B (quality) / 1B (efficiency) |
| **Code retrieval / agentic coding** | Voyage Code 4 (32K context, CoIR) | Codestral Embed (8K context) |
| **Multilingual (100+ langs)** | Cohere Embed 5 / Qwen3-Embedding-8B | BGE-M3 (sparse+dense hybrid) |
| **Long-context documents (128K)** | Cohere Embed 5 (128K) | Gemini Embedding 2 (8K) / Qwen3 (32K) |
| **Cost-sensitive self-hosted** | BGE-M3 / Qwen3-Embedding / EmbeddingGemma 2 | Nemotron 3.5 Embed (OpenMDW-1.1) |

### 3.3 Critical Notes — **Reported/Measured**

- **MTEB versions not comparable** — English v2, Multilingual v2, partial task sets, provider-run evals differ. Always evaluate on *your* corpus (Respan 2026-11-06, Cognee 2026-09-14).
- **Switching embeddings = re-embedding corpus** — choice is sticky (Inferbase 2026-11-05).
- **Vector storage math:** 1M × 4,096-dim float32 = ~16.4 GB; 1M × 1,024-dim = ~4.1 GB (OpenRouter 2026-09-23).
- **Matryoshka truncation:** L2-normalize retained dimensions; update index consistently (OpenRouter).

---

## 4. Vision Models for Plant / Medical Identification

### 4.1 Medical Vision-Language Models — **Measured** (peer-reviewed benchmarks)

| Model | Params | Release | License | Key Benchmarks (Measured) |
|-------|--------|---------|---------|---------------------------|
| **MedGemma 4B / 27B / 27B Text** | 4B / 27B | 2026-10-06 (Nature Medicine) | Open (Gemma base) | **Medical MCQ:** 4B: 64.1% (Gemma 3 52.4%); 27B Text: 86.2% (Gemma 3 74.9%). **CheXpert (OOD):** 4B Macro F1 48.1 (Gemma 3 32.6). **Pathology MCQ:** 4B 69.8% (Gemma 3 37.1%). **CXR Report Gen:** 81% radiologist-rated "≥ original". **OOD Med VQA:** +2.6–10% vs base. **Agentic eval:** +10.8%. |
| **MedGemma 1.5 4B** | 4B | 2026-04 (arXiv:2604.05081) | Open | High-dim imaging (CT/MRI volumes, histopathology WSI), anatomical localization (bbox), multi-timepoint CXR, medical doc understanding (lab reports, EHR). Outperforms Qwen3-VL-4B on clinical vision tasks. |
| **MedSigLIP** | 400M (encoder) | 2026-10-06 | Open | Multi-domain medical image encoder; powers MedGemma vision; comparable/better than specialized medical encoders. |
| **MedBLIP2** | 2.7B | CVPR 2026 Workshop | Open (GitHub) | MedQFormer alignment; SOTA on medical classification; BLIP-2 architecture with frozen encoders. |
| **Anatomy-VLM** | — | WACV 2026 | — | Fine-grained anatomical localization + structured knowledge; in/out-of-distribution SOTA. |
| **MedPLIB** | — | TPAMI 2026-08 | — | Pixel-level biomedical MLLM; MoE architecture; VQA, grounding, segmentation; 19.7/15.6 mDice improvement zero-shot. |
| **RadiSim-CL** | — | npj Digital Med 2026-06-05 | — | Curriculum learning (radiologist pathway); 5-stage validation (modality→anatomy→localization→diagnosis). |
| **MS-VLM** | — | Med Image Anal 2026-04 | — | 3D medical imaging (CT/MRI); slice-sequential radiologist mimic; CT-RATE + rectal MRI; report generation SOTA. |

**MedGemma availability:** Hugging Face (google/medgemma-*); Google Health AI Developer Foundations (goo.gle/hai-def, goo.gle/medgemma). Demos: EHR Navigator Agent, Radiology Learning Companion.

---

### 4.2 Plant Identification / Agriculture Vision — **Measured** (peer-reviewed)

| Model / System | Params | Release | Key Benchmarks (Measured) |
|----------------|--------|---------|---------------------------|
| **Qwen3-VL-235B** | 235B | 2026 (Frontiers Plant Sci) | **Medicinal plant ID: 90.50% accuracy** (200 images, 4-choice); beats GPT-4o (85%), Gemma3-27B (65.5%), Llama4Scout (58.5%), DeepSeek-VL2 (58%). Advantage: trained on Chinese medical/botanical data. |
| **Qwen3.5-35B-A3B + KG** | 35B | 2026-11-02 (Plant Pathology J) | Plant disease: **68.94% acc / 66.33% macro F1 (K=19)** vs 40.87% direct classification. **GraphRAG-only: 74.55%; Hybrid: 97.27%** (idealized QA, 440 images). Uses Qwen3-Embedding-8B + Neo4j KG. AI Plant Doctor v2. |
| **EfficientViT-Net (hybrid CNN-ViT)** | — | 2026-08-02 (Discov AI) | Indian medicinal plants: **94.7% accuracy**; surpasses pure ViT; XAI (Grad-CAM, Eigen-CAM). |
| **A100 (Agricultural Foundation Model)** | — | 2026-10-16 (arXiv:2610.22991) | 3M unlabeled images, 100+ crops; hybrid CNN-Transformer (MBConv + Transformer). **99.90% (32-class crop ID), 99.02% (44-class disease)**. **98.01% at 1% labels (284 img/cat)** — high label efficiency. Beats FoMo4Wheat, LeafVision by >14 pts at 1% labels. |
| **SAM2 + GroundingDINO + Multimodal (Solidago)** | — | 2026-08-01 (SciDirect) | 18 Solidago species; ROI-focused vision + GPT-4o botanical descriptions; cross-platform mobile app for field ID. |
| **PlantMicro Benchmark** | — | 2026-06-21 (arXiv:2606.22497) | 5,000+ microscopic plant images; standardized VLM eval for microscopy; reveals significant gap in current VLMs. |
| **PlantExpertVQA Dataset** | — | 2026-08-10 (Sci Data) | VQA benchmark for plant science; 4 question types (Visual Attribute Grounding, Detailed Verification, General Health Assessment, Species ID). |

---

### 4.3 Deployment-Relevant Vision Models — **Measured/Reported**

| Model | Size | Edge Suitability | Notes |
|-------|------|------------------|-------|
| **Gemma 4 E2B/E4B** | 2B/4B eff. | **High** (phones, Pi, Jetson, browser) | Native vision + audio; 128K context; QAT mobile quantization; Apache 2.0 |
| **Phi-4-multimodal** | 5.6B | Medium (NPU laptops/phones) | Speech+vision+text unified; MIT license |
| **Qwen3.5-4B/9B** | 4B/9B | Medium-High (consumer GPU) | Vision benchmarks strong (MMMU-Pro 66.3/70.1); Apache 2.0 |
| **MedGemma 4B** | 4B | Medium | Medical specialist; requires fine-tuning for deployment; open weights |
| **SmolVLM2 / Moondream2 / LLaVA / InternVL2-2B** | 2B range | **High** (IPDPSW 2026 eval) | Moondream2: 895ms latency (Jetson Thor), 12GB mem; SmolVLM2: 183–796 tok/s, 3M tok/run |
| **A100 (agri)** | — | Unknown | Foundation model; release planned; label-efficient fine-tuning |

---

### 4.4 Practical Recommendations for NOMAD Hyper — **Inferred**

| Task | Recommended Model(s) | Rationale |
|------|---------------------|-----------|
| **On-device plant ID (phone)** | Gemma 4 E4B (4B) / Qwen3.5-4B / SmolVLM2 | Apache 2.0, <500MB RAM quantized, native vision, 128K context |
| **Medical image triage (edge)** | MedGemma 4B (fine-tuned) / Phi-4-multimodal | Medical domain adaptation; MIT/Apache license |
| **High-accuracy plant disease (server)** | Qwen3.5-35B-A3B + KG (AI Plant Doctor v2) / A100 (when released) | GraphRAG hybrid 97.27%; A100 label-efficient |
| **Microscopic plant analysis** | Wait for PlantMicro-adapted models | Current VLMs have significant gap (PlantMicro benchmark) |
| **Multimodal plant QA (field app)** | Gemma 4 E4B + EmbeddingGemma 2 (unified embedding space) | Same architecture family; on-device RAG |

---

## 5. Code Models for Repair

### 5.1 2026 Code Repair Advances — **Measured** (benchmarks)

| Approach / Model | Venue / Release | Key Innovation | Measured Results |
|------------------|-----------------|----------------|------------------|
| **QiMeng-PRepair** (EA-GRPO) | ACL 2026 Main | Edit-aware reward optimization; Self-Breaking (bug injection) + Self-Repairing; mitigates over-editing | **+31.4% repair precision** (fix₁@1 metric: correctness + extent); increased decoding throughput with speculative editing |
| **Anchored Self-Play (ASP)** | ICML 2026 | Generator-fixer self-play anchored to reference bugs (code-embedding similarity reward + reference bug mixing); BugSourceBench (human/LM/human-edited bugs) | **+25% relative / +7.2 pp absolute** avg fix rate; **+100% relative / +11 pp** on LM-error bugs; **+7.1% / +3.4 pp** on human-authored |
| **SRepair** | CodeSOTA 2026 | — | **101 correct patches** on Defects4J (top of leaderboard) |
| **Claude Opus 4** | CodeSOTA 2026 | — | 89.0 correct patches on Defects4J |
| **GPT-4o** | CodeSOTA 2026 | — | 82.0 correct patches on Defects4J |
| **ChatRepair** | CodeSOTA 2026 | — | 78.0 correct patches on Defects4J |
| **Self-bootstrapping APR** | Expert Systems 2026-07-05 | LLMs generate & evaluate synthetic bug-fix pairs; quality filtering; cross-model eval (DeepSeek-Coder-V2, Qwen2.5-Coder-32B, Qwen3-Coder-30B, Devstral-Small) | Quality-filtered synthetic data significantly enhances APR |
| **Iterative Test-and-Repair** | arXiv 2026-04-07 | Competitive code generation; test-driven repair loop | LLMs modify more lines than human fixes; sometimes generate new solutions; better solving from scratch than patching |

### 5.2 Key Benchmarks & Datasets — **Reported**

- **Defects4J:** 835 real bugs from 17 Java projects; canonical program repair benchmark (CodeSOTA).
- **BugSourceBench (ICML 2026):** Human-authored bugs, human-edited LM bugs, LM-generated errors — reflects real LM-assisted programming.
- **ViDoRe / CoIR:** Visual document retrieval / Code Information Retrieval Benchmark (10 datasets, 8 tasks, 7 domains).
- **ParseBench:** Nemotron 3.5 Parse #1 among <1B param models (75.20 score, 10.5 docs/sec).

### 5.3 Practical Takeaways for NOMAD Hyper — **Inferred**

1. **Edit-aware rewards (PRepair)** — integrate into NOMAD's code repair pipeline to minimize over-editing; critical for preserving developer intent.
2. **Anchored self-play** — generate synthetic training data for NOMAD's repair model using a small reference set of real NOMAD bugs to prevent drift.
3. **BugSourceBench-style evaluation** — test NOMAD repair on three bug sources: human-written, human-edited LM code, LM-generated errors.
4. **Speculative editing + PRepair** — throughput gains for interactive repair latency.
5. **SRepair (101/835 Defects4J)** — investigate architecture; likely combines retrieval + repair + verification loop.

---

## 6. Synthesis: Priority Integration Paths for NOMAD Hyper

### 6.1 Immediate (Q4 2026 / Q1 2027)

| Priority | Integration | Model/Tool | Effort | Impact |
|----------|-------------|------------|--------|--------|
| **1** | On-device agentic tool-calling | **Needle 2** (45M, 14MB) + **Gemma 4 E4B** (4B) | Medium | Enables fully offline NOMAD agents on phones/wearables; confidence gating for cloud escalation |
| **2** | Multimodal embedding for edge RAG | **EmbeddingGemma 2** (740M, Apache 2.0) | Low | Unified text/image/audio/video embeddings on-device (~191MB RAM); replaces separate captioning+embedding pipeline |
| **3** | Medical vision for health features | **MedGemma 4B** (fine-tuned) | Medium | SOTA medical VQA/classification/report gen; open weights; deployable on 16GB edge |
| **4** | Plant disease ID for agri features | **AI Plant Doctor v2** (Qwen3.5-35B-A3B + KG) OR **A100** (when released) | High | Hybrid GraphRAG 97.27% accuracy; modular explainable framework |
| **5** | Code repair precision | **PRepair (EA-GRPO)** + **Anchored Self-Play** | High | 31.4% precision gain; prevents over-editing; synthetic data generation for NOMAD-specific bugs |

### 6.2 Strategic (2027)

- **Phi-4-multimodal / Gemma 4 E2B/E4B** convergence: unified speech+vision+text on-device for multimodal NOMAD agents.
- **Nemotron 3.5 Embed 1B** (OpenMDW-1.1) as EmbeddingGemma 2 alternative for 32K context + multimodal enterprise docs.
- **GraphRAG/agentic retrieval** (SPARKLE, VecTree-RAG) for NOMAD knowledge base: plant taxonomy, medical conditions, code patterns.
- **Qwen3.5-9B** as strongest Apache-2.0 edge model for tool-calling + vision if hardware permits (16GB GPU).

### 6.3 Licensing & Commercial Readiness

| Model | License | Commercial Safe? |
|-------|---------|------------------|
| Needle 2 | MIT / Apache-2.0 | ✅ |
| Gemma 4 family | Apache 2.0 | ✅ |
| Phi-4 family | MIT | ✅ |
| Qwen 3.5 | Apache 2.0 | ✅ |
| EmbeddingGemma 2 | Apache 2.0 | ✅ |
| MedGemma | Gemma-based (open) | ✅ (verify Gemma 3 terms) |
| Nemotron 3.5 Embed | OpenMDW-1.1 | ✅ (check terms) |
| Cohere Embed 5 | Proprietary (API) | ⚠️ API-only |
| Voyage Code 4 | Proprietary | ⚠️ API-only |

---

## 7. Sources Summary

| # | Query | Key Sources |
|---|-------|-------------|
| 1 | Needle 2 2026 | Cactus Compute blog (2026-08-09), MarkTechPost (2026-08-13), GitHub cactus-compute/needle, HF Cactus-Compute/needle2 |
| 2 | Gemma 4 2026 | Google DeepMind blog (2026-03-31), Google Developers Blog (2026-04-02, 2026-06-03, 2026-06-05), ai.google.dev/gemma releases |
| 3 | Phi-4 2026 | Azure AI Foundry blog (2026-05-01), MS Research blog (2026-03-04), Foundry Labs, Azure pricing (2026-11-05) |
| 4 | Graph/Agentic RAG 2026 | ACL 2026 papers: T²RAG, SPARKLE, VecTree-RAG, Is GraphRAG Needed?; KDD 2026 MemGraphRAG; EACL 2026 E²RAG; Airbyte blogs (2026-03-23, updated 2026-11-05) |
| 5 | Embedding models 2026 | Respan (2026-11-06), Inferbase (2026-11-05), Maximem (2026-10-29), Airbyte (2026-06-16 updated 2026-11-05), Cognee (2026-09-14), OpenRouter (2026-09-23), ZenMux (2026-10-29), ReviewRamble (2026-11-07) |
| 6 | Plant/medical vision 2026 | Nature Medicine MedGemma (2026-10-06), Frontiers Plant Sci Qwen3-VL (2026-06-26), Plant Pathology J (2026-11-02), Discov AI (2026-08-02), arXiv A100 (2026-10-16), Sci Data PlantExpertVQA (2026-08-10), arXiv PlantMicro (2026-06-21), CVPR/WACV/TPAMI 2026 papers |
| 7 | Code repair 2026 | ACL 2026 QiMeng-PRepair, ICML 2026 Anchored Self-Play, CodeSOTA Defects4J leaderboard (2026), Expert Systems 2026-07-05, arXiv 2026-04-07 |

---

## 8. Confidence Assessment

| Area | Confidence (0-10) | Notes |
|------|-------------------|-------|
| Needle 2 specs/benchmarks | 9 | Primary source blog + GitHub + multiple secondary confirmations |
| Gemma 4 family | 9 | Official Google DeepMind / Developers blog; model cards; release timeline |
| Phi-4 family | 8 | Microsoft Foundry + Research blog + Azure pricing; some benchmarks from vendor |
| Qwen 3.5 | 8 | NYU Shanghai RITS article + benchmark tables; Apache 2.0 confirmed |
| Graph/Agentic RAG papers | 9 | ACL/KDD/EACL 2026 proceedings; PDFs accessible |
| Embedding models 2026 | 8 | Multiple independent reviews (Respan, Inferbase, Cognee, OpenRouter); some vendor claims unverified |
| MedGemma | 9 | Nature Medicine peer-reviewed (2026-10-06); detailed benchmarks; open release |
| Plant vision benchmarks | 8 | Peer-reviewed journals (Frontiers, Plant Pathology, Discov AI); some idealized conditions noted |
| Code repair (PRepair, ASP) | 9 | ACL/ICML 2026 peer-reviewed; CodeSOTA leaderboard independent |

---

**Next Steps for NOMAD Hyper Team:**
1. Prototype Needle 2 + Gemma 4 E4B on-device agent loop (Week 1-2)
2. Integrate EmbeddingGemma 2 for multimodal edge RAG (Week 2-3)
3. Evaluate MedGemma 4B fine-tuning for NOMAD medical features (Week 3-4)
4. Pilot AI Plant Doctor v2 / A100 for agriculture module (Month 2)
5. Implement PRepair-style edit-aware reward in code repair pipeline (Month 2)

---

*Document generated by deep research subagent. All benchmarks labeled per source type. Verify critical numbers against primary sources before production decisions.*