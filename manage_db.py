import importlib
import json
import string
from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy.sql import column
from sqlalchemy import exc
from video_base import engine, KPinfo, VideoFiles, Categories, Library, Series, Seasons, Settings

db = Session(autoflush=False, bind=engine)
models = importlib.import_module('video_base')
video_format = ['.avi', '.mkv', '.mp4', '.flv']
default_categories = [{'category': 'Movies', 'name': 'Фильмы', 'poster': r'static\img\categories\movies.jpg'},
                      {'category': 'Serials', 'name': 'Сериалы', 'poster': r'static\img\categories\serials.webp'},
                      {'category': 'Cartoons', 'name': 'Полнометражные мультфильмы',
                       'poster': r'static\img\categories\cartoons.jpg'},
                      {'category': 'CartoonsKids', 'name': 'Мультики',
                       'poster': r'static\img\categories\cartoonskids.jpg'},
                      {'category': 'MultSerial', 'name': 'Мультсериалы',
                       'poster': r'static\img\categories\multserials.jpg'}]

one_file_video = ['Movies', 'Cartoons', 'CartoonsKids']
multi_file_video = ['Serials', 'MultSerial']

"""  Import from json  """


def new_record_categories():
    model_class = getattr(models, 'Categories')
    for item in default_categories:
        rec = model_class(category=item.get('category'),
                          name=item.get('name'),
                          poster=item.get('poster'))
        print(f'create record {item.get("url")}')
        db.add(rec)
    db.commit()
    db.close()


def new_record_kpinfo(cat, data):
    model_class = getattr(models, cat)
    kp_id = data[1]
    name_rus = data[3]
    year = data[4]
    poster = data[6]
    describe = data[7]
    rate = data[9]

    new_static_path = r'static\img\posters'
    new_poster_path = Path(new_static_path, Path(poster).name)

    video_file = model_class(kp_id=kp_id,
                             name=name_rus,
                             year=year,
                             poster=str(new_poster_path),
                             describe=describe,
                             rate=rate)
    db.add(video_file)
    db.commit()
    db.close()
    print(f'create record {name_rus}')


def open_json(path, cat):
    f = open(path, 'r', encoding="utf-8")
    data = json.loads(f.read())
    for i in data['rows']:
        if i[1] is not None:
            new_record_kpinfo(cat, i)
    f.close()


# new_record('KPinfo', default_data)
# new_record_categories()

# open_json('export_table_movies.json', 'KPinfo')


""" Library """


def list_library():
    """Получаем списос групп видео"""
    categories = db.query(Categories).all()
    library_list = {}
    for category in categories:
        library_list[category.name] = category.library
    db.close()
    return library_list


def add_library(data):
    """Добавление новой группы видео"""
    category = db.query(Categories).filter_by(name=data['service']).one_or_none()
    new_path = Library(category_id=category.id, category_path=data['path'])
    db.add(new_path)
    db.commit()
    db.close()


def delete_library(lib_id):
    """Удаление группы видео"""
    library = db.query(Library).filter_by(id=lib_id).one_or_none()
    db.delete(library)
    db.commit()
    db.close()


"""List files on disk"""


def find_path(data):
    """Если data is None Получаем список дисков, если нет то ищем директории в директории data.path"""
    path = data.get('path')
    if path == '' or path is None:
        paths = []
        for letter in string.ascii_lowercase:
            disk = letter + r':\\'
            if Path(disk).exists() is True:
                paths.append({'dir_name': letter + ':', 'dir_path': disk})
    else:
        brows_paths = Path(path).iterdir()
        paths = []
        for item in brows_paths:
            if item.is_dir():
                paths.append({'dir_name': item.name, 'dir_path': str(item)})

    print(paths)
    return paths


""" SELECT DATA """


