from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import alternatives, availability, delivery, products

app = FastAPI(
    title="LAAM Purchase Confidence API",
    description="Backend for the product-detail purchase-confidence experience.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(availability.router)
app.include_router(delivery.router)
app.include_router(alternatives.router)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
