from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
import json

class SocialAllocatorAgent(BaseAgent):
    def __init__(
        self, 
        name: str, 
        fairness_criteria: Dict[str, float],
        context_agent=None,
        mediator_agent=None
    ):
        system_prompt = """You are responsible for the fair and ethical distribution of emergency resources to communities in need. Your role is to:

1. Analyze community needs and vulnerability factors
2. Consider socioeconomic context and historical inequities
3. Describe prioritization based on factors you consider to be most important.
4. Make transparent, justifiable decisions
5. Balance competing needs when resources are scarce.

When making allocations, define what considerations most influenced your decision making. 

Provide your response in the following JSON format:
{
    "allocations": [
        {
            "recipient_group": "group_name",
            "amount": number,
            "reasoning": "detailed explanation",
            "priority_level": "critical/high/medium/low",
            "expected_impact": "description",
            "vulnerability_factors": ["factor1", "factor2"]
        }
    ],
    "overall_strategy": "explanation of allocation strategy",
    "fairness_analysis": {
        "equity_considerations": "description",
        "access_barriers_addressed": ["barrier1", "barrier2"],
        "long_term_implications": "analysis"
    },
    "unmet_needs": {
        "description": "analysis of needs that couldn't be met",
        "recommendations": ["recommendation1", "recommendation2"]
    }
}"""
        
        super().__init__(name, "social_allocator", system_prompt)
        self.fairness_criteria = fairness_criteria
        self.context_agent = context_agent
        self.mediator_agent = mediator_agent

    async def _get_context(self, situation_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get contextual information if context agent is available"""
        if self.context_agent:
            try:
                context = await self.context_agent.process(situation_data)
                return context
            except Exception as e:
                print(f"Error getting context: {e}")
        return None

    async def _check_conflicts(self, allocation_plan: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check for conflicts if mediator agent is available"""
        if self.mediator_agent:
            try:
                conflicts = await self.mediator_agent.process(allocation_plan)
                return conflicts
            except Exception as e:
                print(f"Error checking conflicts: {e}")
        return None

    def _format_input(self, input_data: Dict[str, Any]) -> str:
        """Format the allocation scenario with all available context"""
        total_funds = input_data.get("total_funds", 0)
        community_data = input_data.get("community_data", {})
        context = input_data.get("context", {})
        constraints = input_data.get("constraints", {})
        
        prompt = f"""Emergency Resource Allocation Scenario

Available Funds: ${total_funds}

Community Information:
{json.dumps(community_data, indent=2)}

Context and Background:
{json.dumps(context, indent=2)}

Constraints and Requirements:
{json.dumps(constraints, indent=2)}

Based on this information, allocate the available funds to best serve the community's needs. Consider both immediate impact and long-term sustainability. Provide detailed reasoning for your decisions using the specified JSON format."""

        return prompt

    def _validate_allocation(self, allocation: Dict[str, Any], total_funds: float) -> bool:
        """Validate that allocation meets basic requirements"""
        try:
            total_allocated = sum(item["amount"] for item in allocation["allocations"])
            if total_allocated > total_funds:
                return False
                
            # Check for required fields in each allocation
            required_fields = ["recipient_group", "amount", "reasoning", "priority_level"]
            for item in allocation["allocations"]:
                if not all(field in item for field in required_fields):
                    return False
                    
            return True
        except Exception:
            return False

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process allocation request with context and conflict checking"""
        try:
            # Get additional context if available
            context = await self._get_context(input_data)
            if context:
                input_data["context"] = context

            # Generate initial allocation plan
            allocation_result = await super().process(input_data)
            
            # Check for conflicts if available
            if "allocation_decision" in allocation_result:
                conflicts = await self._check_conflicts(allocation_result["allocation_decision"])
                if conflicts:
                    # Adjust allocation based on conflicts
                    input_data["conflicts"] = conflicts
                    allocation_result = await super().process(input_data)

            return allocation_result

        except Exception as e:
            return {
                "status": "error",
                "error": f"Error in allocation process: {str(e)}"
            }

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate the allocation decision"""
        try:
            allocation_decision = json.loads(response)
            
            # Validate structure and required fields
            required_fields = ["allocations", "overall_strategy", "fairness_analysis", "unmet_needs"]
            if not all(field in allocation_decision for field in required_fields):
                raise ValueError("Missing required fields in allocation decision")
            
            result = {
                "status": "success",
                "allocation_decision": allocation_decision,
                "metadata": {
                    "allocator_name": self.name,
                    "fairness_criteria_used": self.fairness_criteria,
                    "context_used": bool(self.context_agent),
                    "mediation_used": bool(self.mediator_agent)
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