---
id: unsloth-lora
title: Unsloth LoRA Training
summary: LoRA training with Unsloth on 4GB GPU + CPU locally and in parallel in cloud. Internal API for training jobs. Roadmap for additional models.
tags: [unsloth, lora, training, gpu]
entities: [Unsloth, LoRA, GPU]
claims: []
sources: [docs/hyper/hyperspec.md]
updated: 2026-11-11
---

# Unsloth LoRA Training

## Goal
Train specialized LoRA adapters for NOMAD domains (medical, survival, repair, navigation)
on local 4GB GPU + CPU, and in parallel in cloud.

## Local setup
- Unsloth (https://unsloth.ai) supports 4GB VRAM with QLoRA
- Base models: Qwen3.5 0.8b/2b/4b (fit in 4GB)
- Training data: domain-specific corpora from Kiwix ZIM + curated datasets

## Roadmap
- [ ] Collect training data from medical/survival ZIM collections
- [ ] Fine-tune Qwen3.5-4b for medical domain
- [ ] Fine-tune Qwen3.5-2b for survival domain
- [ ] Set up internal training API (FastAPI + Unsloth)
- [ ] Cloud parallel training (RunPod / Lambda)
- [ ] Evaluate and merge adapters

## Resources
- Unsloth docs: https://unsloth.ai/docs
- Qwen3.5 Unsloth guide: https://unsloth.ai/docs/models/qwen3.5
