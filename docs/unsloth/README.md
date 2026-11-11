# Unsloth LoRA Training for NOMAD Hyper

## Overview
Train specialized LoRA adapters for NOMAD domains (medical, survival, repair, navigation)
on local 4GB GPU + CPU, and in parallel in cloud.

## Local setup (4GB GPU + CPU)
1. Install Unsloth: https://unsloth.ai/docs/get-started
2. Install dependencies: pip install unsloth transformers trl peft accelerate bitsandbytes
3. Use QLoRA (4-bit) for 4GB VRAM

## Base models (fit in 4GB)
- Qwen3.5 0.8b / 2b / 4b (QLoRA)
- Qwen2.5 0.5b / 1.5b (fallback)

## Training data
- Domain-specific corpora from Kiwix ZIM + curated datasets
- Medical: Merck Manual, WHO Essential Medicines
- Survival: SAS Survival Guide, Wilderness Medicine
- Repair: iFixit guides, Arduino/ESP32 docs
- Navigation: OSM, trail data

## Roadmap
- [ ] Collect training data from medical/survival ZIM collections
- [ ] Fine-tune Qwen3.5-4b for medical domain
- [ ] Fine-tune Qwen3.5-2b for survival domain
- [ ] Set up internal training API (FastAPI + Unsloth)
- [ ] Cloud parallel training (RunPod / Lambda)
- [ ] Evaluate and merge adapters
- [ ] Publish adapters to HuggingFace (optional)

## Cloud parallel
- RunPod: https://runpod.io
- Lambda Labs: https://lambdalabs.com
- Vast.ai: https://vast.ai

## Internal API
FastAPI endpoint for submitting training jobs, checking status, downloading adapters.
Endpoint: POST /api/train { model, dataset, epochs, lr }
