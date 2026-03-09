from fastapi import FastAPI, HTTPException

# Initialize the FastAPI app
app = FastAPI(title="Basic Calculator API")

# 1. Addition Endpoint
@app.get("/add")
def add(a: float, b: float):
    return {"operation": "addition", "a": a, "b": b, "result": a + b}

# 2. Subtraction Endpoint
@app.get("/subtract")
def subtract(a: float, b: float):
    return {"operation": "subtraction", "a": a, "b": b, "result": a - b}

# 3. Multiplication Endpoint
@app.get("/multiply")
def multiply(a: float, b: float):
    return {"operation": "multiplication", "a": a, "b": b, "result": a * b}

# 4. Division Endpoint (with basic error handling)
@app.get("/divide")
def divide(a: float, b: float):
    if b == 0:
        # Prevent division by zero errors
        raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
    return {"operation": "division", "a": a, "b": b, "result": a / b}