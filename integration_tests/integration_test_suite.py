#!/usr/bin/env python3
"""
Comprehensive Integration Test Suite for Chatterbox TTS
======================================================

This test suite is designed to help you understand the behavior, performance,
and integration characteristics of Chatterbox TTS before integrating it into
a larger system.

Test Categories:
1. Basic Functionality Tests
2. Performance & Resource Tests  
3. Parameter Sensitivity Tests
4. Error Handling & Edge Cases
5. Memory & Resource Management
6. Integration Readiness Tests
"""

import time
import json
import traceback
import psutil
import torch
import torchaudio as ta
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from chatterbox.tts import ChatterboxTTS
from chatterbox.vc import ChatterboxVC


@dataclass
class TestResult:
    """Structure to hold test results"""
    test_name: str
    success: bool
    execution_time: float
    memory_usage_mb: float
    gpu_memory_mb: Optional[float]
    output_info: Dict[str, Any]
    error_message: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)


class ChatterboxIntegrationTester:
    """Comprehensive test suite for Chatterbox TTS integration"""
    
    def __init__(self, device: str = "auto", output_dir: str = "test_outputs"):
        self.device = self._detect_device() if device == "auto" else device
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results: List[TestResult] = []
        self.model_tts: Optional[ChatterboxTTS] = None
        self.model_vc: Optional[ChatterboxVC] = None
        
        print(f"🚀 Initializing Chatterbox Integration Tester")
        print(f"📱 Device: {self.device}")
        print(f"📁 Output directory: {self.output_dir}")
        
    def _detect_device(self) -> str:
        """Auto-detect the best available device"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def _get_memory_usage(self) -> tuple[float, Optional[float]]:
        """Get current memory usage (RAM and GPU if available)"""
        ram_mb = psutil.Process().memory_info().rss / 1024 / 1024
        gpu_mb = None
        if torch.cuda.is_available():
            gpu_mb = torch.cuda.memory_allocated() / 1024 / 1024
        return ram_mb, gpu_mb
    
    def _run_test(self, test_name: str, test_func, *args, **kwargs) -> TestResult:
        """Run a single test and capture metrics"""
        print(f"\n🧪 Running: {test_name}")
        
        start_time = time.time()
        start_ram, start_gpu = self._get_memory_usage()
        
        try:
            output_info = test_func(*args, **kwargs)
            success = True
            error_message = None
        except Exception as e:
            output_info = {}
            success = False
            error_message = str(e)
            print(f"❌ Test failed: {error_message}")
            traceback.print_exc()
        
        end_time = time.time()
        end_ram, end_gpu = self._get_memory_usage()
        
        result = TestResult(
            test_name=test_name,
            success=success,
            execution_time=end_time - start_time,
            memory_usage_mb=end_ram - start_ram,
            gpu_memory_mb=end_gpu - start_gpu if end_gpu and start_gpu else None,
            output_info=output_info,
            error_message=error_message
        )
        
        self.results.append(result)
        
        if success:
            print(f"✅ Completed in {result.execution_time:.2f}s")
        
        return result

    # ==================== BASIC FUNCTIONALITY TESTS ====================
    
    def test_model_loading(self) -> Dict[str, Any]:
        """Test model loading and initialization"""
        self.model_tts = ChatterboxTTS.from_pretrained(self.device)
        
        return {
            "model_loaded": True,
            "device": self.device,
            "sample_rate": self.model_tts.sr,
            "model_components": {
                "t3": type(self.model_tts.t3).__name__,
                "s3gen": type(self.model_tts.s3gen).__name__,
                "ve": type(self.model_tts.ve).__name__,
                "tokenizer": type(self.model_tts.tokenizer).__name__,
            }
        }
    
    def test_basic_tts(self) -> Dict[str, Any]:
        """Test basic text-to-speech functionality"""
        if not self.model_tts:
            self.model_tts = ChatterboxTTS.from_pretrained(self.device)
        
        text = "Hello world, this is a basic test of the text to speech system."
        wav = self.model_tts.generate(text)
        
        output_path = self.output_dir / "basic_tts.wav"
        ta.save(str(output_path), wav, self.model_tts.sr)
        
        return {
            "text_length": len(text),
            "audio_shape": wav.shape,
            "audio_duration_seconds": wav.shape[-1] / self.model_tts.sr,
            "output_file": str(output_path),
            "sample_rate": self.model_tts.sr
        }
    
    def test_parameter_variations(self) -> Dict[str, Any]:
        """Test different parameter combinations"""
        if not self.model_tts:
            self.model_tts = ChatterboxTTS.from_pretrained(self.device)
        
        text = "Testing parameter variations for integration."
        results = {}
        
        # Test different parameter combinations
        param_sets = [
            {"exaggeration": 0.3, "cfg_weight": 0.3, "temperature": 0.6},
            {"exaggeration": 0.5, "cfg_weight": 0.5, "temperature": 0.8},
            {"exaggeration": 0.8, "cfg_weight": 0.7, "temperature": 1.0},
        ]
        
        for i, params in enumerate(param_sets):
            wav = self.model_tts.generate(text, **params)
            output_path = self.output_dir / f"params_test_{i}.wav"
            ta.save(str(output_path), wav, self.model_tts.sr)
            
            results[f"param_set_{i}"] = {
                "parameters": params,
                "audio_duration": wav.shape[-1] / self.model_tts.sr,
                "output_file": str(output_path)
            }
        
        return results

    def test_text_variations(self) -> Dict[str, Any]:
        """Test different types of text input"""
        if not self.model_tts:
            self.model_tts = ChatterboxTTS.from_pretrained(self.device)
        
        test_texts = [
            "Short text.",
            "This is a medium length sentence with some punctuation, numbers like 123, and common words.",
            "This is a much longer text that contains multiple sentences. It includes various punctuation marks! Does it handle questions? It should also handle different types of content including technical terms, abbreviations like TTS, and various linguistic patterns that might appear in real-world applications.",
            "Testing special characters: @#$%^&*()_+-=[]{}|;':\",./<>?",
            "Numbers and dates: 123, 456.78, January 1st 2024, phone number 555-123-4567.",
        ]
        
        results = {}
        for i, text in enumerate(test_texts):
            wav = self.model_tts.generate(text)
            output_path = self.output_dir / f"text_variation_{i}.wav"
            ta.save(str(output_path), wav, self.model_tts.sr)
            
            results[f"text_{i}"] = {
                "text": text,
                "text_length": len(text),
                "audio_duration": wav.shape[-1] / self.model_tts.sr,
                "output_file": str(output_path)
            }

        return results

    # ==================== PERFORMANCE & RESOURCE TESTS ====================

    def test_performance_benchmarks(self) -> Dict[str, Any]:
        """Benchmark performance across different text lengths"""
        if not self.model_tts:
            self.model_tts = ChatterboxTTS.from_pretrained(self.device)

        test_cases = [
            ("short", "Quick test."),
            ("medium", "This is a medium length sentence for performance testing."),
            ("long", "This is a much longer text that will help us understand how performance scales with input length. " * 3),
        ]

        results = {}
        for name, text in test_cases:
            # Warm up
            _ = self.model_tts.generate(text)

            # Actual benchmark
            times = []
            for _ in range(3):  # Run 3 times for average
                start = time.time()
                wav = self.model_tts.generate(text)
                end = time.time()
                times.append(end - start)

            avg_time = np.mean(times)
            std_time = np.std(times)

            results[name] = {
                "text_length": len(text),
                "avg_generation_time": avg_time,
                "std_generation_time": std_time,
                "audio_duration": wav.shape[-1] / self.model_tts.sr,
                "realtime_factor": (wav.shape[-1] / self.model_tts.sr) / avg_time
            }

        return results

    # ==================== ERROR HANDLING & EDGE CASES ====================

    def test_edge_cases(self) -> Dict[str, Any]:
        """Test edge cases and error handling"""
        if not self.model_tts:
            self.model_tts = ChatterboxTTS.from_pretrained(self.device)

        results = {}

        # Test empty text
        try:
            wav = self.model_tts.generate("")
            results["empty_text"] = {"success": True, "audio_duration": wav.shape[-1] / self.model_tts.sr}
        except Exception as e:
            results["empty_text"] = {"success": False, "error": str(e)}

        # Test very short text
        try:
            wav = self.model_tts.generate("A")
            results["single_char"] = {"success": True, "audio_duration": wav.shape[-1] / self.model_tts.sr}
        except Exception as e:
            results["single_char"] = {"success": False, "error": str(e)}

        # Test very long text (near max tokens)
        long_text = "This is a very long text. " * 100  # Approximately 2700 characters
        try:
            wav = self.model_tts.generate(long_text)
            results["very_long_text"] = {
                "success": True,
                "text_length": len(long_text),
                "audio_duration": wav.shape[-1] / self.model_tts.sr
            }
        except Exception as e:
            results["very_long_text"] = {"success": False, "error": str(e)}

        # Test extreme parameters
        try:
            wav = self.model_tts.generate("Testing extreme parameters.",
                                        exaggeration=2.0, cfg_weight=1.0, temperature=2.0)
            results["extreme_params"] = {"success": True, "audio_duration": wav.shape[-1] / self.model_tts.sr}
        except Exception as e:
            results["extreme_params"] = {"success": False, "error": str(e)}

        return results

    def test_concurrent_usage(self) -> Dict[str, Any]:
        """Test behavior under concurrent usage patterns"""
        if not self.model_tts:
            self.model_tts = ChatterboxTTS.from_pretrained(self.device)

        # Simulate rapid successive calls
        texts = [f"Concurrent test number {i}." for i in range(5)]

        start_time = time.time()
        results = []

        for i, text in enumerate(texts):
            call_start = time.time()
            wav = self.model_tts.generate(text)
            call_end = time.time()

            results.append({
                "call_index": i,
                "generation_time": call_end - call_start,
                "audio_duration": wav.shape[-1] / self.model_tts.sr
            })

        total_time = time.time() - start_time

        return {
            "total_calls": len(texts),
            "total_time": total_time,
            "avg_time_per_call": total_time / len(texts),
            "individual_results": results
        }

    # ==================== INTEGRATION READINESS TESTS ====================

    def test_api_consistency(self) -> Dict[str, Any]:
        """Test API consistency and predictability"""
        if not self.model_tts:
            self.model_tts = ChatterboxTTS.from_pretrained(self.device)

        text = "Testing API consistency."

        # Test same input produces consistent output shapes
        results = []
        for i in range(3):
            wav = self.model_tts.generate(text, temperature=0.1)  # Low temp for consistency
            results.append({
                "run": i,
                "shape": wav.shape,
                "duration": wav.shape[-1] / self.model_tts.sr
            })

        # Check consistency
        shapes_consistent = all(r["shape"] == results[0]["shape"] for r in results)
        durations = [r["duration"] for r in results]
        duration_variance = np.var(durations)

        return {
            "runs": results,
            "shapes_consistent": shapes_consistent,
            "duration_variance": duration_variance,
            "avg_duration": np.mean(durations)
        }

    def test_memory_usage_patterns(self) -> Dict[str, Any]:
        """Test memory usage patterns during generation"""
        if not self.model_tts:
            self.model_tts = ChatterboxTTS.from_pretrained(self.device)

        text = "Testing memory usage patterns during text to speech generation."

        # Baseline memory
        baseline_ram, baseline_gpu = self._get_memory_usage()

        # Generate multiple times to check for memory leaks
        memory_snapshots = []
        for i in range(5):
            wav = self.model_tts.generate(text)
            ram, gpu = self._get_memory_usage()
            memory_snapshots.append({
                "iteration": i,
                "ram_mb": ram - baseline_ram,
                "gpu_mb": gpu - baseline_gpu if gpu and baseline_gpu else None
            })

        return {
            "baseline_ram_mb": baseline_ram,
            "baseline_gpu_mb": baseline_gpu,
            "memory_snapshots": memory_snapshots,
            "memory_growth": {
                "ram_mb": memory_snapshots[-1]["ram_mb"] - memory_snapshots[0]["ram_mb"],
                "gpu_mb": (memory_snapshots[-1]["gpu_mb"] - memory_snapshots[0]["gpu_mb"])
                          if memory_snapshots[-1]["gpu_mb"] is not None else None
            }
        }

    # ==================== MAIN TEST RUNNER ====================

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        print("🚀 Starting Comprehensive Integration Test Suite")
        print("=" * 60)

        # Basic functionality tests
        self._run_test("Model Loading", self.test_model_loading)
        self._run_test("Basic TTS", self.test_basic_tts)
        self._run_test("Parameter Variations", self.test_parameter_variations)
        self._run_test("Text Variations", self.test_text_variations)

        # Performance tests
        self._run_test("Performance Benchmarks", self.test_performance_benchmarks)
        self._run_test("Memory Usage Patterns", self.test_memory_usage_patterns)

        # Error handling tests
        self._run_test("Edge Cases", self.test_edge_cases)
        self._run_test("Concurrent Usage", self.test_concurrent_usage)

        # Integration readiness tests
        self._run_test("API Consistency", self.test_api_consistency)

        # Generate summary report
        return self.generate_summary_report()

    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate a comprehensive summary report"""
        successful_tests = [r for r in self.results if r.success]
        failed_tests = [r for r in self.results if not r.success]

        # Performance metrics
        execution_times = [r.execution_time for r in successful_tests]
        memory_usage = [r.memory_usage_mb for r in successful_tests]

        summary = {
            "test_summary": {
                "total_tests": len(self.results),
                "successful_tests": len(successful_tests),
                "failed_tests": len(failed_tests),
                "success_rate": len(successful_tests) / len(self.results) * 100
            },
            "performance_summary": {
                "avg_execution_time": np.mean(execution_times) if execution_times else 0,
                "max_execution_time": np.max(execution_times) if execution_times else 0,
                "avg_memory_usage_mb": np.mean(memory_usage) if memory_usage else 0,
                "max_memory_usage_mb": np.max(memory_usage) if memory_usage else 0
            },
            "failed_tests": [{"name": r.test_name, "error": r.error_message} for r in failed_tests],
            "device_info": {
                "device": self.device,
                "cuda_available": torch.cuda.is_available(),
                "mps_available": torch.backends.mps.is_available() if hasattr(torch.backends, 'mps') else False
            }
        }

        # Save detailed results
        detailed_results = {
            "summary": summary,
            "detailed_results": [r.to_dict() for r in self.results]
        }

        report_path = self.output_dir / "integration_test_report.json"
        with open(report_path, 'w') as f:
            json.dump(detailed_results, f, indent=2, default=str)

        print(f"\n📊 Test Summary:")
        print(f"✅ Successful: {summary['test_summary']['successful_tests']}/{summary['test_summary']['total_tests']}")
        print(f"❌ Failed: {summary['test_summary']['failed_tests']}")
        print(f"📈 Success Rate: {summary['test_summary']['success_rate']:.1f}%")
        print(f"⏱️  Avg Execution Time: {summary['performance_summary']['avg_execution_time']:.2f}s")
        print(f"💾 Avg Memory Usage: {summary['performance_summary']['avg_memory_usage_mb']:.1f}MB")
        print(f"📄 Detailed report saved to: {report_path}")

        return summary


def main():
    """Main function to run the integration test suite"""
    import argparse

    parser = argparse.ArgumentParser(description="Chatterbox TTS Integration Test Suite")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "mps", "cpu"],
                       help="Device to use for testing")
    parser.add_argument("--output-dir", default="test_outputs",
                       help="Directory to save test outputs")

    args = parser.parse_args()

    # Install psutil if not available
    try:
        import psutil
    except ImportError:
        print("Installing psutil for memory monitoring...")
        import subprocess
        subprocess.check_call(["pip", "install", "psutil"])
        import psutil

    tester = ChatterboxIntegrationTester(device=args.device, output_dir=args.output_dir)
    summary = tester.run_all_tests()

    return summary


if __name__ == "__main__":
    main()
