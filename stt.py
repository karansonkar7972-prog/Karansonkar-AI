import os
import whisper

model = whisper.load_model("base")

files = os.listdir("audios")

for f in files:
    if f.endswith(".mp3"):
        print(f"Processing: {f}")

        result = model.transcribe(
            audio=f"audios/{f}",
            fp16=False,
            temperature=0,
            condition_on_previous_text=False
        )

        print(result["text"])