from PIL import Image, ImageDraw
import requests
from io import BytesIO



def create_icon_image(profile_pic_url, bg_color):
    rectangle_height = 80  # px
    circle_dimension = 196  # px, both width and height
    resize_value = 4  # times bigger resolution
    mp = circle_dimension * resize_value

    response = requests.get(profile_pic_url)
    im = Image.open(BytesIO(response.content))

    #create circle
    circle_img = Image.new('RGBA', (mp, mp), (0, 0, 0, 0))
    d = ImageDraw.Draw(circle_img)
    d.ellipse([(0, 0), (mp, mp)], fill=bg_color, outline="black", width=4)
    im_resized = circle_img.resize((circle_dimension, circle_dimension))

    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))

    #paste circle at bottom and create mask
    img.paste(im_resized, (int((256-circle_dimension)/2), int(256-circle_dimension)))
    circle_mask = img.copy()
    #paste profile pic on top of circle
    img.paste(im, (0, 0), im)

    transparentpic = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    #create alpha mask as square - circle
    alphamask = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(alphamask)
    a_draw.rectangle([(0, 256-rectangle_height), (256, 256)], fill="red")
    #pagar uma secção em circulo do retangulo
    alphamask.paste(transparentpic, (0, 0), circle_mask)
    #usar uma imagem trnsparente e a alphamask para limpar o bottom da imagem fora do circulo inicial
    img.paste(transparentpic, (0, 0), alphamask)
    #img.save("circulonocanto.png", "PNG")
    return img


#url ="https://styles.redditmedia.com/t5_2xrdhm/styles/profileIcon_snooa2e574ad-0e44-49bb-b865-682a6194354e-headshot.png?width=256&height=256&crop=256:256,smart&s=e168ebd996cb4ba0704f65cd0bc5244eec9c0b42"
#img_file = create_icon_image(url)



