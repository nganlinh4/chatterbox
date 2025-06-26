#!/usr/bin/env python3
"""
Simple test to check if Chatterbox TTS works
"""

import torch
import torchaudio as ta
import time
import traceback

def test_basic_functionality():
    """Test basic TTS functionality"""
    print("🧪 Testing Basic Chatterbox TTS Functionality")
    print("=" * 50)
    
    # Check device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"📱 Using device: {device}")
    
    try:
        # Import and load model
        print("📦 Loading Chatterbox TTS...")
        from chatterbox.tts import ChatterboxTTS
        
        start_time = time.time()
        model = ChatterboxTTS.from_pretrained(device)
        load_time = time.time() - start_time
        print(f"✅ Model loaded in {load_time:.2f}s")
        
        # Test basic generation
        print("🎵 Generating speech...")
        text = "Hello world, this is a test of the Chatterbox text to speech system."
        
        start_time = time.time()
        wav = model.generate(text)
        gen_time = time.time() - start_time
        
        print(f"✅ Speech generated in {gen_time:.2f}s")
        print(f"📊 Audio shape: {wav.shape}")
        print(f"📊 Audio duration: {wav.shape[-1] / model.sr:.2f}s")
        print(f"📊 Sample rate: {model.sr}")
        print(f"📊 Realtime factor: {(wav.shape[-1] / model.sr) / gen_time:.2f}x")
        
        # Save output
        output_path = "simple_test_output.wav"
        ta.save(output_path, wav, model.sr)
        print(f"💾 Audio saved to: {output_path}")
        
        # Test with different parameters
        print("🎛️ Testing parameter variations...")
        
        params_to_test = [
            {"exaggeration": 0.3, "cfg_weight": 0.3},
            {"exaggeration": 0.8, "cfg_weight": 0.7},
        ]
        
        for i, params in enumerate(params_to_test):
            start_time = time.time()
            wav = model.generate(text, **params)
            gen_time = time.time() - start_time
            
            output_path = f"param_test_{i}.wav"
            ta.save(output_path, wav, model.sr)
            print(f"✅ Params {params}: {gen_time:.2f}s, saved to {output_path}")
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    exit(0 if success else 1)
