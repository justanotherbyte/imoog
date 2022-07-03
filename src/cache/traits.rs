use async_trait::async_trait;
use crate::{
    ImoogResult,
    database::traits::MediaData
};

#[async_trait]
pub trait CacheTrait {
    async fn insert(&self, media: &MediaData) -> ImoogResult<()>;
    async fn get(&self, identifier: String) -> ImoogResult<Option<MediaData>>;
    async fn delete(&self, identifier: String) -> ImoogResult<()>;
}