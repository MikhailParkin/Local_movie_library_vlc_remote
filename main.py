import os

from fastapi import FastAPI, Body, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import exc
from starlette.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from typing import Union
import aiofiles
import uvicorn as uvicorn
from pathlib import Path

import manage_db as db_query
import vlc_remote as vlc

from iptv import epg_for_list_channel_now, epg_for_one_channel, update_epg, update_playlist

from library import update_library, get_backups, backup_bd, restore_bd, length_video_vlc


app = FastAPI()
templates = Jinja2Templates(directory='templates')

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:5000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://0.0.0.0:5500",
    "http://0.0.0.0:5550",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

favicon_path = 'static/img/favicon.ico'
index_path = 'static/test.html'


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get('/tv')
async def iptv_hls(request: Request):
    return templates.TemplateResponse(
        "pages/iptv_hls.html",
        {"request": request}
    )


@app.get('/manage_local_db/library')
async def show_libraries(request: Request):
    libraries = db_query.list_library()
    return templates.TemplateResponse(
        "pages/library.html",
        {"request": request, "title": 'Библиотеки', 'services': libraries}
        )


@app.post('/manage_local_db/api/library/add')
async def add(data=Body()):
    print(data)
    db_query.add_library(data)
    return {'result': 'Data change!'}


@app.delete('/manage_local_db/api/library/delete/{lib_id}')
async def delete(lib_id: str):
    print(lib_id)
    db_query.delete_library(lib_id)
    return {'result': 'Data change!'}


@app.post('/manage_local_db/api/library/getPath')
async def add(data=Body()):
    print(data)
    paths = db_query.find_path(data)
    return {'result': paths}


@app.get('/manage_local_db/api/library/update/{lib_id}')
async def update(lib_id: str):
    print(lib_id)
    res = update_library(lib_id)
    return {'result': res}


@app.get('/kpbase')
async def show_files(request: Request):
    list_kp = db_query.get_kpinfo_all()
    return templates.TemplateResponse(
        "pages/kpbase.html",
        {"request": request, "title": 'KPinfo', 'list_kp': list_kp}
        )


@app.get('/manage_kp_db/api/kpinfo/{kp_id}')
async def get_kpinfo(kp_id: str):
    video_info = db_query.get_kpinfo(kp_id)
    return {'result': video_info}


@app.get('/manage_kp_db/api/kpinfo/{action}/{path}')
def edit_paths(action: str, path: str, q: Union[str, None] = None):
    print(f'Action: {action}, file_id {path},  kp ID = {q}')
    if action == 'deletepath':
        db_query.delete_kpinfo_path(path)
        result = 'Path Deleted!'
    elif action == 'addpath':
        result = db_query.select_all_video()
        print(result)
    elif action == 'addValue':
        video_id = path
        kp_id = q
        result = db_query.add_kpinfo_on_film_base(video_id, kp_id)
    elif action == 'deactive':
        video_id = path
        result = db_query.deactive_video(video_id)
    return {'result': result}


@app.post('/manage_kp_db/api/kpinfo/{file_id}')
def edit_kpinfo(file_id: str, data=Body()):
    print(file_id)
    print(data)
    try:
        if file_id == 'new':
            result = db_query.new_record_kpinfo(data)
        else:
            result = db_query.edit_kpinfo(data, file_id)
    except exc.SQLAlchemyError as r:
        result = r
    return result


@app.post('/manage_kp_db/api/kpinfo/upload/{file_id}')
async def upload_poster(file_id: str, poster: UploadFile):
    local_path = Path.cwd()
    out_file_path = Path(local_path, 'static', 'img', 'posters', poster.filename)
    if out_file_path.exists():
        os.remove(out_file_path)
    path_to_db = Path('static', 'img', 'posters', poster.filename)
    print(str(path_to_db))
    # result = db_query.edit_kpinfo_poster(file_id, str(path_to_db))
    result = 'File Upload'

    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await poster.read(1024):
            await out_file.write(content)

    return {'result': result}


@app.get('/localbase')
async def show_files(request: Request):
    list_files = db_query.get_files_all()
    return templates.TemplateResponse(
        "pages/localbase.html",
        {"request": request, "title": 'LocalFileBase', 'list_files': list_files}
        )


