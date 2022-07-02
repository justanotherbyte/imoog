use axum::{
    Server,
    Router,
    response::{IntoResponse, Response},
    http::StatusCode,
    routing::{post, get}
};
use tower_http::catch_panic::CatchPanicLayer;
use once_cell::sync::OnceCell;
use std::{
    fs,
    net::SocketAddr,
};

mod config;
use config::Config;

mod database;
use database::{
    mongo::MongoDriver,
    postgres::PostgresDriver
};

mod state;
use state::State;

mod routes;
use routes::{
    upload_media,
    deliver_media
};

// some global stuff

static STATE: OnceCell<State> = OnceCell::new();

pub struct Error(anyhow::Error);
impl<E: Into<anyhow::Error>> From<E> for Error {
    fn from(err: E) -> Self {
        Self(err.into())
    }
}

pub type ImoogResult<T, E = Error> = Result<T, E>;

impl IntoResponse for Error {
    fn into_response(self) -> Response {
        let description = self.0.to_string();
        (StatusCode::INTERNAL_SERVER_ERROR, description).into_response()
    }
}

#[tokio::main]
async fn main() {
    let config_raw = fs::read_to_string("imoog.config.toml")
        .expect("Failed to read imoog.config.toml file. Are you sure it exists, and lives in the cwd?");

    let config: Config = toml::from_str(config_raw.as_str())
        .expect("Failed to parse config file");

    let database_driver = config.database.driver.as_str();

    match database_driver {
        "mongo" => {
            let driver = MongoDriver::new(config.database.connection_uri.as_str())
                .await; // panics occur within the new method
                // i don't like handling results in match blocks
            STATE.set(State {
                database: Box::new(driver),
                config: config.clone()
            }).unwrap() // we know its empty, so its fine here
        },
        "postgres" => {
            let driver = PostgresDriver::new(config.database.connection_uri.as_str())
                .await;
            STATE.set(State {
                database: Box::new(driver),
                config: config.clone()
            }).unwrap()
        },
        other => {
            panic!("Unknown database driver {other}")
        }
    }

    let router = Router::new()
        .route("/upload", post(upload_media))
        .route("/media/:identifier", get(deliver_media))
        .layer(CatchPanicLayer::new());

    let addr = SocketAddr::from((config.server.host, config.server.port));

    Server::bind(&addr)
        .serve(router.into_make_service())
        .await
        .expect("Failed to serve");
}