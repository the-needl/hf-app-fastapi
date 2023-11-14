import asyncio
import httpx
import time
import json

async def send_get_request(session, text):
    url = "http://0.0.0.0:8000/"
    
    response = await session.get(url)

    return response

async def send_post_request(session, text):
    url = "http://0.0.0.0:8000/api/sum/"
    payload = {'context': text}
    
    try:
        start_time = time.time()
        response = await session.post(url, json=payload)
        end_time = time.time()
        
        result = response.json()
        print(f"Response: {result}")
        
        request_time = end_time - start_time
        print(f"Time taken: {request_time:.2f} seconds\n")
        
        return request_time
    except Exception as e:
        print(f"Error: {e}")
        return None

async def send_multiple_requests(num_requests, text):
    total_start_time = time.time()
    payload = {'text': {text}}

    async with httpx.AsyncClient(timeout=None, params=payload) as session:
    # async with httpx.AsyncClient() as session:
        tasks = [send_get_request(session, text) for _ in range(num_requests)]
        # tasks = [send_post_request(session, text) for _ in range(num_requests)]
        request_times = await asyncio.gather(*tasks)

    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time
    
    return total_elapsed_time, request_times


if __name__ == "__main__":
    num_requests = 10 # Replace with the desired number of requests
    user_text = """
    Warren Buffett's cash pile surged to a record $157bn in the third quarter, as the Hathaway Hathaway continues to sell stakes in publicly traded companies.
    """
    # user_text = "Ray is great!"
    total_time, request_times = asyncio.run(send_multiple_requests(num_requests, user_text))

    print(f"Total time spent for {num_requests} requests: {total_time:.2f} seconds")

    if request_times:
        average_request_time = sum(request_times) / len(request_times)
        print(f"Average time per request: {average_request_time:.2f} seconds")

        for i, request_time in enumerate(request_times, start=1):
            print(f"Time for request {i}: {request_time:.2f} seconds")
    else:
        print("No valid request times to calculate averages.")
