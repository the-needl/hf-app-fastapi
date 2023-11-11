from fastapi import FastAPI, Depends, HTTPException, Request
from typing import Dict

# Dependency to get the ML models dictionary
def get_ml_models(app: FastAPI = Depends()) -> Dict:
    if not hasattr(app.state, "ml_models"):
        raise HTTPException(status_code=500, detail="ML models not initialized")
    
    return app.state.local_models