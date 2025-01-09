# agents/individual_allocator.py
from typing import Dict, Any, List
from .base_agent import BaseAgent
import json

class IndividualAllocatorAgent(BaseAgent):
    def __init__(
        self, 
        name: str, 
        fairness_criteria: Dict[str, float],
        context_agent=None
    ):
        system_prompt = """You are responsible for distributing emergency funds to individuals during a crisis. Your role is to:

1. Evaluate each individual's needs and circumstances to determine appropriate allocation of funds.
   
2. Consider holistic factors such as existing resources and support.
   
3. Balance competing principles. 

Provide your response in the following JSON format:
{
    "individual_allocations": [
        {
            "persona": "description",
            "allocation_amount": number,
            "reasoning": "detailed explanation",
            "impact_analysis": {
                "immediate_needs_addressed": ["need1", "need2"],
                "long_term_benefits": ["benefit1", "benefit2"],
                "potential_risks": ["risk1", "risk2"]
            },
            "priority_level": "critical/high/medium/low",
            "special_considerations": ["consideration1", "consideration2"]
        }
    ],
    "allocation_strategy": {
        "principles_applied": ["principle1", "principle2"],
        "fairness_justification": "explanation",
        "trade_offs_considered": ["tradeoff1", "tradeoff2"]
    },
    "distribution_summary": {
        "total_allocated": number,
        "average_per_person": number,
        "allocation_range": {
            "minimum": number,
            "maximum": number
        }
    },
    "recommendations": {
        "additional_support_needed": ["recommendation1", "recommendation2"],
        "follow_up_actions": ["action1", "action2"]
    }
}"""
        
        super().__init__(name, "individual_allocator", system_prompt)
        self.fairness_criteria = fairness_criteria

    def _format_input(self, input_data: Dict[str, Any]) -> str:
        """Format allocation scenario for individual assessment"""
        total_funds = input_data.get("total_funds", 0)
        personas = input_data.get("personas", [])
        crisis_context = input_data.get("crisis_context", {})
        
        prompt = f"""Individual Emergency Fund Allocation Scenario

Available Funds: ${total_funds:,}

Crisis Context:
{json.dumps(crisis_context, indent=2)}

Individual Personas to Evaluate:
{json.dumps(personas, indent=2)}

Fairness Criteria:
{json.dumps(self.fairness_criteria, indent=2)}

Based on this information, determine the optimal allocation of funds to each individual.

Provide detailed reasoning for each allocation using the specified JSON format."""

        return prompt

    def _validate_allocations(self, 
        allocations: List[Dict[str, Any]], 
        total_funds: float
    ) -> bool:
        """Validate allocation decisions"""
        try:
            total_allocated = sum(item["allocation_amount"] 
                                for item in allocations)
            if total_allocated > total_funds:
                return False
            
            # Check all required fields
            required_fields = ["persona", "allocation_amount", "reasoning", 
                             "impact_analysis", "priority_level"]
            for item in allocations:
                if not all(field in item for field in required_fields):
                    return False
                    
            return True
        except Exception:
            return False

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate the allocation decision"""
        try:
            allocation_decision = json.loads(response)
            
            # Validate structure
            required_sections = ["individual_allocations", "allocation_strategy", 
                               "distribution_summary", "recommendations"]
            if not all(section in allocation_decision for section in required_sections):
                raise ValueError("Missing required sections in allocation decision")
            
            result = {
                "status": "success",
                "allocation_decision": allocation_decision,
                "metadata": {
                    "allocator_name": self.name,
                    "fairness_criteria_used": self.fairness_criteria
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