![diagram](https://media.discordapp.net/attachments/806271593956507698/914619170287669258/unknown.png)
# imoog

### A simple to use database-based deployable CDN node for hobbyist developers who wish to have their own CDN!

## Setup
---
- Clone this repo via this command: `git clone https://github.com/justanotherbyte/imoog`
- Go into the `imoog/settings.py` file and adjust your settings. Examples for both database drivers have been provided in the file.
- Install a production asgi server of your choice. The 2 I recommend are [`hypercorn`](https://pypi.org/project/hypercorn/) and [`uvicorn`](https://pypi.org/project/uvicorn/). Installing their base packages will suffice.
- To automatically install the respective dependencies, please run `pip install -r requirements.txt` in the directory where you wish to store your node.
- It is recommended to house the `imoog` folder within another folder, as there are other files that come with this repo, that are not housed within the `imoog` folder.

## Uploading Files
---
This Node receives files via `multipart/form-data`. So it's best if you were to adapt your upload system to this. The field name the node expects is just `file`, so please upload it with this name. Please remember to register the `Authorization` header. This key can be set in the `imoog/settings.py` file.

## Upload example (aiohttp)
```py
import aiohttp
import asyncio


async def main():
    session = aiohttp.ClientSession()
    form  = aiohttp.FormData()
    form.add_field("file", b'imagebyteshere', content_type="bytes")
    resp = await session.post("http://localhost:8000/upload", data=form, headers={"Authorization": "myawesomesecretkey"})
    returned_data = await resp.json()
    print(returned_data)
    await session.close()

asyncio.get_event_loop().run_until_complete(main())
```
```sh
>>> {'status': 200, 'file_id': 'FSTSH2RPI'}
```

## Driver and dependency information
Internally, imoog uses 2 different libraries for the 2 different supported database drivers. 

- PostgreSQL - [`asyncpg`](https://github.com/MagicStack/asyncpg)
- MongoDB - [`motor`](https://github.com/mongodb/motor)

Both of these libraries are currently the best in their field for asynchronous client side connections to their respective databases.