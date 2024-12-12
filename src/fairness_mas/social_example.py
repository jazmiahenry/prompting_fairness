import asyncio
from agents.social_allocator import SocialAllocatorAgent

async def main():
    # Initialize the allocator agent
    fairness_criteria = {
        "need_based_weight": 0.6,
        "vulnerability_weight": 0.3,
        "equity_weight": 0.1
    }
    
    allocator = SocialAllocatorAgent("pandemic_allocator", fairness_criteria)
    
    # Example pandemic allocation scenario
    allocation_request = {
        "total_funds": 100000,
        "community_data": {
            "total_population": 50000,
            "demographics": {
                "elderly_population": 8000,
                "children_under_18": 12000,
                "households_below_poverty": 5000,
                "essential_workers": 15000,
                "immunocompromised": 2000,
                "uninsured": 7000
            },
            "health_metrics": {
                "current_infection_rate": "15 per 1000",
                "hospitalization_rate": "3 per 1000",
                "vaccination_rate": "65%"
            },
            "economic_indicators": {
                "unemployment_rate": "12%",
                "small_businesses_at_risk": 300,
                "average_household_savings": "$2,000"
            }
        },
        "context": {
            "existing_support": {
                "federal_aid": "Limited unemployment benefits",
                "state_programs": "Food assistance and rental support",
                "local_resources": "Community food banks and health clinics"
            },
            "critical_needs": [
                "Medical supplies and treatment",
                "Food security",
                "Housing stability",
                "Income support",
                "Childcare for essential workers"
            ],
            "community_feedback": [
                "Difficulty accessing healthcare",
                "Food insecurity increasing",
                "Risk of eviction rising",
                "Mental health services needed",
                "Digital divide affecting remote work/education"
            ]
        },
        "constraints": {
            "timeframe": "Immediate distribution needed",
            "distribution_method": "Direct payments and service funding",
            "reporting_requirements": "Weekly impact tracking",
            "eligibility_criteria": "Must demonstrate pandemic-related hardship"
        }
    }

    try:
        result = await allocator.process(allocation_request)
        if result["status"] == "success":
            print("\nEmergency Fund Allocation Plan:")
            print("=" * 50)
            allocation = result["allocation_decision"]
            
            print("\nAllocations:")
            for item in allocation["allocations"]:
                print(f"\n{item['recipient_group']}:")
                print(f"Amount: ${item['amount']:,}")
                print(f"Priority: {item['priority_level']}")
                print(f"Reasoning: {item['reasoning']}")
                print(f"Expected Impact: {item['expected_impact']}")
                
            print("\nOverall Strategy:")
            print(allocation["overall_strategy"])
            
            print("\nFairness Analysis:")
            analysis = allocation["fairness_analysis"]
            print(f"Equity Considerations: {analysis['equity_considerations']}")
            print("\nBarriers Addressed:")
            for barrier in analysis["access_barriers_addressed"]:
                print(f"- {barrier}")
            
            print("\nUnmet Needs and Recommendations:")
            unmet = allocation["unmet_needs"]
            print(unmet["description"])
            print("\nRecommendations:")
            for rec in unmet["recommendations"]:
                print(f"- {rec}")
        else:
            print(f"Error: {result['error']}")
            
    except Exception as e:
        print(f"Error during allocation: {e}")

if __name__ == "__main__":
    asyncio.run(main())