use super::traits::{
    DatabaseTrait,
    MediaData
};
use async_trait::async_trait;
use sqlx::{
    Pool,
    Postgres,
    postgres::PgPoolOptions
};
use bytes::Bytes;
use crate::ImoogResult;

pub struct PostgresDriver {
    pool: Pool<Postgres>
}

type PostgresValues = (String, Vec<u8>, String);

#[async_trait]
impl DatabaseTrait for PostgresDriver {
    async fn get(&self, identifier: String) -> ImoogResult<Option<MediaData>> {
        dbg!(identifier);
        let row: Option<PostgresValues> = sqlx::query_as("SELECT (identifier, media, mime) FROM imoog WHERE identifier = $1")
            .bind(identifier)
            .fetch_optional(&self.pool)
            .await
            .ok();
        
        println!("{row:?}");

        Ok(row.map(|x| {
            MediaData {
                _id: x.0,
                content: x.1,
                mime: x.2
            }
        }))
    }
    async fn insert(&self, identifier: String, data: Bytes, mime: String) -> ImoogResult<()> {
        sqlx::query("INSERT INTO imoog(identifier, media, mime) VALUES($1, $2, $3)")
            .bind(identifier)
            .bind(&data[..])
            .bind(mime)
            .execute(&self.pool)
            .await?;

        Ok(())
    }
    async fn delete(&self, identifier: String) -> ImoogResult<()> {
        sqlx::query("DELETE FROM imoog WHERE identifier = $1")
            .bind(identifier)
            .execute(&self.pool)
            .await?;

        Ok(())
    }
}

impl PostgresDriver { // I don't want to make state cry
    pub async fn new(connection_uri: &str) -> Self {
        let pool = PgPoolOptions::new()
            .min_connections(1)
            .connect(connection_uri)
            .await
            .expect("Failed to connect to PostgreSQL database");

        Self { pool }
    }
}