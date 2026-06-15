"""
generate_synthetic_data.py

Creates the raw seed data for the dbt-dimensional-model project.
Writes to seeds/raw_jobs_tasks.csv, which dbt loads with `dbt seed`.

All data is randomly generated. It contains no real or proprietary information.

Usage:
    python generate_synthetic_data.py
"""

import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)  # Reproducible: same data every run.

NUM_ROWS = 600
SEED_DIR = "seeds"
OUTPUT_FILE = os.path.join(SEED_DIR, "raw_jobs_tasks.csv")

CUSTOMERS = ["North Region Retail", "Coastal Logistics", "Summit Healthcare",
             "Lakeside Education", "Metro Warehousing"]
JOB_TYPES = ["Preventive", "Reactive", "Inspection", "Installation", "Repair"]
STATUSES = ["Open", "Closed", "On Hold", "Pending Approval"]
CITIES = ["Springfield", "Riverton", "Fairview", "Greenville", "Madison"]


def random_date(days_back=365):
    start = datetime.now() - timedelta(days=days_back)
    return start + timedelta(days=random.randint(0, days_back))


def build_rows(num_rows):
    rows = []
    num_jobs = num_rows // 2

    # Assign a fixed customer and city to each job up front,
    # so a job always belongs to exactly one customer (correct grain).
    job_customer = {}
    job_city = {}
    for j in range(1, num_jobs + 1):
        job_customer[80000 + j] = random.choice(CUSTOMERS)
        job_city[80000 + j] = random.choice(CITIES)

    for i in range(1, num_rows + 1):
        job_id = 80000 + random.randint(1, num_jobs)
        job_type = random.choice(JOB_TYPES)
        cost = round(random.uniform(75, 5000), 2)
        # sales_price is set at the job level, so it repeats across a job's tasks.
        random.seed(job_id)              # same price for the same job
        sales_price = round(random.uniform(500, 12000), 2)
        random.seed(42 + i)              # restore varied randomness per task
        rows.append({
            "job_id": job_id,
            "task_id": 200000 + i,
            "customer": job_customer[job_id],
            "city": job_city[job_id],
            "job_type": job_type,
            "status": random.choice(STATUSES),
            "created_at": random_date().strftime("%Y-%m-%d"),
            "task_cost": cost,
            "sales_price": sales_price,
        })
    return rows


def main():
    os.makedirs(SEED_DIR, exist_ok=True)
    rows = build_rows(NUM_ROWS)
    fieldnames = list(rows[0].keys())
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
