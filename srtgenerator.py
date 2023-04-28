import os
import requests

folder_path = "(Insert your path for media)" # replace with your folder path
base_url = "http://dockercontainerurl:9000/asr?method=openai-whisper&task=transcribe&language=en&encode=true&output=srt"

#This will parse through all files in the folder you added for folder path and generate a .srt file for each video

file_count = 0
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if file_name.endswith(".mkv") or file_name.endswith(".mp4") or file_name.endswith(".avi"):
            # check if there is a corresponding srt file
            srt_file_name = os.path.splitext(file_name)[0] + ".srt"
            srt_file_path = os.path.join(root, srt_file_name)
            if not os.path.exists(srt_file_path):
                # create HTTP request to transcribe audio file
                audio_file_path = os.path.join(root, file_name)
                audio_file = {"audio_file": (file_name, open(audio_file_path, "rb"), "video/x-matroska")}
                response = requests.post(base_url, files=audio_file, stream=True)
                response.raise_for_status()

                # save response data to SRT file
                with open(srt_file_path, "wb") as srt_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        srt_file.write(chunk)

                # increment file count and display progress
                file_count += 1
                print(f"Processed {file_count} files. Current file: {file_name}")
