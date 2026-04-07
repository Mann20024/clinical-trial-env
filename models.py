from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ClinicalTrialAction(BaseModel):
    """What the agent sends — a finding about the protocol"""
    action_type: str  # "flag_issue", "submit_review", "request_section"
    issue_category: str  # "missing_section", "dosing_error", "contradiction", "none"
    issue_description: str  # Agent's explanation of what it found
    section_name: Optional[str] = None  # Which section has the issue
    confidence: float = 1.0  # How confident agent is (0.0 to 1.0)


class ClinicalTrialObservation(BaseModel):
    """What the agent sees — the protocol content"""
    protocol_text: str  # The full protocol text to review
    task_name: str  # Which task: easy, medium, hard
    step_number: int  # Current step
    max_steps: int  # Maximum allowed steps
    issues_found_so_far: List[str]  # Issues agent already flagged
    feedback: str  # Feedback on last action
    done: bool = False
    reward: float = 0.0


class ClinicalTrialState(BaseModel):
    """Internal state of the environment"""
    task_name: str
    current_step: int
    max_steps: int
    protocol_id: str
    total_issues_in_protocol: int
    issues_found: List[str]
    score: float
    episode_done: bool


class StepResult(BaseModel):
    """What step() returns"""
    observation: ClinicalTrialObservation
    reward: float
    done: bool
    info: Dict[str, Any] = {}