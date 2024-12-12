from typing import Dict, Any, List, Optional, Union
import numpy as np
import pandas as pd
from enum import Enum
from pathlib import Path
import json
from datetime import datetime
import logging
from tqdm import tqdm

class ScenarioType(Enum):
    STATIC = "static"
    DYNAMIC = "dynamic"
    CULTURAL = "cultural"

class SimulationEnvironment:
    def __init__(
        self,
        output_dir: str = "simulation_results",
        num_episodes: int = 100,
        random_seed: Optional[int] = None
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.num_episodes = num_episodes
        
        if random_seed is not None:
            np.random.seed(random_seed)
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Set up logging configuration"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.output_dir / f"simulation_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _generate_scenario_data(self, scenario_type: ScenarioType) -> Dict[str, Any]:
        """Generate appropriate scenario data based on agent type"""
        base_data = {
            "available_resources": 100000,
            "total_funds": 100000,  # for compatibility with different agent types
            "constraints": {
                "minimum_allocation": 1000,
                "maximum_allocation": 30000
            }
        }

        if scenario_type == ScenarioType.STATIC:
            # Add data for AllocatorAgent
            base_data["requests"] = [
                {
                    "department": f"Department_{i}",
                    "priority": np.random.choice(["high", "medium", "low"]),
                    "current_allocation": {
                        "resource_type": np.random.randint(1000, 5000)
                    },
                    "requested_resources": {
                        "resource_type": np.random.randint(5000, 15000)
                    }
                } for i in range(5)
            ]

            # Add data for SocialAllocatorAgent
            base_data["community_data"] = {
                "total_population": 50000,
                "vulnerable_groups": ["elderly", "disabled", "low_income"],
                "economic_indicators": {
                    "unemployment_rate": "12%",
                    "poverty_rate": "15%"
                }
            }

            # Add data for IndividualAllocatorAgent
            base_data["personas"] = [
                {
                    "type": "unemployed",
                    "details": {
                        "current_income": 0,
                        "dependents": 2,
                        "savings": 1000
                    }
                },
                {
                    "type": "essential_worker",
                    "details": {
                        "current_income": 35000,
                        "dependents": 1,
                        "savings": 2000
                    }
                }
            ]

        return base_data

    def _extract_metrics_by_agent_type(self, 
        decision: Dict[str, Any], 
        agent_name: str
    ) -> Dict[str, float]:
        """Extract metrics based on agent type"""
        try:
            if decision["status"] != "success":
                return {}

            allocation_decision = decision["allocation_decision"]
            
            if "resource_allocator" in agent_name:
                # Handle AllocatorAgent metrics
                allocations = allocation_decision["allocations"]
                amounts = [
                    sum(alloc["allocated_resources"].values())
                    for alloc in allocations
                ]
                return {
                    "minimum_welfare": min(amounts),
                    "average_welfare": np.mean(amounts),
                    "equity_score": 1.0 - (max(amounts) - min(amounts)) / max(amounts) if max(amounts) > 0 else 1.0
                }

            elif "social_allocator" in agent_name:
                # Handle SocialAllocatorAgent metrics
                allocations = allocation_decision["allocations"]
                amounts = [float(alloc["amount"]) for alloc in allocations]
                return {
                    "minimum_welfare": min(amounts),
                    "average_welfare": np.mean(amounts),
                    "equity_score": 1.0 - (max(amounts) - min(amounts)) / max(amounts) if max(amounts) > 0 else 1.0
                }

            elif "individual_allocator" in agent_name:
                # Handle IndividualAllocatorAgent metrics
                allocations = allocation_decision["individual_allocations"]
                amounts = [float(alloc["allocation_amount"]) for alloc in allocations]
                summary = allocation_decision["distribution_summary"]
                return {
                    "minimum_welfare": summary["allocation_range"]["minimum"],
                    "average_welfare": summary["average_per_person"],
                    "equity_score": 1.0 - (summary["allocation_range"]["maximum"] - 
                                        summary["allocation_range"]["minimum"]) / 
                                        summary["allocation_range"]["maximum"]
                }

            elif "veil_of_ignorance" in agent_name:
                # Handle AnonymousFairnessAgent metrics
                if "metrics" in allocation_decision:
                    return allocation_decision["metrics"]
                else:
                    allocations = allocation_decision["allocations"]
                    amounts = [float(alloc["amount"]) for alloc in allocations]
                    return {
                        "minimum_welfare": min(amounts),
                        "average_welfare": np.mean(amounts),
                        "equity_score": 1.0 - (max(amounts) - min(amounts)) / max(amounts) if max(amounts) > 0 else 1.0
                    }

            return {}

        except Exception as e:
            self.logger.error(f"Error extracting metrics for {agent_name}: {str(e)}")
            return {}

    async def run_simulation(self, agents: List[Any], scenario_type: ScenarioType) -> List[Dict[str, Any]]:
        """Run simulation with specified agents and scenario type"""
        results = []
        
        with tqdm(total=self.num_episodes, desc=f"Running {scenario_type.value} scenarios") as pbar:
            for episode in range(self.num_episodes):
                scenario_data = self._generate_scenario_data(scenario_type)
                episode_results = await self._run_episode(agents, scenario_data, episode)
                results.append(episode_results)
                
                if episode % 10 == 0:
                    self._save_results(results, scenario_type)
                
                pbar.update(1)
        
        self._save_results(results, scenario_type)
        return results

    async def _run_episode(
        self,
        agents: List[Any],
        scenario_data: Dict[str, Any],
        episode: int
    ) -> Dict[str, Any]:
        """Run a single simulation episode"""
        episode_results = {
            "episode": episode,
            "scenario_data": scenario_data,
            "agent_decisions": []
        }
        
        for agent in agents:
            try:
                decision = await agent.process(scenario_data)
                
                metrics = self._extract_metrics_by_agent_type(decision, agent.name)
                
                episode_results["agent_decisions"].append({
                    "agent_name": agent.name,
                    "decision": decision,
                    "metrics": metrics
                })
                
                self.logger.info(f"Episode {episode}, Agent {agent.name} completed decision")
            except Exception as e:
                self.logger.error(f"Error with agent {agent.name} in episode {episode}: {str(e)}")
        
        return episode_results

    def _save_results(self, results: List[Dict[str, Any]], scenario_type: ScenarioType):
        """Save simulation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        results_file = self.output_dir / f"results_{scenario_type.value}_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Create summary DataFrame
        summary_data = []
        for result in results:
            for decision in result["agent_decisions"]:
                if decision.get("metrics"):
                    summary_data.append({
                        "episode": result["episode"],
                        "agent_name": decision["agent_name"],
                        **decision["metrics"]
                    })
        
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            summary_file = self.output_dir / f"summary_{scenario_type.value}_{timestamp}.csv"
            summary_df.to_csv(summary_file, index=False)