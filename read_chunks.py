import requests
import os
import json
import numpy as np
import pandas as pd
import joblib

# 🔹 Embedding function
def create_embedding(text_list):
    try:
        r = requests.post(
            "http://localhost:11434/api/embed",
            json={
                "model": "bge-m3",
                "input": text_list
            },
            timeout=60
        )

        r.raise_for_status()
        data = r.json()

        if "embeddings" not in data:
            print("Embedding API error:", data)
            return None

        return data["embeddings"]

    except Exception as e:
        print("Embedding error:", e)
        return None


# 🔹 Folder check
folder_path = "jsons"

if not os.path.exists(folder_path):
    print("❌ 'jsons' folder not found!")
    exit()

json_files = os.listdir(folder_path)

my_dicts = []
chunk_id = 0


# 🔹 Main loop
for json_file in json_files:

    if not json_file.endswith(".mp3.json"):
        continue

    file_path = os.path.join(folder_path, json_file)

    with open(file_path, encoding="utf-8") as f:
        content = json.load(f)

    print(f"📦 Processing: {json_file}")

    chunks = content.get("chunks", [])

    if not chunks:
        print("⚠️ No chunks found")
        continue

    # Extract valid texts
    texts = [c.get("text", "").strip() for c in chunks if c.get("text")]

    if not texts:
        print("⚠️ No valid text found")
        continue

    # Create embeddings
    embeddings = create_embedding(texts)

    if embeddings is None:
        print("❌ Embedding failed")
        continue

    if len(embeddings) != len(texts):
        print("❌ Embedding length mismatch")
        continue

    # Map embeddings to chunks
    text_index = 0

    for chunk in chunks:
        text = chunk.get("text", "").strip()

        if not text:
            continue

        chunk_data = {
            "chunk_id": chunk_id,
            "file_name": json_file,
            "number": chunk.get("number"),
            "title": chunk.get("title"),
            "start": chunk.get("start"),
            "end": chunk.get("end"),
            "text": text,
            "embedding": embeddings[text_index]
        }

        my_dicts.append(chunk_data)

        chunk_id += 1
        text_index += 1


# 🔹 Final check
if len(my_dicts) == 0:
    print("❌ No embeddings created! Check JSON or API.")
    exit()


# 🔹 Create DataFrame
df = pd.DataFrame(my_dicts)

# 🔹 Save file
joblib.dump(df, "embeddings.joblib")

print("\n✅ Done!")
print("Total chunks:", len(df))