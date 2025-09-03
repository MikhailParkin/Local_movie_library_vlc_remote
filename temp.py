from datetime import datetime
from lxml import etree

from video_base import Session, Base, engine
from video_base import Playlist, Favorite, EpgProgrammes

db = Session(autoflush=False, bind=engine)

test = {'name': 'Śpiewające brzdące', 'desc': '', 'start': '20250716100000', 'stop': '20250716110000', 'channel': '4fun-gold'}

epg_path = r'static\iptv\epg.xml'

# programme = EpgProgrammes(programme_start=datetime.strptime(test.get('start'), '%Y%m%d%H%M%S'),
#                           programme_end=datetime.strptime(test.get('stop'), '%Y%m%d%H%M%S'),
#                           title=test.get('name'),
#                           describe=test.get('desc'),
#                           tvg_id=test.get('channel')
#                           )
# db.add(programme)
# db.commit()
# db.close()
# channel = db.query(Playlist).filter_by(tvg_id='2na2').one_or_none()
# programms = db.query(EpgProgrammes).filter_by(tvg_id='bcu-action').all()
# for item in programms:
#     print(item.title, ' ', item.programme_start)

test2 = '<programme start="20250803225500 +0300" stop="20250803235500 +0300" channel="kinosemiya"><desc>79 год н. э.</desc><title>х/ф Помпеи</title></programme>'
#
# print(test2.find('channel'))
# print(test2.find('>'))
# print(test2[68:88].split('"')[1])

epg_for_list_channel = {'date': '2025-07-25T14:12:57.082Z',
                        'channels': ['bcu-action',
                                     'bcu-catastrophe',
                                     'bcu-cinema',
                                     'bcu-cinemaplus',
                                     'bcu-comedy',
                                     'bcu-comedy',
                                     'bcu-history',
                                     'bcu-fantastic',
                                     'bcu-kinorating',
                                     'bcu-marvel',
                                     'bcu-marvel',
                                     'bcu-premiere',
                                     'bcu-romantic',
                                     'bcu-russian',
                                     'bcu-vhs',
                                     'bcu-kinozal-prem-1',
                                     'bcu-kinozal-prem-1',
                                     'bcu-kinozal-prem-2',
                                     'bcu-kinozal-prem-2',
                                     'bcu-kinozal-prem-3']}


def convert_date(date_string):
    datetime_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    print(datetime_object)
    return datetime_object


def get_epg_on_channel_now(date_now, tvg_id):
    prog_now = db.query(EpgProgrammes).filter_by(tvg_id=tvg_id).filter(EpgProgrammes.programme_start <= date_now,
                                                                       EpgProgrammes.programme_end >= date_now).first()
    programme = {'title': prog_now.title}
    db.close()
    return programme


def epg_for_list_channel_now(data):
    date_now = convert_date(data['date'])
    list_epg_now = {}
    for channel in data['channels']:
        prog = get_epg_on_channel_now(date_now, channel)
        list_epg_now[channel] = prog
    print(list_epg_now)
    return list_epg_now


# epg_for_list_channel_now(epg_for_list_channel)
# convert_date(epg_for_list_channel)


def parse_large_xml_event(xml_file_path):
    """
    Парсит большой XML файл, используя event-based парсинг с lxml.

    Args:
        xml_file_path: Путь к XML файлу.
    """
    start_time = datetime.now()

    playlist = db.query(Playlist).all()
    channels = []
    for favorite_channel in playlist:
        channels.append(favorite_channel.tvg_id)
    db.close()

    context = etree.iterparse(xml_file_path, events=('start', 'end'))

    for event, element in context:
        if event == 'start' and element.tag == 'programme':
            # Обработка начала элемента 'some_tag'
            # Например, извлечение атрибутов
            attribute_value = element.get('channel')
            if attribute_value in channels:
                start = element.get('start')
                stop = element.get('stop')
                print(f"channel: {attribute_value} start: {start} - end: {stop}")
                title_element = element.findall('./title')
                if title_element:
                    for child in title_element:
                        print(child.text)
                desc_element = element.findall('./desc')
                if desc_element:
                    for desc in desc_element:
                        print(desc.text)

        elif event == 'end' and element.tag == 'programme':
            element.clear()
            while element.getprevious() is not None:
                del element.getparent()[0]
    end_time = datetime.now()
    print('Start: ', start_time)
    print('Stop: ', end_time)


# parse_large_xml_event(epg_path)

epg_line = r'<programme start="20240505233400 +0300" stop="20240506010800 +0300" channel="bcu-filmystic"><category lang="ru">Фильм</category><desc lang="ru">Желая заработать, видеоблогер собрал команду молодых людей и отправил их в «одно из самых страшных мест на планете» - закрытую в 1979 году психиатрическую больницу Конджиам, где покончили с собой 42 пациента и где теперь водятся их привидения. Парни и девушки должны были вести прямой эфир из страшных помещений больницы, собирая десятки тысяч лайков. Однако главная задача любителей хайпа - добраться до палаты №402, которая не открывалась более 30 лет и где, возможно, сокрыта какая-то страшная тайна. Молодые люди и не предполагали, какой кошмар ожидает их за дверями этой комнаты… Корея Южная</desc><title lang="ru">х/ф Психиатрическая больница Конджиам</title></programme>'

str_time = "20240506010800 +0300"

epg_for_list_channel = {'date': '2025-07-29T10:03:04.751Z', 'channels': ['bcu-action', 'bcu-catastrophe', 'bcu-cinema', 'bcu-cinemaplus', 'bcu-comedy', 'bcu-comedy', 'bcu-history', 'bcu-fantastic', 'bcu-kinorating', 'bcu-marvel', 'bcu-marvel', 'bcu-premiere', 'bcu-romantic', 'bcu-russian', 'bcu-vhs', 'bcu-kinozal-prem-1', 'bcu-kinozal-prem-1', 'bcu-kinozal-prem-2', 'bcu-kinozal-prem-2', 'bcu-kinozal-prem-3']}
epg_for_one_channel_example = {'date': '2025-07-25T13:58:09.729Z', 'channel': 'kinoxit'}


def test_xml_event(xml_file_path, channel):
    """
    Парсит большой XML файл, используя event-based парсинг с lxml.

    Args:
        xml_file_path: Путь к XML файлу.
    """
    start_time = datetime.now()

    context = etree.iterparse(xml_file_path, events=('start', 'end'))

    for event, element in context:
        if event == 'start' and element.tag == 'programme':
            # Обработка начала элемента 'some_tag'
            # Например, извлечение атрибутов
            attribute_value = element.get('channel')
            if attribute_value == channel:
                start = element.get('start')
                stop = element.get('stop')
                print(f"channel: {attribute_value} start: {start} - end: {stop}")
                title_element = element.findall('./title')
                if title_element:
                    for child in title_element:
                        print(child.text)
                desc_element = element.findall('./desc')
                if desc_element:
                    for desc in desc_element:
                        print(desc.text)

        elif event == 'end' and element.tag == 'programme':
            element.clear()
            while element.getprevious() is not None:
                del element.getparent()[0]
    end_time = datetime.now()
    print('Start: ', start_time)
    print('Stop: ', end_time)


# test_xml_event(epg_path, 'translation-mm')
# test_xml_event(epg_path, 'bcu-action')
