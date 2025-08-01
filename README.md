# Local_movie_library_vlc_remote
A small application for creating a local database of movies and play it on VLC Player whith remote control.

Небольшое приложение для создания локальной базы фильмов, сериалов и т.д.,  добавления описаний к  ним, редактирования названий, добавления постеров без изменения оригинальных файлов.

Своеобразный медиаплеер. Запускаем на пк с контентом подключеном к тв, заполняем бд, затем,  например с телефона или планшета, сидя на диване, листаем постеры фильмов или сериалов, выбираем нужный и он запускается в проигрывателе VLC в полноэкранном режиме. В разделе "управление" видео можно поставить на паузу, выключить, отключить субтитры, выбрать аудиодорожку, продолжить с места последнего  просмотра  (при нажатии "Пауза" запись о текущей позиции просмотра добавляется в бд). 

Для заполнения таблицы видеофайлов  указывается путь к каталогу с контентом. Для заполнения необходимы ffmpeg прописанная в PATH (для определиния длины видео) и mkvpropedit, лежащая в корне со скриптом (для исправления  "title" в mkv контейнере, чтобы соответствовал имени файла).

Также есть IPTV плеер с возможностью загрузки EPG и просмотра архива передач. Тестировался только на одном провайдере IPTV, в плейлисте должны быть ссылки на логотипы каналов (tvg-logo), tvg-id, просмотр архива возможен с catchup-type="flussonic", также используется catchup-days.



A small application for creating a local database of movies, TV shows, etc., adding descriptions, editing titles, and adding posters without altering the original files.

It's a unique media player. You run it on a PC connected to a TV with your content library. You populate the database. Then, for example, while sitting on the couch, you can browse movie or TV show posters from your phone or tablet. You select the desired item, and it launches in fullscreen mode in the VLC player. In the "Control" section, you can pause the video, stop it, disable subtitles, select an audio track, or resume playback from the last viewed position (when "Pause" is pressed, the current playback position is recorded in the database).

To populate the video files table, you specify the path to the directory containing the content. Populating the database requires ffmpeg to be in the system PATH (to determine video duration) and mkvpropedit located in the script's root directory (to correct the "title" field inside MKV containers to match the filename).

Additionally, there's an IPTV player with the ability to load EPG (Electronic Program Guide) and view program archives. It was only tested with one specific IPTV provider. The playlist must contain links to channel logos (tvg-logo) and tvg-id entries. Archive viewing is possible with catchup-type="flussonic"; catchup-days is also utilized.
