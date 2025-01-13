from pydantic import BaseModel
from typing import List, Optional, Dict, Any
'''
The output pydantic models for eachg task
'''

class TargetGroupsPydantic(BaseModel):
    characteristics: str
    reasons: str

# Define the main model that contains target_audience as a key
class Task11Pydantic(BaseModel):
    target_audience: Dict[str,TargetGroupsPydantic]

class Task21Pydantic(BaseModel):
    buyer_persona:str
    narrative:str
    demographic_information:str 
    psychographic_information:str
    behavioral_information:str
    buying_process:str
    consumption_patterns:str 
    aspirations:str

class Task24Pydantic(BaseModel):
    jtbd_statement:str

class Task25Pydantic(BaseModel):
    stages_of_awareness_analysis:str
    unaware:str
    problem_aware:str
    solution_aware:str
    product_aware:str
    most_aware:str
    summary_and_recommendations:str

class Task31Pydantic(BaseModel):
    value_proposition_canvas:str
    customer_profile:str
    customer_jobs:str
    customer_pains:str
    customer_gains:str
    value_map:str
    pain_relievers:str
    gain_creators:str
    products_and_services:str
    fit_evaluation:str

class Task32Pydantic(BaseModel):
    product:str
    price:str
    place:str
    promotion:str

class Task33Pydantic(BaseModel):
    swot_analysis:str

class Task34Pydantic(BaseModel):
    buyers_journey:str
    awareness_stage:str
    consideration_stage:str
    decision_stage:str
    post_purchase_stage:str
    key_insights:str

class Task35Pydantic(BaseModel):
    market_analysis:str

class Task41Pydantic(BaseModel):
    brand_story:str
    hero:str
    problem:str
    guide:str
    call_to_action:str
    result:str

class Task42Pydantic(BaseModel):
    aida_framework:str
    summary:str

class Task43Pydantic(BaseModel):
    platform_recommendations:str

class Task44Pydantic(BaseModel):
    lead_stages:str
    stage_name:str
    audience_behavior:str
    audience_thoughts:str
    content_ideas:str
    call_to_action:str
    example_prompt:str

class Task45Pydantic(BaseModel):
    lead_qualification_checklist:str

class Task46Pydantic(BaseModel):
    product_description:str

class Task47Pydantic(BaseModel):
    user_experience_map:str

class Task48Pydantic(BaseModel):
    customer_feedback:str

class Task51Pydantic(BaseModel):
    target_audience:str

class Task52Pydantic(BaseModel):
    user_story:str

class Task53Pydantic(BaseModel):
    user_journey:str

class Task54Pydantic(BaseModel):
    user_needs:str

class Task61Pydantic(BaseModel):
    market_research:str

class Task62Pydantic(BaseModel):
    market_trends:str

class Task63Pydantic(BaseModel):
    market_opportunities:str

class Task64Pydantic(BaseModel):
    market_threats:str

class Task65Pydantic(BaseModel):
    market_share:str

class Task66Pydantic(BaseModel):
    market_positioning:str

class Task67Pydantic(BaseModel):
    market_competitors:str

class Task71Pydantic(BaseModel):
    product_design:str

class Task72Pydantic(BaseModel):
    product_features:str

class Task73Pydantic(BaseModel):
    product_usability:str

class Task74Pydantic(BaseModel):
    product_performance:str

class Task81Pydantic(BaseModel):
    branding:str

class Task82Pydantic(BaseModel):
    brand_voice:str

class Task83Pydantic(BaseModel):
    brand_identity:str

class Task84Pydantic(BaseModel):
    brand_colors:str

class Task91Pydantic(BaseModel):
    marketing_strategy:str

class Task92Pydantic(BaseModel):
    marketing_channels:str

class Task93Pydantic(BaseModel):
    marketing_tools:str

class Task94Pydantic(BaseModel):
    marketing_budget:str

class Task95Pydantic(BaseModel):
    marketing_results:str

class Task96Pydantic(BaseModel):
    marketing_leadership:str
    

