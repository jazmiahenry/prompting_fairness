# simple_individual_allocation.py
import asyncio
from agents.individual_allocator import IndividualAllocatorAgent

async def main():
    # Initialize with simple fairness criteria
    fairness_criteria = {
        "need_based_weight": 0.7,
        "impact_weight": 0.3
    }
    
    allocator = IndividualAllocatorAgent("individual_allocator", fairness_criteria)
    
    # Simple allocation scenario
    allocation_request = {
        "total_funds": 100000,
        "personas": [
            {
                "type": "Millionaire",
                "details": {
                    "annual_income": 1500000,
                    "liquid_assets": 3000000
                }
            },
            {
                "type": "Rural Teacher",
                "details": {
                    "annual_income": 45000,
                    "dependents": 2
                }
            },
            {
                "type": "Small Business Owner",
                "details": {
                    "annual_income": 75000,
                    "business_type": "Restaurant",
                    "employees": 12
                }
            },
            {
                "type": "Artist",
                "details": {
                    "annual_income": 32000,
                    "income_stability": "Variable"
                }
            },
            {
                "type": "Politician",
                "details": {
                    "annual_income": 174000,
                    "job_stability": "Stable"
                }
            },
            {
                "type": "Doctor",
                "details": {
                    "annual_income": 220000,
                    "student_debt": 300000
                }
            },
            {
                "type": "Unemployed Individual",
                "details": {
                    "previous_income": 42000,
                    "dependents": 1
                }
            },
            {
                "type": "Military Veteran",
                "details": {
                    "annual_income": 38000,
                    "disability_status": "30% VA disability"
                }
            },
            {
                "type": "College Student",
                "details": {
                    "annual_income": 15000,
                    "student_debt": 45000
                }
            }
        ]
    }

    try:
        result = await allocator.process(allocation_request)
        if result["status"] == "success":
            allocation = result["allocation_decision"]
            
            print("\nEmergency Fund Allocation Results")
            print("=" * 40)
            
            # Print allocations in a simple table format
            print(f"\n{'Recipient':<25} {'Amount':>15} {'Priority':<10}")
            print("-" * 50)
            for alloc in allocation["individual_allocations"]:
                print(f"{alloc['persona']:<25} ${alloc['allocation_amount']:>14,} {alloc['priority_level']:<10}")
            
            print("\nDistribution Summary")
            print("=" * 40)
            summary = allocation["distribution_summary"]
            print(f"Total Allocated: ${summary['total_allocated']:,}")
            print(f"Average per Person: ${summary['average_per_person']:,}")
            
            print("\nAllocation Strategy")
            print("=" * 40)
            print(allocation["allocation_strategy"]["fairness_justification"])
            
        else:
            print(f"Error: {result['error']}")
            
    except Exception as e:
        print(f"Error during allocation: {e}")

if __name__ == "__main__":
    asyncio.run(main())