# def get_kpinfo_all():
#     kpinfo = db.query(KPinfo).order_by(KPinfo.id.desc()).all()
#     list_rec = []
#     for item in kpinfo:
#         rec = {'id': item.id,
#                'name': item.name,
#                'kp_id': item.kp_id, }
#         list_rec.append(rec)
#     db.close()
#     return list_rec
#
#
# def get_kpinfo(kp_id):
#     kpinfo = db.query(KPinfo).filter_by(id=kp_id).one_or_none()
#     file_info = {'id': kpinfo.id,
#                  'kp_id': kpinfo.kp_id,
#                  'name': kpinfo.name,
#                  'year': kpinfo.year,
#                  'poster': kpinfo.poster,
#                  'describe': kpinfo.describe,
#                  'rate': kpinfo.rate}
#     list_files = []
#     if len(kpinfo.video_files) > 0:
#         for item in kpinfo.video_files:
#             files_path = {'id': item.id, 'file_path': item.file_path}
#             list_files.append(files_path)
#     file_info['list_files'] = list_files
#     db.close()
#     return file_info


# def delete_kpinfo_path(file_id):
#     video = db.query(VideoFiles).filter_by(id=file_id).one_or_none()
#     video.kpinfo = None
#     db.commit()
#     db.close()


# def select_all_video():
#     video_files = []
#     files = db.query(VideoFiles).filter_by(kpinfo_id=None).order_by(VideoFiles.id.desc()).all()
#     for video in files:
#         rec = {'id': video.id, 'file_name': video.file_name}
#         video_files.append(rec)
#     db.close()
#     return video_files


# def add_kpinfo_on_film_base(video_id, kp_id):
#     video = db.query(VideoFiles).filter_by(id=video_id).one_or_none()
#     video.kpinfo_id = kp_id
#     category = video.category
#     db.commit()
#     db.close()
#     if category in multi_file_video:
#         try:
#             kpinfo = db.query(KPinfo).filter_by(id=kp_id).one_or_none()
#             seasons = db.query(Seasons).filter_by(videofiles_id=video_id).all()
#             for season in seasons:
#                 season.poster = kpinfo.poster
#                 series = db.query(Series).filter_by(seasons_id=season.id).all()
#                 for episode in series:
#                     episode.poster = kpinfo.poster
#             db.commit()
#             db.close()
#         except exc.SQLAlchemyError as e:
#             print(e)
#     return 'info added!'


# def edit_kpinfo(data: dict, file_id: str):
#     rec = db.query(KPinfo).filter_by(id=file_id).one_or_none()
#     rec.kp_id = data.get('kp_id')
#     rec.year = data.get('year')
#     rec.rate = data.get('rate')
#     rec.name_rus = data.get('name_rus')
#     rec.describe = data.get('describe')
#     if data.get('poster') is not None and len(data.get('poster')) > 0:
#         path_to_db = Path('static', 'img', 'posters', data.get('poster'))
#         rec.poster = str(path_to_db)
#     db.commit()
#     db.close()
#     return 'info edited!'


# def edit_kpinfo_poster(file_id: str, poster_path: str):
#     rec = db.query(KPinfo).filter_by(id=file_id).one_or_none()
#     rec.poster = poster_path
#     db.commit()
#     db.close()
#     return 'poster added'


def new_record_kpinfo(data):
    poster = r'/static/img/categories/kinopoisk.jpg'
    if data.get('poster') is not None and len(data.get('poster')) > 0:
        poster = Path('static', 'img', 'posters', data.get('poster'))

    new_rec = KPinfo(kp_id=data.get('kp_id'),
                     name=data.get('name'),
                     year=data.get('year'),
                     describe=data.get('describe'),
                     rate=data.get('rate'),
                     poster=poster)
    db.add(new_rec)
    db.commit()
    db.close()
    added_rec = db.query(KPinfo).order_by(KPinfo.id.desc()).first()
    db.close()
    return added_rec.id


# def get_files_all():
#     files = db.query(VideoFiles).order_by(VideoFiles.id.desc()).all()
#     files_list = []
#     for file in files:
#         rec = {'id': file.id, 'file_name': file.file_name, 'active': file.active, 'category': file.category}
#         files_list.append(rec)
#     db.close()
#     return files_list


# def get_kp_name_all():
#     kp_all = db.query(KPinfo).order_by(KPinfo.id.desc()).all()
#     kpinfo_list = []
#     for item in kp_all:
#         rec = {'id': item.id, 'name': item.name}
#         kpinfo_list.append(rec)
#     db.close()
#     return kpinfo_list


