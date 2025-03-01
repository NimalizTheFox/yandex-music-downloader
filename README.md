# yandex-music-downloader

## Содержание
1. [О программе](#О-программе)
2. [Установка](#Установка)
3. [Получение данных для авторизации](#Получение-данных-для-авторизации)
4. [Примеры использования](#Примеры-использования)
5. [Использование](#Использование)
6. [Что делать при ошибке 400?](#Ошибка-400)
7. [Спасибо](#Спасибо)
8. [Дисклеймер](#Дисклеймер)

## О программе
Загрузчик, созданный вследствие наличия *фатального недостатка* в проекте [yandex-music-download](https://github.com/kaimi-io/yandex-music-download).

### Возможности
- Возможность загрузки:
    - Всех треков исполнителя
    - Всех треков из альбома
    - Всех треков из плейлиста
    - Отдельного трека
- Загрузка всех метаданных трека/альбома:
    - Номер трека
    - Номер диска
    - Название трека
    - Исполнитель
    - Дополнительные исполнители
    - Год выпуска альбома
    - Обложка альбома
    - Название альбома
    - Текст песни (при использовании флага `--add-lyrics`)
- Поддержка паттерна для пути сохранения музыки

## Установка
Для запуска скрипта требуется Python 3.9+
```
pip install git+https://github.com/NimalizTheFox/yandex-music-downloader
yandex-music-downloader --help
```

## Получение данных для авторизации
1. Войдите в свой Яндекс аккаунт.
2. Передайте название вашего браузера в качестве аргумента `--browser`

Если программа выдает ошибку при загрузке cookies - укажите путь к файлу
с cookies в качестве аргумента `--cookies-path`. Информацию о
расположении данного файла для вашего браузера вы можете найти в
интернете. Если что-то не получается - откройте issue.


## Примеры использования
Во всех примерах замените `<браузер>` на название своего браузера (для
получения допустимых значений запустите программу с флагом `--help`)

### Скачать все треки [Twenty One Pilots](https://music.yandex.ru/artist/792433) в высоком качестве
```
yandex-music-downloader --browser "<браузер>" --hq --url "https://music.yandex.ru/artist/792433"
```

### Скачать альбом [Nevermind](https://music.yandex.ru/album/294912) в высоком качестве, загружая тексты песен
```
yandex-music-downloader --browser "<браузер>" --hq --add-lyrics --url "https://music.yandex.ru/album/294912"
```

### Скачать трек [Seven Nation Army](https://music.yandex.ru/album/11644078/track/6705392)
```
yandex-music-downloader --browser "<браузер>" --url "https://music.yandex.ru/album/11644078/track/6705392"
```

## Использование

```
usage: yandex-music-downloader [-h] [--hq] [--skip-existing] [--add-lyrics]
                               [--embed-cover]
                               [--cover-resolution <Разрешение обложки>]
                               [--delay <Задержка>] [--stick-to-artist]
                               [--only-music]
                               (--artist-id <ID исполнителя> | --album-id <ID альбома> | --track-id <ID трека> | --playlist-id <владелец плейлиста>/<тип плейлиста> | -u URL)
                               [--unsafe-path] [--dir <Папка>]
                               [--path-pattern <Паттерн>] --browser BROWSER
                               [--cookies-path COOKIES_PATH]
                               [--user-agent <User-Agent>]

Загрузчик музыки с сервиса Яндекс.Музыка

options:
  -h, --help            show this help message and exit

Общие параметры:
  --hq                  Загружать треки в высоком качестве
  --skip-existing       Пропускать уже загруженные треки
  --add-lyrics          Загружать тексты песен
  --embed-cover         Встраивать обложку в .mp3 файл
  --cover-resolution <Разрешение обложки>
                        по умолчанию: 400
  --delay <Задержка>    Задержка между запросами, в секундах (по умолчанию: 3)
  --stick-to-artist     Загружать альбомы, созданные только данным
                        исполнителем
  --only-music          Загружать только музыкальные альбомы (пропускать
                        подкасты и аудиокниги)

ID:
  --artist-id <ID исполнителя>
  --album-id <ID альбома>
  --track-id <ID трека>
  --playlist-id <владелец плейлиста>/<тип плейлиста>
  -u URL, --url URL     URL исполнителя/альбома/трека/плейлиста

Указание пути:
  --unsafe-path         Не очищать путь от недопустимых символов
  --dir <Папка>         Папка для загрузки музыки (по умолчанию: .)
  --path-pattern <Паттерн>
                        Поддерживает следующие заполнители: #number, #artist,
                        #album-artist, #title, #album, #year, #artist-id,
                        #album-id, #track-id, #track-number (по умолчанию:
                        #album-artist/#album/#number - #title)

Авторизация:
  --browser BROWSER     Браузер из которого будут извлечены данные для
                        авторизации. Укажите браузер через который вы входили
                        в Яндекс Музыку. Допустимые значения: chrome, opera,
                        opera_gx, firefox, edge, safari, chromium, vivaldi,
                        librewolf
  --cookies-path COOKIES_PATH
                        Путь к файлу с cookies. Используйте если возникает
                        ошибка получения cookies
  --user-agent <User-Agent>
                        по умолчанию: Mozilla/5.0 (X11; Linux x86_64)
                        AppleWebKit/537.36 (KHTML, like Gecko)
                        Chrome/106.0.0.0 Safari/537.36
```
## Ошибка 400
Ниже приведена инструкция по устранению ошибки 400.

1. Перейдите на сайт Яндекс.Музыки
2. Прорешайте капчу
3. Готово, теперь вы можете скачивать треки без ошибок

Если проблема сохраняется - откройте issue.

## Спасибо
Разработчикам проекта [yandex-music-download](https://github.com/kaimi-io/yandex-music-download). Оттуда был взят [код хэширования](https://github.com/kaimi-io/yandex-music-download/blob/808443cb32be82e1f54b2f708884cb7c941b4371/src/ya.pl#L720).

## Дисклеймер
Данный проект является независимой разработкой и никак не связан с компанией Яндекс.
