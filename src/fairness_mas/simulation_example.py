from simulations.scenarios import SimulationEnvironment, ScenarioType
from agents.veil_allocator import AnonymousFairnessAgent
from agents.individual_allocator import IndividualAllocatorAgent
from agents.social_allocator import SocialAllocatorAgent
import asyncio

async def main():
    # Initialize environment
    env = SimulationEnvironment(
        output_dir="simulation_results",
        num_episodes=1,
        random_seed=42
    )
    
    # Initialize all agent types
    agents = [
        # Veil of Ignorance Agent
        AnonymousFairnessAgent(
            name="veil_of_ignorance",
            num_profiles=10
        ),
        
        # Individual Consideration Agent
        IndividualAllocatorAgent(
            name="individual_allocator",
            fairness_criteria={
                "need_based_weight": 0.7,
                "impact_weight": 0.3
            }
        ),
        
        # Social Standards Agent
        SocialAllocatorAgent(
            name="social_allocator",
            fairness_criteria={
                "distributive_justice_weight": 0.4,
                "procedural_justice_weight": 0.3,
                "social_welfare_weight": 0.3,
                "equity_weight": 0.4,
                "vulnerability_weight": 0.6
            }
        ),
    ]

    # Dictionary to store comparative metrics
    comparative_results = {
        ScenarioType.STATIC: {},
        ScenarioType.DYNAMIC: {},
        ScenarioType.CULTURAL: {}
    }
    
    # Run simulations for each scenario type
    for scenario_type in ScenarioType:
        print(f"\nRunning {scenario_type.value} scenarios...")
        results = await env.run_simulation(agents, scenario_type)
        print(f"Completed {scenario_type.value} simulation")
        
        # Print summary statistics
        print("\nSummary Statistics:")
        print("=" * 50)
        
        scenario_metrics = {}
        
        for agent in agents:
            agent_results = [
                r["agent_decisions"] 
                for r in results 
                if any(d["agent_name"] == agent.name for d in r["agent_decisions"])
            ]
            print(f"\nAgent: {agent.name}")
            print(f"Total decisions: {len(agent_results)}")
            
            # Calculate average metrics
            metrics = []
            for result in agent_results:
                for decision in result:
                    if decision["agent_name"] == agent.name:
                        if decision["decision"]["status"] == "success":
                            metrics.append(decision["decision"]["allocation_decision"]["metrics"])
            
            if metrics:
                avg_min_welfare = np.mean([m["minimum_welfare"] for m in metrics])
                avg_avg_welfare = np.mean([m["average_welfare"] for m in metrics])
                avg_gini = np.mean([m["gini_coefficient"] for m in metrics])
                avg_equity = np.mean([m["equity_score"] for m in metrics])
                
                scenario_metrics[agent.name] = {
                    "avg_min_welfare": avg_min_welfare,
                    "avg_avg_welfare": avg_avg_welfare,
                    "avg_gini": avg_gini,
                    "avg_equity": avg_equity
                }
                
                print(f"Average minimum welfare: {avg_min_welfare:.3f}")
                print(f"Average welfare: {avg_avg_welfare:.3f}")
                print(f"Average Gini coefficient: {avg_gini:.3f}")
                print(f"Average equity score: {avg_equity:.3f}")
        
        comparative_results[scenario_type] = scenario_metrics
    
    # Generate comparative analysis
    print("\nComparative Analysis Across Scenarios")
    print("=" * 50)
    
    metrics_to_compare = ["avg_min_welfare", "avg_gini", "avg_equity"]
    
    for metric in metrics_to_compare:
        print(f"\n{metric.replace('_', ' ').title()}:")
        print("-" * 30)
        for scenario_type in ScenarioType:
            print(f"\n{scenario_type.value.title()} Scenario:")
            scenario_data = comparative_results[scenario_type]
            for agent_name, metrics in scenario_data.items():
                print(f"{agent_name}: {metrics[metric]:.3f}")
    
    # Save comparative results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    comparative_file = env.output_dir / f"comparative_analysis_{timestamp}.json"
    with open(comparative_file, 'w') as f:
        json.dump(comparative_results, f, indent=2)
    
    # Generate CSV summary
    summary_data = []
    for scenario_type in ScenarioType:
        for agent_name, metrics in comparative_results[scenario_type].items():
            row = {
                "scenario_type": scenario_type.value,
                "agent_name": agent_name,
                **metrics
            }
            summary_data.append(row)
    
    summary_df = pd.DataFrame(summary_data)
    summary_file = env.output_dir / f"comparative_summary_{timestamp}.csv"
    summary_df.to_csv(summary_file, index=False)
    
    # Print location of saved files
    print("\nResults saved to:")
    print(f"Comparative analysis: {comparative_file}")
    print(f"Summary CSV: {summary_file}")

if __name__ == "__main__":
    asyncio.run(main())