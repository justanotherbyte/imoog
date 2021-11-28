DATABASE_DRIVERS = {
    "driver": "imoog.database.mongo", # https://www.mongodb.com/
    "config": {
        "connection_uri": "your mongodb connection uri",
        "database_name": "your database name",
        "collection_name": "your collection name"
    }
}

###### Postgres Driver example
# ==============================
# DATABASE_DRIVERS = {
#     "driver": "imoog.database.postgres", # https://www.postgresql.org/
#     "config": {
#         "connection_uri": "your connection uri",
#         "max_size": 100,
#         "min_size": 75,
#         "table_name": "my_images"
#     }
# }

COMPRESSION_LEVEL = 6 # this is the optimal level for speed and compression.
# the higher the number, the better the compression, but it takes longer.
# the smaller the number, the worse the compression, but its much faster.

MAX_CACHE_SIZE = 100 # set a maximum cache size. If you want a cache with no limit -
# simply set this value to 'inf'. This is setting is useful if you have a limited amount
# of memory to work with.

SECRET_KEY = "Universemandarin" # a secret key that will be checked in the 'Authorization' header
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
