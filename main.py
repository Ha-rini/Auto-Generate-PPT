# MultipleFiles/main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from services.pptx_generator import generate_presentation # Corrected import path
import os
from dotenv import load_dotenv
from utils.file_processor import save_file, remove_file # Import utility functions
from fastapi.staticfiles import StaticFiles




# Load environment variables from .env file
load_dotenv()

app = FastAPI()



# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
# Create an uploads directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.post("/generate-presentation/")
async def create_presentation(
    content: str = Form(...),
    guidance: str = Form(...),
    template: UploadFile = File(...)
):
    # Use the Aipipe token from the .env file
    api_key = os.getenv("OPENAI_API_KEY") # Aipipe uses this env var
    if not api_key:
        raise HTTPException(status_code=400, detail="Aipipe API key (OPENAI_API_KEY) not set in environment variables.")

    template_path = None # Initialize to None for finally block
    output_path = None # Initialize to None for finally block

    try:
        # Save the uploaded template file
        template_path = os.path.join("uploads", template.filename)
        await save_file(template.file, template_path) # Use the utility function

        # Generate the presentation using Aipipe
        output_path = generate_presentation(content, guidance, api_key, template_path)

        # Return the generated file
        return FileResponse(output_path, media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation', filename=os.path.basename(output_path))

    except Exception as e:
        print(f"Error during presentation generation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate presentation: {e}")
    finally:
        # Clean up: Remove the uploaded template and generated presentation
        if template_path and os.path.exists(template_path):
            remove_file(template_path)
        if output_path and os.path.exists(output_path):
            remove_file(output_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

