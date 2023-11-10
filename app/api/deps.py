from fastapi import FastAPI, Depends, HTTPException

# Dependency to get the ML models dictionary
def get_ml_models(app: FastAPI = Depends()):
    if not hasattr(app.state, "ml_models"):
        raise HTTPException(status_code=500, detail="ML models not initialized")
    return app.state.ml_models