import requests
import re


def save_media(url):
    print(url)
    match = re.search(
        pattern=r'https\:\/\/.*\/([^\/\.]+).*?(jpg|jpeg|png|mp4)', string=url)
    try:
        res = requests.get(url=url)
        name = f'{match.group(1)}.{match.group(2)}'
        print(name)
    except:
        pass
    else:
        with open(f'static/media/{name}', mode='wb+') as f:
            f.write(res.content)
        return f'https://getcdnlink.xyz/media/{name}'
