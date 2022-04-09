DATABASE_DRIVERS = {
    "driver": "imoog.database.mongo", # https://www.mongodb.com/
    "config": {
        "connection_uri": "mongodb cluster connection uri",
        "database_name": "database name",
        "collection_name": "collection name"
    }
}

###### Postgres Driver example
# ==============================
# DATABASE_DRIVERS = {
#     "driver": "imoog.database.postgres", # https://www.postgresql.org/
#     "config": {
#         "connection_uri": "your connection uri",
#         "max_size": 100, # the maximum amount of connections to create for the PostgreSQL connection pool
#         "min_size": 75, # the minimum amount of connections to create for the PostgreSQL connection pool
#         "table_name": "my_images"
#     }
# }

CACHE_DRIVERS = {
    "driver": "imoog.cache.memorycache", # basic in memory cache. Cleared everytime your node shutsdown.
    "config": {} # leave this empty as memory caches have no config
    # apart from the MAX_CACHE_SIZE which is inferred from the setting automatically.
}

##### Redis Cache Driver example
# ==============================
# CACHE_DRIVERS = {
#     "driver": "imoog.cache.rediscache",
#     "config": {
#         "connection_uri": "redis connection uri",
#         "username": "username for auth",
#         "password": "password for auth"
#         # please REMOVE the username and password keys if your redis instance
#         # does not require username and password authentication
#         # OR if your connection uri includes these details.
#     }
# }

COMPRESSION_LEVEL = 6 # this is the optimal level for speed and compression.
# the higher the number, the better the compression, but it takes longer.
# the smaller the number, the worse the compression, but its much faster.

MAX_CACHE_SIZE = 100 # set a maximum cache size. If you want a cache with no limit -
# simply set this value to 'inf'. This setting is useful if you have a limited amount
# of memory to work with. THIS APPLIES ONLY TO THE IN MEMORY DATABASE.

SECRET_KEY = "SET_A_CUSTOM_KEY" # a secret key that will be checked in the 'Authorization' header
# whenever a POST request is made to /upload endpoint.

NOT_FOUND_STATUS_CODE = 404 # the status code to return when a file is not found.
# this can be custsomised to your liking. A good use case to customise this is if
# you are requesting files off your network programatically.

FILE_NAME_LENGTH = 9 # the length that the generated unique file names should be.
# usually reducing this value will not change how large your keys are inside in your database.
# 9 is a nice value, as it makes it quite unique, while still being a manageable size to remember.

DELIVER_ENDPOINT_METHODS = ["GET"] # the HTTP methods that your deliver endpoint will allow.
# this is really just something to customise.

DELIVER_ENDPOINT = "/image/" # the path for your deliver endpoint. the default is '/image/'.
# an example would be: https://yourdomain.com/<DELIVER_ENDPOINT>/<UNQIUE_FILE_ID>
# this MUST end with a trailing slash.

ALLOWED_HOSTS = ["*"] # set a list of allowed hosts. 
# by default, this is set to ALL hosts, as indicated through the '*'
# this internally uses Starlette's Trusted Host middleware (starlette.middleware.trustedhost.TrustedHostMiddleware)

ENFORCE_SECURE_SCHEME = False # any incoming requests must be from,
# the https or wss protocols. Any other protcol will be redirected to their secure variant.

CORS_ALLOWED_ORIGINS = ["*"] # a list of allowed origins
# that browsers are allowed to use in a Cross-Domain context.
# by default, this is set to all domains.

FALLBACK_FILE_EXT = "png" # the file extension that imoog will fallback on
# if a file extension was unable to be parsed from the mime type.

FILE_DELETED_STATUS_CODE = 204 # the status code to return when
# a file deletion has succeeded

DELETE_ENDPOINT_METHODS = ["DELETE", "POST", "GET"] # the allowed methods
# for the delete endpoint

REQUIRE_AUTH_FOR_DELETE = True # whether authorization is needed via the secret key
# to delete the file

USE_OPENGRAPH = False # tells imoog whether to use the set open graph properties
# allows you to easily turn on and off open graph usage

OPENGRAPH_PROPERTIES = {
    "title": "a cool title",
    "description": "some other cool description",
    "type": "website",
    "site_name": "imoog"
} # these follow the opengraph specification. Say you add a property called "netflix", imoog will render it as
# og:netflix. Be careful to not add invalid properties. DO NOT add the image or video properties. This will override
# imoog's handling, and could break something internally.

OPENGRAPH_BASE_HTML = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {opengraph}
    <title>imoog</title>
</head>
<body>
    
</body>
</html>
""" # don't change this unless you actually know what you're doing.