def deactive_video(video_id):
    video = db.query(VideoFiles).filter_by(id=video_id).one_or_none()
    if video.active:
        video.active = False
        result = 'Video deactiv!'
    else:
        video.active = True
        result = 'Video active!'
    db.commit()
    db.close()
    return result


# def select_multiseries(file_id):
#     videos = db.query(VideoFiles).filter_by(id=file_id).one_or_none()
#     all_records = {}
#     list_season = []
#
#     for item in videos.seasons:
#         list_season.append({'id': item.id, 'file_name': item.name})
#         list_series = []
#         for season in item.series:
#             rec = {'id': season.id, 'file_name': season.name}
#             list_series.append(rec)
#         all_records[item.name] = list_series
#     all_records['Seasons'] = list_season
#     print(all_records)
#     db.close()
#     return all_records


# def select_episode(base, file_id):
#     rec = db.query(getattr(models, base)).filter_by(id=file_id).one_or_none()
#     db.close()
#     return {'id': rec.id, 'file_name': rec.name, 'poster': rec.poster}
#
#
# def update_episode(base, file_id, data):
#
#     rec = db.query(getattr(models, base)).filter_by(id=file_id).one_or_none()
#     if data.get('poster') is not None and len(data.get('poster')) > 0:
#         poster = Path('static', 'img', 'posters', data.get('poster'))
#         rec.poster = str(poster)
#     rec.name = data.get('file_name')
#     db.commit()
#     db.close()
#     return {'result': 'Record Updated!'}


# def edit_serials_poster(base, file_id, path_to_db):
#     rec = db.query(getattr(models, base)).filter_by(id=file_id).one_or_none()
#     rec.poster = path_to_db
#     if base == 'Seasons':
#         for item in rec.series:
#             item.poster = path_to_db
#     db.commit()
#     db.close()
#     return 'Poster added'


def get_categories():
    categories = db.query(Categories).all()
    categories_list = []
    for item in categories:
        rec = {'id': item.id, 'category': item.category, 'name': item.name, 'multiseries': item.multiseries}
        categories_list.append(rec)
    db.close()
    return categories_list


def get_video_list(category):
    list_videos = db.query(VideoFiles).filter_by(category=category).order_by(VideoFiles.id.desc()).all()
    list_records = []
    for item in list_videos:
        if item.kpinfo_id is not None:
            file_name = item.kpinfo.name
            poster = item.kpinfo.poster
            rate = item.kpinfo.rate
            year = item.kpinfo.year
        else:
            file_name = item.file_name
            poster = item.poster
            rate = 0
            year = 0

        if item.active:
            record = {'id': item.id,
                      'file_name': file_name,
                      'poster': poster,
                      'rate': rate,
                      'year': year
                      }
            list_records.append(record)
    db.close()
    print(list_records)
    return list_records


# def select_multiseries_list(base, file_id):
#     if base == 'Seasons':
#         list_series = db.query(getattr(models, base)).filter_by(videofiles_id=file_id).order_by(Seasons.file_name).all()
#     else:
#         list_series = db.query(getattr(models, base)).filter_by(seasons_id=file_id).order_by(Series.file_name).all()
#     db.close()
#     print(list_series)
#     return list_series


def play_video(category, file_id):
    if category == 'Series':
        play_file = db.query(Series).filter_by(id=file_id).one_or_none()

    else:
        play_file = db.query(VideoFiles).filter_by(id=file_id).one_or_none()

    video_info = {'file_path': play_file.file_path,
                  'video_length': play_file.video_length,
                  'last_position': play_file.last_position,
                  'file_name': play_file.file_name}
    if category == 'Series':
        series_list = db.query(Series).filter_by(seasons_id=play_file.seasons_id).order_by(Series.file_path).all()
        all_episode = []
        for episode in series_list:
            all_episode.append(episode.file_path)
        position_on_list = all_episode.index(play_file.file_path)
        if position_on_list == len(all_episode):
            playlist = []
        else:
            playlist = all_episode[:position_on_list + 1]
        video_info['playlist'] = playlist
    return video_info


