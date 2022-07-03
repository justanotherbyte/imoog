use async_trait::async_trait;
use crate::{
    ImoogResult,
    database::traits::MediaData
};

#[async_trait]
pub trait CacheTrait {
    async fn insert(&mut self, media: &MediaData) -> ImoogResult<()>;
    async fn get(&mut self, identifier: String) -> ImoogResult<Option<MediaData>>;
    async fn delete(&mut self, identifier: String) -> ImoogResult<()>;
}