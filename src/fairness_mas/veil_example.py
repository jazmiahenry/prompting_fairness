# example_maximin_allocation.py
import asyncio
from agents.veil_allocator import AnonymousFairnessAgent

async def main():
    agent = AnonymousFairnessAgent(
        name="anonymous_allocator",
        num_profiles=10,
        consensus_threshold=0.8
    )
    
    allocation_request = {
        "available_resources": 100000,
        "constraints": {
            "minimum_allocation": 1000,
            "maximum_allocation": 30000
        }
    }

    try:
        result = await agent.process(allocation_request)
        if result["status"] == "success":
            allocation = result["allocation_decision"]
            
            print("\nAnonymous Resource Allocation Results")
            print("=" * 50)
            
            # Print allocations
            print(f"\n{'Profile ID':<15} {'Amount':>12} {'Need Level':>12} {'Vulnerability':>12}")
            print("-" * 55)
            for alloc in allocation["allocations"]:
                print(f"{alloc['profile_id']:<15} "
                      f"${alloc['amount']:>11,.2f} "
                      f"{alloc['need_level']:>11.2f} "
                      f"{alloc['vulnerability_index']:>11.2f}")
            
            # Print standard metrics
            print("\nStandard Metrics")
            print("=" * 50)
            metrics = allocation["standard_metrics"]
            print(f"Minimum Welfare: {metrics['minimum_welfare']:.3f}")
            print(f"Average Welfare: {metrics['average_welfare']:.3f}")
            print(f"Gini Coefficient: {metrics['gini_coefficient']:.3f}")
            print(f"Equity Score: {metrics['equity_score']:.3f}")
            
            # Print maximin analysis
            print("\nMaximin Analysis")
            print("=" * 50)
            maximin = allocation["maximin_analysis"]
            print(f"Worst Case Outcome: {maximin['worst_case_outcome']:.3f}")
            print(f"Worst Case Profile: {maximin['worst_case_profile']}")
            print(f"Maximin Score: {maximin['maximin_score']:.3f}")
            print(f"Improvement Potential: {maximin['improvement_potential']:.3f}")
            print(f"Maximin Principle Satisfied: {maximin['maximin_principle_satisfied']}")
            
            # Print fairness analysis
            print("\nFairness Analysis")
            print("=" * 50)
            analysis = allocation["fairness_analysis"]
            for key, value in analysis.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            
        else:
            print(f"Error: {result['error']}")
            
    except Exception as e:
        print(f"Error during allocation: {e}")

if __name__ == "__main__":
    asyncio.run(main())