def find_video_by_file_name(file_name):
    tables_video_files = ['VideoFiles', 'Series']
    rec = {'title': None}
    for table in tables_video_files:
        model_service = getattr(models, table)
        file = db.query(model_service).filter_by(file_name=file_name).one_or_none()
        if file is not None:
            rec = {'table': table,
                   'id': file.id,
                   'video_length': file.video_length,
                   'last_position': file.last_position,
                   'title': file_name}
    print(rec)
    return rec


def set_last_position(video, position):
    video_table = video.get('table')
    video_id = video.get('id')
    model_service = getattr(models, video_table)
    rec = db.query(model_service).filter_by(id=video_id).first()
    rec.last_position = position
    db.commit()
    db.close()


# def find_video(value):
#     tables = ['VideoFiles', 'Series']
#     key_low = value.casefold()
#     key_hi = value.capitalize()
#     list_data = []
#     result = []
#     for table in tables:
#         if table == 'VideoFiles':
#             files = db.query(VideoFiles).filter((VideoFiles.file_name.ilike(f'%{key_low}%'))
#                                                 | VideoFiles.file_name.ilike(f'%{key_hi}%')).all()
#             for file in files:
#                 rec = {'id': file.id, 'file_name': file.file_name}
#                 list_data.append(rec)
#
#             files_kp = db.query(VideoFiles).filter(column('kpinfo_id').isnot(None)).all()
#
#             for file in files_kp:
#                 if key_low in file.name or key_hi  in file.name:
#                     rec = {'id': file.id, 'file_name': file.name}
#                     list_data.append(rec)
#
#         elif table == 'Series':
#             files = db.query(Series).filter((Series.name.ilike(f'%{key_low}%'))
#                                             | Series.name.ilike(f'%{key_hi}%')).all()
#             for file in files:
#                 rec = {'id': file.id, 'file_name': file.name}
#                 list_data.append(rec)
#
#         result.append({'table': table, 'files': list_data})


# def playlist_settings(data):
#     print('DATA: ', data)
#     playlist = db.query(Settings).first()
#     if playlist:
#         result = playlist.playlist_url
#         if len(data.get('playlist')) > 0:
#             playlist.playlist_url = data.get('playlist')
#             db.commit()
#             db.close()
#             result = data.get('playlist')
#
#     else:
#         result = data.get('playlist')
#         new_playlist = Settings(playlist_url=data.get('playlist'))
#         db.add(new_playlist)
#         db.commit()
#         db.close()
#
#     return result


# playlist_settings('')
# def poster_filename():
#     videos = db.query(VideoFiles).all()
#     for item in videos:
#         poster_name = Path(item.poster).name
#         print(poster_name)
#         item.poster_filename = poster_name
#     db.commit()
#     db.close()


# poster_filename()


def api_get_video_list(category):
    list_videos = db.query(VideoFiles).filter_by(category=category).order_by(VideoFiles.id.desc()).all()
    list_records = []
    for item in list_videos:
        if item.kpinfo_id is not None:
            file_name = item.kpinfo.name
            poster = item.kpinfo.poster_filename
            rate = item.kpinfo.rate
            year = item.kpinfo.year
        else:
            file_name = item.file_name
            poster = item.poster_filename
            rate = 0
            year = 0

        if item.active:
            record = {'id': item.id,
                      'file_name': file_name,
                      'poster': poster,
                      'rate': rate,
                      'year': year
                      }
            list_records.append(record)
    db.close()
    print(list_records)
    return list_records


def api_get_multiseries_list(base, file_id):
    list_records = []
    if base == 'Seasons':
        list_series = db.query(getattr(models, base)).filter_by(videofiles_id=file_id).order_by(Seasons.file_name).all()
    else:
        list_series = db.query(getattr(models, base)).filter_by(seasons_id=file_id).order_by(Series.file_name).all()
    db.close()
    for item in list_series:
        record = {'id': item.id,
                  'file_name': item.name,
                  'poster': item.poster_filename,
                  'rate': 0,
                  'year': 0
                  }
        list_records.append(record)
    print(list_records)
    return list_records


