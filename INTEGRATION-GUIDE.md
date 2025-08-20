# Integration Guide

Cross-project integration guidelines for the Neutale ecosystem.

## 📋 Overview

This guide explains how the three main components of the Neutale ecosystem integrate together:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Storygen   │───▶│  Audiobook  │───▶│   Neutale   │
│   (Python)  │    │ (Cloudflare)│    │  (Flutter)  │
│             │    │             │    │             │
│ Story Gen   │    │ Backend API │    │ Mobile App  │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🔄 Content Flow Pipeline

### 1. Story Generation (Storygen → Platform)

**Process:**
1. Storygen generates story with proper structure
2. Exports to `my_platform_stories/` directory
3. Upload scripts push content to R2 storage
4. Backend API serves content via standardized endpoints

**Key Requirements:**
- Follow `UNIFIED-CONTENT-SPEC.md` format exactly
- Generate proper `metadata.json` with all required fields
- Create sequential chapter files (`chapter1.json`, `chapter2.json`, etc.)
- Include proper story ID generation and validation

**Integration Points:**
```python
# Storygen export format
story_data = {
    "id": generate_story_id(title),  # Must follow spec
    "title": title,
    "totalChapters": len(chapters),  # Required field
    "chapters": chapters,            # Structured content blocks
    # ... other metadata fields
}
```

### 2. Content Management (Storygen → Audiobook)

**Upload Process:**
1. Storygen generates content in local directory
2. Upload scripts validate content format
3. Content uploaded to R2 storage with proper structure
4. Database updated with story metadata

**Upload Commands:**
```bash
# From storygen directory
npx tsx upload_to_audiobook.py --story-id my-story --validate

# Bulk upload
npx tsx scripts/bulk-upload-stories.ts --local
```

**Integration Requirements:**
- Story ID validation before upload
- Chapter numbering validation (must be sequential from 1)
- Metadata schema validation
- Asset file validation (images, audio)

### 3. Content Delivery (Audiobook → Neutale)

**API Integration:**
1. Flutter app requests story metadata
2. Backend serves content with absolute URLs
3. App fetches chapters sequentially
4. Audio/images loaded on demand

**Key Integration Points:**
```dart
// Flutter service integration
final metadata = await apiService.getStoryMetadata(storyId, language);
final chapter = await apiService.getChapterContent(
  storyId, 
  language, 
  'chapter${chapterNumber}.json'
);
```

## 🔧 Development Workflow

### Multi-Repository Setup

1. **Clone all repositories:**
```bash
git clone https://github.com/naiduasn/storygen
git clone https://github.com/naiduasn/audiobook  
git clone https://github.com/naiduasn/neutale
```

2. **Initialize documentation submodules:**
```bash
cd storygen && git submodule update --init --recursive
cd ../audiobook && git submodule update --init --recursive
cd ../neutale && git submodule update --init --recursive
```

3. **Development environment:**
```bash
# Terminal 1: Storygen (story generation)
cd storygen && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Terminal 2: Audiobook backend
cd audiobook && npm install && npm run preview

# Terminal 3: Neutale mobile app  
cd neutale/app && flutter pub get && flutter run -d chrome
```

### Cross-Project Testing

1. **Generate test story in Storygen**
2. **Upload to local Audiobook backend**
3. **Verify content in Neutale app**
4. **Test full pipeline end-to-end**

## 📝 Data Validation

### Story ID Validation
```javascript
// Consistent across all projects
function validateStoryId(id) {
  const pattern = /^[a-z0-9][a-z0-9-]{0,48}[a-z0-9]$/;
  return pattern.test(id) && id.length <= 50;
}
```

### Content Format Validation
```python
# Storygen validation
def validate_story_format(story_data):
    required_fields = ['id', 'title', 'totalChapters', 'chapters']
    for field in required_fields:
        if field not in story_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate chapter numbering
    for i, chapter in enumerate(story_data['chapters']):
        expected_number = i + 1
        if chapter['chapterNumber'] != expected_number:
            raise ValueError(f"Chapter numbering error: expected {expected_number}, got {chapter['chapterNumber']}")
```

### API Response Validation
```dart
// Flutter validation
class StoryMetadata {
  void validateResponse(Map<String, dynamic> json) {
    if (!json.containsKey('totalChapters')) {
      throw FormatException('Missing totalChapters field in metadata');
    }
    
    if (json['chapters'] != null) {
      final chapters = json['chapters'] as List;
      for (int i = 0; i < chapters.length; i++) {
        final chapter = chapters[i];
        if (chapter['chapterNumber'] != i + 1) {
          throw FormatException('Invalid chapter numbering');
        }
      }
    }
  }
}
```

## 🔐 Authentication Integration

### Backend Token Validation
```typescript
// Audiobook backend
export async function validateAuthToken(request: Request): Promise<User | null> {
  const authHeader = request.headers.get('Authorization');
  if (!authHeader?.startsWith('Bearer ')) {
    return null;
  }
  
  const token = authHeader.substring(7);
  // Validate JWT token
  return await verifyJWT(token);
}
```

### Flutter Auth Integration  
```dart
// Neutale app
class ApiService {
  String? _accessToken;
  
  Future<Response> _authenticatedRequest(String url) async {
    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    
    if (_accessToken != null) {
      headers['Authorization'] = 'Bearer $_accessToken';
    }
    
    return await dio.get(url, options: Options(headers: headers));
  }
}
```

## 🚨 Error Handling

### Consistent Error Responses
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Story content validation failed",
    "details": {
      "field": "totalChapters",
      "expected": "integer >= 1",
      "actual": "undefined"
    },
    "timestamp": "2025-08-20T10:30:00Z"
  }
}
```

### Error Code Standards
- `STORY_NOT_FOUND`: Story doesn't exist
- `CHAPTER_NOT_FOUND`: Chapter doesn't exist  
- `VALIDATION_ERROR`: Content format validation failed
- `AUTH_REQUIRED`: Authentication token required
- `AUTH_INVALID`: Invalid or expired token
- `RATE_LIMITED`: Too many requests

## 🔄 Deployment Pipeline

### Staging Environment
1. **Storygen**: Deploy to Google Cloud Run staging
2. **Audiobook**: Deploy to Cloudflare Workers staging environment  
3. **Neutale**: Test builds with staging backend

### Production Deployment
1. **Content Validation**: Ensure all content follows specifications
2. **API Compatibility**: Verify API contracts are maintained
3. **Cross-Platform Testing**: Test on iOS, Android, and Web
4. **Performance Monitoring**: Monitor API response times and error rates

## 📊 Monitoring and Analytics

### Key Metrics
- **Story Generation**: Success rate, generation time
- **API Performance**: Response times, error rates, cache hit rates
- **Mobile App**: Crash rates, user engagement, content consumption

### Integration Health Checks
```bash
# Backend health
curl https://audiobook-dev.sunny250486.workers.dev/api/health

# Content validation
npm run test:content-validation

# Mobile app integration test
flutter test integration_test/
```

## 🔮 Future Integrations

### Planned Features
- **Real-time Sync**: Live content updates across clients
- **Analytics Pipeline**: Content performance analytics
- **A/B Testing**: Content variation testing
- **Offline Support**: Enhanced offline content management

### API Evolution
- **Versioning Strategy**: Maintain backward compatibility
- **Migration Path**: Smooth upgrades for client applications
- **Feature Flags**: Gradual rollout of new functionality

---

**Version**: 1.0.0  
**Last Updated**: August 20, 2025  
**Status**: ✅ Active Implementation