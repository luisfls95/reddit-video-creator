from google.cloud import texttospeech
from moviepy.editor import concatenate_audioclips, AudioFileClip
import os

#  lista vozes
#  https://cloud.google.com/text-to-speech/docs/voices

# define as credenciais para acesso à api da google com base no ficheiro json fornecido pela google
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../tts-reddit-345500-97c852acb2e5.json'

# definir dois perfis de vozes diferentes para usar no request mais tarde, fica fora da função pois apenas 2 vozes serão usadas pelo que não é necessário continuamente redefinir as mesmas dentro das funções
male_voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.MALE) # , name="en-US-Wavenet-A"
#male_voice = texttospeech.VoiceSelectionParams(language_code="pt-PT", ssml_gender=texttospeech.SsmlVoiceGender.MALE, name="pt-PT-Wavenet-C")
female_voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE, name="en-US-Standard-C")


# iniciar um client através do qual se vão fazer os pedidos de tts
client = texttospeech.TextToSpeechClient()

def get_single_audio(text_string, gender, speed, pitch, comment_id, part):

    # definir o encoding do ficheiro
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speed, pitch=pitch)

    synthesis_input = texttospeech.SynthesisInput(text=text_string)
    if gender == 'male':
        voice = male_voice
    else:
        voice = female_voice

    # faz o pedido à google API
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    #guarda o ficheiro mp3
    with open('./audios/' + str(comment_id) + "_" + str(part) + '.mp3', 'wb') as out:
        out.write(response.audio_content)


#get_single_audio('Ola está tudo bem', 'male', 1, 0, 456, 1)
