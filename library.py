import importlib
from pathlib import Path
import shutil
from datetime import datetime
import ffmpeg
from time import sleep

import vlc_remote
from vlc_remote import change_title_mkv, open_vlc, get_time_data
from manage_db import db, multi_file_video
from video_base import VideoFiles, Categories, Library, Seasons, Series, BackupBd

models = importlib.import_module('video_base')
video_format = ['.avi', '.mkv', '.mp4', '.flv']

one_file_video = ['Movies', 'Cartoons', 'CartoonsKids']
multi_file_video = ['Serials', 'MultSerial']

""" Video duration """


def video_duration(video_file):
    """Определяем длительность видео"""
    try:
        streams = ffmpeg.probe(video_file)["streams"]
        if Path(video_file).suffix == '.mkv':
            # for stream in streams:
            #     print(f'{stream}: {streams[0].get(f"{stream}")}')
            metadata = streams[0].get('tags')
            duration = metadata
            if metadata:
                for key in dict(metadata).keys():
                    print(key, metadata[key])

                if metadata is not None:
                    duration = metadata.get('DURATION')
                    title = metadata.get('title')
                    if duration is not None:
                        duration = duration.split('.')[0]
                        h, m, s = duration.split(':')
                        duration = int(h) * 3600 + int(m) * 60 + int(s)
                        print(duration)
                    if title is not None:
                        print(title)
                        if title != Path(video_file).name:
                            vlc_remote.change_title_mkv(video_file)
                else:
                    duration = metadata
        else:
            metadata_tag = streams[0].get('duration')
            duration = int(metadata_tag.split('.')[0])
            print(duration)

    except ffmpeg._run.Error:
        print('wrong format')
        duration = None

    print(duration)
    return duration


""" Update list of video  files """


def update_lib_serials(category, files_in_db, files_paths, default_poster):
    serials_in_db = set(files_in_db)
    serials_on_disk = set()
    seasons_in_db = set()
    seasons_on_disk = set()
    series_in_db = set()
    series_on_disk = set()
    seasons = db.query(Seasons).all()
    poster_name = Path(default_poster).name
    for item in seasons:
        print(item.file_path)
        seasons_in_db.add(Path(item.file_path))
    series = db.query(Series).all()
    for item in series:
        series_in_db.add(Path(item.file_path))

    for rec in files_paths:
        files_path = rec
        serials = files_path.iterdir()
        for serial in serials:
            if serial.is_dir:
                serials_on_disk.add(str(serial))
    add_serials = serials_on_disk.difference(serials_in_db)
    for item in add_serials:
        file_name = str(Path(item).name)
        new_rec = VideoFiles(category=category,
                             file_path=item,
                             file_name=file_name,
                             poster=default_poster,
                             poster_filename=poster_name)
        db.add(new_rec)
    db.commit()
    db.close()

    for item in serials_on_disk:
        print(item)
        season_paths = Path(item).iterdir()
        for season_path in season_paths:
            if season_path.is_dir():
                seasons_on_disk.add(season_path)
    add_seasons = seasons_on_disk.difference(seasons_in_db)
    for item in add_seasons:
        name = str(Path(item).name)

        parent_name = str(Path(item).parent)
        serial_id = db.query(VideoFiles).filter_by(file_path=parent_name).one_or_none()
        new_rec = Seasons(videofiles_id=serial_id.id,
                          file_name=name,
                          name=name,
                          file_path=str(item),
                          poster=default_poster,
                          poster_filename=poster_name)
        db.add(new_rec)
    db.commit()
    db.close()
    for item in seasons_on_disk:
        series = item.iterdir()
        for episode in series:
            if episode.suffix in video_format:
                series_on_disk.add(episode)
    add_series = series_on_disk.difference(series_in_db)
    for item in add_series:
        name = str(Path(item).stem)
        parent_name = str(Path(item).parent)
        season_id = db.query(Seasons).filter_by(file_path=parent_name).one_or_none()
        new_rec = Series(seasons_id=season_id.id, name=name, file_path=str(item), poster=default_poster,
                         file_name=str(item.name), poster_filename=poster_name)
        db.add(new_rec)
        # if Path(item).suffix == '.mkv' or Path(item).suffix == '.MKV':
        # change_title_mkv(item)
    db.commit()
    db.close()

    return add_series


