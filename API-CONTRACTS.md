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

## 👤 User Profile Management

### Get User Profile
```http
GET /api/user/profile
Authorization: Bearer {token}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "profile": {
      "id": "user_123",
      "email": "user@example.com",
      "name": "John Doe",
      "bio": "Book lover and storyteller",
      "picture": "https://audiobook-dev.sunny250486.workers.dev/api/assets/profile-images/user_123_1704108600.jpg",
      "defaultLanguage": "en",
      "lastLoginAt": "2024-01-15T10:30:00Z",
      "totalReadingTime": 7200,
      "storiesCompleted": 15,
      "preferredLanguage": "en",
      "timezone": "America/New_York",
      "subscriptionTier": "premium",
      "createdAt": "2023-06-01T12:00:00Z",
      "updatedAt": "2024-01-15T10:30:00Z"
    },
    "preferences": {
      "userId": "user_123",
      "version": 1,
      "needsSync": false,
      "defaultLanguage": "en",
      "preferredReadingMode": "read",
      "fontSize": "medium",
      "fontFamily": "system",
      "lineHeight": 1.6,
      "theme": "auto",
      "audioPlaybackSpeed": 1.0,
      "autoPlayNextChapter": true,
      "backgroundAudio": false,
      "skipSilence": false,
      "pageTurnAnimation": true,
      "readingProgressIndicator": true,
      "chapterCompletionCelebration": true,
      "syncEnabled": true,
      "offlineSync": true,
      "wifiOnlySync": false,
      "syncFrequency": "immediate",
      "readingReminders": false,
      "reminderTime": "19:00",
      "reminderDays": [1, 2, 3, 4, 5],
      "newContentNotifications": true,
      "achievementNotifications": true,
      "bookmarkNotifications": true,
      "analyticsEnabled": true,
      "shareReadingProgress": false,
      "highContrast": false,
      "reduceMotion": false,
      "screenReaderOptimized": false,
      "updatedAt": "2024-01-15T10:30:00Z",
      "lastSyncedAt": "2024-01-15T10:30:00Z"
    }
  }
}
```

### Update User Profile
```http
PATCH /api/user/profile
Authorization: Bearer {token}
Content-Type: application/json

{
  "profile": {
    "name": "Updated Name",
    "bio": "Updated bio text",
    "defaultLanguage": "es"
  },
  "preferences": {
    "theme": "dark",
    "audioPlaybackSpeed": 1.5,
    "fontSize": "large"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "updated": {
    "profile": true,
    "preferences": true
  }
}
```

### Upload Profile Image
```http
POST /api/user/profile/image
Authorization: Bearer {token}
Content-Type: multipart/form-data

FormData:
  image: File (JPEG/PNG, max 5MB, recommended 512x512px)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "imageUrl": "https://audiobook-dev.sunny250486.workers.dev/api/assets/profile-images/user_123_1704108600.jpg"
  }
}
```

## 📊 User Statistics

### Get Reading Statistics
```http
GET /api/user/statistics
Authorization: Bearer {token}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "books_read": 12,
    "total_reading_time_minutes": 1440,
    "current_streak_days": 7,
    "longest_streak_days": 21,
    "chapters_completed": 156,
    "favorite_genre": "Fantasy",
    "reading_sessions": 89,
    "average_session_time_minutes": 16,
    "last_reading_date": "2024-01-15T22:30:00Z",
    "achievements": [
      {
        "id": "first_book",
        "name": "First Chapter",
        "description": "Complete your first chapter",
        "earned_at": "2023-06-01T15:00:00Z"
      },
      {
        "id": "book_lover",
        "name": "Book Lover",
        "description": "Complete 5 stories",
        "earned_at": "2024-01-15T22:30:00Z"
      }
    ]
  }
}
```

## 🛠️ Support System

### Get FAQs
```http
GET /api/support/faqs?category={category}&language={language}
```

**Query Parameters:**
- `category` (optional): Filter by category (`general`, `technical`, `customization`)
- `language` (optional): FAQ language (default: `en`)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "faq_001",
      "question": "How do I download stories for offline reading?",
      "answer": "To download stories for offline reading, tap the download icon on any story. You can manage your downloads in the Library section under 'Downloaded'.",
      "category": "general",
      "order": 1
    },
    {
      "id": "faq_002",
      "question": "Can I change the reading speed of audiobooks?",
      "answer": "Yes! While playing an audiobook, tap the playback speed button (usually shows '1x') and select your preferred speed from 0.5x to 2.0x.",
      "category": "technical",
      "order": 2
    }
  ]
}
```

## 🖼️ Asset Management

### Serve Profile Images
```http
GET /api/assets/profile-images/{filename}
```

**Response**: Binary image data with proper caching headers
- Content-Type: `image/jpeg` or `image/png`
- Cache-Control: `public, max-age=31536000` (1 year)
- ETag and Last-Modified headers for efficient caching

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

### Standard Success Response (Profile & Support APIs)
```json
{
  "success": true,
  "message": "Optional success message",
  "data": {
    // Response data
  }
}
```

### Standard Error Response (Profile & Support APIs)
```json
{
  "success": false,
  "message": "Error description",
  "error_code": "ERROR_CODE",
  "details": {
    // Optional additional error details
  }
}
```

### Legacy Error Response (Content APIs)
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
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found (resource doesn't exist)
- `413`: Payload Too Large (file upload too big)
- `422`: Unprocessable Entity (validation errors)
- `429`: Rate Limited
- `500`: Internal Server Error

### Example Error Responses

**File Too Large (413)**:
```json
{
  "success": false,
  "message": "Profile image too large. Maximum size is 5MB.",
  "error_code": "FILE_TOO_LARGE"
}
```

**Validation Error (400)**:
```json
{
  "success": false,
  "message": "Invalid file type. Only JPEG and PNG images are allowed."
}
```

**Authentication Error (401)**:
```json
{
  "error": "Missing or invalid Authorization header"
}
```

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

## 🚀 Recently Implemented (v1.1.0)

✅ **User Profile Management**
- GET `/api/user/profile` - Complete profile and preferences
- PATCH `/api/user/profile` - Update profile and preferences
- POST `/api/user/profile/image` - Profile image upload

✅ **User Statistics & Analytics**
- GET `/api/user/statistics` - Reading statistics and achievements

✅ **Support System**
- GET `/api/support/faqs` - FAQ system with filtering

✅ **Asset Management**
- GET `/api/assets/profile-images/{filename}` - Profile image serving

## 🚀 Future Endpoints (Planned)

- `/api/stories/recommended`: Personalized recommendations based on reading history
- `/api/support/tickets`: Support ticket system (chat integration planned)
- `/api/user/cache-info`: Cache management endpoints
- `/api/content/{storyId}/analytics`: Content analytics and engagement metrics
- `/api/admin/content`: Content management endpoints
- `/api/user/leaderboards`: Reading competitions and leaderboards

---

**Version**: 1.1.0  
**Last Updated**: August 21, 2025  
**Status**: ✅ Active Implementation with Profile Features