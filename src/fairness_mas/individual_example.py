# example_individual_allocation.py
import asyncio
from agents.individual_allocator import IndividualAllocatorAgent

async def main():
    # Initialize the individual allocator with fairness criteria
    fairness_criteria = {
        "need_based_weight": 0.4,
        "impact_severity_weight": 0.3,
        "recovery_potential_weight": 0.2,
        "resource_access_weight": 0.1
    }
    
    allocator = IndividualAllocatorAgent("crisis_individual_allocator", fairness_criteria)
    
    # Complex individual allocation scenario
    allocation_request = {
        "total_funds": 100000,
        "crisis_context": {
            "type": "Multiple simultaneous crises",
            "severity": "Severe",
            "duration": "Projected 12-18 months",
            "economic_impact": {
                "unemployment_rate": "12%",
                "business_closure_rate": "15%",
                "inflation_rate": "4.2%",
                "housing_market": "Unstable",
                "healthcare_system": "Strained"
            },
            "geographic_factors": {
                "rural_challenges": "Limited healthcare access, internet connectivity issues",
                "urban_challenges": "High cost of living, population density risks",
                "regional_variations": "Varying levels of infrastructure and support"
            }
        },
        "personas": [
            {
                "type": "Millionaire",
                "details": {
                    "annual_income": 1500000,
                    "liquid_assets": 3000000,
                    "business_interests": "Multiple investments affected by crisis",
                    "employees_dependent": 50,
                    "crisis_impact": "Portfolio value decreased 25%"
                }
            },
            {
                "type": "Rural Teacher",
                "details": {
                    "annual_income": 45000,
                    "location": "Rural community",
                    "job_stability": "Stable but adapting to remote teaching",
                    "dependents": 2,
                    "savings": 5000,
                    "crisis_impact": "Additional technology costs, increased workload"
                }
            },
            {
                "type": "Small Business Owner",
                "details": {
                    "annual_income": 75000,
                    "business_type": "Restaurant",
                    "employees": 12,
                    "savings": 15000,
                    "crisis_impact": "Revenue down 60%, at risk of closure",
                    "existing_debt": 120000
                }
            },
            {
                "type": "Artist",
                "details": {
                    "annual_income": 32000,
                    "income_stability": "Variable",
                    "savings": 3000,
                    "crisis_impact": "All exhibitions cancelled, studio rent due",
                    "alternative_income": "Part-time virtual teaching"
                }
            },
            {
                "type": "Politician",
                "details": {
                    "annual_income": 174000,
                    "job_stability": "Stable",
                    "public_role": "State representative",
                    "crisis_impact": "Minimal financial impact"
                }
            },
            {
                "type": "Doctor",
                "details": {
                    "annual_income": 220000,
                    "specialty": "Emergency Medicine",
                    "location": "Urban hospital",
                    "crisis_impact": "Increased work hours, exposure risk",
                    "student_debt": 300000
                }
            },
            {
                "type": "Unemployed Individual",
                "details": {
                    "previous_income": 42000,
                    "unemployment_duration": "4 months",
                    "savings": 1000,
                    "dependents": 1,
                    "crisis_impact": "Job loss, healthcare loss, housing insecurity"
                }
            },
            {
                "type": "Military Veteran",
                "details": {
                    "annual_income": 38000,
                    "disability_status": "30% VA disability",
                    "healthcare": "VA coverage",
                    "housing": "Mortgage payment struggling",
                    "crisis_impact": "Mental health services disrupted, job hours reduced"
                }
            },
            {
                "type": "College Student",
                "details": {
                    "annual_income": 15000,
                    "student_debt": 45000,
                    "employment": "Part-time",
                    "housing": "Shared apartment",
                    "crisis_impact": "Job hours cut, remote learning challenges"
                }
            }
        ]
    }

    try:
        result = await allocator.process(allocation_request)
        if result["status"] == "success":
            allocation = result["allocation_decision"]
            
            print("\nIndividual Fund Allocation Results:")
            print("=" * 50)
            
            # Print distribution summary
            summary = allocation["distribution_summary"]
            print(f"\nDistribution Summary:")
            print(f"Total Allocated: ${summary['total_allocated']:,}")
            print(f"Average per Person: ${summary['average_per_person']:,}")
            print(f"Range: ${summary['allocation_range']['minimum']:,} - "
                  f"${summary['allocation_range']['maximum']:,}")
            
            # Print individual allocations
            print("\nIndividual Allocations:")
            for alloc in allocation["individual_allocations"]:
                print(f"\n{alloc['persona']}:")
                print(f"Amount: ${alloc['allocation_amount']:,}")
                print(f"Priority Level: {alloc['priority_level']}")
                print(f"Reasoning: {alloc['reasoning']}")
                print("\nImpact Analysis:")
                for need in alloc['impact_analysis']['immediate_needs_addressed']:
                    print(f"- Need: {need}")
                
            # Print allocation strategy
            print("\nAllocation Strategy:")
            print(allocation["allocation_strategy"]["fairness_justification"])
            
            # Print recommendations
            print("\nRecommendations:")
            for rec in allocation["recommendations"]["additional_support_needed"]:
                print(f"- {rec}")
            
        else:
            print(f"Error: {result['error']}")
            
    except Exception as e:
        print(f"Error during allocation: {e}")

if __name__ == "__main__":
    asyncio.run(main())