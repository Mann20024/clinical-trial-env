import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import (
    ClinicalTrialAction,
    ClinicalTrialObservation,
    ClinicalTrialState,
    StepResult
)
from data.protocols import get_protocol


class ClinicalTrialEnvironment:

    def __init__(self):
        self.current_task = None
        self.current_protocol = None
        self.current_step = 0
        self.max_steps = 10
        self.issues_found = []
        self.score = 0.0
        self.done = False

    def reset(self, task_name: str = "missing_sections") -> ClinicalTrialObservation:
        """Start a fresh episode for a given task"""
        self.current_task = task_name
        self.current_protocol = get_protocol(task_name)
        self.current_step = 0
        self.issues_found = []
        self.score = 0.0
        self.done = False

        return ClinicalTrialObservation(
            protocol_text=self.current_protocol["text"],
            task_name=task_name,
            step_number=0,
            max_steps=self.max_steps,
            issues_found_so_far=[],
            feedback="New protocol loaded. Please review and flag any issues.",
            done=False,
            reward=0.0
        )

    def step(self, action: ClinicalTrialAction) -> StepResult:
        """Process agent action and return reward"""

        if self.done:
            obs = self._make_observation("Episode already finished.", 0.0)
            return StepResult(observation=obs, reward=0.0, done=True, info={})

        self.current_step += 1
        reward = 0.0
        feedback = ""

        # Run grader based on task
        if self.current_task == "missing_sections":
            reward, feedback = self._grade_missing_sections(action)

        elif self.current_task == "inclusion_exclusion_check":
            reward, feedback = self._grade_inclusion_exclusion(action)

        elif self.current_task == "hidden_contradiction":
            reward, feedback = self._grade_hidden_contradiction(action)

        # Track found issues
        if reward > 0 and action.issue_description not in self.issues_found:
            self.issues_found.append(action.issue_description)

        # Update score
        self.score = min(1.0, self.score + reward)

        # Check if done
        if self.current_step >= self.max_steps:
            self.done = True
            feedback += " Maximum steps reached."

        if action.action_type == "submit_review":
            self.done = True
            feedback += " Review submitted."

        obs = self._make_observation(feedback, reward)
        return StepResult(
            observation=obs,
            reward=round(reward, 2),
            done=self.done,
            info={"score": round(self.score, 2), "step": self.current_step}
        )

    def _grade_missing_sections(self, action: ClinicalTrialAction):
        """Grader for Task 1 — easy"""
        answers = self.current_protocol["answers"]
        description = action.issue_description.upper()

        for answer in answers:
            if answer.upper() in description:
                if answer not in self.issues_found:
                    total = len(answers)
                    reward = round(1.0 / total, 2)
                    return reward, f"Correct! '{answer}' is indeed missing. +{reward} reward."

        if action.issue_category == "none":
            return 0.0, "No issue flagged. Keep reviewing the protocol."

        return 0.0, "That issue is not correct for this protocol. Try again."

    def _grade_inclusion_exclusion(self, action: ClinicalTrialAction):
        """Grader for Task 2 — medium"""
        answers = self.current_protocol["answers"]
        description = action.issue_description.lower()

        for answer in answers:
            if answer.lower() in description:
                if answer not in self.issues_found:
                    reward = 0.33
                    return reward, f"Correct! You found a contradiction involving '{answer}'. +{reward} reward."

        if action.issue_category == "none":
            return 0.0, "No issue flagged. Look carefully at age ranges and dosing."

        return 0.0, "Not quite. Look carefully at the age ranges in inclusion, exclusion and dosing."

    def _grade_hidden_contradiction(self, action: ClinicalTrialAction):
        """Grader for Task 3 — hard"""
        answers = self.current_protocol["answers"]
        description = action.issue_description.lower()

        for answer in answers:
            if answer.lower() in description:
                if answer not in self.issues_found:
                    reward = 0.25
                    return reward, f"Excellent! You found a hidden contradiction involving '{answer}'. +{reward} reward."

        if action.issue_category == "none":
            return 0.0, "No issue flagged. Look for contradictions between sections."

        return 0.0, "Not correct. Look carefully at eGFR ranges, potassium levels, and exclusion criteria."

    def _make_observation(self, feedback: str, reward: float) -> ClinicalTrialObservation:
        return ClinicalTrialObservation(
            protocol_text=self.current_protocol["text"],
            task_name=self.current_task,
            step_number=self.current_step,
            max_steps=self.max_steps,
            issues_found_so_far=self.issues_found.copy(),
            feedback=feedback,
            done=self.done,
            reward=reward
        )

    def state(self) -> ClinicalTrialState:
        return ClinicalTrialState(
            task_name=self.current_task or "none",
            current_step=self.current_step,
            max_steps=self.max_steps,
            protocol_id=self.current_protocol["id"] if self.current_protocol else "none",
            total_issues_in_protocol=len(self.current_protocol["answers"]) if self.current_protocol else 0,
            issues_found=self.issues_found.copy(),
            score=round(self.score, 2),
            episode_done=self.done
        )
    