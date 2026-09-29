import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

BASE_URL = os.getenv("HINDSIGHT_BASE_URL")
API_KEY = os.getenv("HINDSIGHT_API_KEY")

if not API_KEY:
    raise RuntimeError("HINDSIGHT_API_KEY is missing from .env")

print("Connecting to Hindsight...")

client = Hindsight(
    base_url=BASE_URL,
    api_key=API_KEY,
)

BANK_ID = "incident-memory"

print("Creating memory bank...")

client.create_bank(
    bank_id=BANK_ID,
    name="Incident Memory Copilot",
)

print("Memory bank ready!")

incident = """
Incident INC-001:
Service: payment-api
Symptom: The payment API returned HTTP 401 Unauthorized errors.
Root cause: The payment provider API credential had expired.
Resolution: The engineer rotated the API credential and restarted
the payment worker.
Outcome: The incident was resolved in 4 minutes.
"""

print("Storing incident in Hindsight...")

client.retain(
    bank_id=BANK_ID,
    content=incident,
)

print("Incident stored!")

query = "Have we seen a payment API 401 authentication incident before?"

print("\nSearching Hindsight memory...")
print("Query:", query)

result = client.recall(
    bank_id=BANK_ID,
    query=query,
)

print("\n========== HINDSIGHT RESULTS ==========")

if not result.results:
    print("No memories found.")
else:
    for i, memory in enumerate(result.results, 1):
        print(f"\nMemory {i}:")
        print(memory.text)

print("\n========================================")

client.close()

print("\nSUCCESS: Hindsight test completed.")