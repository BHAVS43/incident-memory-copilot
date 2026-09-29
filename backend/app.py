import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from hindsight_client import Hindsight


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BANK_ID = "incident-memory"


if not HINDSIGHT_API_KEY:
    raise RuntimeError("HINDSIGHT_API_KEY is missing from .env")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing from .env")


# ============================================================
# CLIENTS
# ============================================================

hindsight = Hindsight(
    base_url=HINDSIGHT_BASE_URL,
    api_key=HINDSIGHT_API_KEY
)

groq = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Incident Memory Copilot",
    description=(
        "Organization-level incident response copilot "
        "powered by Hindsight memory."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class IncidentRequest(BaseModel):
    incident_id: str
    service: str
    symptom: str
    error_rate: str
    started: str
    recent_deployment: str


class LearnRequest(BaseModel):
    incident_id: str
    service: str
    root_cause: str
    resolution: str
    outcome: str
    resolution_time: str


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Incident Memory Copilot",
        "memory_system": "Hindsight",
        "mode": "organization-level incident learning"
    }


# ============================================================
# ANALYZE INCIDENT
# ============================================================

@app.post("/analyze")
def analyze_incident(request: IncidentRequest):

    current_incident = f"""
Incident ID:
{request.incident_id}

Service:
{request.service}

Current Symptoms:
{request.symptom}

Error Rate:
{request.error_rate}

Started:
{request.started}

Recent Deployment:
{request.recent_deployment}
"""

    try:

        # ====================================================
        # STEP 1: RECALL ORGANIZATIONAL EXPERIENCE
        # ====================================================

        result = hindsight.recall(
            bank_id=BANK_ID,
            query=current_incident
        )

        memories = result.results

        memory_list = [
            memory.text
            for memory in memories
        ]

        memory_text = "\n".join(
            f"[MEMORY {i + 1}]\n{memory}"
            for i, memory in enumerate(memory_list)
        )


        # ====================================================
        # STEP 2: ASK AI TO SYNTHESIZE EXPERIENCE
        # ====================================================

        prompt = f"""
You are an experienced production incident response engineer
working for a large engineering organization.

Your organization has an institutional memory of previous
production incidents.

A NEW INCIDENT has just occurred.

============================================================
CURRENT INCIDENT
============================================================

{current_incident}


============================================================
ORGANIZATIONAL INCIDENT MEMORY
============================================================

{memory_text}


============================================================
YOUR TASK
============================================================

Use the historical incidents as organizational evidence.

Do NOT simply find one similar incident and copy its solution.

Instead:

1. Identify recurring patterns across the historical incidents.

2. Identify different possible causes that could produce the
   current symptoms.

3. Compare the current incident against those historical patterns.

4. Determine which hypothesis is best supported by the
   available evidence.

5. Construct a practical resolution playbook for the engineer.

6. Explain why each recommended step is being suggested.

7. Identify what should be verified before declaring the
   incident resolved.

8. Identify important alternative explanations and risks.

The goal is to preserve organizational knowledge so that a
developer encountering this incident for the first time can
benefit from what the entire engineering organization has
learned from previous incidents.


============================================================
REQUIRED RESPONSE FORMAT
============================================================

INCIDENT ASSESSMENT

Explain what appears to be happening.


ORGANIZATIONAL PATTERNS

Identify recurring patterns found across previous incidents.

Mention the relevant historical experience.


MOST LIKELY ROOT CAUSE

Give the strongest current hypothesis.

Clearly distinguish inference from historical fact.


HISTORICAL EVIDENCE

Explain which previous incidents support the hypothesis.

Do not invent incidents.


RESOLUTION PLAYBOOK

Provide a numbered sequence:

1. First investigation step
2. Second investigation step
3. Third investigation step
4. Resolution action
5. Verification step
6. Monitoring / follow-up step

For every important step, briefly explain why it is recommended.


ALTERNATIVE CAUSES

List other plausible causes and how the engineer can
distinguish them.


RISKS AND CAVEATS

Explain when the recommended resolution should NOT be used.


ORGANIZATIONAL LEARNING

Explain what this incident would teach the organization
if it is later resolved and recorded.


============================================================
IMPORTANT SAFETY RULES
============================================================

- Do not claim certainty without evidence.
- Do not invent historical incidents.
- Do not invent statistics.
- Do not invent runbooks.
- Do not claim a fix was successful unless the historical
  evidence says so.
- Do not execute production changes.
- The human engineer makes the final production decision.
"""


        # ====================================================
        # STEP 3: GROQ SYNTHESIS
        # ====================================================

        response = groq.chat.completions.create(
            model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful production incident "
                        "response copilot. Your job is to "
                        "synthesize organizational incident "
                        "experience into evidence-backed "
                        "resolution guidance."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
        )


        analysis = response.choices[0].message.content


        # ====================================================
        # STEP 4: RETURN ORGANIZATIONAL INTELLIGENCE
        # ====================================================

        return {

            "incident": {
                "id": request.incident_id,
                "service": request.service,
                "symptom": request.symptom,
                "error_rate": request.error_rate,
                "started": request.started,
                "recent_deployment": request.recent_deployment,
            },

            "memory_count": len(memory_list),

            "memories": memory_list,

            "analysis": analysis,

            "organization_memory": {
                "memory_system": "Hindsight",
                "purpose": (
                    "Use accumulated incident experience "
                    "to improve future incident response."
                ),
            }
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# AUTOMATIC INCIDENT LEARNING
# ============================================================

@app.post("/learn")
def learn_incident(request: LearnRequest):

    experience = f"""
Production Incident Experience

Incident ID:
{request.incident_id}

Service:
{request.service}

Root Cause:
{request.root_cause}

Resolution:
{request.resolution}

Outcome:
{request.outcome}

Resolution Time:
{request.resolution_time}

This incident represents organizational operational
experience.

Future incident-response agents should use this experience
when diagnosing similar incidents.
"""

    try:

        hindsight.retain(
            bank_id=BANK_ID,
            content=experience
        )

        return {
            "status": "learned",
            "incident_id": request.incident_id,
            "service": request.service,
            "message": (
                "Incident experience automatically added "
                "to organizational memory."
            )
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )