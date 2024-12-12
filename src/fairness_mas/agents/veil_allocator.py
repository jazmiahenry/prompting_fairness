from typing import Dict, Any, List, Tuple
import numpy as np
from dataclasses import dataclass
import asyncio
import random
from .base_agent import BaseAgent
import json

@dataclass
class MaximinMetrics:
    """Container for maximin-related metrics"""
    worst_case_outcome: float
    worst_case_profile: str
    maximin_score: float
    alternative_allocations: List[float]
    improvement_potential: float

def maximin_decision(
    options: List[str], 
    outcomes: List[List[float]]
) -> Tuple[str, float]:
    """Implements the maximin decision principle"""
    if not options or not outcomes or len(options) != len(outcomes):
        raise ValueError("Invalid input: options and outcomes must be non-empty and same length")
    
    worst_outcomes = [min(scenario) for scenario in outcomes]
    best_index = np.argmax(worst_outcomes)
    best_option = options[best_index]
    best_worst_outcome = worst_outcomes[best_index]
    
    return best_option, best_worst_outcome

@dataclass
class AnonymousProfile:
    """Anonymous profile with probabilistic needs and preferences"""
    profile_id: str
    need_level: float  # 0-1 scale
    resource_utility: float  # How effectively resources can be used
    vulnerability_index: float  # Combined measure of various risk factors
    preference_vector: np.ndarray  # Abstract representation of preferences
    
    @classmethod
    def generate_random(cls, profile_id: str) -> 'AnonymousProfile':
        """Generate a random anonymous profile"""
        return cls(
            profile_id=profile_id,
            need_level=random.random(),
            resource_utility=random.random(),
            vulnerability_index=random.random(),
            preference_vector=np.random.rand(5)  # 5-dimensional preference space
        )

