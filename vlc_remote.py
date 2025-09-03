import socket
import subprocess
from time import sleep
from pathlib import Path
import keyboard

import manage_db as db_query

"""
+----[ Команды дистанционного управления ]

|
| add XYZ  . . . . . . . .  добавить XYZ в плейлист

| enqueue XYZ  . . . . . .  добавить XYZ в очередь плейлиста

| playlist . . . . . . . .  показать имеющиеся позиции в плейлисте

| play . . . . . . . . . .  воспроизвести поток

| stop . . . . . . . . . .  остановить поток

| next . . . . . . . . . .  следующая позиция в плейлисте
| prev . . . . . . . . . .  предыдущая позиция в плейлисте

| goto . . . . . . . . . .  перейти к позиции по индексу

| repeat [on|off] . . . . . вкл./выкл. повтора позиций в плейлисте

| loop [on|off] . . . . . . вкл./выкл. зацикливание плейлиста

| random [on|off] . . . . . вкл./выкл. случайный порядок

| clear . . . . . . . . . . очистить плейлист

| status . . . . . . . . .  текущий статус плейлиста

| title [X]  . . . . . . .  задать/получить заглавие текущей позиции

| title_n  . . . . . . . .  следующее заглавие в текущей позиции

| title_p  . . . . . . . .  предыдущее заглавие в текущей позиции

| chapter [X]  . . . . . .  задать/получить главу текущей позиции

| chapter_n  . . . . . . .  следующая глава в текущей позиции

| chapter_p  . . . . . . .  предыдущая глава в текущей позиции

|
| seek X . . . . . . . . .  переход ко времени (в сек.), например, «seek 12»
| pause  . . . . . . . . .  вкл./выкл. паузу

| fastforward  . . . . . .  установить максимальную скорость

| rewind  . . . . . . . . . установить минимальную скорость

| faster . . . . . . . . .  ускоренное воспроизведение потока

| slower . . . . . . . . .  замедленное воспроизведение потока

| normal . . . . . . . . .  нормальное воспроизведение потока
| frame. . . . . . . . . .  покадровое воспроизведение

| f [on|off] . . . . . . .  вкл./выкл. полноэкранный режим

| info . . . . . . . . . .  информация о текущем потоке

| stats  . . . . . . . . .  вывод статистической информации
| get_time . . . . . . . .  время с начала воспроизведения потока (сек.)

| is_playing . . . .  . . . 1 - если поток проигрывается, 0 - в противном случае

| get_title . . . . . . . . название текущего потока

| get_length . . . . . . .  длина текущего потока
|
| volume [X] . . . . . . .  задать/получить значение уровня громкости

| volup [X]  . . . . . . .  увеличить уровень громкости на X делений

| voldown [X]  . . . . . .  уменьшить уровень громкости на X делений

| adev [устройство]  . . .  задать/получить аудиоустройство

| achan [X]. . . . . . . .  задать/получить аудиоканалы

| atrack [X] . . . . . . .  задать/получить аудиодорожку

| vtrack [X] . . . . . . .  задать/получить видеодорожку

| vratio [X]  . . . . . . . задать/получить соотношение сторон видео

| vcrop [X]  . . . . . . .  задать/получить режим кадрирования видео

| vzoom [X]  . . . . . . .  задать/получить значение увеличения видео

| snapshot . . . . . . . .  сделать снимок видео

| strack [X] . . . . . . . . .  установить/получить дорожку субтитров

| key [название клавиши] . . . . . .  симулировать нажатие горячей клавиши


| help . . . . . . . . . .  эта справка

| logout . . . . . . . . .  выход (при соединении через сокет)

| quit . . . . . . . . . .  закрыть VLC


"""


def open_vlc(file_path):
    command_send('quit')
    vlc_path = r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe'
    subprocess.Popen([vlc_path, file_path, '-f', '-I rc --rc-host localhost:9090'])
    print(rf'"{file_path}"')





def command_send(msg):
    list_data = []
    sock = socket.socket()
    sock.settimeout(1)
    output = ''
    try:
        sock.connect(('localhost', 9090))
        sock.sendall(bytes(msg + '\n', 'utf-8'))
        while output == '' or output.startswith('pos:') or output.startswith('|') or output.startswith('+'):
            data = sock.recv(1024)
            output = data.decode('utf-8')
            if output.startswith('pos') is not True and output.startswith('+--') is not True:
                list_data.append(output.rstrip('\r\n'))

            # print(output)

        sock.close()
        print(list_data)
    except socket.error as e:
        print(e)
    if len(list_data) == 0:
        list_data.append('Socket close')

    print(list_data)
    return list_data


