use std::fmt::Debug;

use crate::{
    database::traits::DatabaseTrait,
    cache::traits::CacheTrait
};
use crate::Config;

pub struct State {
    pub database: Box<dyn DatabaseTrait + Send + Sync + 'static>,
    pub cache: Box<dyn CacheTrait + Send + Sync + 'static>,
    pub config: Config
}

impl Debug for State {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("State")
    }
}