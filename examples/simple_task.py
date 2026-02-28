"""
Simple Task Example - Basic usage of the Multi-Agent AGI System
"""

import sys
sys.path.append('..')

from core.cognitive_loop import CognitiveSystem
from agents.researcher import ResearcherAgent
from agents.planner import PlannerAgent
from loguru import logger


def main():
    """
    Demonstrate basic task solving with the cognitive system.
    """
    
    # Configure logging
    logger.add("logs/simple_task.log", rotation="1 MB")
    
    print("="*70)
    print("MULTI-AGENT AGI SYSTEM - SIMPLE TASK EXAMPLE")
    print("="*70)
    
    # Initialize the cognitive system
    print("\n1. Initializing cognitive system...")
    system = CognitiveSystem(
        researcher=ResearcherAgent(),
        planner=PlannerAgent(),
        max_iterations=5,
        convergence_threshold=0.75
    )
    print("✅ System initialized")
    
    # Define task
    goal = "Research and summarize recent advances in quantum computing"
    
    print(f"\n2. Task: {goal}")
    print("\n3. Starting autonomous problem solving...")
    print("-" * 70)
    
    # Solve task
    result = system.solve_task(
        goal=goal,
        context={
            "domain": "technology",
            "depth": "comprehensive"
        },
        constraints={
            "max_sources": 10,
            "verification_required": True
        }
    )
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    print(f"\nStatus: {result['status'].upper()}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Iterations: {result['iterations']}")
    print(f"\nSummary: {result['summary']}")
    
    # Show execution trace
    print("\n" + "-"*70)
    print("EXECUTION TRACE")
    print("-"*70)
    
    for i, iteration in enumerate(result['execution_trace'], 1):
        print(f"\nIteration {i}:")
        print(f"  Status: {iteration.get('status', 'unknown')}")
        print(f"  Confidence: {iteration.get('confidence', 0):.1%}")
        
        steps = iteration.get('steps', {})
        if steps:
            print(f"  Steps completed: {', '.join(steps.keys())}")
    
    # System metrics
    print("\n" + "="*70)
    print("SYSTEM METRICS")
    print("="*70)
    
    metrics = system.get_metrics()
    print(f"\nTotal tasks completed: {metrics['total_tasks']}")
    print(f"Success rate: {metrics['metrics']['success_rate']:.1%}")
    print(f"Average iterations: {metrics['metrics']['avg_iterations']:.1f}")
    print(f"Average confidence: {metrics['metrics']['avg_confidence']:.1%}")
    
    print("\n" + "="*70)
    print("✅ TASK COMPLETED")
    print("="*70)


if __name__ == "__main__":
    main()
