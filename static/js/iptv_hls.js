document.addEventListener('DOMContentLoaded', () => {
  // Элементы интерфейса
  const videoPlayer = document.getElementById('videoPlayer');
  const listGrid = document.getElementById('listGrid');
  const listTitle = document.getElementById('listTitle');
  const listCount = document.getElementById('listCount');
  const currentChannelGroup = document.getElementById('currentChannelGroup');
  const currentProgramName = document.getElementById('currentProgramName');
  const currentProgramDesc = document.getElementById('currentProgramDesc');
  const prevPageBtn = document.getElementById('prevPageBtn');
  const nextPageBtn = document.getElementById('nextPageBtn');
  const categoriesBtn = document.getElementById('categoriesBtn');
  const epgBtn = document.getElementById('epgBtn');
  const channelsBtn = document.getElementById('channelsBtn');

  // Константы
  const PLAYLIST_URL = '/static/iptv/only4tv_full.m3u8';
  const EPG_API_URL = '/api/list_epg/channels';
  const CHANNEL_EPG_API_URL = '/api/list_epg/channel';
  const ITEMS_PER_PAGE = 20;

  // Состояние приложения
  let allChannels = [];
  let categories = {};
  let currentItems = [];
  let currentPage = 0;
  let totalPages = 0;
  let currentItemIndex = -1;
  let currentChannel = null;
  let currentEpgData = {};
  let currentView = 'categories';
  let currentCategory = null;
  let currentPrograms = [];

  // Состояние для возврата
  let previousViewState = null;
  let previousCategoryState = null;
  let previousPageState = 0;
  let previousItemIndexState = -1;
  let previousItems = [];

  // Инициализация
  loadPlaylist();

  // Обработчики событий
  prevPageBtn.addEventListener('click', () => changePage(-1));
  nextPageBtn.addEventListener('click', () => changePage(1));
  categoriesBtn.addEventListener('click', showCategoriesView);
  epgBtn.addEventListener('click', showEpgForCurrentChannel);
  channelsBtn.addEventListener('click', restorePreviousView);

  // Загрузка плейлиста
  async function loadPlaylist() {
    try {
      const response = await fetch(PLAYLIST_URL);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const playlistText = await response.text();
      parsePlaylist(playlistText);

      if (allChannels.length > 0) {
        showCategoriesView();
      }
    } catch (error) {
      console.error('Ошибка загрузки плейлиста:', error);
      alert('Ошибка загрузки плейлиста: ' + error.message);
    }
  }

  // Парсинг плейлиста
  function parsePlaylist(content) {
    const lines = content.split('\n');
    allChannels = [];
    categories = {};

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      if (line.startsWith('#EXTINF:')) {
        const channel = {};

        // Парсим атрибуты EXTINF
        const attrRegex = /([a-z-]+)="([^"]*)"/g;
        let match;
        while (match = attrRegex.exec(line)) {
          channel[match[1]] = match[2];
        }

        // Извлекаем название канала
        const nameMatch = line.match(/,(.*)$/);
        channel.name = nameMatch ? nameMatch[1].trim() : '';

        // Читаем следующую строку (URL)
        const urlLine = lines[++i]?.trim();
        if (urlLine && urlLine.startsWith('http')) {
          channel.url = urlLine;
          allChannels.push(channel);

          // Группируем по категориям
          const groupTitle = channel['group-title'] || 'Без категории';
          if (!categories[groupTitle]) {
            categories[groupTitle] = [];
          }
          categories[groupTitle].push(channel);
        }
      }
    }
  }

  // Показать список категорий
  function showCategoriesView() {
    currentView = 'categories';
    currentItems = Object.keys(categories).map(name => ({
      name,
      count: categories[name].length
    }));

    totalPages = Math.ceil(currentItems.length / ITEMS_PER_PAGE);
    currentPage = 0;
    currentItemIndex = -1;
    listTitle.textContent = 'Категории';
    listCount.textContent = `${currentItems.length} категорий`;

    categoriesBtn.style.display = 'none';
    epgBtn.style.display = 'none';
    channelsBtn.style.display = 'none';

    renderCurrentPage();
  }

  // Показать каналы категории
  function showCategoryChannels(categoryName) {
    // Сохраняем текущее состояние для возврата
    saveCurrentState();

    currentView = 'channels';
    currentCategory = categoryName;
    currentItems = categories[categoryName] || [];
    totalPages = Math.ceil(currentItems.length / ITEMS_PER_PAGE);
    currentPage = 0;
    currentItemIndex = -1;
    listTitle.textContent = categoryName;
    listCount.textContent = `${currentItems.length} каналов`;

    categoriesBtn.style.display = 'inline-block';
    epgBtn.style.display = 'inline-block';
    channelsBtn.style.display = 'none';

    renderCurrentPage();
    loadEpgForCurrentPage();
  }

  // Показать список всех каналов
  function showChannelsList() {
    // Сохраняем текущее состояние для возврата
    saveCurrentState();

    currentView = 'channels';
    currentCategory = null;
    currentItems = allChannels;
    totalPages = Math.ceil(allChannels.length / ITEMS_PER_PAGE);
    currentPage = 0;
    currentItemIndex = -1;
    listTitle.textContent = 'Все каналы';
    listCount.textContent = `${allChannels.length} каналов`;

    categoriesBtn.style.display = 'inline-block';
    epgBtn.style.display = 'inline-block';
    channelsBtn.style.display = 'none';

    renderCurrentPage();
    loadEpgForCurrentPage();
  }

  // Сохранение текущего состояния
  function saveCurrentState() {
    previousViewState = currentView;
    previousCategoryState = currentCategory;
    previousPageState = currentPage;
    previousItemIndexState = currentItemIndex;
    previousItems = [...currentItems];
  }

  // Восстановление предыдущего вида
  function restorePreviousView() {
    if (!previousViewState) return;

    currentView = previousViewState;
    currentCategory = previousCategoryState;
    currentPage = previousPageState;
    currentItemIndex = previousItemIndexState;
    currentItems = [...previousItems];

    if (currentView === 'categories') {
      showCategoriesView();
    } else if (currentView === 'channels') {
      if (currentCategory) {
        // Восстанавливаем список каналов категории
        currentItems = categories[currentCategory] || [];
        listTitle.textContent = currentCategory;
      } else {
        // Восстанавливаем полный список каналов
        currentItems = allChannels;
        listTitle.textContent = 'Все каналы';
      }

      totalPages = Math.ceil(currentItems.length / ITEMS_PER_PAGE);
      listCount.textContent = `${currentItems.length} каналов`;

      categoriesBtn.style.display = 'inline-block';
      epgBtn.style.display = 'inline-block';
      channelsBtn.style.display = 'none';

      renderCurrentPage();
      loadEpgForCurrentPage();
    }
  }

  // Рендеринг текущей страницы
  function renderCurrentPage() {
    listGrid.innerHTML = '';

    const startIndex = currentPage * ITEMS_PER_PAGE;
    const endIndex = Math.min(startIndex + ITEMS_PER_PAGE, currentItems.length);

    for (let i = startIndex; i < endIndex; i++) {
      const item = currentItems[i];
      const itemElement = document.createElement('div');
      itemElement.className = 'list-item' + (i === currentItemIndex ? ' active' : '');
      itemElement.dataset.index = i;

      if (currentView === 'categories') {
        // Для списка категорий
        itemElement.innerHTML = `
          <div class="item-name">${item.name}</div>
          <div class="category-count">${item.count}</div>
        `;
        itemElement.addEventListener('click', () => showCategoryChannels(item.name));
      }
      else if (currentView === 'epg') {
        // Для списка программ
        itemElement.innerHTML = `
          <div class="item-time">${formatTime(item.start)}</div>
          <div class="item-name">${item.name}</div>
        `;
        itemElement.addEventListener('click', () => selectItem(i));
      }
      else {
        // Для списка каналов
        const logoHtml = item['tvg-logo'] ?
          `<img src="${item['tvg-logo']}" class="item-logo" alt="${item.name}">` :
          '<div class="item-logo"></div>';

        // Добавляем информацию о текущей передаче
        const epgInfo = currentEpgData[item['tvg-id']];
        let epgHtml = '';

        if (epgInfo) {
          // Форматируем только время (без даты) для списка каналов
          const startDate = new Date(epgInfo.start);
          const timeString = `${startDate.getHours().toString().padStart(2, '0')}:${startDate.getMinutes().toString().padStart(2, '0')}`;
          epgHtml = `<div class="item-time">${timeString} ${epgInfo.title || ''}</div>`;
        }

        itemElement.innerHTML = `
          <div class="item-number">${i + 1}</div>
          ${logoHtml}
          <div class="item-name">${item.name}</div>
          ${epgHtml}
        `;
        itemElement.addEventListener('click', () => selectItem(i));
      }

      listGrid.appendChild(itemElement);
    }
  }

  // Выбор элемента (для каналов и программ)
  function selectItem(index) {
    currentItemIndex = index;
    const item = currentItems[index];

    if (currentView === 'epg') {
      // Для программы
      playProgram(item);
    } else {
      // Для канала
      currentChannel = item;
      playChannel(item);
      updateEpgInfo(item);
    }

    renderCurrentPage();
  }

  // Воспроизведение канала

