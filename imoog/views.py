from __future__ import annotations

import zlib
import random
import string
from typing import TYPE_CHECKING

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from imoog.settings import (
    COMPRESSION_LEVEL,
    SECRET_KEY,
    FILE_NAME_LENGTH,
    NOT_FOUND_STATUS_CODE
)

if TYPE_CHECKING:
    from starlette.datastructures import UploadFile, MultiDict


async def upload_file(request: Request):
    # the view that will handle uploading files to our database.
    auth = request.headers.get("Authorization")
    if auth != SECRET_KEY:
        content = {
            "message": "Invalid auth."
        }
        return JSONResponse(content, status_code=401)
    
    form: MultiDict = await request.form()
    _file: UploadFile = form.get("file")
    if _file is None:
        print("\033[91mReceived an upload request that has not given us a 'file' to upload\033[0m")
        content = {
            "message": "No 'file' given."
        }
        return JSONResponse(content, status_code=400)
    
    await _file.seek(0)
    image = await _file.read()
    mime = _file.content_type
    compressed = zlib.compress(image, level=int(COMPRESSION_LEVEL))
    name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(FILE_NAME_LENGTH))
    await request.app.db_driver.insert(image=compressed, name=name, mime=mime)
    request.app.insert_cache(name, {"image": image, "mime": mime}) # we insert the UNCOMPRESSED image into the cache, to avoid
    # having to decompress later. The whole point of the cache is to retrieve the value without any
    # extra processing required.

    # if everything goes well, return an JSON response with a 200 status code and the unique file id.
    content = {
        "status": 200,
        "file_id": name
    }
    return JSONResponse(content, status_code=200)

async def deliver_file(request: Request):
    file_id: str = request.path_params["name"]
    file_id = file_id.split(".")[0] # if a file extension has been provided, we split on the '.',
    # and return the file name.

    cache_result = request.app.get_from_cache(file_id)
    if cache_result is None:
        image, mime = await request.app.db_driver.fetch(file_id) # this will decompress it for us too.
    else:
        image, mime = cache_result

    if image is None:
        # return an empty response with a 404, or a custom status code
        # which would've been provided in settings.py
        return Response(None, status_code=NOT_FOUND_STATUS_CODE)

    return Response(
        image,
        status_code=200,
        media_type=mime
    ) # return a 200 response with the correct mime type. Example: image/png
