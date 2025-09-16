#!/usr/bin/env python3
"""
Phase 5 Demo: Complete Spiritual Gifts Discovery System
Demonstrates how to run the complete system with all Phase 1-5 capabilities

Usage Examples:
  python run_demo.py --web          # Launch web interface
  python run_demo.py --cli          # Run CLI version
  python run_demo.py --test         # Run all tests
  python run_demo.py --compare      # Compare Phase 3 vs Phase 4 systems
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime

def run_web_interface():
    """Launch the Streamlit web interface"""
    print("Launching Spiritual Gifts Discovery Web Interface...")
    print("=" * 60)
    print("Features available in the web interface:")
    print("  • Context-aware AI responses")
    print("  • Dynamic questioning based on your patterns")
    print("  • Communication style adaptation")
    print("  • Real-time insights and analytics")
    print("  • Interactive visualizations")
    print("  • Multi-format export (JSON, HTML, CSV)")
    print("=" * 60)
    print("\nOpening web interface at http://localhost:8501")
    print("Note: Make sure you have GOOGLE_API_KEY in your .env file")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 60)

    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.headless", "false",
            "--server.port", "8501"
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
    except KeyboardInterrupt:
        print("\n\nWeb interface stopped. Thanks for exploring!")

def run_cli_interface():
    """Run the enhanced CLI interface"""
    print("Launching Enhanced CLI Interface...")
    print("=" * 60)
    print("Features in the enhanced CLI:")
    print("  • All Phase 4 enhanced intelligence")
    print("  • Context-aware conversation")
    print("  • Dynamic questioning")
    print("  • Personality profiling")
    print("  • Real-time insights commands")
    print("=" * 60)
    print("\nCommands you can use:")
    print("  • 'insights' - Show AI discoveries")
    print("  • 'style' - Show your communication profile")
    print("  • 'progress' - View enhanced progress")
    print("  • 'quit' - End session with intelligent summary")
    print("-" * 60)

    try:
        from enhanced_discovery_bot import EnhancedSpiritualDiscoveryBot
        bot = EnhancedSpiritualDiscoveryBot()
        bot.start_enhanced_discovery_journey()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("💡 Make sure you have GOOGLE_API_KEY in your .env file")
    except KeyboardInterrupt:
        print("\n\n👋 CLI session ended. Your discovery continues!")

def run_all_tests():
    """Run comprehensive test suite"""
    print("🧪 Running Complete Test Suite...")
    print("=" * 60)

    test_phases = [
        ("Phase 3: Self-Discovery Logic Engine", "test_phase3.py"),
        ("Phase 4: Enhanced Intelligence", "test_phase4.py"),
        ("Phase 5: User Interface & Visualization", "test_phase5.py")
    ]

    results = []

    for phase_name, test_file in test_phases:
        print(f"\n🔍 Testing {phase_name}...")
        try:
            result = subprocess.run([
                sys.executable, test_file
            ], cwd=os.path.dirname(os.path.abspath(__file__)),
               capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✅ {phase_name}: PASSED")
                results.append((phase_name, "PASSED"))
            else:
                print(f"❌ {phase_name}: FAILED")
                print(f"Error: {result.stderr}")
                results.append((phase_name, "FAILED"))

        except Exception as e:
            print(f"❌ {phase_name}: ERROR - {e}")
            results.append((phase_name, "ERROR"))

    # Summary
    print("\n" + "=" * 60)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, status in results if status == "PASSED")
    total = len(results)

    for phase_name, status in results:
        emoji = "✅" if status == "PASSED" else "❌"
        print(f"{emoji} {phase_name}: {status}")

    print(f"\n📊 Overall: {passed}/{total} phases passed")

    if passed == total:
        print("🎉 All systems operational! Ready for production use.")
    else:
        print("⚠️  Some issues detected. Check individual test outputs.")

def compare_systems():
    """Compare Phase 3 vs Phase 4 systems"""
    print("🔍 System Comparison: Phase 3 vs Phase 4")
    print("=" * 60)

    print("📋 PHASE 3 (Basic Structured System):")
    print("  • ✅ Structured 6-stage discovery flow")
    print("  • ✅ Fixed question progression")
    print("  • ✅ Basic conversation memory")
    print("  • ✅ Spiritual gifts assessment")
    print("  • ❌ No context awareness")
    print("  • ❌ No dynamic questioning")
    print("  • ❌ No personality adaptation")
    print("  • 📊 Assessment: Complete but rigid")

    print("\n🧠 PHASE 4 (Enhanced Intelligence):")
    print("  • ✅ All Phase 3 capabilities")
    print("  • ✅ Context-aware responses")
    print("  • ✅ Dynamic questioning based on patterns")
    print("  • ✅ Personality/style profiling")
    print("  • ✅ Real-time insights tracking")
    print("  • ✅ Intelligent conversation steering")
    print("  • ✅ Adaptive communication style")
    print("  • 📊 Assessment: Personalized and adaptive")

    print("\n🌐 PHASE 5 (Web Interface):")
    print("  • ✅ All Phase 4 intelligence")
    print("  • ✅ Interactive web interface")
    print("  • ✅ Real-time visualization")
    print("  • ✅ Multi-format export")
    print("  • ✅ Analytics dashboard")
    print("  • ✅ Shareable prototype")
    print("  • 📊 Assessment: Professional web application")

    print("\n🎯 RECOMMENDATION:")
    print("  • Use Phase 3 for: Learning chatbot fundamentals")
    print("  • Use Phase 4 for: Advanced AI conversation experience")
    print("  • Use Phase 5 for: Production deployment and sharing")
    print("=" * 60)

def show_system_overview():
    """Show complete system overview"""
    print("SPIRITUAL GIFTS DISCOVERY SYSTEM")
    print("=" * 60)
    print("A complete AI-powered spiritual gifts discovery platform")
    print("Built to demonstrate fundamental AI chatbot architecture\n")

    print("🎯 PRIMARY GOAL: Learning AI chatbot architecture & orchestration")
    print("🎁 SECONDARY GOAL: Working prototype for spiritual gifts discovery\n")

    print("🏗️  ARCHITECTURE COMPONENTS:")
    print("  📊 Phase 1-2: Basic API integration & conversation management")
    print("  🧠 Phase 3: Self-discovery logic engine")
    print("  🎨 Phase 4: Enhanced intelligence (context, dynamic, personality)")
    print("  🌐 Phase 5: Web interface & visualization\n")

    print("🚀 AVAILABLE INTERFACES:")
    print("  • Web Interface: Full-featured Streamlit application")
    print("  • CLI Interface: Enhanced command-line experience")
    print("  • API Components: Modular system for custom integration\n")

    print("💡 KEY LEARNING CONCEPTS:")
    print("  • Context management in stateless LLM systems")
    print("  • Adaptive conversation flow & dynamic questioning")
    print("  • User modeling & personality-based adaptation")
    print("  • Web application architecture for AI systems")
    print("  • Data visualization & export systems")
    print("  • Component-based AI system design")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(
        description="Spiritual Gifts Discovery System - Complete AI Chatbot Demo",
        epilog="Example: python run_demo.py --web"
    )

    parser.add_argument("--web", action="store_true",
                       help="Launch Streamlit web interface")
    parser.add_argument("--cli", action="store_true",
                       help="Run enhanced CLI interface")
    parser.add_argument("--test", action="store_true",
                       help="Run comprehensive test suite")
    parser.add_argument("--compare", action="store_true",
                       help="Compare different system phases")

    args = parser.parse_args()

    # Show overview if no specific command
    if not any([args.web, args.cli, args.test, args.compare]):
        show_system_overview()
        print("\n🔧 Usage: python run_demo.py [--web|--cli|--test|--compare]")
        print("   --web     Launch web interface")
        print("   --cli     Run CLI version")
        print("   --test    Run all tests")
        print("   --compare Show system comparison")
        return

    # Execute requested command
    if args.web:
        run_web_interface()
    elif args.cli:
        run_cli_interface()
    elif args.test:
        run_all_tests()
    elif args.compare:
        compare_systems()

if __name__ == "__main__":
    main()