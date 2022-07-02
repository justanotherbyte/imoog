use async_trait::async_trait;
use serde::{Deserialize, Serialize};
use bytes::Bytes;
use crate::ImoogResult;

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct MediaData {
    pub _id: String,
    #[serde(with = "serde_bytes")]
    pub content: Vec<u8>,
    pub mime: String
}

#[async_trait]
pub trait DatabaseTrait {
    async fn get(&self, identifier: String) -> ImoogResult<Option<MediaData>>;
    async fn insert(&self, identifier: String, data: Bytes, mime: String) -> ImoogResult<()>;
    async fn delete(&self, identifier: String) -> ImoogResult<()>;
}