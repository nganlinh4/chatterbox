#!/usr/bin/env python3
"""
Simple runner for Chatterbox Integration Tests
==============================================

This script provides an easy way to run the integration tests with different configurations.
"""

import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install required packages for testing"""
    requirements = [
        "chatterbox-tts",
        "psutil",
        "numpy",
        "torch",
        "torchaudio"
    ]
    
    print("📦 Installing required packages...")
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {req}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {req}")
            return False
    return True

def main():
    """Main function"""
    print("🧪 Chatterbox TTS Integration Test Runner")
    print("=" * 50)
    
    # Check if integration test suite exists
    test_suite_path = Path(__file__).parent / "integration_test_suite.py"
    if not test_suite_path.exists():
        print("❌ integration_test_suite.py not found!")
        print("Please ensure the test suite file is in the integration_tests directory.")
        return 1
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        return 1
    
    print("\n🚀 Starting integration tests...")
    
    # Run the test suite
    try:
        from integration_test_suite import ChatterboxIntegrationTester
        
        tester = ChatterboxIntegrationTester()
        summary = tester.run_all_tests()
        
        # Print final summary
        print("\n" + "=" * 50)
        print("🎯 INTEGRATION TEST RESULTS")
        print("=" * 50)
        
        if summary['test_summary']['failed_tests'] == 0:
            print("🎉 ALL TESTS PASSED!")
            print("✅ The system is ready for integration")
        else:
            print("⚠️  Some tests failed - review before integration")
        
        print(f"\nKey Integration Metrics:")
        print(f"• Success Rate: {summary['test_summary']['success_rate']:.1f}%")
        print(f"• Average Response Time: {summary['performance_summary']['avg_execution_time']:.2f}s")
        print(f"• Memory Usage: {summary['performance_summary']['avg_memory_usage_mb']:.1f}MB")
        
        return 0 if summary['test_summary']['failed_tests'] == 0 else 1
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
