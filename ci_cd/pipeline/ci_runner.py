"""
CI Pipeline Runner
Simulates CI/CD pipeline with Docker and pytest
"""

import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
import json
import logging

# Setup logging
log_dir = Path(__file__).parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"ci_runner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class CIRunner:
    """CI/CD Pipeline Runner"""
    
    def __init__(self, use_simulation=False):
        self.pipeline_history = []
        self.current_iteration = 0
        self.start_time = None
        self.use_simulation = use_simulation
        
        # Auto-detect if Docker is available
        if not use_simulation:
            self.use_simulation = not self._is_docker_available()
            if self.use_simulation:
                logger.warning("Docker not available - using simulation mode")
    
    def _is_docker_available(self):
        """Check if Docker is available"""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
        
    def run_pytest(self, test_path="tests/", verbose=True):
        """
        Run pytest tests
        
        Args:
            test_path (str): Path to tests
            verbose (bool): Verbose output
            
        Returns:
            dict: Test results
        """
        logger.info(f"Running pytest on {test_path}...")
        
        cmd = ["pytest", test_path, "--color=yes", "-v" if verbose else ""]
        
        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            duration = time.time() - start_time
            
            test_result = {
                "timestamp": datetime.now().isoformat(),
                "duration": round(duration, 2),
                "exit_code": result.returncode,
                "passed": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
            if test_result["passed"]:
                logger.info(f"[OK] Tests passed in {duration:.2f}s")
            else:
                logger.error(f"[FAIL] Tests failed (exit code: {result.returncode})")
            
            return test_result
            
        except subprocess.TimeoutExpired:
            logger.error("[FAIL] Tests timed out")
            return {
                "timestamp": datetime.now().isoformat(),
                "passed": False,
                "error": "timeout"
            }
        except Exception as e:
            logger.error(f"[FAIL] Failed to run tests: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "passed": False,
                "error": str(e)
            }
    
    def run_docker_pytest(self):
        """
        Run pytest inside Docker container
        
        Returns:
            dict: Test results
        """
        logger.info("Running pytest in Docker container...")
        
        cmd = ["docker-compose", "run", "--rm", "pytest-runner"]
        
        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            duration = time.time() - start_time
            
            test_result = {
                "timestamp": datetime.now().isoformat(),
                "duration": round(duration, 2),
                "exit_code": result.returncode,
                "passed": result.returncode == 0,
                "environment": "docker",
                "stdout": result.stdout[-2000:],  # Last 2000 chars
                "stderr": result.stderr[-2000:] if result.stderr else None
            }
            
            if test_result["passed"]:
                logger.info(f"[OK] Docker tests passed in {duration:.2f}s")
            else:
                logger.error(f"[FAIL] Docker tests failed")
            
            return test_result
            
        except Exception as e:
            logger.error(f"[FAIL] Failed to run Docker tests: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "passed": False,
                "error": str(e),
                "environment": "docker"
            }
    
    def build_docker_image(self):
        """
        Build Docker image for CI
        
        Returns:
            bool: Success status
        """
        logger.info("Building Docker image...")
        
        cmd = ["docker-compose", "build", "ci-pipeline"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                logger.info("[OK] Docker image built successfully")
                return True
            else:
                logger.error(f"[FAIL] Docker build failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"[FAIL] Failed to build Docker image: {e}")
            return False
    
    def simulate_pipeline_run(self):
        """
        Simulate a CI pipeline run (for when Docker isn't available)
        
        Returns:
            dict: Simulated pipeline results
        """
        import random
        
        self.current_iteration += 1
        logger.info(f"\n{'='*60}")
        logger.info(f"CI Pipeline Iteration #{self.current_iteration} [SIMULATION]")
        logger.info(f"{'='*60}\n")
        
        pipeline_start = time.time()
        
        # Simulate varying success rates for realistic demo
        build_success = random.random() > 0.2  # 80% success rate
        test_success = random.random() > 0.3 if build_success else False  # 70% if build passes
        
        pipeline_result = {
            "iteration": self.current_iteration,
            "start_time": datetime.now().isoformat(),
            "mode": "simulation",
            "stages": {}
        }
        
        # Stage 1: Build (simulated)
        logger.info("Stage 1: Build [SIMULATED]")
        time.sleep(0.5)  # Simulate build time
        pipeline_result["stages"]["build"] = {
            "passed": build_success,
            "timestamp": datetime.now().isoformat(),
            "duration": 0.5,
            "simulated": True
        }
        
        if build_success:
            logger.info("[OK] Build simulated successfully")
        else:
            logger.warning("[FAIL] Build simulation failed (for demo variety)")
            pipeline_result["status"] = "failed"
            pipeline_result["duration"] = round(time.time() - pipeline_start, 2)
            pipeline_result["end_time"] = datetime.now().isoformat()
            self.pipeline_history.append(pipeline_result)
            return pipeline_result
        
        # Stage 2: Test (simulated)
        logger.info("\nStage 2: Test [SIMULATED]")
        time.sleep(0.3)  # Simulate test time
        pipeline_result["stages"]["test"] = {
            "passed": test_success,
            "timestamp": datetime.now().isoformat(),
            "duration": 0.3,
            "tests_run": 15,
            "tests_passed": 15 if test_success else 12,
            "simulated": True
        }
        
        if test_success:
            logger.info("[OK] Tests simulated successfully (15/15 passed)")
        else:
            logger.warning("[FAIL] Tests simulation failed (12/15 passed)")
        
        # Stage 3: Analysis (simulated)
        logger.info("\nStage 3: Code Analysis [SIMULATED]")
        time.sleep(0.2)
        pipeline_result["stages"]["analysis"] = {
            "passed": True,
            "timestamp": datetime.now().isoformat(),
            "duration": 0.2,
            "message": "Analysis stage simulated",
            "simulated": True
        }
        logger.info("[OK] Analysis simulated successfully")
        
        # Calculate overall status
        pipeline_duration = time.time() - pipeline_start
        pipeline_result["duration"] = round(pipeline_duration, 2)
        
        all_passed = all(
            stage.get("passed", False) 
            for stage in pipeline_result["stages"].values()
        )
        
        pipeline_result["status"] = "passed" if all_passed else "failed"
        pipeline_result["end_time"] = datetime.now().isoformat()
        
        # Log summary
        logger.info(f"\n{'='*60}")
        logger.info(f"Pipeline Summary (Iteration #{self.current_iteration}) [SIMULATION]")
        logger.info(f"Status: {pipeline_result['status'].upper()}")
        logger.info(f"Duration: {pipeline_duration:.2f}s")
        logger.info(f"{'='*60}\n")
        
        self.pipeline_history.append(pipeline_result)
        
        return pipeline_result
    
    def run_ci_pipeline(self):
        """
        Run complete CI pipeline
        
        Returns:
            dict: Pipeline results
        """
        # Use simulation mode if Docker isn't available
        if self.use_simulation:
            return self.simulate_pipeline_run()
        
        self.current_iteration += 1
        logger.info(f"\n{'='*60}")
        logger.info(f"CI Pipeline Iteration #{self.current_iteration}")
        logger.info(f"{'='*60}\n")
        
        pipeline_start = time.time()
        
        pipeline_result = {
            "iteration": self.current_iteration,
            "start_time": datetime.now().isoformat(),
            "stages": {}
        }
        
        # Stage 1: Build
        logger.info("Stage 1: Build")
        build_success = self.build_docker_image()
        pipeline_result["stages"]["build"] = {
            "passed": build_success,
            "timestamp": datetime.now().isoformat()
        }
        
        if not build_success:
            logger.error("Build failed, stopping pipeline")
            pipeline_result["status"] = "failed"
            pipeline_result["duration"] = round(time.time() - pipeline_start, 2)
            pipeline_result["end_time"] = datetime.now().isoformat()
            pipeline_result["error"] = "Docker build failed - Docker Desktop not running"
            
            # IMPORTANT: Still record failed runs for timeline tracking
            self.pipeline_history.append(pipeline_result)
            
            return pipeline_result
        
        # Stage 2: Test (Docker)
        logger.info("\nStage 2: Test (Docker)")
        test_result = self.run_docker_pytest()
        pipeline_result["stages"]["test"] = test_result
        
        # Stage 3: Analysis (placeholder)
        logger.info("\nStage 3: Code Analysis")
        pipeline_result["stages"]["analysis"] = {
            "passed": True,
            "timestamp": datetime.now().isoformat(),
            "message": "Analysis stage simulated"
        }
        
        # Calculate overall status
        pipeline_duration = time.time() - pipeline_start
        pipeline_result["duration"] = round(pipeline_duration, 2)
        
        all_passed = all(
            stage.get("passed", False) 
            for stage in pipeline_result["stages"].values()
        )
        
        pipeline_result["status"] = "passed" if all_passed else "failed"
        pipeline_result["end_time"] = datetime.now().isoformat()
        
        # Log summary
        logger.info(f"\n{'='*60}")
        logger.info(f"Pipeline Summary (Iteration #{self.current_iteration})")
        logger.info(f"Status: {pipeline_result['status'].upper()}")
        logger.info(f"Duration: {pipeline_duration:.2f}s")
        logger.info(f"{'='*60}\n")
        
        self.pipeline_history.append(pipeline_result)
        
        return pipeline_result
    
    def run_simulation_loop(self, iterations=3, delay=5):
        """
        Run CI pipeline simulation loop
        
        Args:
            iterations (int): Number of iterations
            delay (int): Delay between iterations (seconds)
            
        Returns:
            list: All pipeline results
        """
        logger.info(f"Starting CI simulation loop: {iterations} iterations")
        self.start_time = datetime.now()
        
        results = []
        
        for i in range(iterations):
            if i > 0:
                logger.info(f"\nWaiting {delay}s before next iteration...")
                time.sleep(delay)
            
            result = self.run_ci_pipeline()
            results.append(result)
        
        logger.info("\n" + "="*60)
        logger.info("CI Simulation Complete")
        logger.info("="*60)
        
        # Summary statistics
        passed = sum(1 for r in results if r["status"] == "passed")
        failed = len(results) - passed
        avg_duration = sum(r["duration"] for r in results) / len(results)
        
        logger.info(f"\nResults: {passed} passed, {failed} failed")
        logger.info(f"Average duration: {avg_duration:.2f}s")
        
        return results
    
    def save_pipeline_data(self):
        """Save pipeline data to JSON"""
        data_dir = Path(__file__).parent.parent.parent / "data"
        data_dir.mkdir(exist_ok=True)
        
        timeline_file = data_dir / "ci_pipeline_timeline.json"
        
        timeline_data = {
            "project": "RIFT'26 - DevOps Lead",
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": datetime.now().isoformat(),
            "total_iterations": self.current_iteration,
            "pipeline_history": self.pipeline_history
        }
        
        with open(timeline_file, 'w') as f:
            json.dump(timeline_data, f, indent=2)
        
        logger.info(f"Pipeline data saved to {timeline_file}")


def main():
    """Main execution"""
    logger.info("=== CI/CD Pipeline Runner ===\n")
    
    runner = CIRunner()
    
    # Run simulation loop
    results = runner.run_simulation_loop(iterations=3, delay=2)
    
    # Save data
    runner.save_pipeline_data()
    
    logger.info("\nPipeline execution complete!")


if __name__ == "__main__":
    main()
