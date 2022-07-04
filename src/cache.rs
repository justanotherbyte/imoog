use dashmap::DashMap;
use std::sync::Arc;
use crate::database::traits::MediaData;

pub struct Cache {
    map: Arc<DashMap<String, MediaData>>
}

impl Cache {
    pub fn build() -> Self {
        let map = DashMap::new();
        let arc_map = Arc::new(map);
        Self { map: arc_map }
    }

    pub fn get(&self, identifier: &String) -> Option<MediaData> {
        let map_ref = self.map.get(identifier);
        map_ref.map(|r| r.value().clone())
    }

    pub fn delete(&self, identifier: &String) {
        self.map.remove(identifier);
    }

    pub fn insert(&self, identifier: String, media: MediaData) {
        self.map.insert(identifier, media);
    }
}

