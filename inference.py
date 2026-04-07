import os
import sys
from openai import OpenAI
from client import ClinicalTrialEnvClient
from models import ClinicalTrialAction

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN", "")

TASKS = [
    "missing_sections",
    "inclusion_exclusion_check",
    "hidden_contradiction"
]

SYSTEM_PROMPT = """You are a clinical trial protocol reviewer. 
You review medical protocols and identify issues such as:
- Missing required sections
- Contradictions between inclusion/exclusion criteria and dosing
- Hidden contradictions across different sections

When you find an issue, respond in this exact format:
ACTION: flag_issue
CATEGORY: missing_section OR contradiction OR dosing_error
SECTION: <section name where issue is>
DESCRIPTION: <clear description of the issue you found>
CONFIDENCE: <0.1 to 1.0>

If you want to finish your review, respond with:
ACTION: submit_review
CATEGORY: none
SECTION: none
DESCRIPTION: Review complete
CONFIDENCE: 1.0"""


def parse_llm_response(text: str) -> ClinicalTrialAction:
    """Parse LLM response into a ClinicalTrialAction"""
    lines = text.strip().split("\n")
    data = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip().upper()] = value.strip()

    return ClinicalTrialAction(
        action_type=data.get("ACTION", "flag_issue").lower(),
        issue_category=data.get("CATEGORY", "none").lower(),
        section_name=data.get("SECTION", ""),
        issue_description=data.get("DESCRIPTION", text[:200]),
        confidence=float(data.get("CONFIDENCE", "0.5"))
    )


def run_task(client: ClinicalTrialEnvClient, openai_client: OpenAI, task_name: str):
    """Run one full episode for a task"""

    obs = client.reset(task_name)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    step = 0
    rewards = []
    done = False
    last_error = None

    print(f"[START] task={task_name} env=clinical-trial-env model={MODEL_NAME}")

    while not done and step < 10:
        # Build user message
        user_content = f"""Please review this clinical trial protocol:

{obs.protocol_text}

Task: {obs.task_name}
Step: {obs.step_number}/{obs.max_steps}
Issues found so far: {obs.issues_found_so_far}
Last feedback: {obs.feedback}

Find the next issue in this protocol."""

        messages.append({"role": "user", "content": user_content})

        # Call LLM
        try:
            response = openai_client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=300,
                temperature=0.1
            )
            llm_text = response.choices[0].message.content
            messages.append({"role": "assistant", "content": llm_text})

        except Exception as e:
            last_error = str(e)
            llm_text = "ACTION: submit_review\nCATEGORY: none\nSECTION: none\nDESCRIPTION: Error occurred\nCONFIDENCE: 0.5"

        # Parse response into action
        action = parse_llm_response(llm_text)

        # Send action to environment
        result = client.step(action)
        step += 1
        rewards.append(result.reward)
        done = result.done
        obs = result.observation
        last_error = None

        action_str = f"{action.action_type}({action.issue_category},{action.section_name[:20] if action.section_name else 'none'})"
        error_str = last_error if last_error else "null"

        print(f"[STEP] step={step} action={action_str} reward={result.reward:.2f} done={str(done).lower()} error={error_str}")

        # If submit review stop
        if action.action_type == "submit_review":
            done = True

    # Calculate final score
    score = round(sum(rewards), 2)
    score = min(1.0, score)
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    success = score > 0.0

    print(f"[END] success={str(success).lower()} steps={step} score={score:.2f} rewards={rewards_str}")

    return score


def main():
    # Initialize clients
    openai_client = OpenAI(
        api_key=HF_TOKEN,
        base_url=API_BASE_URL
    )

    env_url = os.getenv("ENV_URL", "http://localhost:8000")
    client = ClinicalTrialEnvClient(base_url=env_url)

    # Check server health
    health = client.health()
    if health.get("status") != "healthy":
        print("ERROR: Environment server is not healthy")
        sys.exit(1)

    # Run all 3 tasks
    total_score = 0.0
    for task in TASKS:
        score = run_task(client, openai_client, task)
        total_score += score

    average_score = round(total_score / len(TASKS), 2)
    print(f"\nFINAL AVERAGE SCORE: {average_score}")


if __name__ == "__main__":
    main()