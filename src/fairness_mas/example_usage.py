# example_usage.py
import asyncio
import json
from typing import Dict, Any
from agents.allocator import AllocatorAgent
from dotenv import load_dotenv
import os

load_dotenv()

async def analyze_allocation_result(result: Dict[str, Any]) -> None:
    """Analyze and display the allocation results"""
    if result["status"] == "error":
        print(f"\nError in allocation:")
        print(f"Error message: {result['error']}")
        return

    allocation_decision = result["allocation_decision"]
    
    # Display allocations
    print("\nResource Allocations:")
    print("=" * 50)
    for allocation in allocation_decision["allocations"]:
        print(f"\nDepartment: {allocation['department']}")
        print(f"Allocated Resources:")
        for resource, amount in allocation["allocated_resources"].items():
            print(f"  - {resource}: {amount}")
        print(f"Request Fulfillment: {allocation['percentage_of_request_granted']}%")

    # Display reasoning
    print("\nAllocation Reasoning:")
    print("=" * 50)
    reasoning = allocation_decision["reasoning"]
    print(f"\nOverall Strategy:")
    print(reasoning["overall_strategy"])
    
    print("\nDepartment-Specific Reasoning:")
    for dept_reasoning in reasoning["department_specific"]:
        print(f"\n{dept_reasoning['department']}:")
        print(dept_reasoning['reasoning'])
    
    print("\nFairness Analysis:")
    print(reasoning["fairness_analysis"])

    # Display unused resources
    print("\nUnused Resources:")
    print("=" * 50)
    for resource, amount in allocation_decision["unused_resources"].items():
        print(f"{resource}: {amount}")

async def main():
    # Initialize the allocator agent with fairness criteria
    fairness_criteria = {
        "need_based_weight": 0.7,
        "equality_weight": 0.3,
        "historical_weight": 0.2
    }
    
    allocator = AllocatorAgent("resource_allocator_1", fairness_criteria)
    
    # Sample resource allocation scenario
    allocation_request = {
        "available_resources": {
            "cpu_cores": 100,
            "memory_gb": 512,
            "storage_tb": 50
        },
        "requests": [
            {
                "department": "Research",
                "priority": "high",
                "justification": "Running critical ML models",
                "requested_resources": {
                    "cpu_cores": 40,
                    "memory_gb": 256,
                    "storage_tb": 20
                },
                "current_allocation": {
                    "cpu_cores": 20,
                    "memory_gb": 128,
                    "storage_tb": 10
                }
            },
            {
                "department": "Development",
                "priority": "medium",
                "justification": "CI/CD pipelines and development environments",
                "requested_resources": {
                    "cpu_cores": 30,
                    "memory_gb": 128,
                    "storage_tb": 15
                },
                "current_allocation": {
                    "cpu_cores": 25,
                    "memory_gb": 128,
                    "storage_tb": 15
                }
            },
            {
                "department": "Operations",
                "priority": "low",
                "justification": "Monitoring and logging systems",
                "requested_resources": {
                    "cpu_cores": 20,
                    "memory_gb": 64,
                    "storage_tb": 10
                },
                "current_allocation": {
                    "cpu_cores": 15,
                    "memory_gb": 64,
                    "storage_tb": 8
                }
            }
        ]
    }

    try:
        result = await allocator.process(allocation_request)
        await analyze_allocation_result(result)
        
    except Exception as e:
        print(f"Error during allocation: {e}")

if __name__ == "__main__":
    asyncio.run(main())