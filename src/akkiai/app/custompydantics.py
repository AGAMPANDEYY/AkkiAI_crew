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

class BuyerPersonaPydantic(BaseModel):
    name: str
    narrative:str
    demographic_information:str 
    psychographic_information:str
    behavioral_information:str
    buying_process:str
    consumption_patterns:str 
    aspirations:str

class Task21Pydantic(BaseModel):
    buyer_persona: BuyerPersonaPydantic
    
class Task22Pydantic(BaseModel):
    demographics: str
    psychographics: str
    behavior_patterns: str
    consumption_patterns: str
    pain_points: str
    buying_triggers: str
    communication_preferences: str

class Task23Pydantic(BaseModel):
    demographic_information: str
    professional_background: str
    pain_points_and_needs: str
    buying_triggers: str
    buying_behavior:str
    communication_preferences:str 
    personal_goals_and_motivations: str
    key_influencers: str

class Task24Pydantic(BaseModel):
    analysis: str
    jtbd_statement:str

class AwarenessPydantic(BaseModel):
    unaware:str
    problem_aware:str
    solution_aware:str
    product_aware:str
    most_aware:str

class Task25Pydantic(BaseModel):
    stages_of_awareness_analysis:AwarenessPydantic
    summary_and_recommendations:str

class VPCPydantic(BaseModel):
    customer_profile:str
    customer_jobs:str
    customer_pains:str
    customer_gains:str
    value_map:str
    pain_relievers:str
    gain_creators:str
    products_and_services:str
    fit_evaluation:str

class Task31Pydantic(BaseModel):
    value_proposition_canvas: VPCPydantic
    
class ProductPydantic(BaseModel):
    problem_solved: str
    competitive_advantage: str
    key_features_benefits: str
    
class PricePydantic(BaseModel):
    pricing_model: str
    perceived_value: str
    price_sensitivities: str

class PlacePydantic(BaseModel):
    solution_seeking_behavior: str
    distribution_channels: str
    accessibility: str

class PromotionPydantic(BaseModel):
    marketing_messages: str
    advertising_channels: str
    messaging_style: str

class Task32Pydantic(BaseModel):
    product: ProductPydantic
    price:PricePydantic
    place: PlacePydantic
    promotion:PromotionPydantic

class SWOTPydantic(BaseModel):
    strengths: str
    weaknesses: str
    opportunities: str
    threats: str

class Task33Pydantic(BaseModel):
    swot_analysis: SWOTPydantic
    summary: str

class BuyerJourneyPydantic(BaseModel):
    awareness_stage:str
    consideration_stage:str
    decision_stage:str
    post_purchase_stage:str
    key_insights:str

class Task34Pydantic(BaseModel):
    buyers_journey:BuyerJourneyPydantic
  
class RoseAnalysisPydantic(BaseModel):
    relevant:str
    original:str 
    simple:str 
    emotional: str 

class Task35Pydantic(BaseModel):
    rose_analysis:RoseAnalysisPydantic
    top3_USPs: str
    moat: str
    implementation_strategy: str
    success_metric: str
    summary : str

class MarketingStrategyPydantic(BaseModel):
    customer_hero:str
    problem:str
    brand_guide:str
    action_plan:str

class Task41Pydantic(BaseModel):
    marketing_strategy: MarketingStrategyPydantic
  
class Task42Pydantic(BaseModel):
    aida_framework:str
    summary:str

class MarketEntryPydantic(BaseModel):
    market_analysis: str
    target_segments: str
    entry_mode: str
    positioning_strategy: str
    marketing_plan: str
    risk_mitigation: str
    kpis: str 
    growth_strategy: str
    conclusion: str 

class Task43Pydantic(BaseModel):
    market_entry_strategy: MarketEntryPydantic

class BABFrameworkPydantic(BaseModel):
    before: str
    after: str
    bridge: str

class Task44Pydantic(BaseModel):
    bab_framework: BABFrameworkPydantic

class PASFrameworkPydantic(BaseModel):
    problem: str
    agitate: str 
    solution: str 

class Task45Pydantic(BaseModel):
    pas_framework:str

class STPPositioningPydantic(BaseModel):
    value_proposition: str 
    differentiation: str 
    brand_messaging: str 
    positioning_statement: str 


class STPPydantic(BaseModel):
    segmentation: str
    targeting: str 
    positioning: STPPositioningPydantic 

class Task46Pydantic(BaseModel):
    stp_strategy:STPPydantic

class STEPOutputPydantic(BaseModel):
    customer_persona: str 

class STEPPydantic(BaseModel):
    step_analysis:str
    step_output: STEPOutputPydantic

class SummaryPydantic(BaseModel):
    benefits: str
    limitations: str

class Task47Pydantic(BaseModel):
    step_1: STEPPydantic
    step_2: STEPPydantic
    step_3: STEPPydantic
    step_4: STEPPydantic
    step_5: STEPPydantic
    step_6: STEPPydantic
    step_7: STEPPydantic
    step_8: STEPPydantic
    summary: SummaryPydantic

