from PIL import Image, ImageDraw, ImageFont
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import concatenate_videoclips
import re
from tts import get_single_audio
from createprofilepic import create_icon_image
from operator import itemgetter

#textString = "Very interesting.\n\nWe had a talk from one of the ID docs at my hospital a few months ago, and at least amongst the researchers here the speculation that some of the symptoms with long-COVID (mainly fatigue and brain fog) were essentially analogous to a concussion.\nThat intuitively made sense to me since many patients who've recovered from an acute illness or ICU will still have difficulty concentrating and fatigue months later.\n\nI wonder if the idea of \"long-COVID\" will be teased apart into multiple different problems over time. I wonder how much of the symptoms of long-COVID are specific to COVID vs generalizable sequela of acute illness and there's finally a big enough sample size to study it properly."
#textString = "The Denver Airport theory. I mean the capstone of the building literally has the Freemason logo on it, there's some weird ass apocalypse"
#textString = 'Que cena marada. No outro dia cheguei a casa e wtf... A casa estava toda desarrumada, o cão tinha \ncagado em todo\n\n\n o lado. Acreditem ou não nunca tinha visto tanta merda como neste dia nossa senhora. O. \n\nM. G.\n'
#textString = "Very interesting.\n\nWe had a talk from one of the ID docs at my hospital a few months ago, and at least amongst the researchers here the speculation that some of the symptoms with long-COVID (mainly fatigue and brain fog) were essentially analogous to a concussion. That intuitively made sense to me since many patients who've recovered from an acute illness or ICU will still have difficulty concentrating and fatigue months later.\n\nI wonder if the idea of \"long-COVID\" will be teased apart into multiple different problems over time. I wonder how much of the symptoms of long-COVID are specific to COVID vs generalizable sequela of acute illness and there's finally a big enough sample size to study it properly."
#textString = "I would be more worried about clots and affected blood flow to the brain than I would something akin to a concussion with covid, although I could be wrong.  Even if you don't have large clots you can still have teensy tiny ones that cause brain damage like seen with vascular dementia and we know that covid attacks blood vessels and causes clots. \n\n\nEveryone talks about the fatality rate seemingly not understanding just how much long term damage an infection can cause.  You might live but that doesn't mean you fully recover."
#textString = "\n&gt; Codality with a countdown timer while I created algorithms with some random HR person watching me \n\nThat sounds fucking awful. Imagine how bad it would be to work there."
#textString = "My great great grandpa owned a ranch that encompassed a large part of what is now mesa and Gilbert Arizona. \nWhen he passed away, his ranch foreman and some lawyers concocted a story that my great great grandpa had verbally promised him the ranch when he passed. All they had was the word of a few other cowboys that said they heard it. Despite Arizona law back then requiring that real estate exchanges must be in writing to be valid, they won. Several decades later when my mom was in law school in Texas, it was a subject in one of her classes and used as an example of how law is not always as straightforward as it is made out to be, especially in inheritance cases."
#textString = "Ola o meu nome é Rodrigo. Gosto muito de bacon.\n Diria que é a melhor comida alguma vez concebida"
#textString = "I'm Tyler Falbo, I partnered with Bill Burr and All Things Comedy to create Immoral Compass, a dark comedy anthology series for The Roku Channel starring Bill Burr, Vince Vaughn, Bobby Lee, Mary Lynn Rajskub, David Dastmalchian, and many others. No, you don't need a Roku to watch The Roku Channel. It's an app that you can get on many TV's, Amazon firestick, or you can just watch it on your phone or your computer. \n\nWatch now FOR FREE:\nhttps://therokuchannel.roku.com/details/faca68c0f5429c1da58605466a090a24/bill-burr-presents-immoral-compass\n\nedit: The YouTube channel that started this: https://www.youtube.com/c/TylerFalbo\n\n[Here's my proof](https://imgur.com/a/1eRQE0P)!"
#textString = "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?"
textString = "On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains."
#   textString = "On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains. On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains. On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains."
#textString = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc,"
#textString = "Uma vez era o Deus, que queria jogar para sempre na lua. Era muito bom ter algo para olhar? Mas podia ser de novo outra vez! Ok eu vou mas nunca digas que vou outra vez..."
#textString = "And he filed instantly 😂"
#textString = "wingardum leviosaaah. I like a lot of harry potter spells. They're pretty cool. Iulia sucks the P P"


