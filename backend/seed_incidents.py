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
    api_key=HINDSIGHT_API_KEY
)


INCIDENTS = [

    # ========================================================
    # PAYMENT API
    # ========================================================

    {
        "id": "HIST-001",
        "service": "payment-api",
        "symptom": "65% of payment requests returned HTTP 401 Unauthorized.",
        "root_cause": "Expired payment provider API credential.",
        "resolution": "Rotated the payment provider credential and restarted the payment worker.",
        "outcome": "Payment requests returned to normal.",
        "time": "4 minutes",
    },

    {
        "id": "HIST-002",
        "service": "payment-api",
        "symptom": "Payment requests returned HTTP 401 after several hours of normal operation.",
        "root_cause": "Payment provider API credential expired.",
        "resolution": "Rotated the credential and restarted the payment worker.",
        "outcome": "Payment processing recovered.",
        "time": "3 minutes",
    },

    {
        "id": "HIST-003",
        "service": "payment-api",
        "symptom": "Payment requests returned HTTP 401 immediately after a deployment.",
        "root_cause": "Malformed authentication header introduced by a configuration change.",
        "resolution": "Rolled back the configuration change and redeployed the previous version.",
        "outcome": "Payment authentication recovered.",
        "time": "8 minutes",
    },

    {
        "id": "HIST-004",
        "service": "payment-api",
        "symptom": "Payment provider requests returned HTTP 503 errors.",
        "root_cause": "External payment provider outage.",
        "resolution": "Enabled the payment retry queue and waited for provider recovery.",
        "outcome": "Queued payments were processed after the provider recovered.",
        "time": "22 minutes",
    },


    # ========================================================
    # AUTH SERVICE
    # ========================================================

    {
        "id": "HIST-005",
        "service": "auth-service",
        "symptom": "Users were unable to authenticate and received token validation errors.",
        "root_cause": "OAuth signing certificate expired.",
        "resolution": "Renewed the certificate and restarted the authentication service.",
        "outcome": "Token validation returned to normal.",
        "time": "11 minutes",
    },

    {
        "id": "HIST-006",
        "service": "auth-service",
        "symptom": "Authentication latency increased from 100ms to over 4 seconds.",
        "root_cause": "Database connection pool exhaustion.",
        "resolution": "Reduced connection leakage and restarted affected service instances.",
        "outcome": "Authentication latency returned to normal.",
        "time": "14 minutes",
    },

    {
        "id": "HIST-007",
        "service": "auth-service",
        "symptom": "Users received intermittent HTTP 401 responses.",
        "root_cause": "Expired OAuth signing key.",
        "resolution": "Rotated the signing key and restarted authentication workers.",
        "outcome": "Authentication recovered.",
        "time": "9 minutes",
    },


    # ========================================================
    # ORDER SERVICE
    # ========================================================

    {
        "id": "HIST-008",
        "service": "order-service",
        "symptom": "Order creation requests returned HTTP 500 errors.",
        "root_cause": "Database schema was missing a column expected by the new application version.",
        "resolution": "Applied the missing database migration.",
        "outcome": "Order creation recovered without rollback.",
        "time": "12 minutes",
    },

    {
        "id": "HIST-009",
        "service": "order-service",
        "symptom": "Order creation latency increased significantly.",
        "root_cause": "Slow database query caused by a missing index.",
        "resolution": "Added the required database index.",
        "outcome": "Order latency returned to normal.",
        "time": "18 minutes",
    },

    {
        "id": "HIST-010",
        "service": "order-service",
        "symptom": "Order events accumulated in the message queue.",
        "root_cause": "Consumer workers stopped processing messages.",
        "resolution": "Restarted the consumer workers and increased consumer capacity.",
        "outcome": "Queue backlog cleared.",
        "time": "16 minutes",
    },


    # ========================================================
    # NOTIFICATION SERVICE
    # ========================================================

    {
        "id": "HIST-011",
        "service": "notification-service",
        "symptom": "Email delivery success rate dropped to 40%.",
        "root_cause": "Third-party email provider rate limit was exceeded.",
        "resolution": "Reduced request concurrency and enabled exponential backoff.",
        "outcome": "Email delivery returned to normal.",
        "time": "20 minutes",
    },

    {
        "id": "HIST-012",
        "service": "notification-service",
        "symptom": "Push notifications stopped being delivered.",
        "root_cause": "Expired push notification service credentials.",
        "resolution": "Rotated credentials and restarted notification workers.",
        "outcome": "Push delivery recovered.",
        "time": "7 minutes",
    },

    {
        "id": "HIST-013",
        "service": "notification-service",
        "symptom": "Notification queue grew continuously.",
        "root_cause": "Worker memory leak caused workers to restart repeatedly.",
        "resolution": "Restarted workers and rolled out a memory leak fix.",
        "outcome": "Queue backlog cleared.",
        "time": "31 minutes",
    },


    # ========================================================
    # INVENTORY SERVICE
    # ========================================================

    {
        "id": "HIST-014",
        "service": "inventory-service",
        "symptom": "Inventory reads returned stale stock quantities.",
        "root_cause": "Redis cache invalidation stopped after a deployment.",
        "resolution": "Fixed cache invalidation and flushed affected cache keys.",
        "outcome": "Inventory quantities became consistent.",
        "time": "15 minutes",
    },

    {
        "id": "HIST-015",
        "service": "inventory-service",
        "symptom": "Inventory API returned HTTP 503 errors.",
        "root_cause": "Database connection limit was reached.",
        "resolution": "Increased connection capacity and terminated leaked connections.",
        "outcome": "Inventory API recovered.",
        "time": "13 minutes",
    },


    # ========================================================
    # CHECKOUT SERVICE
    # ========================================================

    {
        "id": "HIST-016",
        "service": "checkout-service",
        "symptom": "Checkout requests failed after a feature rollout.",
        "root_cause": "Feature flag enabled an incompatible payment flow.",
        "resolution": "Disabled the feature flag.",
        "outcome": "Checkout recovered immediately.",
        "time": "5 minutes",
    },

    {
        "id": "HIST-017",
        "service": "checkout-service",
        "symptom": "Checkout latency increased sharply.",
        "root_cause": "New downstream inventory calls were executed synchronously.",
        "resolution": "Disabled the new flow and reverted to asynchronous inventory checks.",
        "outcome": "Checkout latency returned to normal.",
        "time": "10 minutes",
    },


    # ========================================================
    # API GATEWAY
    # ========================================================

    {
        "id": "HIST-018",
        "service": "api-gateway",
        "symptom": "Multiple services returned HTTP 502 errors.",
        "root_cause": "Gateway upstream timeout configuration was too aggressive.",
        "resolution": "Increased upstream timeout thresholds.",
        "outcome": "502 errors stopped.",
        "time": "9 minutes",
    },

    {
        "id": "HIST-019",
        "service": "api-gateway",
        "symptom": "API traffic was rejected with HTTP 429 responses.",
        "root_cause": "Rate limiting configuration was accidentally reduced during deployment.",
        "resolution": "Restored the previous rate limit configuration.",
        "outcome": "Normal traffic resumed.",
        "time": "6 minutes",
    },


    # ========================================================
    # SEARCH SERVICE
    # ========================================================

    {
        "id": "HIST-020",
        "service": "search-service",
        "symptom": "Search requests returned HTTP 500 errors.",
        "root_cause": "Search index became corrupted after an interrupted indexing job.",
        "resolution": "Rebuilt the affected search index.",
        "outcome": "Search functionality recovered.",
        "time": "27 minutes",
    },
]


print()
print("==============================================")
print(" INCIDENT MEMORY SEED")
print("==============================================")
print()
print(f"Preparing to store {len(INCIDENTS)} incidents...")
print()


for incident in INCIDENTS:

    experience = f"""
Production Incident Experience

Incident ID:
{incident["id"]}

Service:
{incident["service"]}

Observed Symptom:
{incident["symptom"]}

Root Cause:
{incident["root_cause"]}

Resolution:
{incident["resolution"]}

Outcome:
{incident["outcome"]}

Resolution Time:
{incident["time"]}

This is historical operational experience from a
production incident. Use it when diagnosing future
incidents involving similar services, symptoms,
causes, or failure patterns.
"""

    hindsight.retain(
        bank_id=BANK_ID,
        content=experience
    )

    print(
        f"✓ {incident['id']} | "
        f"{incident['service']} | "
        f"{incident['root_cause']}"
    )


print()
print("==============================================")
print(" SEED COMPLETE")
print("==============================================")
print()
print(f"Stored {len(INCIDENTS)} historical incidents.")
print("Hindsight now has a larger operational history.")
print()


hindsight.close()