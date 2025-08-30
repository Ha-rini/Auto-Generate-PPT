# MultipleFiles/file_processor.py
import os

async def save_file(file_stream, path): # Made async to match FastAPI's async file handling
    with open(path, "wb") as buffer:
        # Read in chunks for large files
        while True:
            chunk = await file_stream.read(8192) # Read 8KB chunks
            if not chunk:
                break
            buffer.write(chunk)

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)

