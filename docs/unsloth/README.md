# Unsloth LoRA Training for NOMAD Hyper

## Overview
Train specialized LoRA adapters for NOMAD domains (medical, survival, repair, navigation)
on local 4GB GPU + CPU, and in parallel in cloud.

## Local setup (4GB GPU + CPU)
1. Install Unsloth Desktop (Windows/macOS/Linux) or CLI: https://unsloth.ai/docs/get-started
2. Install dependencies: pip install unsloth transformers trl peft accelerate bitsandbytes
3. Use QLoRA (4-bit) for 4GB VRAM
4. Unsloth Desktop provides web UI for training + OpenAI-compatible inference endpoint

## Base models (fit in 4GB)
- Qwen3.5 0.8b / 2b / 4b (QLoRA) — multimodal, 256K context
- Qwen3.6 27b (QLoRA, needs 16GB+ VRAM) — agentic coding
- Qwen3.8 flash (experimental, Qwen4 architecture preview)
- DeepSeek V4 Flash distilled variants
- Unsloth provides 2-5x faster training, 50-70% less VRAM vs HF+FA2

## Training methods
- LoRA / QLoRA (4-bit, 8-bit)
- Full fine-tuning (needs more VRAM)
- GRPO (reinforcement learning)
- DPO (preference optimization)
- FP8 LoRA (Ada/Hopper/Blackwell)
- Vision RL (multimodal)

## Export formats
- GGUF (q4_k_m, q5_k_m, etc.) for Ollama/llama.cpp
- FP8 for vLLM
- Merged 16-bit for HuggingFace
- OpenAI-compatible inference endpoint (Unsloth Desktop)

## Training data
- Domain-specific corpora from Kiwix ZIM + curated datasets
- Medical: Merck Manual, WHO Essential Medicines
- Survival: SAS Survival Guide, Wilderness Medicine
- Repair: iFixit guides, Arduino/ESP32 docs
- Navigation: OSM, trail data

## Unsloth Desktop features (2026)
- Web UI for training and inference
- OpenAI-compatible API endpoint (connect to Claude Code, Codex, OpenCode)
- `unsloth start --as-subagent` for delegating tasks to local model
- AMD GPU support (Windows/WSL/Linux)
- ARM64 Windows CUDA
- LTX-2.5 + Wan2.2 video generation
- Image LoRA training with aspect-ratio buckets

## Roadmap
- [ ] Collect training data from medical/survival ZIM collections
- [ ] Fine-tune Qwen3.5-4b for medical domain (QLoRA, 4GB)
- [ ] Fine-tune Qwen3.5-2b for survival domain
- [ ] Set up internal training API (FastAPI + Unsloth)
- [ ] Cloud parallel training (RunPod / Lambda / Vast.ai)
- [ ] Evaluate and merge adapters
- [ ] Publish adapters to HuggingFace (optional)
- [ ] Integrate Unsloth Desktop as local inference backend

## Cloud parallel
- RunPod: https://runpod.io
- Lambda Labs: https://lambdalabs.com
- Vast.ai: https://vast.ai

## Internal API
FastAPI endpoint for submitting training jobs, checking status, downloading adapters.
Endpoint: POST /api/train { model, dataset, epochs, lr }

## References
- Unsloth docs: https://docs.unsloth.ai
- Unsloth changelog: https://unsloth.ai/docs/new/changelog
- Qwen3.5 Unsloth guide: https://unsloth.ai/docs/models/qwen3.5

