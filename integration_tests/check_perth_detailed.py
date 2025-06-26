import perth
print("Perth module analysis:")
print(f"PerthImplicitWatermarker: {perth.PerthImplicitWatermarker}")
print(f"Type: {type(perth.PerthImplicitWatermarker)}")

# Check if we can use DummyWatermarker instead
dummy = perth.DummyWatermarker()
print(f"DummyWatermarker methods: {[m for m in dir(dummy) if not m.startswith('_')]}")

# Test dummy watermarker
import numpy as np
test_audio = np.random.randn(16000)  # 1 second of random audio
try:
    watermarked = dummy.apply_watermark(test_audio, sample_rate=16000)
    print(f"Dummy watermarker works: {watermarked.shape}")
    
    watermark = dummy.get_watermark(watermarked, sample_rate=16000)
    print(f"Watermark detection: {watermark}")
except Exception as e:
    print(f"Dummy watermarker error: {e}")
