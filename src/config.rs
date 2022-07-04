use serde::Deserialize;

#[derive(Deserialize, Clone)]
pub struct Server {
    pub host: [u8; 4],
    pub port: u16
}

#[derive(Deserialize, Clone)]
pub struct DriverInfo {
    pub connection_uri: String,
    pub driver: String
}

#[derive(Deserialize, Clone)]
pub struct Config {
    pub server: Server,
    pub database: DriverInfo,
    pub imoog: Imoog
}

#[derive(Deserialize, Clone)]
pub struct Imoog {
    pub password: String,
    pub id_length: usize,
    pub fallback_mime: String,
    pub deliver_endpoint: String
}