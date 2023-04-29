import logging
from telegram.ext import filters, Application, MessageHandler
from dotenv import load_dotenv
import os
import whisper
import openai


async def textHandler(update, context):
    print("SE ENVIA RESPUESTA...")
    await context.bot.send_message(update.effective_chat.id, "¡Mandame un audio y lo resumiré!")

async def audioHandler(update, context):
    print("SE DESCARGA EL AUDIO...")

    #Download File
    audio_id = update.message.voice.file_id
    new_file = await context.bot.get_file(audio_id)
    downloaded_file = await new_file.download_to_drive()

    #Transcribe with whisper model
    transcription = model.transcribe(downloaded_file.name)["text"]

    #Use OpenAIApi for a summary of the transcribe
    summary = openAIAPI(transcription)

    #Send messages by telegram bot
    await context.bot.send_message(update.effective_chat.id, "Transcripcion:\n" + transcription)
    await context.bot.send_message(update.effective_chat.id, summary)

def openAIAPI(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "Eres una herramienta que resume la transcripcion de un audio. Vas a recibir la transcripcion de un audio y tienes que generar un pequeño resumen del mismo, hazlo en el idioma del texto"},
                {"role": "user", "content": transcription},
            ]
    )
    return response.choices[0].message.content

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
#Config model and API openai connection
model = whisper.load_model("medium")
#Your openapi API key
openai.api_key = os.environ.get('OPENAPI_API_KEY')
#Your bot token
bot_token = os.environ.get('BOT_TOKEN')

def main():
    application = Application.builder().token(bot_token).build()
    application.add_handler(MessageHandler(filters.TEXT, textHandler))
    application.add_handler(MessageHandler(filters.ATTACHMENT, audioHandler))

    application.run_polling()

if __name__ == '__main__':
    main()
