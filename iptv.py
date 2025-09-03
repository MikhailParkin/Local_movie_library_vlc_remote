import requests
import gzip
import shutil
import datetime
from pathlib import Path

from sqlalchemy.orm import aliased
from video_base import Session, engine
from video_base import Playlist, EpgProgrammes, Settings
from sqlalchemy import inspect, select
from lxml import etree
import pytz
from requests.exceptions import ChunkedEncodingError, ConnectionError
import time

playlist_path = r'public\iptv\only4tv_full.m3u8'
playlist_file = 'only4tv_full.m3u8'
epg_path = r'public\iptv\epg.xml'
epg_original_path = r'public\iptv\epg_original.xml'
epg_url = 'https://epg.online/epg.xml.gz'
# epg_url_original = 'http://only4.tv/epg/epg.xml'
epg_file = 'epg.xml.gz'
epg_file_original = 'epg_original.xml'
output_directory = Path(Path.cwd(), 'public', 'iptv')
groups = ['КиноПлюс', 'Познавательные', 'UHD', 'Кино', 'Детские', 'Спорт', 'ХХХ']

db = Session(autoflush=False, bind=engine)


def inspect_table(table_name):
    inspect_engine = inspect(engine)
    print(inspect_engine.has_table(table_name))
    return inspect_engine.has_table(table_name)


