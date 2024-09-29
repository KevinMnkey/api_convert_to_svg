from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from app.image_processing import process_image_to_svg

app = FastAPI()

@app.post("/convert/")
async def convert_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    svg_bytes = process_image_to_svg(image_bytes)
    return Response(content=svg_bytes, media_type="image/svg+xml")