from fastapi import FastAPI, HTTPException
from fastapi.logger import logger
from pydantic import BaseModel
from typing import Dict, List
from cleaner import clean_data
from visualizer import generate_chart
from cloudvisual import generate_wordcloud

app = FastAPI()

# Define request/response models
class CleanDataRequest(BaseModel):
    data: Dict[str, List]
    column_types: Dict[str, str]

class GenerateChartRequest(BaseModel):
    data: Dict[str, List]
    label: str
    connection: str

class GenerateWordCloudRequest(BaseModel):
    texts: str

@app.post('/clean-data')
async def call_cleaning_service(request: CleanDataRequest):
    try:
        df_cleaned = clean_data(request.data, request.column_types)
        return {"cleaned_data": df_cleaned.to_dict(orient="list")}
    except Exception as e:
        logger.error(f"Error in /clean-data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/generate-chart')
async def call_chart_service(request: GenerateChartRequest):
    try:
        chart = generate_chart(request.data, request.label, request.connection)
        if chart:
            return {"chart_html": chart}
        raise HTTPException(status_code=500, detail="Chart generation failed.")
    except Exception as e:
        logger.error(f"Error in /generate-chart: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/generate-wordcloud')
async def call_wordcloud_service(request: GenerateWordCloudRequest):
    try:
        wordcloud_img = generate_wordcloud(request.texts)
        return {"img": wordcloud_img}
    except Exception as e:
        logger.error(f"Error in /generate-wordcloud: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)