line_spacing = 0
# fazer uma font que tenha estas duas
fnt = ImageFont.truetype("../fonts/NotoSans-Regular.ttf", 30)
fnt2 = ImageFont.truetype("../fonts/NotoColorEmoji.ttf", 109, layout_engine=ImageFont.LAYOUT_RAQM)

enders = ".,!?:;()"



def get_text_size(origin, text, font, draw, spacing):
    text_preview_space = draw.textbbox(origin, text, font=font, spacing=spacing)
    #draw.rectangle(text_preview_space, outline='white', width=1)
    return text_preview_space


def find_white_spaces(text):
    array = []
    for i in range(len(text)):
        if text[i] == " ":
            array.append(i)
    return array


def first_string_sweep(string):
    # fazer alterações à string
    # retirar os links com o formato [texto](link)
    # retirar caracters do reddit ** e formatações

    return string


def refactor_string_to_max_width(text, points, draw, font, spacing):
    max_width = points[2] - points[0]
    white_spaces = find_white_spaces(text)
    white_spaces.append(len(text))
    split_text = []
    last = 0
    #print(text)
    for i in range(len(white_spaces)):
        preview_points = get_text_size((0, 0), text[last:white_spaces[i]], font, draw, spacing)
        preview_width = preview_points[2] - preview_points[0]
        if int(preview_width) > int(max_width):
            if last == 0:
                split_text.append(text[last:white_spaces[i-1]])
            else:
                split_text.append(text[last+1:white_spaces[i - 1]])
            last = white_spaces[i-1]
    if split_text == []:
        split_text.append(text[last:])
    else:
        split_text.append(text[last+1:])

    print(split_text)
    return split_text


def refactor_string_to_max_height(array, draw, og_points, font, spacing):
    #dos pontos definidos para o texto ocupar, retirar a altura maxima, max y - min y
    #print(array)
    max_height = og_points[3] - og_points[1]
    last = 0
    picture_array = []
    join_elem = "\n"
    #dividir o array com base na altura maxima
    for i in range(len(array)):
        preview_points = get_text_size((0, 0), join_elem.join(array[last:i+1]), font, draw, spacing)
        preview_height = preview_points[3] - preview_points[1]
        #print(preview_height, array[last:i + 1])
        if preview_height > max_height:
            picture_array.append(array[last:i])
            last = i
    picture_array.append(array[last:])

    return picture_array


def check_for_enders(string):
    for i in range(len(enders)):
        if enders[i] in string:
            return True
    return False


def split_array_by_enders(text_array):
    #print(text_array)
    elements_to_print = []
    last_sentence = ""
    for i in range(len(text_array)):
        if check_for_enders(text_array[i]):
            #split the stuff
            array = re.split('(['+enders+'])', text_array[i])

            for a in range(len(array)):
                if a == 0:
                    if i == 0:
                        #nao por o paragrafo no caso deser o primeiro elemento do texto
                        last_sentence = last_sentence + array[a]
                    else:
                        last_sentence = last_sentence + "\n" + array[a]
                else:
                    last_sentence = last_sentence + array[a]
                if not a % 2 == 0:
                    elements_to_print.append(last_sentence)
                    last_sentence = ""
        else:
            if i == 0:
                last_sentence = last_sentence + text_array[i]
            else:
                last_sentence = last_sentence + "\n" + text_array[i]
    if not last_sentence == "":
        elements_to_print.append(last_sentence)

    #og_text = "\n".join(text_array)
    #print_text = "".join(elements_to_print)
    #print(og_text == print_text)
    #print(len(og_text), len(print_text))

    return elements_to_print


def create_multiple_pics_one_comment_segment(text_array, base_image, indx, comment_id, left_corner):
    text_for_image = split_array_by_enders(text_array)
    text_for_tts = []
    images = []
    #print(text_for_image)
    for i in range(len(text_for_image)):
        image = base_image.copy()
        draw = ImageDraw.Draw(image)
        text = "".join(text_for_image[0:i+1])
        #usar isto para sacar de ca os textos para os audios mas primeiro remover o \n
        #print(text_for_image[i].replace("\n", " "))
        text_for_tts.append(text_for_image[i].replace("\n", " "))
        draw.multiline_text(left_corner, text, font=fnt, spacing=line_spacing, fill="white")
        #name = "comment_id_" + str(comment_id) + "_index_" + str(indx) + "_part_" + str(i)
        images.append(image)
        #image.save("pics/" + name + ".png", "PNG")
    return text_for_tts, images


