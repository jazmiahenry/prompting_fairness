# agents/allocator.py
from typing import Dict, Any, List
import json
from .base_agent import BaseAgent

class AllocatorAgent(BaseAgent):
    def __init__(self, name: str, fairness_criteria: Dict[str, float]):
        system_prompt = """You are an Allocator Agent responsible for fair resource distribution.
        Your role is to:
        1. Analyze resource requests and current allocations
        2. Consider fairness criteria and priorities
        3. Make allocation decisions
        4. Explain your reasoning
        
        Provide your response in the following JSON format:
        {
            "allocations": [
                {
                    "department": "department_name",
                    "allocated_resources": {
                        "resource_type": amount
                    },
                    "percentage_of_request_granted": number
                }
            ],
            "reasoning": {
                "overall_strategy": "explanation",
                "department_specific": [
                    {
                        "department": "department_name",
                        "reasoning": "explanation"
                    }
                ],
                "fairness_analysis": "explanation"
            },
            "unused_resources": {
                "resource_type": amount
            }
        }"""
        
        super().__init__(name, "allocator", system_prompt)
        self.fairness_criteria = fairness_criteria

    def _calculate_priority_score(self, request: Dict[str, Any]) -> float:
        """Calculate priority score based on request attributes"""
        priority_weights = {
            "high": 1.0,
            "medium": 0.7,
            "low": 0.4
        }
        
        base_score = priority_weights[request["priority"].lower()]
        
        # Calculate need-based component
        current = request["current_allocation"]
        requested = request["requested_resources"]
        
        # Calculate percentage increase requested
        need_scores = []
        for resource in current.keys():
            if current[resource] > 0:  # Avoid division by zero
                need_scores.append(
                    (requested[resource] - current[resource]) / current[resource]
                )
        
        avg_need_score = sum(need_scores) / len(need_scores) if need_scores else 0
        normalized_need = min(max(avg_need_score, 0), 1)  # Clamp between 0 and 1
        
        # Combine scores using fairness criteria weights
        final_score = (
            base_score * (1 - self.fairness_criteria["need_based_weight"]) +
            normalized_need * self.fairness_criteria["need_based_weight"]
        )
        
        return final_score

    def _format_input(self, input_data: Dict[str, Any]) -> str:
        """Format resource allocation request with priority scores"""
        resources = input_data["available_resources"]
        requests = input_data["requests"]
        
        # Calculate priority scores for each request
        for request in requests:
            request["priority_score"] = self._calculate_priority_score(request)
        
        # Sort requests by priority score
        sorted_requests = sorted(
            requests,
            key=lambda x: x["priority_score"],
            reverse=True
        )
        
        prompt = f"""Please allocate the following resources based on these requests and priority scores.

Available Resources:
{json.dumps(resources, indent=2)}

Requests (sorted by priority):
{json.dumps(sorted_requests, indent=2)}

Fairness Criteria Weights:
{json.dumps(self.fairness_criteria, indent=2)}

Consider:
1. Higher priority scores should receive more of their requested resources
2. Ensure minimum viable allocations for all departments
3. Keep at least {self.fairness_criteria['equality_weight'] * 100}% of resources for equal distribution
4. Account for historical allocations with {self.fairness_criteria['historical_weight'] * 100}% weight

Provide allocation decision in the specified JSON format."""

        return prompt

    def _validate_allocations(self, 
        allocations: List[Dict[str, Any]], 
        available_resources: Dict[str, Any]
    ) -> bool:
        """Validate that allocations don't exceed available resources"""
        used_resources = {
            resource: 0 for resource in available_resources.keys()
        }
        
        # Sum up all allocated resources
        for alloc in allocations:
            for resource, amount in alloc["allocated_resources"].items():
                used_resources[resource] += amount
        
        # Check if any resource is overallocated
        for resource, amount in used_resources.items():
            if amount > available_resources[resource]:
                return False
        
        return True

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate the allocation decision"""
        try:
            # Parse JSON response
            allocation_decision = json.loads(response)
            
            # Validate required fields
            required_fields = ["allocations", "reasoning", "unused_resources"]
            if not all(field in allocation_decision for field in required_fields):
                raise ValueError("Missing required fields in allocation decision")
            
            # Add metadata about the allocation
            result = {
                "status": "success",
                "allocation_decision": allocation_decision,
                "metadata": {
                    "allocator_name": self.name,
                    "fairness_criteria_used": self.fairness_criteria,
                    "timestamp": None  # Could add timestamp here if needed
                }
            }
            
            return result
            
        except json.JSONDecodeError:
            return {
                "status": "error",
                "error": "Failed to parse allocation response as JSON",
                "raw_response": response
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error processing allocation response: {str(e)}",
                "raw_response": response
            }