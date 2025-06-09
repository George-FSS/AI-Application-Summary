import requests
import argparse
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

def query_qwen(prompt):
    url="http://localhost:11434/api/generate"
    payload = {
        "model": "job_post_creator",
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()

    result = response.json()
    return result["response"]

@app.post("/generate-job-posting")
async def generateJobPosting(request: Request):
    try:
        data = await request.json()
        input_data = data.get("body")
        if not input_data:
            raise HTTPException(status_code=400, detail="Missing 'data' key in request body")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
    prompt = "Take the following string of job requirements and turn it into a job posting that you would see on a job board such as linkedin or indeed: " + str(input_data)
    result = query_qwen(prompt)
    return {"job_posting": result}

