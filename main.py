ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'song.%(ext)s',
    'nocheckcertificate': True,
    'quiet': True,
    'no_warnings': True,
    'source_address': '0.0.0.0', # допомагає обійти блоки IP
}
