from fastapi import FastAPI, UploadFile, File
from PIL import Image
from PIL.ExifTags import TAGS


app = FastAPI()


@app.get("/")
async def root():
    return {"Message" : "This api returns metadata about a picture"}

@app.post("/")
async def upload(file:UploadFile = File()):

    contents = await file.read()

    with open(f"{file.filename}", "wb") as f:
        f.write(contents)


    picture = Image.open(file.filename)
    return image_metadata(picture)


def image_metadata(file):
    info_dict = {
    "Filename": file.filename,
    "Image Height": file.height,
    "Image Width": file.width,
    "Image Format": file.format,
    "Image Mode": file.mode,
    "Image is Animated": getattr(file, "is_animated", False),
    "Frames in Image": getattr(file, "n_frames", 1)
    }
    exifdata = file.getexif()

    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()

        info_dict[str(tag).strip()]=(str(data))
    return info_dict
