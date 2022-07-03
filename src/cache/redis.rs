use redis::{
    AsyncCommands,
    aio::Connection
};
use async_trait::async_trait;
use super::traits::CacheTrait;
use crate::{
    database::traits::MediaData,
    ImoogResult
};

pub struct RedisCache {
    conn: Connection
}

#[async_trait]
impl CacheTrait for RedisCache {
    async fn insert(&mut self, media: &MediaData) -> ImoogResult<()> {
        let content_key = format!("{}-content", &media._id);
        let mime_key = format!("{}-mime", &media._id);
        
        self.conn.set(content_key.as_str(), &media.content)
            .await?;
        self.conn.set(mime_key.as_str(), &media.mime)
            .await?;
        
        Ok(())
    }
    async fn get(&mut self, identifier: String) -> ImoogResult<Option<MediaData>> {
        let content_key = format!("{}-content", &identifier);
        let mime_key = format!("{}-mime", &identifier);

        let content: Option<Vec<u8>> = self.conn.get(content_key.as_str())
            .await?;
        let mime: Option<String> = self.conn.get(mime_key.as_str())
            .await?;

        if (content == None) | (mime == None) {
            return Ok(None)
        }

        let md = MediaData {
            _id: identifier,
            content: content.unwrap(),
            mime: mime.unwrap()
        };

        Ok(Some(md))
    }
    async fn delete(&mut self, identifier: String) -> ImoogResult<()> {
        let content_key = format!("{}-content", &identifier);
        let mime_key = format!("{}-mime", &identifier);

        self.conn.del(content_key.as_str())
            .await?;
        self.conn.del(mime_key.as_str())
            .await?;

        Ok(())
    }
}

impl RedisCache {
    pub async fn new(connection_uri: &str) -> Self {
        let client = redis::Client::open(connection_uri).unwrap();
        let conn = client.get_tokio_connection().await.unwrap();

        Self { conn }
    }
}