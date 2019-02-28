import sys, urllib.request, requests, re, hashlib, os, re, json
from urllib.request import urlopen
from imgurpython import ImgurClient

with open('./json/setup.json') as data_file:
    setup = json.load(data_file)


def file_as_bytes(file):
    with file:
        return file.read()

def save_file(img_url, file_path):
    resp = requests.get(img_url, stream=True)
    if resp.status_code == 200:
        with open(file_path, 'wb') as image_file:
            for chunk in resp:
                image_file.write(chunk)
        image_file.close()
        return file_path
    else:
        print("[EROR] File failed to download. Status code: " +
              str(resp.status_code))
        return

def get_media(img_url, IMGUR_CLIENT = setup["iClientId"], IMGUR_SECRET = setup["iClientSecret"]):
    IMAGE_DIR = './media'
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        print("[Bot] Media folder not found, making one")
    if any(s in img_url for s in ('i.redd.it', 'i.reddituploads.com')):
        file_name = os.path.basename(urllib.parse.urlsplit(img_url).path)
        file_extension = os.path.splitext(img_url)[-1].lower()
        if not file_extension:
            file_extension += '.jpg'
            file_name += '.jpg'
            img_url += '.jpg'
        file_path = IMAGE_DIR + '/' + file_name
        print("[Bot] Downloading file at URL " + img_url + 'to ' +
              file_path + ', file type identified as ' + file_extension)
        img = save_file(img_url, file_path)
        return img
    elif('v.redd.it' in img_url):
        print("[WARN] Reddit videos cannot be uploaded to Twitter due to API limitations")
        return
    elif('imgur.com' in img_url):
        try:
            client = ImgurClient(setup["iClientId"], setup["iClientSecret"])
        except BaseException as e:
            print("[EROR] Error with authing with Imgur:", str(e))
            return
        regex = r"(?:.*)imgur\.com(?:\/gallery\/|\/a\/|\/)(.*?)(?:\/.*|\.|$)"
        m = re.search(regex, img_url, flags=0)
        if m:
            id = m.group(1)
            if any(s in img_url for s in('/a/', '/gallery/')):
                images = client.get_album_images(id)
                img_url = images[0].link
            else:
                imgur_url = client.get_image(id).link
                file_extension = os.path.splitext(imgur_url)[-1].lower()
            if (file_extension == '.gifv'):
                file_extension = file_extension.replace('.gifv', '.gif')
                imgur_url = imgur_url.replace('.gifv', '.gif')
            elif (file_extension == '.mp4'):
                file_extension = file_extension.replace('.mp4', '.gif')
                imgur_url = imgur_url.replace('.mp4', '.gif')
            file_path = IMAGE_DIR + '/' + id + file_extension
            print("[Bot] Downloading Imgur image at URL " +
                  img_url + ' to ' + file_path)
            imgur_file = save_file(imgur_url, file_path)
            if (file_extension == '.gif'):
              img = Image.open(imgur_file)
              mime = Image.MIME[img.format]
              if (mime == 'image/gif'):
                  img.close()
                  return imgur_file
              else:
                  print('[WARN] Imgur has not processed a GIF version of this link, so it can not be posted to Twitter')
                  img.close()
                  try:
                      os.remove(imgur_file)
                  except BaseException as e:
                      print('[EROR] Error while deleting media file:', str(e))
                  return
            else:
                return imgur_file
        else:
            print('[EROR] Could not identify Imgur image/gallery ID in this URL:', img_url)
            return