def download_file(kind_file, url):
    start_time = datetime.datetime.now()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'uk,en-US;q=0.9,en;q=0.8,ru;q=0.7',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }
    if kind_file == 'playlist':
        find_url = db.query(Settings).first()
        url = find_url.playlist_url

        print('Download start!')
        r = requests.get(url, headers=headers)
        with open(fr'{output_directory}/{playlist_file}', 'wb') as f:
            f.write(r.content)
            print('File Download!')
            file_type = 'Playlist Download'

    elif kind_file == 'epg':
        print('Download start!')
        r = requests.get(url,  headers=headers)
        with open(fr'{output_directory}/{epg_file}', 'wb') as f:
            f.write(r.content)
            print('File Download!')
        with gzip.open(fr'{output_directory}/{epg_file}', 'rb') as f_in:
            with open(fr'{output_directory}/epg.xml', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                print('Done')
                file_type = 'EPG Download'
    return file_type, start_time


def download_file_epg_original(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }
    start_time = datetime.datetime.now()
    print('Download start!')
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True, headers=headers)
            with open(fr'{output_directory}/{epg_file_original}', 'wb') as f:
                f.write(response.content)
                print('File Download!')
                file_type = 'EPG Download'
            break  # Exit loop if successful
        except (ChunkedEncodingError, ConnectionResetError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print("Max retries reached. Could not download XML.")
                raise  # Re-raise the exception if all retries fail
                file_type = 'EPG download error!'
    return file_type, start_time


# download_file_epg_original()
# download_file('playlist')
# download_file('epg')


def list_channel(playlist):

    with open(playlist, 'r', encoding='utf-8') as f:
        playlist_list = []
        i = 0
        for line in f:
            dict_param = {}
            print(line)
            if line.startswith('#EXTINF:'):
                list_param = line.split(',')
                if len(list_param) > 1:
                    dict_param['channel_name'] = list_param[1].rstrip()

                for item in list_param[0].split(' '):
                    if item.startswith('#EXTINF') is False and item.count('=') > 0:
                        param = item.split('=')
                        if param[1].startswith('"'):
                            dict_param[param[0]] = param[1].strip('"')
                        else:
                            dict_param[param[0]] = param[1]
                playlist_list.append(dict_param)
            elif line.startswith('#EXTGRP'):
                list_param = line.split(':')
                dict_param['group'] = list_param[1].rstrip()
                playlist_list.append(dict_param)
            if line.startswith('http'):
                dict_param_change = playlist_list[i]
                dict_param_change['url'] = line.rstrip()
                i += 1
    db.query(Playlist).delete()
    db.commit()
    db.close()
    for item in playlist_list:
        if item.get('group-title') in groups:
            uri = item['url']
            uri_part = uri.split('/')
            channel_number = uri_part[3]
            token_part = uri_part[4].split('.')
            m3u_token = token_part[1]
            print(item)
            new_rec = Playlist(channel_name=item['channel_name'],
                               catchup_days=item['catchup-days'],
                               catchup_type=item['catchup-type'],
                               tvg_id=item['tvg-id'],
                               group_title=item['group-title'],
                               tvg_logo=item['tvg-logo'],
                               url=item['url'],
                               channel_number=channel_number,
                               m3u_token=m3u_token)
            db.add(new_rec)
    db.commit()
    db.close()
    return datetime.datetime.now()


# list_channel(playlist_path)


def epg_read(epg):
    start_time = datetime.datetime.now()
    msk_tz = datetime.timezone(datetime.timedelta(hours=3))
    playlist = db.query(Playlist).all()
    channels = []
    actual_epg_time_dict = {}
    dict_data = []
    for favorite_channel in playlist:
        channels.append(favorite_channel.tvg_id)
        catchup_days = int(favorite_channel.catchup_days)
        actual_epg_date = start_time - datetime.timedelta(days=int(catchup_days))
        actual_epg_time_dict[favorite_channel.tvg_id] = actual_epg_date
    channel_id_map = {channel.tvg_id: channel.id for channel in playlist}
    db.close()
    db.query(EpgProgrammes).delete()
    db.commit()
    db.close()
    context = etree.iterparse(epg, events=('start', 'end'))
    i = 0

    for event, element in context:
        if event == 'start' and element.tag == 'programme':
            attribute_value = element.get('channel')
            start = datetime.datetime.strptime(element.get('start'), '%Y%m%d%H%M%S %z').replace(tzinfo=None)

            if attribute_value in channels and actual_epg_time_dict.get(attribute_value) <= start:
                stop = element.get('stop')
                title_element = element.findall('./title')
                if title_element:
                    for child in title_element:
                        title = child.text
                else:
                    title = 'Без назавания'
                desc_element = element.findall('./desc')
                if desc_element:
                    for desc in desc_element:
                        describe = desc.text
                else:
                    describe = ''
                rec = {'programme_start': start,
                       'programme_end': datetime.datetime.strptime(stop, '%Y%m%d%H%M%S %z').replace(tzinfo=None),
                       'title': title,
                       'describe': describe,
                       'tvg_id': attribute_value,
                       'playlist_id': channel_id_map.get(attribute_value)}

                dict_data.append(rec)
                print(i)
                i += 1
        elif event == 'end' and element.tag == 'programme':
            element.clear()
            while element.getprevious() is not None:
                del element.getparent()[0]
    pars_time = datetime.datetime.now()
    db.bulk_insert_mappings(EpgProgrammes, dict_data)
    db.commit()
    db.close()
    end_time = datetime.datetime.now()
    print('Start: ', start_time)
    print('End parsing: ', pars_time)
    print('Stop: ', end_time)

    return end_time


def convert_date(date):
    datetime_object = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    print(datetime_object)
    return datetime_object


def get_epg_on_channel_now(date_now, tvg_id):
    prog_now = db.query(EpgProgrammes).filter_by(tvg_id=tvg_id).filter(EpgProgrammes.programme_start <= date_now,
                                                                       EpgProgrammes.programme_end >= date_now).first()
    if prog_now:
        programme = {'title': prog_now.title, 'start': prog_now.programme_start}
    else:
        programme = {'title': 'Без названия', 'start': 'None'}
    db.close()
    return programme


def epg_for_list_channel_now(data):
    date_now = convert_date(data['date'])
    current_date = date_now + datetime.timedelta(hours=3)
    list_epg_now = {}
    for channel in data['channels']:
        prog = get_epg_on_channel_now(current_date, channel)
        list_epg_now[channel] = prog
    print(list_epg_now)
    return list_epg_now


def find_arch_data(prog_start, prog_end):
    duration = int((prog_end - prog_start).total_seconds())
    msk_tz = pytz.timezone('Europe/Moscow')
    msk_time = msk_tz.localize(prog_start)
    utc_start_time = msk_time.astimezone(pytz.utc)
    time_start_timestamp = int(utc_start_time.timestamp())
    return time_start_timestamp, duration


def epg_for_one_channel(data):
    date = convert_date(data['date'])
    channel = db.query(Playlist).filter_by(tvg_id=data['channel']).first()
    catchup_days = channel.catchup_days
    uri = channel.url
    uri_part = uri.split('/')
    channel_id = uri_part[3]
    token_part = uri_part[4].split('.')
    m3u_token = token_part[1]
    db.close()
    history = date - datetime.timedelta(days=int(catchup_days))
    epg_history = db.query(EpgProgrammes).filter_by(tvg_id=data['channel']).\
        filter(EpgProgrammes.programme_end >= history).all()
    epg_list = []
    for item in epg_history:
        start_timestamp, duration = find_arch_data(item.programme_start, item.programme_end)
        arch_url = f'http://r.only4.online/{channel_id}/tracks-v1a1/index-{start_timestamp}-{duration}.{m3u_token}'
        rec = {'start': item.programme_start, 'end': item.programme_end,
               'title': item.title, 'desc': item.describe, 'url': arch_url}
        epg_list.append(rec)
        print(rec)
    return epg_list


# epg_for_one_channel_example = {'date': '2025-08-1T13:58:09.729Z', 'channel': 'kinoxit'}

# epg_for_one_channel(epg_for_one_channel_example)


def update_epg():
    get_epg_url = db.query(Settings).filter_by(id=1).one_or_none()
    if get_epg_url:
        url = get_epg_url.epg_url
        file_type = url.split('.')[-1]
        if file_type == 'gz':
            result, start = download_file('epg', url)
            file_name = epg_path
        elif file_type == 'xml':
            result, start = download_file_epg_original(url)
            file_name = epg_original_path

    if result == 'EPG Download':
        end = epg_read(file_name)
    return f'EPG Updated! Start time: {start} - End time: {end}'


def update_playlist():
    result, start = download_file('playlist')
    if result == 'Playlist Download':
        end = list_channel(playlist_path)
    return f'Playlist Updated! Start time: {start} - End time: {end}'


# update_playlist()
# update_epg()


def select_channels_by_group(group_name):
    channels = db.query(Playlist).filter_by(group_title=group_name).all()
    return channels


def epg_for_group_channel_now(group):
    date_now = datetime.datetime.now()
    list_epg_now = {}
    prog_now = db.query(EpgProgrammes).filter(EpgProgrammes.programme_start <= date_now,
                                              EpgProgrammes.programme_end >= date_now).all()
    for prog in prog_now:
        list_epg_now[prog.playlist_id] = prog.title
    print(list_epg_now)
    return list_epg_now


def epg_for_channel(channel_id):
    date_now = datetime.datetime.now()
    channel = db.query(Playlist).filter_by(tvg_id=channel_id).first()
    channel_number = channel.channel_number
    m3u_token = channel.m3u_token
    catchup_days = channel.catchup_days
    history = date_now - datetime.timedelta(days=int(catchup_days))
    exist_epg = []
    for item in channel.epg_programme:
        if item.programme_end >= history:
            start_timestamp, duration = find_arch_data(item.programme_start, item.programme_end)
            arch_url = f'http://r.only4.online/{channel_number}/tracks-v1a1/index-{start_timestamp}-{duration}.{m3u_token}'
            rec = {'start': item.programme_start, 'end': item.programme_end,
                   'title': item.title, 'desc': item.describe, 'url': arch_url}
            exist_epg.append(rec)
    db.close()
    return exist_epg


def test(tvg_id):
    date_now = datetime.datetime.now()
    channel = db.query(Playlist).filter_by(tvg_id=tvg_id).first()
    channel_number = channel.channel_number
    m3u_token = channel.m3u_token
    catchup_days = channel.catchup_days
    history = date_now - datetime.timedelta(days=int(catchup_days))
    # exist_epg = channel.epg_programme.filter(EpgProgrammes.programme_end >= history).all
    exist_epg = []
    for item in channel.epg_programme:
        if item.programme_end >= history:
            start_timestamp, duration = find_arch_data(item.programme_start, item.programme_end)
            arch_url = f'http://r.only4.online/{channel_number}/tracks-v1a1/index-{start_timestamp}-{duration}.{m3u_token}'
            rec = {'start': item.programme_start, 'end': item.programme_end,
                   'title': item.title, 'desc': item.describe, 'url': arch_url}
            exist_epg.append(rec)
    db.close()
    return exist_epg

# q = epg_for_channel('bcu-action')
# for item in q:
#     print(item)
# test_date = 'datetime.datetime(2025, 8, 25, 17, 9)'
# test('bcu-action')


# def test():
#     group = ['КиноПлюс', 'Познавательные', 'UHD']
#     for item in group:
#         epg_alias = aliased(EpgProgrammes)
#         query = (
#             select(Playlist).filter_by(group_title=item)
#             .outerjoin(epg_alias, Playlist.id == epg_alias.playlist_id)
#             .where(epg_alias.playlist_id.is_(None))
#         )
#         result = db.execute(query).scalars().all()
#         for rec in result:
#             print(rec.tvg_id)
#
#
# test()
