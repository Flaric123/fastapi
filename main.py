from fastapi import FastAPI, HTTPException, Query
import random
from math import sqrt

app = FastAPI()

@app.get("/about")
async def author_info():
    return {
        "firstname": "Артем",
        "lastname": "Ермолин",
        "group": "Т-323901-НТ",
    }


@app.get("/rnd")
async def random_int():
    return {"randint": random.randint(1, 10)}

@app.post("/t_square")
async def triangle_perimeter_and_area(
    a: float = Query(..., gt=0, description="Сторона A > 0"),
    b: float = Query(..., gt=0, description="Сторона B > 0"),
    c: float = Query(..., gt=0, description="Сторона C > 0"),
):
    if not (a + b > c and a + c > b and b + c > a):
        raise HTTPException(
            status_code=400,
            detail="Треугольник с такими сторонами не существует"
        )
    
    perimeter = a + b + c
    p = perimeter / 2
    area = sqrt(p * (p - a) * (p - b) * (p - c))
    
    return {"perimeter": perimeter, "area": area}