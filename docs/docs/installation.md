# Installation


## Configuration

Configuring an imoog node is pretty darn simple! imoog uses the `TOML` format for its configuration file. Here's an example:

```toml title="imoog.config.toml"
[server]
host = [127, 0, 0, 1]
port= 6969

[database]
connection_uri = "a mongodb connection uri"
driver = "mongo"

[cache]
connection_uri = "blank/redis connection uri" # use "blank" if
# your driver is "memory"
driver = "memory/redis"

[imoog]
force_https = true
password = "my super secret password"
id_length = 5
fallback_mime = "image/png"
```