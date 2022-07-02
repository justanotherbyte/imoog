use super::traits::{
    DatabaseTrait,
    MediaData
};
use async_trait::async_trait;
use mongodb::{
    Client,
    Collection,
    bson::doc,
    options::{ClientOptions, ResolverConfig}
};
use bytes::Bytes;
use crate::ImoogResult;

pub struct MongoDriver {
    collection: Collection<MediaData>
}

#[async_trait]
impl DatabaseTrait for MongoDriver {
    async fn get(&self, identifier: String) -> ImoogResult<Option<MediaData>> {
        let filter = doc! { "_id": identifier };
        let document = self.collection.find_one(filter, None)
            .await
            .ok();

        Ok(document.flatten())
    }
    async fn insert(&self, identifier: String, data: Bytes, mime: String) -> ImoogResult<()> {
        let media = MediaData {
            _id: identifier,
            content: data[..].to_owned(),
            mime
        };
        self.collection.insert_one(&media, None)
            .await?;
        
        Ok(())
    }
    async fn delete(&self, identifier: String) -> ImoogResult<()> {
        let filter = doc! { "_id": identifier };
        self.collection.delete_one(filter, None)
            .await?;
        
        Ok(())
    }
}

impl MongoDriver { // again, to not make state cry
    pub async fn new(connection_uri: &str) -> Self {
        let options = ClientOptions::parse_with_resolver_config(
            connection_uri,
            ResolverConfig::cloudflare()
        )
            .await
            .expect("Failed to parse options from MongoDB connection uri");
        
        let client = Client::with_options(options)
            .expect("Failed to build MongoDB client from options");

        let database = client.database("imoog");
        let collection = database.collection::<MediaData>("media");

        Self { collection }
    }
}