class RecommendationPydantic(BaseModel):
    chosen_archetype: str
    justification: str
    brand_strategy: str
    benefits: str
    examples: str
    implementation: str

class Task48Pydantic(BaseModel):
    recommendations: RecommendationPydantic

class MarketStartegyPydantic(BaseModel):
    target_audience: str 
    product_analysis: str 
    customer_persona: str 
    value_proposition: str 
    market_assumptions: str 
    infrastructure_readiness: str 
    customer_readiness: str 
    key_recommendations: str 

class Task51Pydantic(BaseModel):
    market_startegy:MarketStartegyPydantic

class Task52Pydantic(BaseModel):
    technology_adoption_analysis:str
    recommendations: str 

class StrategyPydantic(BaseModel):
    critical_risks: str 
    resource_constraints:str 
    strategic_decisions: str 
    recommendations: str 

class Task53Pydantic(BaseModel):
    startup_analysis:str
    market_strategy: StrategyPydantic

class FactorsPydantic(BaseModel):
    eliminate: str 
    reduce: str 
    raise_factors:str 
    create: str 

class BlueOcenPydantic(BaseModel):
    industry_factors_plot: str 
    factor_identification: FactorsPydantic
    uncontested_market_space: str 
    summary: str 

class Task54Pydantic(BaseModel):
    blue_ocean_analysis: BlueOcenPydantic

class TAMSAMSOMPydantic(BaseModel):
    size: str 
    explanation: str

class MarketAnalysisPydantic(BaseModel):
    tam: TAMSAMSOMPydantic
    sam: TAMSAMSOMPydantic
    som: TAMSAMSOMPydantic
    competitive_landscape: str 
    trends: str 
    legal_factors: str
    conclusion: str 
   
class Task61Pydantic(BaseModel):
    market_analysis: MarketAnalysisPydantic

class CompetitorPydantic(BaseModel):
    name: str 
    description: str 
    advantages: str 
    disadvantages:str 

class DiNrectCompetitorsPydantic(BaseModel):
    competitor: CompetitorPydantic

class CompetitiveAnalysisPydantic(BaseModel):
    direct_competitors:DiNrectCompetitorsPydantic
    direct_competitors: DiNrectCompetitorsPydantic
    future_potential_competitors: DiNrectCompetitorsPydantic
    overall_assessment: str 

class Task62Pydantic(BaseModel):
    competitive_analysis: CompetitiveAnalysisPydantic

class MarketSizePydantic(BaseModel):
    total_addressable_market: str 
    serviceable_addressable_market: str 
    serviceable_obtainable_market: str 

class MarketAnalysisPydantic2(BaseModel):
    executive_summary: str 
    market_size: MarketSizePydantic
    competitive_landscape: str 
    market_trends: str 
    regulatory_factors:str 
    conclusion:str 

class Task63Pydantic(BaseModel):
    market_analysis:MarketAnalysisPydantic2

class Task64Pydantic(BaseModel):
    strategic_group_map:str
    group_characteristics: str 
    competitive_insights: str 
    strategy_recommendations: str
    step_planning: str 
    output_step_1: str 
    output_step_2: str
    output_step_3: str
    output_step_4: str
    output_step_5: str
    output_step_6: str
    output_step_7: str
    strategic_group_map: str 
    group_characteristics: str 
    competitive_insights: str 
    strategy_recommendations: str 

class ForcePydantic(BaseModel):
    force_analysis:str 
    force: str 

class SynthesisPydantic(BaseModel):
    industry_profitability: str
    strategic_opportunities: str 
    market_positioning: str 

class FrameworkPydantic(BaseModel):
    benefits: str 
    limitations: str 

class PortorsFiveForcePydantic(BaseModel):
    competitive_rivalry: ForcePydantic
    supplier_power:ForcePydantic
    buyer_power: ForcePydantic
    threat_of_substitution: ForcePydantic
    threat_of_new_entry: ForcePydantic
    synthesis: SynthesisPydantic
    framework_evaluation: FrameworkPydantic


class Task65Pydantic(BaseModel):
    porters_five_forces_analysis:PortorsFiveForcePydantic

class CompetitionAnalysisPydantic(BaseModel):
    competitor_strengths: str 
    weaknesses: str 
    opportunities: str 
    threats:str 


class Task66Pydantic(BaseModel):
    competition_analysis: CompetitionAnalysisPydantic 

class Task67Pydantic(BaseModel):
    market_analysis:MarketAnalysisPydantic2

class ProductPlanPydantic(BaseModel):
    step_1: str 
    step_1_info: str 
    step_2: str
    step_2_info: str 
    step_3: str
    step_3_info: str 
    step_4: str
    step_4_info: str
    step_5: str
    step_5_info: str

class Task71Pydantic(BaseModel):
    product_plan:ProductPlanPydantic

class InitiavtePydantic(BaseModel):
    name: str 
    description: str

