import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

BANK_ID = "incident-memory"

if not HINDSIGHT_API_KEY:
    raise RuntimeError("HINDSIGHT_API_KEY is missing from .env")

hindsight = Hindsight(
    base_url=HINDSIGHT_BASE_URL,
    api_key=HINDSIGHT_API_KEY,
)


def learn_from_incident(
    incident_id,
    service,
    root_cause,
    resolution,
    outcome,
    resolution_time,
):
    experience = f"""
Production Incident Experience

Incident ID: {incident_id}
Service: {service}

Root Cause:
{root_cause}

Resolution:
{resolution}

Outcome:
{outcome}

Resolution Time:
{resolution_time}

This incident should be remembered as operational experience
for diagnosing similar incidents in the future.
"""

    print("\n========================================")
    print("LEARNING FROM INCIDENT")
    print("========================================")

    print(experience)

    hindsight.retain(
        bank_id=BANK_ID,
        content=experience,
    )

    print("Incident experience stored in Hindsight.")
    print("========================================")


if __name__ == "__main__":

    learn_from_incident(
        incident_id="INC-002",
        service="payment-api",
        root_cause="Expired payment provider API credential",
        resolution="Rotated the API credential and restarted the payment worker",
        outcome="Payment requests returned to normal and the incident was resolved",
        resolution_time="3 minutes",
    )

    hindsight.close()