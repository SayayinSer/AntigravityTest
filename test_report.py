import httpx
import asyncio

async def test_report():
    url = "http://127.0.0.1:8000/NucleoTallerV1/reports/generate"
    data = {
        "start_date": "2026-02-01",
        "end_date": "2026-04-23",
        "status": "all",
        "tech_id": ""
    }
    
    print(f"Testing POST {url} with data {data}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=data)
            print(f"Status Code: {response.status_code}")
            if response.status_code != 200:
                print("Error Response:")
                print(response.text[:1000]) # Print first 1000 chars of error
            else:
                print("Success! Response contains:")
                print(response.text[:500]) # Print snippet
        except Exception as e:
            print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_report())
