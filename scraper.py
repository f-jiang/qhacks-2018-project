import argparse
import urllib.request
import requests
import json
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
# accept one argument for the url to search
parser.add_argument('url', type=str, nargs='?', help='the list of urls in which to search for imgs')
args = parser.parse_args()

with urllib.request.urlopen(args.url) as response:
    info = {'url': args.url, 'img_files': []}
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    img_elems = soup.find_all('img', 'lazy')

    # obtain all srcs from the html's img tags
    print('getting images from url {}'.format(args.url))
    img_srcs = []
    for img_elem in img_elems:
        img_src = img_elem.get('src') or img_elem.get('data-src')

        # img_src requirements: from scene7, not a gif, must have http:// or https:// at beginning
        if 's7d9.scene7.com' in img_src and 'gif' not in img_src:
            if 'http://' not in img_src and 'https://' not in img_src:
                img_src = 'https:{}'.format(img_src)

            img_srcs.append(img_src)

    img_srcs = list(set(img_srcs)) # remove duplicates

    # try to download the images from img_srcs
    i = 0
    for img_src in img_srcs:
        img_file_name = '{}.jpg'.format(i)
        with open(img_file_name, 'wb') as handle:
            try:
                response = requests.get(img_src, stream=True)

                if not response.ok:
                    print('response not ok: {}'.format(response))
                else:
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)

                    print('SUCCESS: downloaded image from src {}'.format(img_src))
                    info['img_files'].append(img_file_name)
                    i += 1
            except:
                print('ERROR: failed to download image from src {}'.format(img_src))

    with open('info.json', 'w') as outfile:
        json.dump(info, outfile, indent=4)

