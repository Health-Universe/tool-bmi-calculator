import uvicorn
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Health Calculator API",
    description="An API to calculate Body Mass Index (BMI)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BMICategory(str):
    UNDERWEIGHT = "Underweight"
    NORMAL = "Normal weight"
    OVERWEIGHT = "Overweight"
    OBESITY = "Obesity"

class BMICalculation(BaseModel):
    height: float  # in meters
    weight: float  # in kilograms
    bmi: float
    category: str

@app.post("/calculate_bmi", response_model=BMICalculation)
async def calculate_bmi(
    height: float = Form(..., description="Height in meters", gt=0),
    weight: float = Form(..., description="Weight in kilograms", gt=0)
):
    """
    Calculate BMI based on height and weight.

    - **height**: Height in meters (must be > 0)
    - **weight**: Weight in kilograms (must be > 0)
    """
    try:
        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)

        # Determine BMI category
        if bmi < 18.5:
            category = BMICategory.UNDERWEIGHT
        elif 18.5 <= bmi < 24.9:
            category = BMICategory.NORMAL
        elif 25 <= bmi < 29.9:
            category = BMICategory.OVERWEIGHT
        else:
            category = BMICategory.OBESITY

        return BMICalculation(
            height=height,
            weight=weight,
            bmi=bmi,
            category=category
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health", response_class=JSONResponse)
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "Application is running."}
