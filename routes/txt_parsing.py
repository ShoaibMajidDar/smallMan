from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from controllers.txt_parsing import get_similar_chunks, save_embedding
from schemas.txt_parsing import Response



router = APIRouter()

@router.post(
    "/text-parsing",
    response_description="text file parsing",
    response_model=Response
)
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith((".txt")):
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid file type. Only Excel files are allowed."},
        )
    
    contents = await file.read()
    save_embedding_flag = save_embedding(contents)
    if save_embedding_flag:
        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "response_type": "success",
                "description": "text file has been parsed and saved in chromaDB",
                "data": contents,
                }
        )

    else:
        return JSONResponse(
            status_code=400,
            content={
                "status_code": 400,
                "response_type": "Error",
                "description": "Eror occured while saving text file",
                }
        )



@router.post("/ask-question",
             response_description="ask question or query",
             response_model=Response)
async def ask_question(query: str):
    chunks = get_similar_chunks(query)
    if chunks != False:
        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "response_type": "success",
                "description": "Similar chunks",
                "data": chunks,
                }
        )
    else:
       return JSONResponse(
            status_code=400,
            content={
                "status_code": 400,
                "response_type": "Error",
                "description": "error during similarity search",
                }
        )