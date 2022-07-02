use serde::Deserialize;

#[derive(Deserialize, Clone)]
pub struct Server {
    pub host: [u8; 4],
    pub port: u16
}

#[derive(Deserialize, Clone)]
pub struct Database {
    pub connection_uri: String,
    pub driver: String
}

#[derive(Deserialize, Clone)]
pub struct Config {
    pub server: Server,
    pub database: Database,
    pub imoog: Imoog
}

#[derive(Deserialize, Clone)]
pub struct Imoog {
    pub force_https: bool,
    pub password: String,
    pub id_length: usize,
    pub fallback_mime: String
}