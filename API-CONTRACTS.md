# API Contracts Specification

Backend API endpoint documentation for the Neutale audiobook platform.

## 📋 Overview

This document defines the API contracts that must be implemented by the audiobook backend and consumed by client applications.

## 🔗 Base Configuration

### Production Environment
- **Base URL**: `https://audiobook-dev.sunny250486.workers.dev`
- **Protocol**: HTTPS only
- **Authentication**: Bearer tokens in Authorization header

### Development Environment
- **Base URL**: `http://localhost:8787` (Wrangler dev server)
- **Protocol**: HTTP acceptable for local development

## 📝 Content Delivery Endpoints

### Story Metadata
```http
GET /api/content/{storyId}/metadata/{language}
```

**Response Format:**
```json
{
  "id": "story-id",
  "title": "Story Title",
  "author": "AI Story Weaver",
  "description": "Story description...",
  "coverImage": "https://audiobook-dev.sunny250486.workers.dev/api/content/story-id/image/en/cover.jpg",
  "thumbnail": "https://audiobook-dev.sunny250486.workers.dev/api/content/story-id/image/en/thumbnail.jpg",
  "originLanguage": "en",
  "supportedLanguages": ["en"],
  "totalChapters": 5,
  "genre": "Fantasy",
  "readingTime": 45,
  "tags": ["fantasy", "adventure"],
  "status": "published",
  "chapters": [
    {
      "id": "chapter-1",
      "title": "Chapter Title",
      "chapterNumber": 1,
      "duration": 180.5,
      "audioUrl": "https://audiobook-dev.sunny250486.workers.dev/api/content/story-id/audio/en/chapter_01_title.mp3"
    }
  ]
}
```

### Chapter Content
```http
GET /api/content/{storyId}/chapter/{language}/{filename}
```

**Parameters:**
- `filename`: Format `chapter{N}.json` (e.g., `chapter1.json`)

**Response Format:**
```json
{
  "chapterNumber": 1,
  "title": "Chapter Title",
  "blocks": [
    {
      "type": "heading",
      "content": "Chapter Title",
      "level": 1
    },
    {
      "type": "paragraph",
      "content": "Chapter content text..."
    }
  ]
}
```

### Images
```http
GET /api/content/{storyId}/image/{language}/{filename}
```

**Common filenames:**
- `cover.jpg`: Story cover image
- `thumbnail.jpg`: Story thumbnail
- `ch{N}_img{N}.jpg`: Chapter-specific images

### Audio Files
```http
GET /api/content/{storyId}/audio/{language}/{filename}
```

**Filename formats:**
- `chapter_01_title.mp3`: Chapter audio with descriptive naming
- `main.mp3`: Full story audio (legacy format)

## 🔐 Authentication Endpoints

### User Authentication
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "refresh_token": "refresh_token_here",
  "expires_in": 3600,
  "user": {
    "id": "user-id",
    "email": "user@example.com",
    "preferences": {
      "languages": ["en", "es"]
    }
  }
}
```

## 👤 User Tracking Endpoints

### Progress Tracking
```http
POST /api/user/progress
Authorization: Bearer {token}
Content-Type: application/json

{
  "storyId": "story-id",
  "chapterNumber": 1,
  "progress": 0.75,
  "language": "en"
}
```

### Bookmarks
```http
POST /api/user/bookmarks
Authorization: Bearer {token}
Content-Type: application/json

{
  "storyId": "story-id",
  "chapterNumber": 1,
  "position": "paragraph-3",
  "note": "Important plot point",
  "language": "en"
}
```

### Continue Reading
```http
GET /api/user/continue-reading
Authorization: Bearer {token}
```

**Response:**
```json
{
  "storyId": "story-id",
  "chapterNumber": 2,
  "progress": 0.3,
  "language": "en",
  "lastReadAt": "2025-08-20T10:30:00Z"
}
```

## 📊 Story Discovery Endpoints

### Story Listing
```http
GET /api/stories?language={language}&genre={genre}&limit={limit}&offset={offset}
```

**Response:**
```json
{
  "stories": [
    {
      "id": "story-id",
      "title": "Story Title",
      "author": "AI Story Weaver",
      "description": "Brief description...",
      "coverImage": "full_url_to_cover",
      "thumbnail": "full_url_to_thumbnail",
      "genre": "Fantasy",
      "readingTime": 45,
      "totalChapters": 5,
      "tags": ["fantasy", "adventure"]
    }
  ],
  "total": 100,
  "hasMore": true
}
```

### Search Stories
```http
GET /api/stories/search?q={query}&language={language}
```

## ⚠️ Error Handling

### Standard Error Response
```json
{
  "error": {
    "code": "STORY_NOT_FOUND",
    "message": "Story with ID 'invalid-story' not found",
    "details": {
      "storyId": "invalid-story",
      "language": "en"
    }
  }
}
```

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `401`: Unauthorized (missing/invalid token)
- `404`: Not Found (story/chapter doesn't exist)
- `429`: Rate Limited
- `500`: Internal Server Error

## 🔄 Rate Limiting

- **Authenticated users**: 1000 requests/hour
- **Anonymous users**: 100 requests/hour
- **Content delivery**: No limit (cached responses)

## 📝 Implementation Requirements

### Backend Requirements
1. **Content URLs**: Always return absolute URLs in metadata
2. **CORS**: Enable cross-origin requests for web clients
3. **Caching**: Implement proper cache headers for static content
4. **Error Handling**: Return consistent error format
5. **Authentication**: Support JWT tokens with proper validation

### Client Requirements
1. **URL Handling**: Support both relative and absolute URLs
2. **Error Handling**: Handle all documented error codes gracefully
3. **Authentication**: Include Bearer token in protected endpoints
4. **Caching**: Implement client-side caching for metadata and content

## 🚀 Future Endpoints (Planned)

- `/api/stories/recommended`: Personalized recommendations
- `/api/user/preferences`: User preference management
- `/api/content/{storyId}/analytics`: Content analytics
- `/api/admin/content`: Content management endpoints

---

**Version**: 1.0.0  
**Last Updated**: August 20, 2025  
**Status**: ✅ Active Implementation