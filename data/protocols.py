PROTOCOLS = {

    "easy_protocol": {
        "id": "PROT-001",
        "task": "missing_sections",
        "text": """
CLINICAL TRIAL PROTOCOL — PROT-001
Drug: Cardivex 10mg
Sponsor: MedCorp Pharmaceuticals

1. STUDY OBJECTIVES
   To evaluate the safety and efficacy of Cardivex 10mg in adult patients
   with mild to moderate hypertension over a 12-week period.

2. STUDY DESIGN
   Randomized, double-blind, placebo-controlled trial.
   Total duration: 12 weeks.
   Number of patients: 200 (100 active, 100 placebo).

3. PATIENT POPULATION
   Inclusion Criteria:
   - Age 30 to 65 years
   - Diagnosed with mild to moderate hypertension
   - Able to provide informed consent

4. DOSING SCHEDULE
   Cardivex 10mg once daily, taken orally with water.
   Duration: 12 weeks continuous.
""",
        "required_sections": [
            "STUDY OBJECTIVES",
            "STUDY DESIGN",
            "PATIENT POPULATION",
            "DOSING SCHEDULE",
            "SAFETY MONITORING",
            "ADVERSE EVENT REPORTING",
            "STOPPING RULES"
        ],
        "missing_sections": [
            "SAFETY MONITORING",
            "ADVERSE EVENT REPORTING",
            "STOPPING RULES"
        ],
        "answers": [
            "SAFETY MONITORING",
            "ADVERSE EVENT REPORTING",
            "STOPPING RULES"
        ]
    },

    "medium_protocol": {
        "id": "PROT-002",
        "task": "inclusion_exclusion_check",
        "text": """
CLINICAL TRIAL PROTOCOL — PROT-002
Drug: Neurofen-X 50mg
Sponsor: BrainHealth Labs

1. STUDY OBJECTIVES
   To assess Neurofen-X 50mg for treatment of chronic migraine in adults.

2. INCLUSION CRITERIA
   - Age 18 to 45 years
   - Diagnosed with chronic migraine (15+ headache days per month)
   - No prior use of similar medications in last 6 months

3. EXCLUSION CRITERIA
   - Patients under 16 years of age
   - Pregnant or breastfeeding women
   - Patients with severe kidney disease

4. DOSING SCHEDULE
   Adults (18-45): Neurofen-X 50mg twice daily
   Elderly patients (65+): Neurofen-X 25mg once daily
   Pediatric patients (12-17): Neurofen-X 10mg once daily

5. SAFETY MONITORING
   Monthly blood tests required for all patients.
   Immediate reporting of any neurological side effects.

6. ADVERSE EVENT REPORTING
   All adverse events must be reported within 24 hours to the sponsor.

7. STOPPING RULES
   Trial stops if more than 5% of patients report severe adverse events.
""",
        "contradictions": [
            "Inclusion criteria says age 18-45 but dosing schedule includes pediatric patients 12-17 who are excluded",
            "Exclusion criteria says under 16 but dosing has pediatric schedule for 12-17 year olds",
            "Elderly dosing schedule exists for 65+ patients but inclusion criteria only allows up to age 45"
        ],
        "answers": [
            "pediatric",
            "elderly",
            "age contradiction",
            "12-17",
            "65+",
            "inclusion age",
            "exclusion age"
        ]
    },

    "hard_protocol": {
        "id": "PROT-003",
        "task": "hidden_contradiction",
        "text": """
CLINICAL TRIAL PROTOCOL — PROT-003
Drug: Renalyx 100mg
Sponsor: KidneyCare Therapeutics

1. STUDY OBJECTIVES
   To evaluate Renalyx 100mg for treatment of early-stage chronic kidney
   disease (CKD) in adult patients aged 40 to 70 years.

2. STUDY DESIGN
   Open-label, single-arm trial over 24 weeks.
   Target enrollment: 150 patients.

3. INCLUSION CRITERIA
   - Age 40 to 70 years
   - Diagnosed with early-stage CKD (eGFR 45-89 mL/min)
   - Stable kidney function for at least 3 months
   - No current use of nephrotoxic medications

4. EXCLUSION CRITERIA
   - Patients with eGFR below 60 mL/min at screening
   - History of kidney transplant
   - Current use of ACE inhibitors or ARBs
   - Patients with diabetes mellitus type 1 or type 2
   - Serum potassium above 5.0 mEq/L

5. DOSING SCHEDULE
   Week 1-4:   Renalyx 100mg once daily
   Week 5-12:  Renalyx 100mg twice daily (dose escalation)
   Week 13-24: Renalyx 150mg twice daily (maximum dose)

   Note: For patients with eGFR 45-59 mL/min, reduce dose by 50%.

6. SAFETY MONITORING
   eGFR testing every 4 weeks.
   Serum potassium testing every 2 weeks.
   Blood pressure monitoring at every visit.

7. ADVERSE EVENT REPORTING
   All serious adverse events reported within 24 hours.
   Known side effect: Renalyx can elevate serum potassium by 0.5-1.5 mEq/L.

8. STOPPING RULES
   Individual patient stopping: eGFR drops more than 25% from baseline.
   Trial stopping: More than 10% of patients meet individual stopping criteria.
""",
        "hidden_contradictions": [
            "Inclusion allows eGFR 45-89 but exclusion blocks eGFR below 60 — valid range is only 60-89 not 45-89",
            "Dosing note says reduce dose for eGFR 45-59 patients but exclusion criteria blocks these patients entirely",
            "Exclusion blocks patients with potassium above 5.0 but drug raises potassium by 0.5-1.5 pushing borderline patients above 5.0",
            "Exclusion blocks diabetic patients but CKD patients commonly have diabetes making enrollment very difficult"
        ],
        "answers": [
            "egfr",
            "eGFR",
            "potassium",
            "45-59",
            "dose reduction",
            "excluded",
            "contradiction",
            "serum potassium",
            "diabetes",
            "diabetic"
        ]
    }
}


def get_protocol(task_name: str) -> dict:
    mapping = {
        "missing_sections": "easy_protocol",
        "inclusion_exclusion_check": "medium_protocol",
        "hidden_contradiction": "hard_protocol"
    }
    return PROTOCOLS[mapping[task_name]]
