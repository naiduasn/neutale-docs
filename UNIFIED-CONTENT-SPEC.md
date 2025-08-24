# Unified Content Specification
## Neutale Audiobook Platform

This specification defines the unified data formats and API contracts across the entire Neutale content pipeline: **Storygen → Backend → Mobile App**.

## 📁 **File Structure Standard**

### R2 Storage Structure
```
stories/
└── {story-id}/
    └── {language}/
        └── assets/
            ├── images/
            │   ├── cover.jpg
            │   ├── thumbnail.jpg
            │   ├── chapter1_img01.webp
            │   ├── chapter2_img02.webp
            │   ├── chapter3_img03.webp
            │   └── ...
            └── audio/
                ├── chapter_01_Title.mp3
                ├── chapter_02_Title.mp3
                └── ...
```

**Note:** With the unified metadata approach, individual chapter JSON files are not stored in R2. Instead, all chapter content is embedded within the main story metadata as a comprehensive `chapters` array containing content blocks, images, and audio references.

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
  "genre": "Fantasy",
  "language": "en",
  "tags": ["fantasy", "adventure"],
  "chapters": [
    {
      "id": "ch1",
      "title": "Chapter 1: The Beginning",
      "chapterNumber": 1,
      "blocks": [
        {
          "id": "block_1",
          "type": "paragraph",
          "order": 0,
          "content": {
            "text": "Chapter content...",
            "style": "paragraph"
          },
          "metadata": {}
        },
        {
          "id": "block_2",
          "type": "image",
          "order": 1,
          "content": {
            "url": "chapter1_img01.webp",
            "assetId": "chapter1_img01",
            "description": "Chapter illustration"
          },
          "metadata": {}
        },
        {
          "id": "audio_block_1",
          "type": "audio",
          "order": 52,
          "content": {
            "url": "/api/content/story-id/audio/en/chapter_01_narration.mp3",
            "description": "Chapter 1 narration",
            "duration": 655.091
          },
          "metadata": {
            "provider": "google_tts",
            "voice": "Iapetus",
            "format": "MP3 (128kbps)",
            "generated": true
          }
        }
      ],
      "duration": 655.091,
      "audioUrl": "/api/content/story-id/audio/en/chapter_01_narration.mp3"
    }
  ],
  "styleGuide": {
    "theme": "narrative",
    "colorPalette": [],
    "imageStyle": "photorealistic",
    "mood": "engaging"
  },
  "review": {
    "overall_rating": 85,
    "verdict": "accepted",
    "final_rating": 85,
    "quality_achieved": true
  }
}
```

**Required Fields:**
- `id`, `title`, `author`, `description`
- `genre`, `language`
- `chapters` (array of chapter objects with blocks)

**Optional Fields:**
- `tags`, `styleGuide`, `review`

**Chapter Object Fields:**
- `id`, `title`, `chapterNumber`, `blocks` (required)
- `duration`, `audioUrl` (optional, for audio-enabled stories)

**Content Block Types:**
- `paragraph`: Text content with style information
- `image`: Visual content with url, assetId, and description
- `audio`: Audio content with url, duration, and provider metadata
- `heading_1`, `heading_2`, `heading_3`: Structured headings
- `quote`: Quoted text content
- `divider`: Section separators

### 2. Progressive Upload API Format
The unified metadata is uploaded via Progressive Upload API with the following structure:

```json
{
  "metadata": {
    "title": "Story Title",
    "author": "AI Story Weaver", 
    "description": "Story description...",
    "genre": "Fantasy",
    "language": "en",
    "tags": ["fantasy", "adventure"],
    "chapters": [/* full chapters array as shown above */]
  },
  "assets": [
    {
      "id": "cover",
      "filename": "cover.jpg",
      "type": "image",
      "category": "cover",
      "expectedSize": 102400
    },
    {
      "id": "chapter1_img01",
      "filename": "chapter1_img01.webp",
      "type": "image", 
      "category": "chapter",
      "expectedSize": 256000
    },
    {
      "id": "audio_chapter_01",
      "filename": "chapter_01_Title.mp3",
      "type": "audio",
      "category": "chapter",
      "expectedSize": 2048000
    }
  ]
}
```

**Asset Categories:**
- `cover`: Story cover image
- `thumbnail`: Story thumbnail image  
- `chapter`: Chapter images and audio files

## 🔗 **API Endpoints**

### Content Delivery
- **Story Metadata:** `GET /api/stories/{storyId}` *(includes complete chapters array)*
- **Assets:**
  - **Images:** `GET /api/content/{storyId}/image/{language}/{filename}`
  - **Audio:** `GET /api/content/{storyId}/audio/{language}/{filename}`

### Filename Conventions
- **Audio:** `chapter_01_Title.mp3`, `chapter_02_Title.mp3`, ...
- **Images:** `cover.jpg`, `thumbnail.jpg`, `chapter1_img01.webp`, `chapter2_img02.webp`, ...

### Mobile App Integration
**Recommended Approach:** Use the unified story metadata endpoint instead of separate manifests:

```dart
// Single API call gets everything
final story = await apiService.getStory(storyId);

// Access all content from unified structure
for (var chapter in story.chapters) {
  // Text content
  for (var block in chapter.blocks) {
    if (block.type == 'paragraph') {
      displayText(block.content.text);
    }
    // Image content  
    else if (block.type == 'image') {
      loadImage(block.content.url);
    }
    // Audio content
    else if (block.type == 'audio') {
      playAudio(block.content.url, duration: block.content.duration);
    }
  }
}
```

**Benefits:**
- ✅ Single source of truth
- ✅ Complete story structure in one call
- ✅ Audio metadata included per chapter
- ✅ Image references properly mapped

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
        "assets/images/cover.jpg": cover_image,
        "assets/images/thumbnail.jpg": thumbnail_image,
        "assets/images/chapter2.jpg": chapter2_image,
        "assets/images/chapter3.jpg": chapter3_image
    }
)
```

