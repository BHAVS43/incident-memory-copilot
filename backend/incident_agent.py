import os
import sys
from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

load_dotenv()

# =========================
# Configuration
# =========================

HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BANK_ID = "incident-memory"

if not HINDSIGHT_API_KEY:
    raise RuntimeError("HINDSIGHT_API_KEY is missing from .env")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing from .env")


# =========================
# Connect to Hindsight + Groq
# =========================

hindsight = Hindsight(
    base_url=HINDSIGHT_BASE_URL,
    api_key=HINDSIGHT_API_KEY,
)

groq = Groq(api_key=GROQ_API_KEY)


# =========================
# Analyze an incident
# =========================

def analyze_incident(current_incident):

    print("\n========================================")
    print("INCIDENT MEMORY COPILOT")
    print("========================================")

    print("\nCurrent incident:")
    print(current_incident)

    # -------------------------
    # Recall previous experience
    # -------------------------

    print("\nSearching Hindsight memory...")

    result = hindsight.recall(
        bank_id=BANK_ID,
        query=current_incident,
    )

    memories = result.results

    print(f"\nFound {len(memories)} relevant memories.")

    memory_text = ""

    for i, memory in enumerate(memories, 1):
        print(f"\nMemory {i}:")
        print(memory.text)

        memory_text += f"\n- {memory.text}"

    # -------------------------
    # Ask Groq to reason
    # -------------------------

    prompt = f"""
You are an experienced production incident response engineer.

A new production incident has occurred.

CURRENT INCIDENT:
{current_incident}

RELEVANT EXPERIENCE FROM PREVIOUS INCIDENTS:
{memory_text}

Analyze the current incident using the previous experience.

Provide:

1. Likely root cause
2. Evidence from previous incidents
3. Recommended investigation steps
4. Recommended resolution
5. Risk or caveats

Important:
- Do not claim certainty if the evidence is insufficient.
- Clearly distinguish previous evidence from your current inference.
- Do not execute any production changes.
- A human engineer will make the final decision.
"""

    print("\n========================================")
    print("AI ANALYSIS")
    print("========================================")

    response = groq.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful production incident "
                    "response copilot."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    analysis = response.choices[0].message.content

    print(analysis)

    print("\n========================================")
    print("ANALYSIS COMPLETE")
    print("========================================")

    return analysis


# =========================
# Command-line test
# =========================

if __name__ == "__main__":

    current_incident = """
Incident INC-003:

Service: payment-api

Symptom:
The payment API is returning HTTP 401 Unauthorized errors
for customer payment requests.

Error rate:
65% of payment requests are failing.

Started:
8 minutes ago.

Recent deployment:
No deployment in the last 3 hours.
"""

    analyze_incident(current_incident)

    hindsight.close()