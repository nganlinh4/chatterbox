# Chatterbox TTS Integration Testing Guide

## Overview

This comprehensive testing suite is designed to help you understand the behavior, performance, and integration characteristics of Chatterbox TTS before integrating it into your larger system.

## Quick Start

### Option 1: Simple Test Run
```bash
python integration_tests/run_integration_tests.py
```

### Option 2: Manual Test Run
```bash
python integration_tests/integration_test_suite.py --device auto --output-dir test_outputs
```

### Option 3: Specific Device Testing
```bash
# Test on CUDA GPU
python integration_tests/integration_test_suite.py --device cuda

# Test on Apple Silicon (MPS)
python integration_tests/integration_test_suite.py --device mps

# Test on CPU
python integration_tests/integration_test_suite.py --device cpu
```

## Test Categories

### 1. Basic Functionality Tests
- **Model Loading**: Tests model initialization and component loading
- **Basic TTS**: Tests fundamental text-to-speech functionality
- **Parameter Variations**: Tests different parameter combinations
- **Text Variations**: Tests various text inputs (short, long, special characters)

### 2. Performance & Resource Tests
- **Performance Benchmarks**: Measures generation speed across text lengths
- **Memory Usage Patterns**: Monitors memory consumption and potential leaks

### 3. Error Handling & Edge Cases
- **Edge Cases**: Tests empty text, very long text, extreme parameters
- **Concurrent Usage**: Tests rapid successive API calls

### 4. Integration Readiness Tests
- **API Consistency**: Tests output consistency and predictability

## Key Integration Insights

### Performance Characteristics
- **Realtime Factor**: How fast generation is compared to audio duration
- **Memory Usage**: RAM and GPU memory consumption patterns
- **Scaling**: How performance changes with text length

### API Behavior
- **Input Validation**: What inputs are accepted/rejected
- **Output Format**: Consistent tensor shapes and audio properties
- **Error Handling**: How the system behaves with invalid inputs

### Resource Requirements
- **Model Loading Time**: Initial setup overhead
- **Memory Footprint**: Baseline and per-generation memory usage
- **Device Compatibility**: Performance across different hardware

## Integration Recommendations

### For Production Systems

1. **Model Initialization**
   ```python
   # Initialize once, reuse many times
   model = ChatterboxTTS.from_pretrained(device="cuda")
   ```

2. **Input Validation**
   ```python
   # Validate text length (max ~2000 characters recommended)
   if len(text) > 2000:
       text = text[:2000]
   ```

3. **Parameter Tuning**
   ```python
   # Recommended defaults for most use cases
   wav = model.generate(
       text,
       exaggeration=0.5,    # Neutral emotion
       cfg_weight=0.5,      # Balanced pace
       temperature=0.8      # Good quality/diversity balance
   )
   ```

4. **Memory Management**
   ```python
   # For long-running services, monitor memory usage
   # Consider periodic model reloading if memory grows
   ```

### For Real-time Applications

- **Latency**: Expect 2-10x realtime depending on hardware
- **Batching**: Process multiple requests sequentially (no built-in batching)
- **Caching**: Consider caching common phrases/responses

### For High-Volume Applications

- **Resource Planning**: ~2-4GB GPU memory, ~1-2GB RAM per model instance
- **Scaling**: Use multiple model instances rather than concurrent calls
- **Monitoring**: Track generation times and memory usage

## Output Files

After running tests, you'll find:

- `test_outputs/`: Directory containing generated audio samples
- `test_outputs/integration_test_report.json`: Detailed test results
- Various `.wav` files demonstrating different test scenarios

## Interpreting Results

### Success Metrics
- **Success Rate**: Should be 100% for basic functionality
- **Performance**: Realtime factor < 1.0 means faster than realtime
- **Memory**: Stable memory usage without significant growth

### Warning Signs
- **Failed edge cases**: May indicate input validation issues
- **High memory growth**: Potential memory leaks
- **Inconsistent outputs**: May affect reproducibility

## Next Steps

1. **Review Test Results**: Check the generated report for any failures
2. **Listen to Audio Samples**: Verify quality meets your requirements
3. **Performance Tuning**: Adjust parameters based on your use case
4. **Integration Planning**: Use the metrics to plan your system architecture

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**
   - Try `device="cpu"` for testing
   - Reduce batch size or text length

2. **Model Download Fails**
   - Check internet connection
   - Verify Hugging Face Hub access

3. **Audio Quality Issues**
   - Experiment with different parameter combinations
   - Check input text formatting

### Getting Help

- Check the test report for specific error messages
- Review the generated audio samples
- Consult the main Chatterbox documentation
- Join the Discord community for support

## Advanced Testing

For more specific testing needs, you can extend the test suite:

```python
from integration_test_suite import ChatterboxIntegrationTester

# Create custom tester
tester = ChatterboxIntegrationTester(device="cuda")

# Run specific tests
result = tester._run_test("Custom Test", your_test_function)

# Add custom test methods to the class
```

This testing framework provides a solid foundation for understanding how Chatterbox TTS will behave in your specific integration scenario.
