import pandas as pd
import requests
from PIL import Image
from io import BytesIO

def get_profile_picture_from_id(pathOfFile, targetId):
    # Read the CSV file(from given data setput)
    df = pd.read_csv(pathOfFile)

    # Find the row with the given ID Number(person all info)
    row = df[df['ID Number'] == targetId]

    if row.empty:
        return f"No record found for ID Number: {targetId}"

    # Extract Google Drive sharing URL
    drive_url = row.iloc[0]['Profile Picture']

    # Extract the file ID from the Google Drive link
    try:
        if "id=" in drive_url:
            file_id = drive_url.split("id=")[1]
        elif "file/d/" in drive_url:
            file_id = drive_url.split("file/d/")[1].split("/")[0]
        else:
            return "Invalid Google Drive URL format"

        # Construct direct download link(downlad+imagelink)
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        # Download image
        response = requests.get(download_url)
        image = Image.open(BytesIO(response.content))

        return image

    except Exception as e:
        return f"Error processing image: {str(e)}"
    