class AnonymousFairnessAgent(BaseAgent):
    def __init__(
        self,
        name: str,
        num_profiles: int = 10,
        learning_rate: float = 0.01,
        consensus_threshold: float = 0.8
    ):
        system_prompt = """You are a Fairness Allocation Agent operating under the veil of ignorance.
        Your decisions must be made without knowledge of individual identities, focusing on:
        1. Maximizing welfare of the least advantaged (maximin principle)
        2. Ensuring equitable resource distribution
        3. Building consensus through collective decision-making
        
        Evaluate allocations purely on universal fairness principles."""
        
        super().__init__(name, "anonymous_fairness", system_prompt)
        self.num_profiles = num_profiles
        self.learning_rate = learning_rate
        self.consensus_threshold = consensus_threshold
        self.profiles = self._generate_profiles()
        
    def _generate_profiles(self) -> List[AnonymousProfile]:
        """Generate a set of anonymous profiles"""
        return [
            AnonymousProfile.generate_random(f"profile_{i}")
            for i in range(self.num_profiles)
        ]
    
    async def _calculate_welfare(
        self,
        allocation: float,
        profile: AnonymousProfile
    ) -> float:
        """Calculate welfare for a given allocation and profile"""
        # Calculate base welfare as a scalar
        base_welfare = profile.need_level * profile.resource_utility * allocation
        
        # Calculate preference alignment as a scalar
        preference_alignment = np.mean(profile.preference_vector)
        
        return float(base_welfare * (1 + preference_alignment))

    async def _evaluate_allocation(
        self,
        allocation: np.ndarray
    ) -> Tuple[float, float]:
        """Evaluate an allocation based on maximin principle"""
        welfare_scores = []
        for i, profile in enumerate(self.profiles):
            welfare = await self._calculate_welfare(allocation[i], profile)
            welfare_scores.append(welfare)
        
        return min(welfare_scores), np.mean(welfare_scores)

    async def _build_consensus(
        self,
        initial_allocation: np.ndarray,
        max_iterations: int = 100
    ) -> np.ndarray:
        """Build consensus through iterative refinement"""
        current_allocation = initial_allocation.copy()
        best_min_welfare = float('-inf')
        best_allocation = current_allocation.copy()
        
        for _ in range(max_iterations):
            # Generate adjustments
            adjustment = np.random.normal(0, 0.1, size=current_allocation.shape)
            proposed_allocation = np.clip(current_allocation + adjustment, 0, 1)
            # Ensure sum equals 1
            proposed_allocation = proposed_allocation / np.sum(proposed_allocation)
            
            # Evaluate proposed allocation
            min_welfare, avg_welfare = await self._evaluate_allocation(proposed_allocation)
            
            if min_welfare > best_min_welfare:
                best_min_welfare = min_welfare
                best_allocation = proposed_allocation.copy()
                current_allocation = proposed_allocation.copy()
        
        return best_allocation

    def _format_input(self, input_data: Dict[str, Any]) -> str:
        """Format the allocation scenario for the agent"""
        resources = input_data.get("available_resources", 100)
        constraints = input_data.get("constraints", {})
        
        scenario = {
            "total_resources": resources,
            "number_of_profiles": self.num_profiles,
            "profile_statistics": {
                "avg_need_level": float(np.mean([p.need_level for p in self.profiles])),
                "avg_vulnerability": float(np.mean([p.vulnerability_index for p in self.profiles])),
                "need_distribution": "heterogeneous"
            },
            "constraints": constraints
        }
        
        return json.dumps(scenario, indent=2)

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the agent's response"""
        try:
            return {
                "status": "success",
                "message": "Using internally calculated allocation"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error parsing response: {str(e)}"
            }
    async def _evaluate_maximin_metrics(
        self,
        current_allocation: np.ndarray
    ) -> MaximinMetrics:
        """Evaluate allocation using maximin principles"""
        # Generate alternative allocations for comparison
        num_alternatives = 10
        alternative_allocations = []
        alternative_outcomes = []
        
        # Include current allocation
        current_welfare_scores = []
        for i, profile in enumerate(self.profiles):
            welfare = await self._calculate_welfare(current_allocation[i], profile)
            current_welfare_scores.append(welfare)
        
        worst_current = min(current_welfare_scores)
        worst_profile_idx = np.argmin(current_welfare_scores)
        worst_profile = self.profiles[worst_profile_idx].profile_id
        
        # Generate and evaluate alternatives
        for _ in range(num_alternatives):
            alt_allocation = np.random.dirichlet(np.ones(self.num_profiles))
            alt_welfare_scores = []
            for i, profile in enumerate(self.profiles):
                welfare = await self._calculate_welfare(alt_allocation[i], profile)
                alt_welfare_scores.append(welfare)
            alternative_allocations.append(alt_allocation)
            alternative_outcomes.append(alt_welfare_scores)
        
        # Apply maximin decision principle
        allocation_labels = [f"alternative_{i}" for i in range(num_alternatives)]
        allocation_labels.append("current")
        all_outcomes = alternative_outcomes + [current_welfare_scores]
        
        best_option, best_worst_outcome = maximin_decision(
            allocation_labels, 
            all_outcomes
        )
        
        # Calculate improvement potential
        improvement_potential = best_worst_outcome - worst_current if best_worst_outcome > worst_current else 0
        
        return MaximinMetrics(
            worst_case_outcome=worst_current,
            worst_case_profile=worst_profile,
            maximin_score=best_worst_outcome,
            alternative_allocations=[list(alloc) for alloc in alternative_allocations],
            improvement_potential=improvement_potential
        )

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process allocation request with enhanced maximin metrics"""
        try:
            total_resources = float(input_data.get("available_resources", 100))
            
            # Generate and evaluate allocation
            initial_allocation = np.ones(self.num_profiles) / self.num_profiles
            final_allocation = await self._build_consensus(initial_allocation)
            scaled_allocation = final_allocation * total_resources
            
            # Calculate standard metrics
            min_welfare, avg_welfare = await self._evaluate_allocation(final_allocation)
            gini = float(self._calculate_gini(scaled_allocation))
            equity = float(self._calculate_equity(scaled_allocation))
            
            # Calculate maximin metrics
            maximin_metrics = await self._evaluate_maximin_metrics(final_allocation)
            
            # Prepare detailed result
            allocations = []
            for profile, alloc in zip(self.profiles, scaled_allocation):
                allocations.append({
                    "profile_id": profile.profile_id,
                    "amount": float(alloc),
                    "need_level": float(profile.need_level),
                    "vulnerability_index": float(profile.vulnerability_index)
                })
            
            return {
                "status": "success",
                "allocation_decision": {
                    "allocations": allocations,
                    "standard_metrics": {
                        "minimum_welfare": float(min_welfare),
                        "average_welfare": float(avg_welfare),
                        "gini_coefficient": gini,
                        "equity_score": equity
                    },
                    "maximin_analysis": {
                        "worst_case_outcome": float(maximin_metrics.worst_case_outcome),
                        "worst_case_profile": maximin_metrics.worst_case_profile,
                        "maximin_score": float(maximin_metrics.maximin_score),
                        "improvement_potential": float(maximin_metrics.improvement_potential),
                        "maximin_principle_satisfied": maximin_metrics.improvement_potential == 0
                    },
                    "fairness_analysis": {
                        "maximin_satisfaction": (
                            "Optimal" if maximin_metrics.improvement_potential == 0 
                            else f"Suboptimal with {maximin_metrics.improvement_potential:.3f} improvement potential"
                        ),
                        "equity_principle": "Resources distributed based on anonymous needs",
                        "consensus_level": "Achieved through collective optimization"
                    }
                }
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _calculate_gini(self, allocation: np.ndarray) -> float:
        """Calculate Gini coefficient for allocation"""
        sorted_allocation = np.sort(allocation)
        n = len(allocation)
        index = np.arange(1, n + 1)
        return float(((2 * np.sum(index * sorted_allocation)) / 
                     (n * np.sum(sorted_allocation))) - ((n + 1) / n))

    def _calculate_equity(self, allocation: np.ndarray) -> float:
        """Calculate equity score based on need-weighted distribution"""
        need_levels = np.array([p.need_level for p in self.profiles])
        ideal_allocation = need_levels / np.sum(need_levels)
        return float(1 - np.mean(np.abs(allocation - ideal_allocation)))