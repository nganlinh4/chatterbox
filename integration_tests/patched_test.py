#!/usr/bin/env python3
"""
Patched test for Chatterbox TTS that works around the watermarker issue
"""

import torch
import torchaudio as ta
import time
import traceback
import perth

# Monkey patch the perth module to fix the None issue
if perth.PerthImplicitWatermarker is None:
    print("🔧 Patching PerthImplicitWatermarker with DummyWatermarker")
    perth.PerthImplicitWatermarker = perth.DummyWatermarker

def test_chatterbox_with_patch():
    """Test Chatterbox TTS with watermarker patch"""
    print("🧪 Testing Chatterbox TTS (Patched)")
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
        output_path = "patched_test_output.wav"
        ta.save(output_path, wav, model.sr)
        print(f"💾 Audio saved to: {output_path}")
        
        # Test with different parameters
        print("🎛️ Testing parameter variations...")
        
        test_cases = [
            {"name": "Low exaggeration", "exaggeration": 0.3, "cfg_weight": 0.3},
            {"name": "High exaggeration", "exaggeration": 0.8, "cfg_weight": 0.7},
            {"name": "Different temperature", "temperature": 1.2},
        ]
        
        for i, case in enumerate(test_cases):
            name = case.pop("name")
            start_time = time.time()
            wav = model.generate(text, **case)
            gen_time = time.time() - start_time
            
            output_path = f"test_case_{i}_{name.replace(' ', '_').lower()}.wav"
            ta.save(output_path, wav, model.sr)
            print(f"✅ {name}: {gen_time:.2f}s, saved to {output_path}")
        
        # Test different text lengths
        print("📝 Testing different text lengths...")
        
        texts = [
            ("Short", "Hello."),
            ("Medium", "This is a medium length sentence for testing purposes."),
            ("Long", "This is a much longer text that contains multiple sentences. It includes various types of content to test how the system handles longer inputs. The goal is to see how performance scales with text length."),
        ]
        
        for name, test_text in texts:
            start_time = time.time()
            wav = model.generate(test_text)
            gen_time = time.time() - start_time
            
            output_path = f"length_test_{name.lower()}.wav"
            ta.save(output_path, wav, model.sr)
            
            print(f"✅ {name} ({len(test_text)} chars): {gen_time:.2f}s, "
                  f"audio: {wav.shape[-1] / model.sr:.2f}s, "
                  f"RT factor: {(wav.shape[-1] / model.sr) / gen_time:.2f}x")
        
        print("\n🎉 All tests passed!")
        print("\n📊 Summary:")
        print(f"   • Model loading time: {load_time:.2f}s")
        print(f"   • Device: {device}")
        print(f"   • Sample rate: {model.sr}")
        print(f"   • Generated multiple audio files for testing")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chatterbox_with_patch()
    exit(0 if success else 1)