### 3. Mobile App Consumption
```dart
// Fetch complete story with unified metadata
final story = await apiService.getStory(storyId);

// Access all content from chapters array
for (var chapter in story.chapters) {
  print('Chapter ${chapter.chapterNumber}: ${chapter.title}');
  
  // Process content blocks
  for (var block in chapter.blocks) {
    switch (block.type) {
      case 'paragraph':
        displayText(block.content.text);
        break;
      case 'image':
        loadImage(block.content.url);
        break;
      case 'audio':
        playAudio(block.content.url, duration: block.content.duration);
        break;
    }
  }
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
- Use consistent image names: `cover.jpg`, `thumbnail.jpg`, `chapter2.jpg`, `chapter3.jpg`, ...

### Content Quality Rules
- **No Template Text:** Titles and descriptions must not contain `[placeholder]` text
- **Clean Titles:** Only alphanumeric characters, spaces, hyphens, apostrophes, and periods
- **Standardized Genres:** Must use one of: Fantasy, Sci-Fi, Mystery, Romance, Historical, Thriller, Horror, Adventure
- **Proper Descriptions:** Generated from actual story content, not template prompts
- **Image Compliance:** Cover shows story scenes, thumbnail shows book design

### Post-Upload Validation
- **Metadata Check:** Validates title, description, genre standardization
- **Chapter Verification:** Confirms all chapters exist and contain proper content blocks
- **Image Validation:** Verifies cover, thumbnail, and chapter images are accessible
- **Content Quality:** Ensures no template placeholders remain in any content

## 🔧 **Implementation Guidelines**

### For Storygen
- Always generate `totalChapters` field in metadata
- Use consistent chapter numbering starting from 1
- Validate story ID format before export

### For Backend APIs
- Serve complete story metadata with embedded `chapters` array
- Include all content blocks (text, images, audio) in chapter structures
- Provide asset endpoints for images and audio files
- Support WebP, JPG, PNG image formats
- Return comprehensive audio metadata (duration, voice, provider)

### For Mobile Apps
- Use unified story endpoint: `GET /api/stories/{storyId}`
- Process `chapters` array for all content (text, images, audio)
- Handle content blocks by type: paragraph, image, audio, heading, quote
- Load assets using content block URLs with proper assetId mapping
- **Eliminate separate audio manifest calls** - use unified metadata instead

## 📊 **Content Statistics**

### Current Pipeline Status
- **Storygen Stories:** 80+ generated with proper format
- **Backend Storage:** R2 bucket with validated stories and assets
- **Mobile App:** Fixed to use unified specification
- **Chapter Images:** 7 images per story (chapters 2-8) with proper metadata mapping

### Quality Metrics
- **Format Consistency:** 100% with this specification
- **API Compatibility:** Full compatibility across pipeline
- **Error Reduction:** Eliminates hardcoded content fallbacks
- **Content Quality:** Backend uses structured chapters data, not text parsing

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

## 🎯 **Validation Results**

### Recent Testing (August 19, 2025)
- **Test Stories:** "Secrets of the Timeless Archive" with Google TTS integration
- **Chapter Structure:** 8 chapters with structured content blocks (50+ blocks per chapter)
- **Images:** Flux-generated chapter images (WebP format) + cover + thumbnail
- **Audio Integration:** Google Gemini TTS with genre-based voice selection (Iapetus for Sci-Fi)
- **Progressive Upload:** Complete asset upload with 18+ files (images + audio + metadata)
- **Format Preservation:** WebP images maintain original format (no unnecessary JPG conversion)
- **URL Processing:** Proper mapping of scene_XX.webp → chapter{N}_img{N:02d}.webp
- **Mobile App Compatibility:** Working image/audio URLs via unified metadata

### Key Fixes Applied
1. **Unified Metadata Structure:** Complete story data in single `chapters` array with embedded content blocks
2. **Google TTS Integration:** Gemini TTS with genre-based voice selection and comprehensive audio metadata
3. **Flux Image Integration:** WebP format preservation with proper scene → chapter image mapping  
4. **Progressive Upload API:** Smart asset collection with R2-compliant structure
5. **URL Processing:** Fixed malformed image URLs (scene_01.webp → working API endpoints)
6. **Content Block System:** Proper type mapping (text→paragraph) and unique UUID generation
7. **Format Preservation:** Maintains original WebP/JPG/PNG formats instead of unnecessary conversion
8. **Mobile App Compatibility:** Audio metadata embedded in chapters, eliminating separate manifest calls
9. **Asset Management:** 18+ file uploads (cover, thumbnail, 8 chapter images, 8 audio files)

---

**Last Updated:** August 19, 2025  
**Version:** 2.0.0  
**Status:** ✅ Implemented and Validated

## 🔥 **Version 2.0.0 Features**

### **Major Updates:**
- **Unified Metadata Architecture:** Single comprehensive structure with embedded chapters
- **Google Gemini TTS Integration:** Genre-based voice selection with full audio metadata
- **Flux Image Generation:** High-quality WebP images with format preservation
- **Progressive Upload API:** Complete asset management with R2 compliance
- **Mobile App Optimization:** Eliminates separate API calls, uses unified endpoint

### **Breaking Changes:**
- Mobile apps should use `GET /api/stories/{storyId}` instead of separate manifest endpoints
- Audio metadata now embedded in chapter content blocks
- R2 storage simplified to assets-only structure (no separate chapter JSON files)

### **Backward Compatibility:**
- Existing content works with new structure
- Legacy endpoints maintained during transition period
- All current mobile app integrations supported
