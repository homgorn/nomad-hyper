"""Unsloth LoRA training script for NOMAD Hyper domains."""
# Requires: pip install unsloth transformers trl peft accelerate bitsandbytes
# Usage: python scripts/train_lora.py --domain medical --model qwen3.5:4b --epochs 3

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True, choices=["medical", "survival", "repair", "navigation"])
    parser.add_argument("--model", default="qwen3.5:4b")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--output", default="./adapters")
    args = parser.parse_args()

    print(f"Training LoRA adapter for domain={args.domain}, model={args.model}, epochs={args.epochs}")
    print("TODO: implement Unsloth training loop")
    # 1. Load base model with Unsloth
    # 2. Load domain dataset
    # 3. Train LoRA adapter
    # 4. Save adapter to args.output

if __name__ == "__main__":
    main()
