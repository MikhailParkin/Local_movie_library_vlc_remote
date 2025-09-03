import os

import iptv
from fastapi import FastAPI, Body, Request, UploadFile, Form, HTTPException, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from typing import Union, Optional
import aiofiles
import uvicorn as uvicorn
from pathlib import Path

import manage_db as db_query
import vlc_remote as vlc

from iptv import epg_for_list_channel_now, epg_for_one_channel, update_epg, update_playlist

from library import update_library, get_backups, backup_bd, restore_bd, length_video_vlc


app = FastAPI()
templates = Jinja2Templates(directory='templates')

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

origins = [
    "http://localhost",
    "http://localhost:5000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://0.0.0.0:5500",
    "http://0.0.0.0:5550",
    "http://0.0.0.0:5174",
    "http://localhost:5174",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

favicon_path = 'public/img/favicon.ico'
index_path = 'templates/index.html'
UPLOAD_DIRECTORY = 'public/img/posters'


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get('/api/play/{category}/{file_id}')
def play_video_file(category: str, file_id: str):
    video = db_query.play_video(category, file_id)
    file_path = (video.get('file_path'))
    playlist = video.get('playlist')
    vlc.open_vlc(file_path)
    vlc.set_playlist(playlist)
    return {'video': video}


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


################################################################
@app.get("/api/get-categories")
async def api_categories_list():
    categories = db_query.get_categories()
    return categories


@app.get("/api/get-list-video/{category}")
async def get_list_video(category: str):
    list_videos = db_query.api_get_video_list(category)
    return list_videos


@app.get("/api/posters/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    return FileResponse(file_path)


@app.get('/api/get-list-multiseries/{base}/{file_id}')
async def select_series(base: str, file_id: str):
    print('BASE: ', base, 'ID: ', file_id)
    list_series = db_query.api_get_multiseries_list(base, file_id)
    return list_series


@app.get('/api/play-video/{category}/{file_id}')
def play_video_file(category: str, file_id: str):
    video = db_query.play_video(category, file_id)
    file_path = (video.get('file_path'))
    playlist = video.get('playlist')
    vlc.open_vlc(file_path)
    vlc.set_playlist(playlist)
    return {'video': video}


@app.get('/api/library/get-list')
async def get_library():
    libraries = db_query.list_library()
    return libraries


@app.post('/api/library/add')
async def add(data=Body()):
    print(data)
    db_query.add_library(data)
    return {'result': 'Data change!'}


@app.delete('/api/library/delete/{lib_id}')
async def delete(lib_id: str):
    print(lib_id)
    db_query.delete_library(lib_id)
    return {'result': 'Data change!'}


@app.post('/api/library/getPath')
async def add(data=Body()):
    print(data)
    paths = db_query.find_path(data)
    return paths


@app.get('/api/library/update/{lib_id}')
async def update(lib_id: str):
    print(lib_id)
    res = update_library(lib_id)
    # res = "OK"
    return {'result': res}


@app.get('/api/remote/{command}')
async def control(command: str, q: Union[str, None] = None):
    if q:
        command = f'{command} {q}'
        print('COMMAND', command)

    print(command)
    data = vlc.set_command(command)

    return data


@app.get('/api/check_vlc_status')
async def check_vlc():
    data = vlc.check_vlc_status()
    return data


@app.get('/api/iptv/group')
async def select_groups():
    data = iptv.groups
    return data


@app.get('/api/iptv/channels/{group}')
async def check_vlc(group: str):
    data = iptv.select_channels_by_group(group)
    return data


@app.get('/api/iptv/epg/{group}')
async def check_vlc(group: str):
    data = iptv.epg_for_group_channel_now(group)
    return data


@app.get('/api/iptv/epg-channel/{channel_id}')
async def check_vlc(channel_id: str):
    data = iptv.epg_for_channel(channel_id)
    return data


@app.post('/api/iptv/play')
def play_video_file(data=Body()):
    print(data.get('url'))
    vlc.open_vlc(data.get('url'))
    return {'Ok'}


@app.get('/api/kpinfo')
async def get_kpinfo_data():
    data = db_query.get_kpinfo_data()
    return data


@app.post('/api/kpinfo/{rec_id}')
async def update_kp_info(
        rec_id: int,
        kp_id: Optional[str] = Form(None),
        name: Optional[str] = Form(None),
        year: Optional[str] = Form(None),
        rate: Optional[str] = Form(None),
        describe: Optional[str] = Form(None),
        poster: Optional[UploadFile] = File(None)
):
    try:
        updated_fields = {}
        if kp_id is not None:
            updated_fields["kp_id"] = kp_id
        if name is not None:
            updated_fields["name"] = name
        if year is not None:
            updated_fields["year"] = year
        if rate is not None:
            updated_fields["rate"] = rate
        if describe is not None:
            updated_fields["describe"] = describe
        if poster is not None:
            print(poster.filename)
            local_path = Path.cwd()
            out_file_path = Path(local_path, UPLOAD_DIRECTORY, poster.filename)
            if out_file_path.exists():
                os.remove(out_file_path)
            path_to_db = Path(UPLOAD_DIRECTORY, poster.filename)
            updated_fields["poster"] = str(path_to_db)
            updated_fields["poster_filename"] = poster.filename
            async with aiofiles.open(out_file_path, 'wb') as out_file:
                while content := await poster.read(1024):
                    await out_file.write(content)
        record = db_query.update_kpinfo_data(rec_id, updated_fields)
        print(record)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Данные успешно обновлены",
                "updated_fields": updated_fields
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обновлении данных: {str(e)}"
        )


@app.post('/api/update-multiseries')
async def update_kp_info(
        database: Optional[str] = Form(None),
        rec_id: Optional[str] = Form(None),
        name: Optional[str] = Form(None),
        poster: Optional[UploadFile] = File(None)
):
    try:
        updated_fields = {'database': database, 'rec_id': rec_id}

        if name is not None:
            updated_fields["name"] = name
        if poster is not None:
            local_path = Path.cwd()
            out_file_path = Path(local_path, UPLOAD_DIRECTORY, poster.filename)
            if out_file_path.exists():
                os.remove(out_file_path)
            path_to_db = Path(UPLOAD_DIRECTORY, poster.filename)
            updated_fields["poster"] = str(path_to_db)
            updated_fields["poster_filename"] = poster.filename
            async with aiofiles.open(out_file_path, 'wb') as out_file:
                while content := await poster.read(1024):
                    await out_file.write(content)
        record = db_query.update_multiseries_info(updated_fields)
        print(record)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Данные успешно обновлены",
                "updated_fields": updated_fields
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обновлении данных: {str(e)}"
        )


