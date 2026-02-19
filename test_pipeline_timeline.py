"""
Quick test for CI pipeline timeline generation
"""
import sys
from pathlib import Path

# Add to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "ci_cd" / "pipeline"))

from ci_runner import CIRunner

def test_pipeline_timeline():
    """Test that pipeline runs are recorded even when Docker is unavailable"""
    
    print("\n" + "="*70)
    print("  Testing CI Pipeline Timeline Generation")
    print("="*70)
    
    # Force simulation mode
    runner = CIRunner(use_simulation=True)
    
    print("\n[TEST] Running 3 simulated pipeline iterations...")
    results = runner.run_simulation_loop(iterations=3, delay=1)
    
    # Check history
    print(f"\n[CHECK] Pipeline history: {len(runner.pipeline_history)} iterations recorded")
    print(f"[CHECK] Results returned: {len(results)} iterations")
    
    # Save data
    runner.save_pipeline_data()
    
    # Verify file
    timeline_file = project_root / "data" / "ci_pipeline_timeline.json"
    import json
    
    if timeline_file.exists():
        timeline_data = json.loads(timeline_file.read_text())
        history_count = len(timeline_data.get("pipeline_history", []))
        
        print(f"\n[VERIFY] Timeline file exists: {timeline_file}")
        print(f"[VERIFY] Pipeline history entries: {history_count}")
        
        if history_count > 0:
            print("\n[SUCCESS] Pipeline timeline data generated! [OK]")
            
            # Show sample
            print("\n[SAMPLE] First pipeline run:")
            first_run = timeline_data["pipeline_history"][0]
            print(f"  - Iteration: {first_run.get('iteration')}")
            print(f"  - Status: {first_run.get('status')}")
            print(f"  - Duration: {first_run.get('duration')}s")
            print(f"  - Stages: {len(first_run.get('stages', {}))}")
            
            return True
        else:
            print("\n[FAIL] Pipeline history is still empty")
            return False
    else:
        print(f"\n[FAIL] Timeline file not found: {timeline_file}")
        return False


if __name__ == "__main__":
    success = test_pipeline_timeline()
    sys.exit(0 if success else 1)
