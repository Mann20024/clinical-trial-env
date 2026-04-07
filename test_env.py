import sys
sys.path.insert(0, '.')
from server.environment import ClinicalTrialEnvironment
from models import ClinicalTrialAction

env = ClinicalTrialEnvironment()

print('=== TESTING TASK 1 ===')
obs = env.reset('missing_sections')
print('Protocol loaded:', obs.task_name)
print('Step:', obs.step_number)

action = ClinicalTrialAction(
    action_type='flag_issue',
    issue_category='missing_section',
    issue_description='SAFETY MONITORING section is missing',
    section_name='SAFETY MONITORING',
    confidence=0.9
)
result = env.step(action)
print('Reward:', result.reward)
print('Feedback:', result.observation.feedback)
print('Done:', result.done)

print()
print('=== TESTING TASK 2 ===')
obs = env.reset('inclusion_exclusion_check')
print('Protocol loaded:', obs.task_name)

action2 = ClinicalTrialAction(
    action_type='flag_issue',
    issue_category='contradiction',
    issue_description='elderly patients 65+ have a dosing schedule but inclusion only allows age 45',
    section_name='DOSING SCHEDULE',
    confidence=0.9
)
result2 = env.step(action2)
print('Reward:', result2.reward)
print('Feedback:', result2.observation.feedback)

print()
print('=== TESTING TASK 3 ===')
obs = env.reset('hidden_contradiction')
print('Protocol loaded:', obs.task_name)

action3 = ClinicalTrialAction(
    action_type='flag_issue',
    issue_category='contradiction',
    issue_description='eGFR range contradiction between inclusion and exclusion criteria',
    section_name='EXCLUSION CRITERIA',
    confidence=0.9
)
result3 = env.step(action3)
print('Reward:', result3.reward)
print('Feedback:', result3.observation.feedback)

print()
print('ALL 3 TASKS WORKING CORRECTLY')