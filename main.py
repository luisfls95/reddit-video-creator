from PIL import Image, ImageDraw, ImageFont
from python_functions import createprofilepic



url ="https://styles.redditmedia.com/t5_2xrdhm/styles/profileIcon_snooa2e574ad-0e44-49bb-b865-682a6194354e-headshot.png?width=256&height=256&crop=256:256,smart&s=e168ebd996cb4ba0704f65cd0bc5244eec9c0b42"
img = createprofilepic.create_icon_image(url)
img.save("bro.png", "PNG")
