# Chatterbox TTS Integration Tests

This folder contains comprehensive integration tests and utilities for testing Chatterbox TTS before integrating it into larger systems.

## 📁 Files Overview

### 🧪 **Main Test Scripts**
- **`integration_test_suite.py`** - Comprehensive test suite with performance metrics
- **`run_integration_tests.py`** - Simple test runner script
- **`patched_test.py`** - Working test script with watermarker fixes

### 📋 **Documentation**
- **`integration_testing_guide.md`** - Detailed testing guide and instructions
- **`test_results_summary.md`** - Results from the successful test run

### 🔧 **Utility Scripts**
- **`simple_test.py`** - Basic functionality test
- **`check_cuda.py`** - CUDA environment checker
- **`check_perth.py`** - Perth watermarker module checker
- **`check_perth_detailed.py`** - Detailed Perth module analysis

### 🎵 **Generated Audio Samples**
- **`patched_test_output.wav`** - Basic TTS test output
- **`test_case_0_low_exaggeration.wav`** - Low emotion parameters
- **`test_case_1_high_exaggeration.wav`** - High emotion parameters
- **`test_case_2_different_temperature.wav`** - Different temperature setting
- **`length_test_short.wav`** - Short text sample (0.76s)
- **`length_test_medium.wav`** - Medium text sample (2.56s)
- **`length_test_long.wav`** - Long text sample (11.04s)

## 🚀 Quick Start

### Run All Tests
```bash
python integration_tests/run_integration_tests.py
```

### Run Specific Test
```bash
python integration_tests/patched_test.py
```

### Check CUDA Setup
```bash
python integration_tests/check_cuda.py
```

## 📁 Directory Structure

```
chatterbox/                          # Original Chatterbox TTS repository (git managed)
├── LICENSE                          # Keep this updated with git
├── README.md                        # Original documentation
├── src/                             # Source code
└── [other original files]           # All original repo files

integration_tests/                   # Our test suite (separate from git repo)
├── README.md                        # This file
├── integration_test_suite.py        # Comprehensive test suite
├── run_integration_tests.py         # Simple test runner
├── patched_test.py                  # Working test with fixes
└── [other test files and audio]     # Test scripts and generated samples

test_env/                            # Virtual environment
```

## 🔄 Git Management

The `chatterbox/` directory is the original repository that you can update with:
```bash
cd chatterbox
git pull origin main
```

The `integration_tests/` folder is separate and won't be affected by git updates to the original repository.

## ✅ Test Results Summary

**Status**: All tests passed successfully!

- **Device**: CUDA (RTX 4050)
- **Performance**: 0.72x - 1.17x realtime factor
- **Memory**: Stable, no leaks detected
- **Quality**: High-quality audio generation

## 🎯 Integration Ready

The system has been validated and is ready for integration into larger systems. See `test_results_summary.md` for detailed metrics and recommendations.

## 📞 Support

All tests completed successfully. The audio samples demonstrate the quality and capabilities of the system across different scenarios and parameters.
