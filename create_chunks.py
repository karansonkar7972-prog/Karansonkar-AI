import whisper
import json
import os

# 🔹 Load Whisper model (first time slow hoga)
model = whisper.load_model("base")

# 🔹 Folder paths
AUDIO_FOLDER = "audios"
OUTPUT_FOLDER = "jsons"

# 🔹 Create output folder if not exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 🔹 Check audio folder
if not os.path.exists(AUDIO_FOLDER):
    print("❌ 'audios' folder not found!")
    exit()

audios = os.listdir(AUDIO_FOLDER)

# 🔹 Process each audio file
for audio in audios:

    # Only process .mp3 files
    if not audio.endswith(".mp3"):
        continue

    # Expect format: 1_title.mp3
    if "_" not in audio:
        print(f"⚠️ Skipping (wrong format): {audio}")
        continue

    try:
        number = audio.split("_")[0]
        title = audio.split("_")[1].replace(".mp3", "")

        print(f"\n🎧 Processing: {audio}")
        print(f"➡️ Number: {number}, Title: {title}")

        # 🔹 Transcribe + Translate
        result = model.transcribe(
            audio=os.path.join(AUDIO_FOLDER, audio),
            language="hi",          # Hindi input
            task="translate",       # Output in English
            word_timestamps=False
        )

        chunks = []

        for segment in result["segments"]:
            chunk = {
                "number": number,
                "title": title,
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip()
            }
            chunks.append(chunk)

        # 🔹 Final JSON structure
        chunks_with_metadata = {
            "file": audio,
            "chunks": chunks,
            "full_text": result["text"]
        }

        # 🔹 Save JSON
        output_path = os.path.join(OUTPUT_FOLDER, f"{audio}.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks_with_metadata, f, ensure_ascii=False, indent=2)

        print(f"✅ Saved: {output_path}")

    except Exception as e:
        print(f"Error processing {audio}: {e}")

print("\n🚀 All files processed!")