import aiohttp
import asyncio
import time

async def fetch_sum(session, prompt):
    url = f"http://127.0.0.1:8000/sum?sentence={prompt}"
    async with session.get(url) as response:
        resp = await response.json()
        return response.status, resp

async def main(num_requests):
    prompts = [
        """
        Warren Buffett's cash pile surged to a record $157bn in the third quarter, as the Hathaway Hathaway continues to sell stakes in publicly traded companies. Berkshire Hathaway has been one of the big beneficiaries of rising US interest rates, which have climbed above 5% this year. The company's operating businesses, which span the BNSF railroad, Geico auto-insurer, and aircraft parts maker Precision Castparts, reported strong underwriting profits of $2.4bn. However, revenue from these businesses experienced modest declines due to weak demand for new inventory. Sales slid across all industries except apparel and real estate.Berkshire Hathaway also took a large charge related to the 2020 and 2022 wildfires that spread through California and Oregon. The decline of the company's stock portfolio, which is accounted for in Berkshire's profit statement, dragged down the overall results.
        """,
        # Add more prompts as needed
    ]

    total_start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for prompt in prompts*num_requests:
            task = asyncio.create_task(fetch_sum(session, "%20".join(prompt.split(" "))))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        for resp in responses:
            # print(f"Prompt: {prompt}")
            print(resp)

    total_end_time = time.time()
    print(f"Total time for all requests: {total_end_time - total_start_time:.2f} seconds")

if __name__ == "__main__":
    num_requests = 200  # Specify the number of requests you want to send
    asyncio.run(main(num_requests))
