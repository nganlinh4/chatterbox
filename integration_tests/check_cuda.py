#!/usr/bin/env python3
import torch

print("🔍 CUDA Environment Check")
print("=" * 30)
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA device count: {torch.cuda.device_count()}")
    print(f"Current device: {torch.cuda.current_device()}")
    print(f"Device name: {torch.cuda.get_device_name()}")
    print(f"CUDA version: {torch.version.cuda}")
else:
    print("CUDA not available - will use CPU")

print(f"PyTorch version: {torch.__version__}")
