import ray
import requests
import numpy as np
import time

@ray.remote
def send_query(text):
    start_time = time.time()
    resp = requests.get("http://localhost:8000/?text={}".format(text))
    end_time = time.time()
    return resp.text, end_time - start_time

# Let's use Ray to send all queries in parallel
texts = [
    """
    Warren Buffett's cash pile surged to a record $157bn in the third quarter, as the Hathaway Hathaway continues to sell stakes in publicly traded companies. Berkshire Hathaway has been one of the big beneficiaries of rising US interest rates, which have climbed above 5% this year. The company's operating businesses, which span the BNSF railroad, Geico auto-insurer, and aircraft parts maker Precision Castparts, reported strong underwriting profits of $2.4bn. However, revenue from these businesses experienced modest declines due to weak demand for new inventory. Sales slid across all industries except apparel and real estate.Berkshire Hathaway also took a large charge related to the 2020 and 2022 wildfires that spread through California and Oregon. The decline of the company's stock portfolio, which is accounted for in Berkshire's profit statement, dragged down the overall results.
    """,
    # Add more prompts as needed
]

# Measure the total time taken
start_total_time = time.time()

results = ray.get([send_query.remote(text) for text in texts*20])

# Calculate total time taken
total_time = time.time() - start_total_time

print("Results returned:", results)
print("Total time taken:", total_time)
