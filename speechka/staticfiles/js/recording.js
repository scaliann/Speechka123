document.addEventListener('DOMContentLoaded', function() {
    let currentWordIndex = 0;
    let audioContext;
    let mediaStream;
    let recorder;
    let audioChunks = [];

    // Убедимся, что words доступен и содержит данные
    if (typeof words !== 'undefined' && words.length > 0) {
        console.log('Words:', words);

        function showNextWord() {
            if (currentWordIndex < words.length) {
                document.getElementById('wordDisplay').innerText = words[currentWordIndex];
            } else {
                document.getElementById('wordDisplay').innerText = 'Все слова произнесены!';
            }
        }

        async function setupRecorder() {
            try {
                // Инициализация AudioContext

                const audioContext = new AudioContext({ sampleRate: 44100 });
                // Захват аудиопотока
                mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });

                // Подключение к источнику записи
                const input = audioContext.createMediaStreamSource(mediaStream);

                // Используем MediaRecorder для записи
                recorder = new MediaRecorder(mediaStream);

                recorder.ondataavailable = function(event) {
                    audioChunks.push(event.data);
                };

                recorder.onstop = function() {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const formData = new FormData();
                    formData.append('audio', audioBlob, 'audio.wav');
                    formData.append('word', words[currentWordIndex]); // Отправляем текущее слово

                    // Отправка аудиофайла на сервер
                    fetch('/upload/', {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': getCSRFToken()
                        }
                    }).then(response => {
                        alert(response.ok ? 'Аудиофайл успешно загружен' : 'Ошибка при загрузке аудиофайла');
                        currentWordIndex++; // Переход к следующему слову
                        showNextWord();
                    }).catch(error => {
                        console.error('Ошибка при загрузке аудиофайла:', error);
                    });
                };
            } catch (error) {
                console.error('Ошибка инициализации записи:', error);
            }
        }

        document.getElementById('start-record-btn').onclick = function() {
            audioChunks = [];
            recorder.start();

            document.getElementById('stop-record-btn').disabled = false;
        };

        document.getElementById('stop-record-btn').onclick = function() {
            recorder.stop();
            document.getElementById('stop-record-btn').disabled = true;

        };

        // Инициализируем запись
        setupRecorder();

        // Отображаем первое слово
        showNextWord();
    } else {
        console.error('Список слов не загружен или пуст.');
        document.getElementById('wordDisplay').innerText = 'Ошибка загрузки слов.';
    }

    function getCSRFToken() {
        return document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    }
});
