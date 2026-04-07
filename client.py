import requests
from models import ClinicalTrialAction, ClinicalTrialObservation, ClinicalTrialState, StepResult


class ClinicalTrialEnvClient:
    """HTTP client to talk to the environment server"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")

    def health(self) -> dict:
        response = requests.get(f"{self.base_url}/health")
        return response.json()

    def reset(self, task_name: str = "missing_sections") -> ClinicalTrialObservation:
        response = requests.post(
            f"{self.base_url}/reset",
            params={"task_name": task_name}
        )
        return ClinicalTrialObservation(**response.json())

    def step(self, action: ClinicalTrialAction) -> StepResult:
        response = requests.post(
            f"{self.base_url}/step",
            json=action.model_dump()
        )
        data = response.json()
        return StepResult(
            observation=ClinicalTrialObservation(**data["observation"]),
            reward=data["reward"],
            done=data["done"],
            info=data["info"]
        )

    def state(self) -> ClinicalTrialState:
        response = requests.get(f"{self.base_url}/state")
        return ClinicalTrialState(**response.json())

    def tasks(self) -> dict:
        response = requests.get(f"{self.base_url}/tasks")
        return response.json()