---
title: Clinical Trial Protocol Review Environment
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
tags:
  - openenv
  - reinforcement-learning
  - clinical-trial
  - rl-environment
---

# Clinical Trial Protocol Review Environment

An RL environment where AI agents review clinical trial protocols for safety violations, missing sections, and contradictions.

## What it does

Simulates the real-world task of reviewing clinical trial protocols — documents that pharmaceutical companies must submit before testing drugs on humans. The agent must find errors, missing sections, and contradictions in these protocols.

## Action Space

The agent sends a `ClinicalTrialAction` with these fields:
- `action_type` — "flag_issue" or "submit_review"
- `issue_category` — "missing_section", "contradiction", "dosing_error", "none"
- `issue_description` — text description of the issue found
- `section_name` — which section has the issue
- `confidence` — float 0.0 to 1.0

## Observation Space

The agent receives a `ClinicalTrialObservation` with:
- `protocol_text` — full protocol to review
- `task_name` — which task is running
- `step_number` — current step
- `issues_found_so_far` — list of issues already found
- `feedback` — feedback on last action
- `reward` — reward received

## Tasks

| Task | Difficulty | Description |
|------|-----------|-------------|
| missing_sections | Easy | Find obviously missing required sections |
| inclusion_exclusion_check | Medium | Detect age and dosing contradictions |
| hidden_contradiction | Hard | Find subtle contradictions across sections |

## Setup
```bash
pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 8000
```

## Baseline Scores

- Task 1 (easy): 0.33
- Task 2 (medium): 1.00
- Task 3 (hard): 1.00
- Average: 0.78

## API Endpoints

- `GET /health` — health check
- `POST /reset?task_name=missing_sections` — start new episode
- `POST /step` — send action, get observation
- `GET /state` — get current state
- `GET /tasks` — list all tasks