@app.get('/api/local-db')
async def get_local_db_data():
    data = db_query.get_videos_all()
    return data


@app.post('/api/local-db')
async def update_local_db_data(data=Body()):
    print(data.get('file_id'))
    print(data.get('kpinfo_id'))
    res = db_query.update_videos_describe(data)
    return res


@app.get('/api/multiseries/{record_id}')
async def get_local_db_data(record_id: int):
    data = db_query.select_all_multiseries_files(record_id)
    return data


@app.get("/api/get-backups")
async def list_backup_record():
    backups = get_backups()
    return backups


@app.get('/api/admin-page/{action}')
def admin_action(action: str, q: Union[str, None] = None):
    if action == 'backup':
        print('backup')
        backup_bd()
    elif action == 'length':
        length_video_vlc()
        print('length')
    elif action == 'restore':
        restore_bd(q)
        print('restore ', q)
    elif action == 'playlist-update':
        print('playlist')
        update_playlist()
    elif action == 'epg_update':
        print('epg')
        update_epg()
    data = f'{action} complete'
    return {'output': data}


@app.get("/api/playlist")
async def api_get_settings():
    playlist = db_query.get_settings_list()
    return playlist


@app.post("/api/playlist")
async def api_set_settings(playlist_url: Optional[str] = Form(None),
                           epg_url: Optional[str] = Form(None),):
    updated_fields = {}
    try:
        if playlist_url is not None:
            updated_fields["playlist_url"] = playlist_url
        if epg_url is not None:
            updated_fields["epg_url"] = epg_url
        playlist = db_query.set_playlist_settings(updated_fields)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Данные успешно обновлены",
                "updated_fields": playlist
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обновлении данных: {str(e)}"
        )


###################################################################


# @app.get('/{category}')
# async def video_list(category: str, request: Request):
#     print(category)
#     return templates.TemplateResponse(
#             "pages/list_video_js.html",
#             {"request": request, "title": category}
#         )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5550, reload=True)
