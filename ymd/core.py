import re
import urllib.parse
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Optional

import eyed3
from eyed3.id3.frames import ImageFrame
from requests import Session

from ymd import http_utils
from ymd.ym_api import BasicTrackInfo, FullTrackInfo
from ymd.ym_api.api import YandexMusicApi

ENCODED_BY = "https://github.com/llistochek/yandex-music-downloader"
FILENAME_CLEAR_RE = re.compile(r"[^\w\-\'() ]+")

DEFAULT_PATH_PATTERN = Path("#album-artist", "#album", "#number - #title")
DEFAULT_COVER_RESOLUTION = 400


def clear_name(text: str):
    ban_chars = ['/', '\\', '*', '?', '<', '>', '"', '|', ':']   # Запрещенные для Windows символы в имени файла
    text_spl = text.split('\\')
    for i in range(1, len(text_spl)):
        for char in ban_chars:
            text_spl[i] = text_spl[i].replace(char, "")
        while text_spl[i][-1] == ".":
            text_spl[i] = text_spl[i][:-1]
    text = '\\'.join(text_spl)
    while text.find("  ") != -1:
        text = text.replace("  ", " ")
    text = text.strip()
    return text


def prepare_track_path(
    path_pattern: Path,
    track: BasicTrackInfo,
    unsafe_path: bool = False,
    track_number_str: str = "",
) -> Path:
    path_str = str(path_pattern)
    album = track.album
    artist = album.artists[0]
    repl_dict = {
        "#album-artist": album.artists[0].name,
        "#artist-id": artist.name,
        "#album-id": album.id,
        "#track-id": track.id,
        "#number-padded": track_number_str,
        "#number": track.number,
        "#artist": artist.name,
        "#title": track.title,
        "#album": album.title,
        "#year": album.year,
    }
    for placeholder, replacement in repl_dict.items():
        replacement = str(replacement)
        if not unsafe_path:
            replacement = FILENAME_CLEAR_RE.sub("_", replacement)
        path_str = path_str.replace(placeholder, replacement)
    path_str = clear_name(path_str)
    path_str += ".mp3"
    return Path(path_str)


def set_id3_tags(
    path: Path,
    track: BasicTrackInfo,
    lyrics: Optional[str],
    album_cover: Optional[bytes],
    domain: str,
) -> None:
    if track.album.release_date is not None:
        release_date = eyed3.core.Date(*track.album.release_date.timetuple()[:6])
    else:
        release_date = track.album.year
    audiofile = eyed3.load(path)
    assert audiofile

    tag = audiofile.initTag()

    tag.artist = chr(0).join(a.name for a in track.artists)
    tag.album_artist = track.album.artists[0].name
    tag.album = track.album.title
    tag.title = track.title
    tag.track_num = track.number
    tag.disc_num = track.disc_number
    tag.release_date = tag.original_release_date = release_date
    tag.encoded_by = ENCODED_BY
    tag.audio_file_url = f"https://{domain}/album/{track.album.id}/track/{track.id}"

    if lyrics is not None:
        tag.lyrics.set(lyrics)
    if album_cover is not None:
        tag.images.set(ImageFrame.FRONT_COVER, album_cover, "image/jpeg")

    tag.save()


def setup_session(
    session: Session, cookie_jar: CookieJar, user_agent: str, domain: str
) -> Session:
    session.cookies = cookie_jar  # type: ignore
    session.headers["User-Agent"] = user_agent
    session.headers["X-Retpath-Y"] = urllib.parse.quote_plus(f"https://{domain}")
    return session


def download_track(
    client: YandexMusicApi,
    track: BasicTrackInfo,
    target_path: Path,
    covers_cache: dict[str, bytes],
    cover_resolution: int = DEFAULT_COVER_RESOLUTION,
    hq: bool = False,
    add_lyrics: bool = False,
    embed_cover: bool = False,
):
    album = track.album

    url = client.get_track_download_url(track, hq)
    http_utils.download_file(client.session, url, target_path)

    lyrics = None
    if add_lyrics and track.has_lyrics:
        if isinstance(track, FullTrackInfo):
            lyrics = track.lyrics
        else:
            full_track = client.get_full_track_info(track.id)
            if full_track is not None:
                lyrics = full_track.lyrics

    cover = None
    cover_url = track.cover_info.cover_url(cover_resolution)
    if cover_url is not None:
        if embed_cover:
            if cached_cover := covers_cache.get(album.id):
                cover = cached_cover
            else:
                cover = covers_cache[album.id] = http_utils.download_bytes(
                    client.session, cover_url
                )
        else:
            cover_path = target_path.parent / "cover.jpg"
            if not cover_path.is_file():
                http_utils.download_file(client.session, cover_url, cover_path)

    set_id3_tags(target_path, track, lyrics, cover, client.domain)
