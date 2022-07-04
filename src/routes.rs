use axum::{
    extract::{Multipart, Path},
    response::{Response, Json},
    body::Body,
    http::{HeaderMap, header::AUTHORIZATION, StatusCode}
};
use serde::{Deserialize, Serialize};
use uuid::Uuid;
use bytes::Bytes;

use crate::{
    ImoogResult,
    STATE,
    database::traits::MediaData
};

#[derive(Serialize, Deserialize)]
pub struct UploadResponse {
    keys: Vec<String>,
    message: &'static str
}

pub async fn upload_media(mut multipart: Multipart, headers: HeaderMap) -> ImoogResult<(StatusCode, Json<UploadResponse>)> {
    let mut keys: Vec<String> = vec![];
    let state = STATE.get().expect("Request received before state has been filled");

    let auth = headers.get(AUTHORIZATION);
    if let Some(auth) = auth {
        let value = auth.to_str()?;
        if value != state.config.imoog.password {
            let up = UploadResponse {
                keys: Vec::new(),
                message: "Bad Authorization"
            };

            return Ok((StatusCode::UNAUTHORIZED, Json(up)))
        }
    } else {
        let up = UploadResponse {
            keys: Vec::new(),
            message: "No Authorization header"
        };

        return Ok((StatusCode::BAD_REQUEST, Json(up)))
    }

    while let Some(field) = multipart.next_field().await? {
        let length = state.config.imoog.id_length;
        let unique_id = &Uuid::new_v4().as_simple().to_string()[0..length];
        keys.push(unique_id.to_string());

        let mime = field.content_type().unwrap_or(state.config.imoog.fallback_mime.as_str()).to_string();
        let data = field.bytes().await?;
        let compressed = deflate::deflate_bytes_zlib(&data[..]);
        let container = Bytes::from(compressed);
        state.database.insert(unique_id.to_string(), container, mime)
            .await?;
    }

    let up = UploadResponse { 
        keys,
        message: "Everything went smoothly :)"
     };
    Ok((StatusCode::OK, Json(up)))
}

pub async fn deliver_media(Path(identifier): Path<String>) -> ImoogResult<Response<Body>> {
    let state = STATE.get().expect("Request received before state has been filled");

    let media: Option<MediaData>;
    let mut update_cache = false;

    let cache_result = state.cache.get(&identifier);
    
    if let Some(cr) = cache_result {
        media = Some(cr)
    } else {
        let db_result = state.database.get(identifier.clone())
            .await?;
        media = db_result;
        update_cache = true
    }
    
    let status_code;
    let media_content;
    let content_type;

    match media {
        Some(m) => {
            if update_cache {
                state.cache.insert(identifier, m.clone());
            }
            let content = inflate::inflate_bytes_zlib(&m.content).expect("Failed to inflate content"); // catch panic layer :)
            media_content = Bytes::from(content);
            status_code = 200;
            content_type = m.mime;
        },
        None => {
            media_content = Bytes::new(); // empty
            content_type = String::new();
            status_code = 404;
        }
    }

    let response = Response::builder()
        .header("content-type", content_type) // can be empty content type
        .status(status_code)
        .body(Body::from(media_content))?;

    Ok(response)
}

pub async fn delete_media(Path(identifier): Path<String>, headers: HeaderMap) -> ImoogResult<StatusCode> {
    let state = STATE.get().expect("Request received before state has been filled");

    let auth = headers.get(AUTHORIZATION);
    if let Some(auth) = auth {
        let value = auth.to_str()?;
        if value != state.config.imoog.password {
            return Ok(StatusCode::UNAUTHORIZED)
        }
    } else {
        return Ok(StatusCode::BAD_REQUEST)
    }

    state.cache.delete(&identifier);
    state.database.delete(identifier)
        .await?;

    Ok(StatusCode::NO_CONTENT)
}