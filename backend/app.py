from pathlib import Path
import uuid,shutil
from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.responses import FileResponse
from analyzer import analyze
app=FastAPI(title='SquashFrame AI V0.1')
ROOT=Path(__file__).resolve().parent/'outputs';ROOT.mkdir(exist_ok=True)
@app.get('/health')
def health():return {'ok':True,'version':'0.1.0'}
@app.post('/analyze')
async def run_analysis(video:UploadFile=File(...)):
    job=uuid.uuid4().hex;folder=ROOT/job;folder.mkdir()
    size=0
    try:
        with (folder/'input.mp4').open('wb') as f:
            while chunk:=await video.read(1024*1024):
                size+=len(chunk)
                if size>200*1024*1024:raise HTTPException(413,'Video exceeds 200 MB')
                f.write(chunk)
        summary=analyze(folder/'input.mp4',folder/'analysis')
        return {'job_id':job,**summary,'csv_url':f'/results/{job}/angles.csv','json_url':f'/results/{job}/results.json'}
    except HTTPException:
        shutil.rmtree(folder,ignore_errors=True);raise
    except Exception as e:
        shutil.rmtree(folder,ignore_errors=True);raise HTTPException(422,str(e))
@app.get('/results/{job}/{filename}')
def result(job:str,filename:str):
    if len(job)!=32 or any(c not in '0123456789abcdef' for c in job):raise HTTPException(400,'Invalid job')
    if filename not in ('angles.csv','results.json'):raise HTTPException(404,'Unknown result')
    p=ROOT/job/'analysis'/filename
    if not p.is_file():raise HTTPException(404,'Not found')
    return FileResponse(p)
