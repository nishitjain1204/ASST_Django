import re
import base64


def save_screenshot(filename, image_data):
    print('save function called')
    filename = ''.join(e for e in filename if e.isalnum())+'.jpg'
    dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
    image_data = dataUrlPattern.match(image_data).group(2)
    image_data = image_data.encode()
    image_data = base64.b64decode(image_data)

    with open(filename, 'wb') as f:
        f.write(image_data)
        print('image generated')
    return filename
