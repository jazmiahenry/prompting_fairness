# run_simulation.py
import asyncio
from simulations.scenarios import SimulationEnvironment, ScenarioType
from agents.veil_allocator import AnonymousFairnessAgent
from agents.individual_allocator import IndividualAllocatorAgent
from agents.social_allocator import SocialAllocatorAgent
from agents.allocator import AllocatorAgent
from datetime import datetime
import numpy as np
import pandas as pd

def extract_agent_metrics(decision: dict, agent_name: str) -> dict:
    """Safely extract metrics from agent decisions based on agent type"""
    try:
        if decision["status"] != "success":
            return {}
            
        alloc_decision = decision["allocation_decision"]
        
        if "resource_allocator" in agent_name:
            allocations = alloc_decision["allocations"]
            amounts = [sum(alloc["allocated_resources"].values()) for alloc in allocations]
            return {
                "min_welfare": min(amounts),
                "avg_welfare": np.mean(amounts)
            }
            
        elif "social_allocator" in agent_name:
            allocations = alloc_decision["allocations"]
            amounts = [float(alloc["amount"]) for alloc in allocations]
            return {
                "min_welfare": min(amounts),
                "avg_welfare": np.mean(amounts)
            }
            
        elif "individual_allocator" in agent_name:
            summary = alloc_decision["distribution_summary"]
            return {
                "min_welfare": summary["allocation_range"]["minimum"],
                "avg_welfare": summary["average_per_person"]
            }
            
        elif "veil_of_ignorance" in agent_name:
            if "metrics" in alloc_decision:
                return alloc_decision["metrics"]
            else:
                allocations = alloc_decision["allocations"]
                amounts = [float(alloc["amount"]) for alloc in allocations]
                return {
                    "min_welfare": min(amounts),
                    "avg_welfare": np.mean(amounts)
                }
                
        return {}
        
    except Exception as e:
        print(f"Error extracting metrics for {agent_name}: {str(e)}")
        return {}

async def main():
    # Initialize environment
    env = SimulationEnvironment(
        output_dir="simulation_results",
        num_episodes=10,
        random_seed=42
    )
    
    # Initialize agents
    agents = [
        AnonymousFairnessAgent(
            name="veil_of_ignorance",
            num_profiles=10
        ),
        
        IndividualAllocatorAgent(
            name="individual_allocator",
            fairness_criteria={
                "need_based_weight": 0.7,
                "impact_weight": 0.3
            }
        ),
        
        SocialAllocatorAgent(
            name="social_allocator",
            fairness_criteria={
                "distributive_justice_weight": 0.4,
                "procedural_justice_weight": 0.3,
                "social_welfare_weight": 0.3
            }
        ),
        
        AllocatorAgent(
            name="resource_allocator",
            fairness_criteria={
                "need_based_weight": 0.7,
                "equality_weight": 0.2,
                "historical_weight": 0.1
            }
        )
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
            metrics_list = []
            for result in agent_results:
                for decision in result:
                    if decision["agent_name"] == agent.name:
                        metrics = extract_agent_metrics(decision["decision"], agent.name)
                        if metrics:
                            metrics_list.append(metrics)
            
            if metrics_list:
                avg_metrics = {
                    key: np.mean([m[key] for m in metrics_list if key in m])
                    for key in ["min_welfare", "avg_welfare"]
                }
                
                scenario_metrics[agent.name] = avg_metrics
                
                print(f"Average minimum welfare: {avg_metrics['min_welfare']:.3f}")
                print(f"Average welfare: {avg_metrics['avg_welfare']:.3f}")
        
        comparative_results[scenario_type] = scenario_metrics
    
    # Generate comparative analysis
    print("\nComparative Analysis Across Scenarios")
    print("=" * 50)
    
    metrics_to_compare = ["min_welfare", "avg_welfare"]
    
    for metric in metrics_to_compare:
        print(f"\n{metric.replace('_', ' ').title()}:")
        print("-" * 30)
        for scenario_type in ScenarioType:
            print(f"\n{scenario_type.value.title()} Scenario:")
            scenario_data = comparative_results[scenario_type]
            for agent_name, metrics in scenario_data.items():
                if metric in metrics:
                    print(f"{agent_name}: {metrics[metric]:.3f}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("simulation_results")
    output_dir.mkdir(exist_ok=True)
    
    # Save comparative results
    comparative_file = output_dir / f"comparative_analysis_{timestamp}.json"
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
    summary_file = output_dir / f"comparative_summary_{timestamp}.csv"
    summary_df.to_csv(summary_file, index=False)
    
    print("\nResults saved to:")
    print(f"Comparative analysis: {comparative_file}")
    print(f"Summary CSV: {summary_file}")

if __name__ == "__main__":
    asyncio.run(main())