function playChannel(channel) {
  if (!channel?.url) {
    console.error('URL канала не найден!');
    return;
  }

  // Очищаем предыдущий интервал мониторинга
  clearInterval(audioCheckInterval);
  
  // Останавливаем предыдущее воспроизведение
  videoPlayer.pause();
  if (videoPlayer.hls) {
    videoPlayer.hls.destroy();
    videoPlayer.hls = null;
  }

  const hlsConfig = {
    maxBufferLength: 60,
    backBufferLength: 90,
    enableWorker: true,
    enableSoftwareAES: true,
    stretchShortVideoTrack: true,
    maxMaxBufferLength: 120,
    fragLoadingRetryDelay: 1000,
    manifestLoadingRetryDelay: 1000,
    audioStreamSwitch: true,
    maxAudioFramesDrift: 1,
    autoStartLoad: true,
    initialAudioTrack: 0,
    defaultAudioCodec: 'mp4a.40.2'
  };

  if (Hls.isSupported()) {
    const hls = new Hls(hlsConfig);
    videoPlayer.hls = hls;

    hls.loadSource(channel.url);
    hls.attachMedia(videoPlayer);

    // Флаг для отслеживания состояния восстановления
    let isRecovering = false;

    // 1. Обработчик для инициализации аудиодорожек
    hls.on(Hls.Events.AUDIO_TRACKS_UPDATED, (event, data) => {
      console.log('Аудиодорожки доступны:', hls.audioTracks);
      console.log(data)
           
      if (hls.audioTracks.length > 0) {
        // Попробуем найти AAC дорожку
        const aacTrackIndex = hls.audioTracks.findIndex(track => {
          return track.codec && track.codec.includes('mp4a');
        });
        
        // Выбираем дорожку
        const selectedTrack = aacTrackIndex !== -1 ? aacTrackIndex : 0;
        hls.audioTrack = selectedTrack;
        console.log('Аудиодорожка активирована:', hls.audioTracks[selectedTrack]);
      }
    });

    // 2. Обработка ошибок аудио
    hls.on(Hls.Events.ERROR, (event, data) => {
      console.error('HLS Error:', data.type, data.details);
      
      if (data.type === Hls.ErrorTypes.MEDIA_ERROR) {
        switch (data.details) {
          case Hls.ErrorDetails.AUDIO_TRACK_LOAD_ERROR:
          case Hls.ErrorDetails.AUDIO_TRACK_LOAD_TIMEOUT:
            if (isRecovering) return;
            isRecovering = true;
            
            console.warn('Ошибка загрузки аудио, пробуем восстановить...');
            
            // Пробуем следующую дорожку
            if (hls.audioTracks.length > 1) {
              const newTrack = (hls.audioTrack + 1) % hls.audioTracks.length;
              hls.audioTrack = newTrack;
              console.log(`Переключено на аудиодорожку ${newTrack}`);
            } 
            // Перезагрузка с другим аудиокодеком
            else {
              hls.swapAudioCodec();
              hls.recoverMediaError();
              console.log('Аудиокодек переинициализирован');
            }
            
            setTimeout(() => isRecovering = false, 2000);
            break;
        }
      }
    });
    
    // 3. Запуск воспроизведения с защитой от AbortError
    hls.on(Hls.Events.MANIFEST_PARSED, () => {
      console.log('Манифест загружен, начинаем воспроизведение');
      const playAttempt = () => {
        videoPlayer.play().catch(error => {
          // Игнорируем AbortError - это нормально при переключении
          if (error.name === 'AbortError') {
            console.log('Play request aborted, ignoring');
            return;
          }
          
          console.error('Ошибка воспроизведения:', error);
          
          // Пробуем воспроизвести с задержкой
          setTimeout(() => {
            videoPlayer.play().catch(e => {
              console.error('Повторная ошибка воспроизведения:', e);
            });
          }, 500);
        });
      };
      
      // Первая попытка воспроизведения
      playAttempt();
    });

    // 4. Отслеживание активации аудио
    hls.on(Hls.Events.AUDIO_TRACK_SWITCHED, (event, data) => {
      console.log('Аудиодорожка переключена:', data.id);
    });

  } 
  // Поддержка нативного HLS (Safari)
  else if (videoPlayer.canPlayType('application/vnd.apple.mpegurl')) {
    console.log('Используется нативный HLS');
    videoPlayer.src = channel.url;
    
    videoPlayer.play().catch(error => {
      console.error('Safari play error:', error);
    });
  } 
  else {
    console.error('Браузер не поддерживает HLS');
  }

  // 5. Запускаем мониторинг состояния аудио с задержкой
  setTimeout(startAudioMonitoring, 5000);
}

