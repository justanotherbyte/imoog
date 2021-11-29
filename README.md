
<h1 align="center">
<sub>
    <img src="https://www.cloudflare.com/static/e483f0dab463205cec2642ab111e81fc/cdn-global-hero-illustration.svg" height="36">
</sub>
&nbsp;
imoog
</h1>
<p align="center">
<sup>
A database-based CDN node supporting PostgreSQL and MongoDB backends. 
</sup>
<br>
<sup>
    <a href="https://www.digitalocean.com/community/tutorials/how-to-host-a-website-using-cloudflare-and-nginx-on-ubuntu-16-04">Ubuntu host guide by Digital Ocean.</a>
</sup>
</p>

***

### A simple to use database-based deployable CDN node for hobbyist developers who wish to have their own CDN!

## Setup
---
- Clone this repo via this command: `git clone https://github.com/justanotherbyte/imoog`
- Go into the `imoog/settings.py` file and adjust your settings. Examples for both database drivers have been provided in the file.
- Install a production asgi server of your choice. The 2 I recommend are [`hypercorn`](https://pypi.org/project/hypercorn/) and [`uvicorn`](https://pypi.org/project/uvicorn/). Installing their base packages will suffice.
- To automatically install the respective dependencies, please run `pip install -r requirements.txt` in the directory where you wish to store your node.
- It is recommended to house the `imoog` folder within another folder, as there are other files that come with this repo, that are not housed within the `imoog` folder.

## Running your ASGI server
---
#### Hypercorn
```sh
# inside the imoog directory
hypercorn app:app --graceful-timeout 3 --workers 3

# outside of the imoog directory
hypercorn imoog.app:app --graceful-timeout 3 --workers 3
```
#### Uvicorn
```sh
# inside the imoog directory
uvicorn app:app --workers 3 

# outside of the imoog directory
uvicorn imoog.app:app --workers 3
```
Please keep in mind that both Uvicorn and Hypercorn support running applications through the Unix Domain Socket (UDS) protocol rather than the Transmission Control Protocol (TCP). The choice is yours.


## Settings
---
- imoog offers granular control over many key aspects of the node. Most of these can be extremely overwhelming. Go ahead and hop into the `imoog/settings.py` file, where you'll find detailed explanations of each and every setting.
- Another thing that can be overwhelming are the 2 database drivers. How do you configure them? What are their optimal settings. Again, everything is explained inside the `imoog/settings.py` file.

## Proxy
---
- In order to use this node cleanly, I recommend placing yourself behind a proxy server. One of the most popular choices is [`NGINX`](https://www.nginx.com/).

## Caching + Cloudflare
---
- The Imoog Node handles a lot of the caching for you, however, a good next step would be to place your CDN on cloudflare. 
- Cloudflare has some awesome caching solutions. Also, overall, they make it easy to expose your CDN to the open-web.

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