def get_time_data(msg):
    # msg = 'get_time'
    # msg = 'get_length'
    receive_data = command_send(msg)
    if len(receive_data) > 0 and receive_data[0].isdigit():
        video_length = int(receive_data[0])
    else:
        video_length = None
    print(video_length)
    return video_length


def get_audio_stream():
    msg = "atrack"
    receive_data = command_send(msg)
    streams = []
    i = 1
    for stream in receive_data:
        if stream.startswith('| ') and not stream.startswith('| -1'):
            streams.append({'stream_index': i, 'title': stream.strip('| ')})
            i += 1

    print('receive_data: ', receive_data)
    print('streams: ', streams)
    return streams


def get_info():
    msg = "info"
    receive_data = command_send(msg)
    video_info = []
    for line in receive_data:
        if line.startswith('| '):
            video_info.append(line.strip('| '))

    print('receive_data: ', receive_data)
    print('info: ', video_info)
    return video_info


def get_file_name():
    msg = "get_title"
    receive_data = command_send(msg)
    sleep(1)
    receive_data = command_send(msg)
    if len(receive_data) > 0:
        title = receive_data[0]
        print('title : ', title)
    return title


def get_playlist():
    msg = 'playlist'
    receive_data = command_send(msg)


def set_command(command):
    if command == 'info':
        file_name = get_file_name()
        data = db_query.find_video_by_file_name(file_name)
    elif command == 'pause':
        try:
            title = get_file_name()
            video = db_query.find_video_by_file_name(title)
            position = get_time_data('get_time')
            db_query.set_last_position(video, position)
            command_send('pause')
            data = {'title': title, 'position': position}
        except:
            command_send('pause')
            data = {'title': None, 'position': None}
    elif command == 'audio_list':
        data = get_audio_stream()
    elif command == 'sub_off':
        data = command_send('strack -1')

    else:
        data = command_send(command)
    return data


def change_title_mkv(file_path):
    tool_path = r'mkvpropedit.exe'
    file_name = Path(file_path).name
    command = rf'{tool_path} "{file_path}" -e info -s title="{file_name}"'
    print(command)
    subprocess.run(command)


def set_playlist(playlist: list):
    if playlist  is not None:
        for video in playlist:
            command = f'enqueue {video}'
            command_send(command)


def minimize_all_windows():
    keyboard.press_and_release('win+d')
    return 'Minimized'


# minimize_all_windows()
test_mkv = r"W:\Фильмы\1080p.Predator.Ultimate.Hunter.Edition.1987.DKom.[BDRip.H264.DTSRus.AC3Rus.DTSRus.DTSRus.DTSRus.DTSEng].mkv"


def start_stream(mkv):
    app_path = Path.cwd()
    temp_path = Path(app_path, 'static', 'temp')
    temp_fragment = (temp_path, 'stream_%03d.ts')
    temp_file = Path(temp_path, 'output.m3u8')
    ffmpeg_command = f'ffmpeg -i "{mkv}" -codec:v libx264 -profile:v main -preset:v slow -b:v 2000k -maxrate 2500k -bufsize 4000k -codec:a aac -b:a 128k -f hls -hls_time 10 -hls_list_size 5 -hls_flags delete_segments+append_list -hls_segment_filename "{temp_fragment}" {temp_file}'
    print(ffmpeg_command)
    subprocess.run(ffmpeg_command)


# open_vlc(test_mkv)
# set_command('audio_list')
# command_send('title')
# command_send('pause')


def check_vlc_status():
    response = command_send('title')
    duration = 0
    time = 0
    if response[0] == 'Socket close':
        status = 'Close'
        title = 'В данный момент ничего не воспроизводится'
    elif response[0] == 'Для продолжения нажмите кнопку паузы.':
        status = 'Pause'
    else:
        status = 'Playing'

    if status == 'Pause' or status == 'Playing':
        title = command_send('get_title')
        title = title[0]
        duration = get_time_data('get_length')
        time = get_time_data('get_time')
    return {'status': status, 'title': title, 'duration': duration, 'time': time}


# print(check_vlc_status())
iptv = "http://r.only4.online/1116/video.m3u8?token=9MLHHqDt5t"
# open_vlc(iptv)
