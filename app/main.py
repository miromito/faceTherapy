from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
import os
from emotion_api import analyze_emotion

app = FastAPI()

# Set up CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Ensure temp directory exists
os.makedirs("temp", exist_ok=True)


@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    temp_file_path = f"temp/{file.filename}"
    try:

        async with aiofiles.open(temp_file_path, 'wb') as out_file:
            content = await file.read()  # read file content
            await out_file.write(content)  # write to file
        emotion = analyze_emotion(temp_file_path)

        # After processing, delete the file
        os.remove(temp_file_path)

        return JSONResponse(content={"message": "File received", "emotion": emotion})
    except Exception as e:
        # Try to clean up even in case of an error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return JSONResponse(status_code=500, content={"message": "Error processing file", "error": str(e)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
