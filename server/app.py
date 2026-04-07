import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import ClinicalTrialAction
from server.environment import ClinicalTrialEnvironment
import uvicorn

app = FastAPI(
    title="Clinical Trial Protocol Review Environment",
    description="An RL environment where AI agents review clinical trial protocols",
    version="1.0.0"
)

env = ClinicalTrialEnvironment()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/reset")
def reset(task_name: str = "missing_sections"):
    obs = env.reset(task_name)
    return obs.model_dump()


@app.post("/step")
def step(action: ClinicalTrialAction):
    result = env.step(action)
    return {
        "observation": result.observation.model_dump(),
        "reward": result.reward,
        "done": result.done,
        "info": result.info
    }


@app.get("/state")
def state():
    return env.state().model_dump()


@app.get("/tasks")
def tasks():
    return {
        "tasks": [
            {
                "name": "missing_sections",
                "difficulty": "easy",
                "description": "Find obviously missing required sections in the protocol"
            },
            {
                "name": "inclusion_exclusion_check",
                "difficulty": "medium",
                "description": "Detect age and dosing contradictions in patient criteria"
            },
            {
                "name": "hidden_contradiction",
                "difficulty": "hard",
                "description": "Find subtle contradictions between dosing and exclusion criteria"
            }
        ]
    }


def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
    