class KeyIntiativesPydantic(BaseModel):
    initiative_1: InitiavtePydantic 
    initiative_2: InitiavtePydantic
    initiative_3: InitiavtePydantic
    


class NowNextLaterPydantic(BaseModel):
    timeframe:str 
    goal: str 
    key_initiatives: KeyIntiativesPydantic
    success_metrics: str 
    dependencies: str 
    owner:str 
    risks_and_mitigation: str 

class ProductRoadMapPydantic(BaseModel):
    now: NowNextLaterPydantic
    next: NowNextLaterPydantic
    later: NowNextLaterPydantic

class Task72Pydantic(BaseModel):
    product_roadmap: ProductRoadMapPydantic

class MVPPydantic(BaseModel):
    core_features: str 
    exclusions: str 


class PRDPydantic(BaseModel):
    product_overview: str 
    goals_and_success_metrics: str 
    scope_of_mvp: MVPPydantic
    user_stories_and_use_cases:str 
    functional_requirements: str 
    technical_requirements: str 
    wireframes_or_mockups: str 
    risks_and_assumptions: str 
    success_validation_plan: str 
    timeline_and_milestones: str 

class Task73Pydantic(BaseModel):
    prd:PRDPydantic

class Task74Pydantic(BaseModel):
    prd:PRDPydantic

class QuestionAnalysisAnswerPydantic(BaseModel):
    question: str
    analysis: str
    answer: str

class QuestionPydantic(BaseModel):
    question_1: QuestionAnalysisAnswerPydantic
    question_2: QuestionAnalysisAnswerPydantic
    question_3: QuestionAnalysisAnswerPydantic
    question_4: QuestionAnalysisAnswerPydantic
    question_5: QuestionAnalysisAnswerPydantic
    question_6: QuestionAnalysisAnswerPydantic
    question_7: QuestionAnalysisAnswerPydantic
    question_8: QuestionAnalysisAnswerPydantic
    question_9: QuestionAnalysisAnswerPydantic
    question_10: QuestionAnalysisAnswerPydantic
    question_11: QuestionAnalysisAnswerPydantic
    #question_11: Dict[str, QuestionAnalysisAnswerPydantic]

class Task81Pydantic(BaseModel):
    yc_response: QuestionPydantic

class FeedbackProblemSuggestionExamplePydantic(BaseModel):
    problem: str
    suggestion: str
    example: str

class Task82Pydantic(BaseModel):
    vc_feedback:  Dict[str, FeedbackProblemSuggestionExamplePydantic]

class Task83Pydantic(BaseModel):
    yc_response: QuestionPydantic

class Task84Pydantic(BaseModel):
    yc_response: QuestionPydantic

class SlidesPydantic(BaseModel):
    contents: str

class Task91Pydantic(BaseModel):
    pitch_deck : Dict[str,SlidesPydantic]

class Task92Pydantic(BaseModel):
    pitch_deck_planning: str
    pitch_deck: Dict[str,SlidesPydantic]

class SlidesPlanningPydantic(BaseModel):
    slide_planning: str
    content: str
    presenter_notes: str

class Task93Pydantic(BaseModel):
    slides: Dict[str,SlidesPlanningPydantic]

class Task94Pydantic(BaseModel):
    pitch_deck: Dict[str,SlidesPydantic]

class SlidesPydanticRiskSummation(BaseModel):
    slide_preparation: str 
    content: str

class Slides(BaseModel):
    Slide_1: SlidesPydanticRiskSummation
    Slide_2: SlidesPydanticRiskSummation
    Slide_3: SlidesPydanticRiskSummation
    Slide_4: SlidesPydanticRiskSummation
    Slide_5: SlidesPydanticRiskSummation
    Slide_6: SlidesPydanticRiskSummation
    Slide_7: SlidesPydanticRiskSummation
    Slide_8: SlidesPydanticRiskSummation
    Slide_9: SlidesPydanticRiskSummation
    Slide_10: SlidesPydanticRiskSummation
    Slide_11: SlidesPydanticRiskSummation
    
class Task95Pydantic(BaseModel):
    pitch_deck: Slides

class SlidesPlanningPydanticYCDeck(BaseModel):
    slide_planning: str
    content: str

class SlidesYC(BaseModel):
    Slide_1: SlidesPlanningPydanticYCDeck
    Slide_2: SlidesPlanningPydanticYCDeck
    Slide_3: SlidesPlanningPydanticYCDeck
    Slide_4: SlidesPlanningPydanticYCDeck
    Slide_5: SlidesPlanningPydanticYCDeck
    Slide_6: SlidesPlanningPydanticYCDeck
    Slide_7: SlidesPlanningPydanticYCDeck
    Slide_8: SlidesPlanningPydanticYCDeck
    Slide_9: SlidesPlanningPydanticYCDeck
    Slide_10: SlidesPlanningPydanticYCDeck

class Task96Pydantic(BaseModel):
    pitch_deck: SlidesYC
    