def update_library(lib_id):
    categories = db.query(Categories).filter_by(name=lib_id).one_or_none()
    default_poster = categories.poster
    all_files = db.query(VideoFiles).filter_by(category=categories.category).all()
    files_in_db = set()
    files_on_disk = set()
    files_paths = set()
    for rec in all_files:
        files_in_db.add(rec.file_path)
    for rec in categories.library:
        files_paths.add(Path(rec.category_path))
    if categories.category in multi_file_video:
        add_files = update_lib_serials(categories.category, files_in_db, files_paths, default_poster)
    else:
        for files_path in files_paths:
            files_path = Path(files_path)
            sub_dir = []
            for item in files_path.iterdir():
                if item.is_dir():
                    sub_dir.append(item)

                elif item.suffix in video_format:
                    files_on_disk.add(str(item))
            if len(sub_dir) > 0:
                while len(sub_dir) > 0:
                    for folder in sub_dir:
                        files_subdir = folder.iterdir()
                        for file_subdir in files_subdir:
                            if file_subdir.is_dir():
                                sub_dir.append(file_subdir)
                            else:
                                if file_subdir.suffix in video_format:
                                    files_on_disk.add(str(file_subdir))
                        sub_dir.remove(folder)

        add_files = files_on_disk.difference(files_in_db)
        for item in add_files:
            print(item)
            video_len = video_duration(item)
            file_name = Path(item).name
            poster_name = Path(default_poster).name
            new_rec = VideoFiles(category=categories.category,
                                 file_path=str(item),
                                 file_name=file_name,
                                 video_length=video_len,
                                 poster=default_poster,
                                 poster_filename=poster_name)
            db.add(new_rec)
            # if Path(item).suffix == '.mkv' or Path(item).suffix == '.MKV':
            #     change_title_mkv(item)

        delete_files_from_db = files_in_db.difference(files_on_disk)
        for item in delete_files_from_db:
            delete_rec = db.query(VideoFiles).filter_by(file_path=item).one_or_none()
            delete_rec.active = False
        db.commit()
        db.close()
    return add_files


# update_library('Фильмы')
# update_library('Сериалы')


def length_video_vlc():
    tables = ['VideoFiles', 'Series']
    for table in tables:
        video_without_len = db.query(getattr(models, table)).filter_by(video_length=None).all()
        for video in video_without_len:
            print(video.file_name)
            open_vlc(video.file_path)
            sleep(5)
            len_video = get_time_data('get_length')
            while len_video is None:
                sleep(2)
                len_video = get_time_data('get_length')
            print(len_video)
            video.video_length = len_video
            db.commit()
    db.close()


def change_title_for_all():
    tables_video_files = ['Videos', 'Series']
    for table in tables_video_files:
        model_service = getattr(models, table)
        files = db.query(model_service).all()
        for file in files:
            if Path(file.file_path).suffix == '.mkv' or Path(file.file_path).suffix == '.MKV':
                change_title_mkv(file)
                print(file.file_path)


def backup_bd():
    dt = datetime.today()
    file_name = f'{dt.year}-{dt.month}-{dt.day}_{dt.hour}-{dt.minute}-{dt.second}'
    backup_path = Path('backup', f'{file_name}.db')
    bd_path = 'video_base.db'
    shutil.copy(bd_path, backup_path)
    rec = BackupBd(file_path=str(backup_path), file_name=str(backup_path.name))
    db.add(rec)
    db.commit()
    db.close()
    print(file_name)


def restore_bd(file_name):
    rec = db.query(BackupBd).filter_by(file_name=file_name).one_or_none()
    restore_path = 'video_base.db'
    bd_path = rec.file_path
    shutil.copy(bd_path, restore_path)


def get_backups():
    all_rec = db.query(BackupBd).order_by(BackupBd.created_at.desc()).all()
    list_records = []
    for item in all_rec:
        rec = {'id': item.id, 'file_path': item.file_path, 'file_name': item.file_name}
        list_records.append(rec)
    return list_records
