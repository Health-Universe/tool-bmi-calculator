from typing import Annotated, Literal
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="BMI Calculator Tool",
    description="Calculates Body Mass Index (BMI).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BMICalculationInput(BaseModel):
    """
    Form-based input schema for calculating BMI.
    """

    unit_system: Literal["metric", "imperial"] = Field(
        default="metric",
        title="Unit System",
        examples=["metric"],
        description="Select your measurement system.",
    )

    height: float = Field(
        ...,
        title="Height",
        ge=0.1,
        examples=[1.75],
        description=(
            "Enter your height in inches if using imperial or meters if using metric."
        ),
    )
    weight: float = Field(
        ...,
        title="Weight",
        ge=0.1,
        examples=[70.0],
        description=(
            "Enter your weight in pounds if using imperial or kilograms if using metric."
        ),
    )


class BMICalculationOutput(BaseModel):
    """
    Form-based output schema for Body Mass Index (BMI).
    """

    bmi: float = Field(
        title="Body Mass Index",
        examples=[22.86],
        description="Your calculated Body Mass Index.",
        format="display",
    )
    category: Literal["Underweight", "Normal weight", "Overweight", "Obesity"] = Field(
        title="BMI Category",
        examples=["Normal weight"],
        description="Your BMI category based on your BMI value.",
        format="display",
    )


@app.post(
    "/calculate_bmi/",
    response_model=BMICalculationOutput,
)
def calculate_bmi(
        data: Annotated[BMICalculationInput, Form()],
) -> BMICalculationOutput:
    """Calculate Body Mass Index (BMI) based on height and weight.

    Args:
        data (BMICalculationInput): Input data for calculating BMI.

    Returns:
        BMICalculationOutput: The calculated BMI and category.

    """
    conversion_factors = {
        "metric": {"height": 1.0, "weight": 1.0},
        "imperial": {"height": 0.0254, "weight": 0.453592},
    }

    unit = data.unit_system.lower()
    if unit not in conversion_factors:
        raise HTTPException(
            status_code=400,
            detail="Invalid unit system. Must be 'metric' or 'imperial'.",
        )

    factors = conversion_factors[unit]
    height_in_meters = data.height * factors["height"]
    weight_in_kg = data.weight * factors["weight"]

    bmi = weight_in_kg / (height_in_meters ** 2)
    bmi = round(bmi, 2)

    category: Literal[
        "Underweight", "Normal weight", "Overweight", "Obesity"] = "Underweight" if bmi < 18.5 else "Normal weight" if 18.5 <= bmi < 24.9 else "Overweight" if 25 <= bmi < 29.9 else "Obesity"

    return BMICalculationOutput(bmi=bmi, category=category)


@app.get("/health", response_class=JSONResponse)
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "Application is running."}