def get_images_and_tts_text(print_array, background, comment_id, text_origin):
    text_tts_array = []
    text_images_array = []
    for index in range(len(print_array)):
        tts, path_names = create_multiple_pics_one_comment_segment(print_array[index], background, index, comment_id, text_origin)
        # print(print_array[index])
        for elem in tts:
            text_tts_array.append(elem)
        for name in path_names:
            text_images_array.append(name)

    return text_tts_array, text_images_array


def create_video_of_image_and_audio(img, audio, b):
    a_clip = AudioFileClip(audio, fps=44100)
    v_clip = ImageClip(img, ismask=False, transparent=False, duration=a_clip.duration)
    v_a_clip = v_clip.set_audio(a_clip)
    v_a_clip = v_a_clip.audio_fadein(0.01).audio_fadeout(0.01)
    #v_a_clip.write_videofile("videos/" + str(b) + ".mp4", fps=30, codec='mpeg4')
    #print(v_clip.duration, a_clip.duration)
    return v_a_clip


def create_picture_background(comment_array, bg_size, text_area):

    background_image = Image.new('RGB', bg_size, (0, 0, 0))
    draw = ImageDraw.Draw(background_image)

    img_width, img_height = background_image.size

    corner = (50, 110)
    img_size = (80, 80)
    margin = 15
    text_area_height = 0
    upvote_area_height = 80

    if text_area is not None:
        text_area_height = text_area[3] - text_area[1]



    #check se ha um ou dois objetos de comentario
    if len(comment_array) == 1:

        create_comment_template_for_user(comment_array[0], img_size, background_image, draw, margin, corner, text_area_height + upvote_area_height)
        text_area_to_return = (corner[0] + img_size[0] + margin, corner[1] + img_size[1] + margin, img_width - (corner[0] + int(img_size[0] / 2)), img_height - 300 + corner[1])

    else:
        # elementos do comentario pai
        create_comment_template_for_user(comment_array[0], img_size, background_image, draw, margin, corner, text_area_height + upvote_area_height + img_size[1] + margin)

        #elementos do filho
        corner2 = (corner[0] + int(img_size[0]/2) + margin, corner[1] + img_size[0] + margin)
        create_comment_template_for_user(comment_array[1], img_size, background_image, draw, margin, corner2, text_area_height + upvote_area_height)
        text_area_to_return = (corner2[0] + img_size[0] + margin, corner2[1] + img_size[1] + margin, img_width - (corner[0] + int(img_size[0] / 2)), img_height - 300 + corner[1])

    if text_area is None:
        return text_area_to_return
    else:
        draw.rectangle(text_area, outline="red", width=1)
        print(text_area)

        # fazer uma condição para se por a cena dos upvotes no ultimo bloco de texto
        upvote_area = (text_area[0], text_area[3], text_area[2], text_area[3] + upvote_area_height)
        draw.rectangle(upvote_area, outline="red", width=1)

        background_image.save("gandacena.png", "PNG")

        return background_image



        #redifinir o text area para ter mais ou menos o espaço a menos
    #se nao criar o de single coment individual

def print_user_time_awards(initial_corner, draw_element, username, time, awards):
    fnt_title = ImageFont.truetype("../fonts/NotoSans-Regular.ttf", 50)

    #draw_element.text(initial_corner, username + " - " + str(time) + " - " + awards, fill="red", font=fnt_title)
    text_area_1 = draw_element.textbbox(initial_corner, username, font=fnt_title)
    draw_element.text(initial_corner, username, font=fnt_title)
    t_a_width = text_area_1[2] - text_area_1[0]
    t_a_height = text_area_1[3] - text_area_1[1]
    print(t_a_width, t_a_height)



def create_comment_template_for_user(array_element, image_size, bg_image, draw_element, margin, pic_corner, text_area_height):
    pic_url, username, time, awards = itemgetter("pic_url", "reddit_username", "time_utc", "awards")(array_element)
    img = create_icon_image(pic_url, "yellow")
    img = img.resize(image_size)
    bg_image.paste(img, pic_corner)
    # retangulo a volta da profile pic
    draw_element.rectangle((pic_corner[0], pic_corner[1], pic_corner[0]+image_size[0], pic_corner[1] + image_size[1]), outline="red", width=2)
    # o 10 é so para ajustar por agora
    print_user_time_awards((pic_corner[0] + image_size[0] + margin, pic_corner[1] + 10), draw_element, username, time, awards)
    draw_element.line((pic_corner[0] + image_size[0] / 2, pic_corner[1] + image_size[0] + margin, pic_corner[0] + image_size[0] / 2, pic_corner[1] + image_size[1] + margin + text_area_height), width=10, fill="red")



