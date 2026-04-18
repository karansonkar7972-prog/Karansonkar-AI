import whisper

model = whisper.load_model("base")

result = model.transcribe(audio = "audios.mp3/1_WhatsApp.mp3",
                          language="hi",
                          task="translate")

print(result["text"])