@app.get('/localbase/api/kpinfo_all')
async def show_kpinfo():
    list_kp_base = db_query.get_kp_name_all()
    return list_kp_base


@app.get('/localbase/api/multiseries/{file_id}')
async def select_series(file_id: str):
    list_series = db_query.select_multiseries(file_id)
    return list_series


@app.get('/localbase/api/multiseries/{base}/{file_id}')
async def select_episode(base:  str, file_id: str):
    result = db_query.select_episode(base, file_id)
    return result

###############################################################


@app.post('/localbase/api/multiseries/{base}/{file_id}')
async def upload_poster(base:  str, file_id: str, data=Body()):
    result = db_query.update_episode(base, file_id, data)
    return {'result': result}


@app.post('/localbase/api/upload/{base}/{file_id}')
async def upload_poster(base:  str, file_id: str, poster: UploadFile):
    local_path = Path.cwd()
    out_file_path = Path(local_path, 'static', 'img', 'posters', poster.filename)
    path_to_db = Path('static', 'img', 'posters', poster.filename)
    print(str(path_to_db))

    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await poster.read(1024):
            await out_file.write(content)
    result = 'File Upload'
    return {'result': result}
######################################################################


@app.get("/home")
async def home(request: Request):
    categories = db_query.get_categories()
    return templates.TemplateResponse(
        "pages/home.html",
        {"request": request, "title": "Home", 'categories': categories}
    )


@app.get('/api/play/{category}/{file_id}')
def play_video_file(category: str, file_id: str):
    video = db_query.play_video(category, file_id)
    file_path = (video.get('file_path'))
    playlist = video.get('playlist')
    vlc.open_vlc(file_path)
    vlc.set_playlist(playlist)
    return {'video': video}


@app.get('/localbase/api/listmultiseries/{base}/{file_id}')
async def select_series(base: str, file_id: str):
    print('BASE: ', base, 'ID: ', file_id)
    list_series = db_query.select_multiseries_list(base, file_id)
    return list_series


@app.get('/api/remote/{command}')
def control(command: str, q: Union[str, None] = None):
    if len(q) > 0:
        command = f'{command} {q}'
        print('COMMAND', command)

    print(command)
    data = vlc.set_command(command)

    return {'output': data}


@app.get("/adminpage")
async def admin_page(request: Request):
    backups = get_backups()
    return templates.TemplateResponse(
        "pages/adminpage.html",
        {"request": request, "title": "Admin", 'backups': backups}
    )


@app.post("/adminpage/api/playlist")
async def api_playlist_settings(data=Body()):
    playlist = db_query.playlist_settings(data)
    return playlist


@app.get("/adminpage/api/playlist_update/{key}")
async def api_playlist_settings(key: str):
    if key == 'playlist':
        result = update_playlist()
    if key == 'epg':
        result = update_epg()
    return result


@app.get("/search")
async def search_page(request: Request):
    return templates.TemplateResponse(
        "pages/search.html",
        {"request": request, "title": "Поиск"}
    )


@app.get("/search/api/{value}")
async def search_video(value: str):
    list_videos = db_query.find_video(value)
    return list_videos


@app.get('/localbase/api/adminpage/{action}')
def backup(action: str, q: Union[str, None] = None):
    if action == 'backup':
        backup_bd()
    elif action == 'length':
        length_video_vlc()
    else:
        restore_bd(q)
    data = f'{action} complete'
    return {'output': data}


@app.get("/api/list_video/{category}")
async def search_video(category: str):
    list_videos = db_query.get_video_list(category)
    return list_videos


@app.post("/api/list_epg/channels")
async def search_epg_for_list_channel(data=Body()):
    print(data)
    res = epg_for_list_channel_now(data)
    return res


@app.post("/api/list_epg/channel")
async def search_epg_for_one_channel(data=Body()):
    print(data)
    res = epg_for_one_channel(data)
    return res


@app.get('/{category}')
async def video_list(category: str, request: Request):
    print(category)
    return templates.TemplateResponse(
            "pages/list_video_js.html",
            {"request": request, "title": category}
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5550, reload=True)