def make_video_of_comment(comments_array, size):

    last_index = len(comments_array)-1
    comment_string = comments_array[last_index]["comment_body"]
    comment_id = comments_array[last_index]["comment_id"]

    print(comment_string)

    sweapt_string = first_string_sweep(comment_string)

    test_img = Image.new('RGBA', size, (0, 0, 0, 0))
    test_draw = ImageDraw.Draw(test_img)

    #definir a area onde o texto vai ser posto
    text_area = create_picture_background(comment_array, size, None)
    print(text_area)
    #text_area = (200, 300, 600, 600)


    #divide o texto em com base na largura maxima
    split_text_array = refactor_string_to_max_width(sweapt_string, text_area, test_draw, fnt, line_spacing)

    #divide o texto com base na altura maxima
    array_to_print = refactor_string_to_max_height(split_text_array, test_draw, text_area, fnt, line_spacing)


    if len(array_to_print) == 1:
        # se couber tudo na mesma text_area ver se da para encurtar a text area e o quanto se tem que encurtar
        #print(array_to_print)
        text_to_try = "\n".join(array_to_print[0])
        text_box = test_draw.textbbox((0, 0), text_to_try, font=fnt, spacing=line_spacing)
        text_area_width = text_box[2]
        text_area_height = text_box[3]
        text_area = (text_area[0], text_area[1], text_area[0] + text_area_width, text_area[1] + text_area_height)

    before_text_image = create_picture_background(comment_array, size, text_area)



    return

    text_tts, text_images = get_images_and_tts_text(array_to_print, before_text_image, comment_id, (text_area[0], text_area[1]))

    print(len(text_tts), len(text_images))

    #  gravar as imagens
    for i in range(len(text_images)):
        text_images[i].save("pics/" + str(comment_id) + "_" + str(i) + ".png", "PNG")

    #  fazer pedidos ao tts
    for i in range(len(text_tts)):
        #retirar a ultima pontuação do tts e substituir por um ponto final
        # se houverem 3 pontos seguidos, substituir no tts por apenas um ponto, ou por uma virgula
        get_single_audio(text_tts[i], "male", 1, 0, comment_id, i)

    #  fazer um video para cada par audio/imagem
    clip_array = []
    for i in range(len(text_images)):
        img_src = "pics/" + str(comment_id) + "_" + str(i) + ".png"
        audio_src = "audios/" + str(comment_id) + "_" + str(i) + ".mp3"
        clip = create_video_of_image_and_audio(img_src, audio_src, i)
        clip_array.append(clip)


    #  juntar todos os videos
    video_name = "comment_" + str(comment_id) + ".mp4"
    comment_clip = concatenate_videoclips(clip_array)
    # o codec está a rebentar a qualidade toda por alguma razão, tem que se encontrar um que tenha qualidade mm boa
    comment_clip.write_videofile("videos/" + video_name, fps=24)  # codec='mpeg4'

    for elem in clip_array:
        elem.close()

    #return comment_clip
    return video_name


# picture size
size = (1920, 1080)
comment_array = [
        {
            "pic_url": "https://styles.redditmedia.com/t5_2xrdhm/styles/profileIcon_snooa2e574ad-0e44-49bb-b865-682a6194354e-headshot.png?width=256&height=256&crop=256:256,smart&s=e168ebd996cb4ba0704f65cd0bc5244eec9c0b42",
            "reddit_username": "JoãoLmao",
            "time_utc": 1039423232,
            "awards": "ainda nao sei",
            "comment_body": "Então campeão como vai a festa",
            "comment_id": 142332234
        },
        {
            "pic_url": "https://styles.redditmedia.com/t5_c5hq6/styles/profileIcon_snooc3f2e7e5-0cb2-4e6c-a19c-0cf60ad1f5a9-headshot.png?width=256&height=256&crop=256:256,smart&s=f8a399bc4a4831326d68945a496cc8259b1e8e12",
            "reddit_username": "Segundo_joao_Lmao",
            "time_utc": 1258452146,
            "awards": "sei la o crl",
            "comment_body": textString,
            "comment_id": 14233
        }
    ]

make_video_of_comment(comment_array, size)





