import os
import subprocess

# create folder if not exists
os.makedirs("audios", exist_ok=True)

files = os.listdir("videos")

for file in files:

    # skip non-video files
    if not file.lower().endswith((".mp4", ".mkv", ".mov")):
        continue

    try:
        
        base_name = os.path.splitext(file)[0]   # remove .mp4
        parts = base_name.split("_")

        if len(parts) < 2:
            print(f"Skipping (bad name): {file}")
            continue

        tutorial_number = parts[0]
        title = "_".join(parts[1:])

        # clean title (remove spaces & symbols)
        title = title.replace(" ", "_")

        output_file = f"audios/{tutorial_number}_{title}.mp3"

        print(f"🎧 Converting: {file} → {output_file}")

        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", f"videos/{file}",
                "-vn",
                "-acodec", "libmp3lame",
                "-ar", "16000",   # better for speech
                "-ac", "1",       # mono
                output_file
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            print(f"FFmpeg error in {file}")
            print(result.stderr.decode())

    except Exception as e:
        print(f"Error processing {file}: {e}")