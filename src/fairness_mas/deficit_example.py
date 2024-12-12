import asyncio
from agents.social_allocator import SocialAllocatorAgent

async def main():
    # Initialize the allocator agent with updated fairness criteria
    fairness_criteria = {
        "need_based_weight": 0.5,
        "vulnerability_weight": 0.2,
        "fiscal_responsibility_weight": 0.2,
        "equity_weight": 0.1
    }
    
    allocator = SocialAllocatorAgent("pandemic_deficit_allocator", fairness_criteria)
    
    # Complex allocation scenario with deficit considerations
    allocation_request = {
        "total_funds": 100000,
        "national_context": {
            "national_deficit": 715000,
            "deficit_interest_rate": 0.025,  # 2.5% annual interest
            "economic_indicators": {
                "gdp_growth": "-2.3%",
                "inflation_rate": "4.2%",
                "federal_debt_to_gdp": "133%"
            },
            "fiscal_constraints": {
                "debt_servicing_cost": "Annual interest payment on deficit: $17,875",
                "deficit_growth_rate": "3.5% annually",
                "credit_rating_impact": "At risk of downgrade if deficit increases"
            }
        },
        "community_data": {
            "total_population": 50000,
            "demographics": {
                "elderly_population": 8000,
                "children_under_18": 12000,
                "households_below_poverty": 5000,
                "essential_workers": 15000,
                "immunocompromised": 2000,
                "uninsured": 7000,
                "recently_unemployed": 3000
            },
            "health_metrics": {
                "current_infection_rate": "15 per 1000",
                "hospitalization_rate": "3 per 1000",
                "vaccination_rate": "65%",
                "mental_health_crisis_rate": "Increased 40% since pandemic"
            },
            "economic_indicators": {
                "unemployment_rate": "12%",
                "small_businesses_at_risk": 300,
                "average_household_savings": "$2,000",
                "housing_instability": "25% at risk of eviction",
                "food_insecurity": "32% increase since pandemic"
            }
        },
        "context": {
            "existing_support": {
                "federal_aid": {
                    "unemployment_benefits": "Limited to 6 months",
                    "small_business_loans": "78% of funds depleted",
                    "rental_assistance": "Backlogged 45 days"
                },
                "state_programs": {
                    "food_assistance": "At capacity",
                    "rental_support": "Waitlist 2000 households",
                    "healthcare_subsidies": "Limited funding remaining"
                },
                "local_resources": {
                    "food_banks": "Operating at 150% capacity",
                    "health_clinics": "Overwhelmed",
                    "mental_health_services": "3-week waiting list"
                }
            },
            "critical_needs": [
                {
                    "category": "Medical supplies and treatment",
                    "urgency": "Critical",
                    "current_gap": "$45,000"
                },
                {
                    "category": "Food security",
                    "urgency": "High",
                    "current_gap": "$30,000"
                },
                {
                    "category": "Housing stability",
                    "urgency": "High",
                    "current_gap": "$50,000"
                },
                {
                    "category": "Income support",
                    "urgency": "Medium",
                    "current_gap": "$40,000"
                },
                {
                    "category": "Childcare for essential workers",
                    "urgency": "Medium",
                    "current_gap": "$25,000"
                }
            ],
            "deficit_impact_analysis": {
                "cost_of_inaction": {
                    "healthcare_system_strain": "Estimated $200,000 additional cost if untreated cases rise",
                    "economic_productivity_loss": "Estimated $150,000 if businesses fail",
                    "social_services_burden": "Potential $100,000 increase in long-term support needs"
                },
                "savings_opportunities": {
                    "preventive_care": "Every $1 spent saves $4 in emergency care",
                    "housing_stability": "Every $1 spent saves $3 in emergency shelter costs",
                    "food_security": "Every $1 spent saves $2 in healthcare costs"
                }
            }
        },
        "constraints": {
            "timeframe": "Immediate distribution needed",
            "distribution_method": "Direct payments and service funding",
            "reporting_requirements": {
                "weekly_impact_tracking": True,
                "deficit_reduction_reporting": True,
                "cost_benefit_analysis": True
            },
            "eligibility_criteria": {
                "pandemic_impact": "Must demonstrate hardship",
                "means_testing": "Income below 300% of poverty line",
                "resource_optimization": "Must show efficient use of funds"
            },
            "deficit_considerations": {
                "minimum_deficit_payment": "10% of unused funds",
                "cost_saving_documentation": "Required for all programs",
                "long_term_impact_assessment": "Must demonstrate ROI"
            }
        }
    }

    try:
        result = await allocator.process(allocation_request)
        if result["status"] == "success":
            print("\nEmergency Fund Allocation Plan:")
            print("=" * 50)
            allocation = result["allocation_decision"]
            
            # Calculate total allocated and saved
            total_allocated = sum(item["amount"] for item in allocation["allocations"])
            amount_to_deficit = allocation_request["total_funds"] - total_allocated
            
            print(f"\nTotal Available: ${allocation_request['total_funds']:,}")
            print(f"Total Allocated: ${total_allocated:,}")
            print(f"Amount to Deficit: ${amount_to_deficit:,}")
            print(f"Deficit Impact: {(amount_to_deficit/allocation_request['national_context']['national_deficit'])*100:.2f}% of deficit")
            
            print("\nDetailed Allocations:")
            for item in allocation["allocations"]:
                print(f"\n{item['recipient_group']}:")
                print(f"Amount: ${item['amount']:,}")
                print(f"Priority: {item['priority_level']}")
                print(f"Reasoning: {item['reasoning']}")
                print(f"Expected Impact: {item['expected_impact']}")
                if "cost_savings" in item:
                    print(f"Projected Cost Savings: ${item['cost_savings']:,}")
                
            print("\nOverall Strategy:")
            print(allocation["overall_strategy"])
            
            print("\nFairness Analysis:")
            analysis = allocation["fairness_analysis"]
            print(f"Equity Considerations: {analysis['equity_considerations']}")
            print("\nBarriers Addressed:")
            for barrier in analysis["access_barriers_addressed"]:
                print(f"- {barrier}")
            
            print("\nDeficit Impact Analysis:")
            print(f"Immediate Deficit Reduction: ${amount_to_deficit:,}")
            if "projected_savings" in allocation:
                print(f"Projected Long-term Savings: ${allocation['projected_savings']:,}")
            
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