def get_kpinfo_data():
    kpinfo = db.query(KPinfo).order_by(KPinfo.name).all()
    db.close()
    return kpinfo


def get_videos_all():
    files = db.query(VideoFiles).order_by(VideoFiles.id.desc()).all()
    db.close()
    return files


def update_videos_describe(data):
    file_id = data.get('file_id')
    kpinfo_id = data.get('kpinfo_id')
    video_file = db.query(VideoFiles).filter_by(id=file_id).one_or_none()
    if video_file:
        video_file.kpinfo_id = kpinfo_id
        category = video_file.category
        poster = video_file.poster
        poster_filename = video_file.poster_filename
        db.commit()
        db.close()
    if category == 'Serials':
        seasons_id = []
        seasons = db.query(Seasons).filter_by(videofiles_id=file_id).order_by(Seasons.name).all()
        for season in seasons:
            season.poster = poster
            season.poster_filename = poster_filename
            seasons_id.append(season.id)
        db.commit()
        db.close()
        for item in seasons_id:
            series = db.query(Series).filter_by(seasons_id=item).order_by(Series.name).all()
            for episode in series:
                episode.poster = poster
                episode.poster_filename = poster_filename
        db.commit()
        db.close()
    return 'OK'


def update_kpinfo_data(rec_id: int, data: dict):
    if rec_id == 999999:
        new_record = KPinfo(kp_id=data.get('kp_id'), name=data.get('name'),
                            year=data.get('year'), poster=data.get('poster'),
                            poster_filename=data.get('poster_filename'), describe=data.get('describe'),
                            rate=data.get('rate'))
        db.add(new_record)
        db.commit()
        db.close()
    else:
        record = db.query(KPinfo).filter_by(id=rec_id).first()
        for key, value in data.items():
            setattr(record, key, value)
        db.commit()
        db.close()
    return 'ok'


def select_all_multiseries_files(record_id):
    all_seasons = []
    seasons = db.query(Seasons).filter_by(videofiles_id=record_id).order_by(Seasons.name).all()
    for season in seasons:
        all_seasons.append({'season_id': season.id, 'season_name': season.name})
    db.close()
    for item in all_seasons:
        list_series = []
        series = db.query(Series).filter_by(seasons_id=item['season_id']).order_by(Series.name).all()
        for episode in series:
            list_series.append({'episode_id': episode.id, 'episode_name': episode.name})
        item['series'] = list_series
    print(all_seasons)
    return all_seasons


def update_multiseries_info(data: dict):
    database = data.get('database')
    rec_id = data.get('rec_id')
    tablename = getattr(models, database)
    if data.get('name'):
        name = data.get('name')
        record = db.query(tablename).filter_by(id=rec_id).one_or_none()
        record.name = name
        db.commit()
        db.close()
        print(database, rec_id, name)
    if data.get('poster'):
        poster = data.get('poster')
        poster_filename = data.get('poster_filename')
        if database == 'Seasons':
            record = db.query(Seasons).filter_by(id=rec_id).one_or_none()
            record.poster = poster
            record.poster_filename = poster_filename
            db.commit()
            db.close()
            series = db.query(Series).filter_by(seasons_id=rec_id).all()
            for episode in series:
                episode.poster = poster
                episode.poster_filename = poster_filename
            db.commit()
            db.close()
        elif database == 'Series':
            record = db.query(Series).filter_by(id=rec_id).one_or_none()
            record.poster = poster
            record.poster_filename = poster_filename
            db.commit()
            db.close()
    return 'ok'


def get_settings_list():
    record = db.query(Settings).first()
    settings_list = {}
    if record:
        settings_list['playlist_url'] = record.playlist_url
        settings_list['epg_url'] = record.epg_url
    else:
        settings_list['playlist_url'] = ''
        settings_list['epg_url'] = ''
    return settings_list


def set_playlist_settings(data: dict):
    record = db.query(Settings).filter_by(id=1).one_or_none()
    print(record)

    if record is None:
        record = Settings(id=1)
        db.add(record)

    for key, value in data.items():
        setattr(record, key, value)
        print(f"Set {key} = {value}")

    db.commit()
    db.close()
    return data