// Обновленный мониторинг состояния аудио
let audioCheckInterval;
function startAudioMonitoring() {
  clearInterval(audioCheckInterval);
  
  audioCheckInterval = setInterval(() => {
    // Не проверяем если видео на паузе или не загружено
    if (videoPlayer.paused || videoPlayer.readyState < 2) return;
    
    // Для hls.js
    if (videoPlayer.hls) {
      const audioActive = videoPlayer.hls.audioTrack !== -1;
      const audioBuffering = videoPlayer.buffered.length > 0;
      
      if (!audioActive || !audioBuffering) {
        console.warn('Проблема с аудио: активная дорожка', audioActive, 'буферизация', audioBuffering);
      }
    }
  }, 5000); // Проверяем только каждые 5 секунд
}

// Упрощенная функция восстановления аудио
function handleAudioFallback() {
  if (!videoPlayer.hls) return;
  
  console.warn('Запуск восстановления аудио...');
  
  // Просто перезагружаем текущий фрагмент
  videoPlayer.hls.recoverMediaError();
}




  // function playChannel(channel) {
  //   if (!channel?.url) {
  //     alert('URL канала не найден!');
  //     return;
  //   }
  //   console.log(channel.url)
  //   if (Hls.isSupported()) {
  //     if (videoPlayer.hls) videoPlayer.hls.destroy();

  //     const hlsConfig = {
  //       maxMaxBufferLength: 60,
  //       backBufferLength: 90,
  //       enableWebVTT: true,
  //       fragLoadingRetryDelay: 1000,
  //       manifestLoadingRetryDelay: 1000,
  //       stretchShortVideoTrack: true, // Важно для потоков с разной длительностью сегментов
  //       forceKeyFrameOnDiscontinuity: true,
  //       // Дополнительные параметры для аудио
  //       audioTrackSelection: true,
  //       defaultAudioCodec: 'mp4a.40.2', // Приоритетный аудиокодек
  //       enableAudio: true, // Гарантирует инициализацию аудио
  //       autoStartLoad: true,
  //       audioPreference: 'default', // Приоритет для AAC
  //     };

  //     const hls = new Hls(hlsConfig);
  //     hls.loadSource(channel.url);
  //     hls.attachMedia(videoPlayer);
  //     videoPlayer.hls = hls;

  //     hls.on(Hls.Events.MANIFEST_PARSED, () => {

  //      if (hls.audioTracks && hls.audioTracks.length > 0) {
  //       console.log('AAAAAudio')
  //       console.log(hls.audioTracks)
  //       hls.audioTrack = 0;
  //     }

  //       videoPlayer.play().catch(e => console.error('Ошибка воспроизведения:', e));
  //     });


  //     // Обработчик для управления аудиодорожками
  //     hls.on(Hls.Events.AUDIO_TRACKS_UPDATED, () => {
  //       if (hls.audioTracks && hls.audioTracks.length > 0) {
  //       hls.audioTrack = 0;
  //       console.log('AAAAAudio')
  //       console.log(hls.audioTracks)
  //     }
  //   });


  //     hls.on(Hls.Events.ERROR, (event, data) => {
  //       if (data.fatal) {
  //         switch (data.type) {
  //           case Hls.ErrorTypes.MEDIA_ERROR:
  //             if (data.details === Hls.ErrorDetails.AUDIO_TRACK_LOAD_ERROR) {
  //               // Пробуем следующую аудиодорожку
  //               if (hls.audioTracks && hls.audioTracks.length > 1) {
  //                 const newTrack = (hls.audioTrack + 1) % hls.audioTracks.length;
  //                 hls.audioTrack = newTrack;
  //               }
  //             }
  //             break;
  //         }
  //       }
  //     });


  //   } else if (videoPlayer.canPlayType('application/vnd.apple.mpegurl')) {
  //     videoPlayer.src = channel.url;
  //     videoPlayer.play().catch(e => console.error('Ошибка воспроизведения:', e));
  //   } else {
  //     alert('Ваш браузер не поддерживает HLS воспроизведение');
  //   }
  // }

  // Воспроизведение программы
    function playProgram(program) {

        // const videoUrl = 'http://r.only4.online/6275/tracks-v1a1/index-1753884690-3600.m3u8?token=9MLHHqDt5t'
        console.log(program)
        const videoUrl = program.url
        console.log(videoUrl)

        if (Hls.isSupported()) {
            if (videoPlayer.hls) videoPlayer.hls.destroy();
            const hls = new Hls({
                // Включите важные опции для Flussonic
                maxBufferLength: 60,
                backBufferLength: 90, // Критически важно для перемотки
                enableWebVTT: true,
                fragLoadingRetryDelay: 1000,
                manifestLoadingRetryDelay: 1000,
            });
            
            hls.loadSource(videoUrl);
            hls.attachMedia(videoPlayer);
            
            // Обработчики событий
            hls.on(Hls.Events.MANIFEST_PARSED, () => {
                console.log('Manifest parsed');
                videoPlayer.play();
            });
            
            hls.on(Hls.Events.ERROR, (event, data) => {
                console.error('Error:', data);
            });

            updateEpgInfo(currentChannel, program);
            
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            // Для Safari
            videoPlayer.src = videoUrl;
            videoPlayer.addEventListener('loadedmetadata', () => videoPlayer.play());
        }
    }

  // Обновление информации EPG
  function updateEpgInfo(channel, program = null) {
    currentChannelGroup.textContent = channel['group-title'] || 'Без категории';

    if (program) {
      currentProgramName.textContent = program.name;
      currentProgramDesc.textContent = program.desc || 'Нет описания';
    } else if (currentEpgData[channel['tvg-id']]) {
      const epg = currentEpgData[channel['tvg-id']];
      currentProgramName.textContent = epg.title;
      currentProgramDesc.textContent = epg.desc || 'Нет описания';
    } else {
      currentProgramName.textContent = channel.name;
      currentProgramDesc.textContent = 'Информация о программе загружается...';
    }
  }

  // Загрузка EPG для текущей страницы каналов
  async function loadEpgForCurrentPage() {
    if (currentView !== 'channels') return;

    const startIndex = currentPage * ITEMS_PER_PAGE;
    const endIndex = Math.min(startIndex + ITEMS_PER_PAGE, currentItems.length);
    const pageChannels = currentItems.slice(startIndex, endIndex);
    const channelIds = pageChannels.map(c => c['tvg-id']).filter(id => id);

    if (channelIds.length === 0) return;

    try {
      const response = await fetch(EPG_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          date: new Date().toISOString(),
          channels: channelIds
        })
      });

      if (response.ok) {
        const data = await response.json();
        // Обновляем данные EPG
        for (const channelId in data) {
          currentEpgData[channelId] = data[channelId];
        }
        renderCurrentPage();

        // Обновляем информацию о текущем канале
        if (currentChannel && currentEpgData[currentChannel['tvg-id']]) {
          updateEpgInfo(currentChannel);
        }
      }
    } catch (error) {
      console.error('Ошибка загрузки EPG:', error);
    }
  }

  // Показать EPG для текущего канала
  async function showEpgForCurrentChannel() {
    if (!currentChannel || !currentChannel['tvg-id']) {
      alert('Нет информации о текущем канале');
      return;
    }

    // Сохраняем текущее состояние для возврата
    saveCurrentState();

    try {
      const response = await fetch(CHANNEL_EPG_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          date: new Date().toISOString(),
          channel: currentChannel['tvg-id']
        })
      });

      if (response.ok) {
        const data = await response.json();
        // Преобразуем данные в массив программ
        currentPrograms = Object.values(data).map(prog => ({
          name: prog.title,
          start: prog.start,
          desc: prog.desc,
          end: prog.end, 
          url: prog.url || new Date(new Date(prog.start).getTime() + 3600000).toISOString()
        }));

        // Сортируем по времени начала
        currentPrograms.sort((a, b) => new Date(a.start) - new Date(b.start));

        currentView = 'epg';
        currentItems = currentPrograms;
        totalPages = Math.ceil(currentPrograms.length / ITEMS_PER_PAGE);
        currentPage = 0;
        currentItemIndex = -1;
        listTitle.textContent = `Программа: ${currentChannel.name}`;
        listCount.textContent = `${currentPrograms.length} программ`;

        categoriesBtn.style.display = 'inline-block';
        epgBtn.style.display = 'none';
        channelsBtn.style.display = 'inline-block';

        // Находим текущую программу
        const now = new Date();
        for (let i = 0; i < currentPrograms.length; i++) {
          const prog = currentPrograms[i];
          const start = new Date(prog.start);
          const end = new Date(prog.end);

          if (start <= now && now < end) {
            currentItemIndex = i;
            currentPage = Math.floor(i / ITEMS_PER_PAGE);
            break;
          }
        }

        renderCurrentPage();
      }
    } catch (error) {
      console.error('Ошибка загрузки программы:', error);
      alert('Ошибка загрузки программы передач');
    }
  }

  // Смена страницы
  function changePage(delta) {
    const newPage = currentPage + delta;
    if (newPage >= 0 && newPage < totalPages) {
      currentPage = newPage;
      currentItemIndex = -1;
      renderCurrentPage();

      if (currentView === 'channels') {
        loadEpgForCurrentPage();
      }
    }
  }

  // Форматирование времени (добавлена дата)
  function formatTime(isoString) {
    if (!isoString) return '';
    const date = new Date(isoString);
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${day}.${month} ${hours}:${minutes}`;
  }

  // Обработка колеса мыши
  listGrid.addEventListener('wheel', (e) => {
    if (e.deltaY > 0) {
      changePage(1);
    } else {
      changePage(-1);
    }
    e.preventDefault();
  });

  // Обработка клавиш
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') {
      if (currentItemIndex < currentItems.length - 1) {
        currentItemIndex++;
        if (currentItemIndex >= (currentPage + 1) * ITEMS_PER_PAGE) {
          changePage(1);
        } else {
          selectItem(currentItemIndex);
        }
      }
      e.preventDefault();
    } else if (e.key === 'ArrowUp') {
      if (currentItemIndex > 0) {
        currentItemIndex--;
        if (currentItemIndex < currentPage * ITEMS_PER_PAGE) {
          changePage(-1);
        } else {
          selectItem(currentItemIndex);
        }
      }
      e.preventDefault();
    } else if (e.key === 'Enter' && currentItemIndex >= 0) {
      selectItem(currentItemIndex);
      e.preventDefault();
    }
  });
});