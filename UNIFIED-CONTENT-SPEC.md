# Unified Content Specification
## Neutale Audiobook Platform

This specification defines the unified data formats and API contracts across the entire Neutale content pipeline: **Storygen → Backend → Mobile App**.

## 📁 **File Structure Standard**

### R2 Storage Structure
```
stories/
└── {story-id}/
    └── {language}/
        ├── metadata.json              # Story metadata
        ├── content/                   # Chapter content
        │   ├── chapter1.json
        │   ├── chapter2.json
        │   └── ...
        └── assets/
            ├── images/
            │   ├── cover.jpg
            │   └── thumbnail.jpg
            └── audio/
                ├── chapter1.wav
                └── chapter2.wav
```

### Story ID Format
- **Pattern:** `[a-z0-9-]+`
- **Max Length:** 50 characters
- **Examples:** `harmonics-of-europa`, `sorcerers-quest-001`
- **Generation:** Sanitize title → lowercase → replace spaces with hyphens

## 📝 **Data Formats**

### 1. Story Metadata (`metadata.json`)
```json
{
  "id": "story-id",
  "title": "Story Title",
  "author": "AI Story Weaver",
  "description": "Story description...",
  "coverImage": "cover.jpg",
  "thumbnail": "thumbnail.jpg", 
  "originLanguage": "en",
  "supportedLanguages": ["en"],
  "totalChapters": 5,
  "genre": "Fantasy",
  "readingTime": 45,
  "tags": ["fantasy", "adventure"],
  "status": "published"
}
```

**Required Fields:**
- `id`, `title`, `author`, `description`
- `originLanguage`, `supportedLanguages`
- `totalChapters` (integer ≥ 1)
- `genre`, `status`

**Optional Fields:**
- `coverImage`, `thumbnail`, `readingTime`, `tags`

### 2. Chapter Content (`chapter{N}.json`)
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
    },
    {
      "type": "paragraph",
      "content": "More content..."
    }
  ]
}
```

**Block Types:**
- `paragraph`: Standard text content
- `heading`: Chapter/section titles with `level` (1-6)

**Required Fields:**
- `chapterNumber` (integer starting from 1)
- `title` (string)
- `blocks` (array of block objects)

## 🔗 **API Endpoints**

### Content Delivery
- **Metadata:** `GET /api/content/{storyId}/metadata/{language}`
- **Chapter:** `GET /api/content/{storyId}/chapter/{language}/chapter{N}.json`
- **Images:** `GET /api/content/{storyId}/image/{language}/{filename}`
- **Audio:** `GET /api/content/{storyId}/audio/{language}/chapter{N}.wav`

### Filename Conventions
- **Chapters:** `chapter1.json`, `chapter2.json`, ...
- **Audio:** `chapter1.wav`, `chapter2.wav`, ...
- **Images:** `cover.jpg`, `thumbnail.jpg`

## 🔄 **Pipeline Workflow**

### 1. Story Generation (Storygen)
```python
# Generate story with proper structure
story_data = {
    "title": "Story Title",
    "content": "Full story text...",
    "chapters": [
        {"chapterNumber": 1, "title": "Chapter 1", "blocks": [...]},
        {"chapterNumber": 2, "title": "Chapter 2", "blocks": [...]}
    ]
}

# Export to audiobook format
converter.convert_story(story_data, output_dir="my_platform_stories")
```

### 2. Backend Upload
```python
# Upload structure to R2
upload_to_r2(
    bucket="audiobook-content",
    path=f"stories/{story_id}/{language}/",
    files={
        "metadata.json": metadata,
        "content/chapter1.json": chapter1_content,
        "content/chapter2.json": chapter2_content,
        "assets/images/cover.jpg": cover_image
    }
)
```

### 3. Mobile App Consumption
```dart
// Fetch metadata
final metadata = await apiService.getStoryMetadata(storyId, language);

// Navigate through chapters
for (int i = 0; i < metadata.totalChapters; i++) {
  final filename = 'chapter${i + 1}.json';
  final content = await apiService.getChapterContent(storyId, language, filename);
}
```

## ✅ **Validation Rules**

### Story ID Validation
- Must match pattern: `^[a-z0-9][a-z0-9-]{0,48}[a-z0-9]$`
- Cannot start or end with hyphens
- Must be unique across platform

### Chapter Numbering
- Must start from 1 (not 0)
- Must be consecutive (no gaps)
- Must match `totalChapters` in metadata

### File Naming
- Use lowercase with hyphens for story IDs
- Use `chapterN.json` format (not `chapter_N` or `chapterN`)
- Use consistent image names: `cover.jpg`, `thumbnail.jpg`

## 🔧 **Implementation Guidelines**

### For Storygen
- Always generate `totalChapters` field in metadata
- Use consistent chapter numbering starting from 1
- Validate story ID format before export

### For Backend APIs
- Serve metadata with `totalChapters` (not chapters array)
- Use exact filename matching for chapter requests
- Return 404 for missing chapters instead of empty responses

### For Mobile Apps
- Generate filenames using `chapter${N}.json` pattern
- Use `metadata.totalChapters` for navigation limits
- Handle missing chapters gracefully with user-friendly messages

## 📊 **Content Statistics**

### Current Pipeline Status
- **Storygen Stories:** 50+ generated with proper format
- **Backend Storage:** R2 bucket with 74+ stories
- **Mobile App:** Fixed to use unified specification

### Quality Metrics
- **Format Consistency:** 100% with this specification
- **API Compatibility:** Full compatibility across pipeline
- **Error Reduction:** Eliminates hardcoded content fallbacks

## 🚀 **Benefits of Unified Spec**

1. **Eliminates Content Issues:** No more "hardcoded" or fallback content
2. **Consistent Navigation:** Proper chapter listing and navigation
3. **Scalable Architecture:** Easy to add new content types and features
4. **Developer Experience:** Clear contracts for all team members
5. **Quality Assurance:** Automated validation across pipeline

## 📝 **Migration Notes**

### Existing Content
- All existing content already follows this specification
- No migration needed for current R2 storage
- Mobile app has been updated to match specification

### Future Development
- Always reference this specification for new features
- Update this document when adding new content types
- Maintain backward compatibility for existing content

---

**Last Updated:** August 8, 2025  
**Version:** 1.0.0  
**Status:** ✅ Implemented and Active