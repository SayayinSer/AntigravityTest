from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_report():
    print("Testing GET /NucleoTallerV1/reports")
    response = client.get("/NucleoTallerV1/reports")
    print(f"GET Status: {response.status_code}")
    
    print("\nTesting POST /NucleoTallerV1/reports/generate")
    response = client.post("/NucleoTallerV1/reports/generate", data={
        "start_date": "2026-02-01",
        "end_date": "2026-04-23",
        "status": "all",
        "tech_id": ""
    })
    print(f"POST Status: {response.status_code}")
    if response.status_code != 200:
        print(response.text)
    else:
        print("Success! Contains HTML:")
        print(response.text[:200])

if __name__ == "__main__":
    test_report()
