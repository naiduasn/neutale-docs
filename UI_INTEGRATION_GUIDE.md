# UI Integration Guide: StoryGen Import System v3.0

## 🏗️ Architecture Overview

After the StoryGen import redesign, the UI should use this clean architecture for optimal performance:

```
┌─── D1 Database ──────────────────────┐
│ • Essential metadata for queries     │
│ • Fast listing and filtering         │
│ • Cover/thumbnail URLs               │
└──────────────────────────────────────┘
                    │
┌─── R2 Storage ───────────────────────┐
│ • Complete story content             │
│ • Chapter JSON files                 │
│ • Asset files (images, audio)       │
└──────────────────────────────────────┘
```

## 📱 UI Data Flow Pattern

### 1. **Story Discovery & Listing**
```typescript
// ✅ Use D1-powered endpoints for fast queries
GET /api/stories?language=en&page=1&limit=20
GET /api/stories?genre=Sci-Fi&sort=newest
GET /api/stories/{storyId}
```

### 2. **Story Content Reading**
```typescript
// ✅ Use R2-powered endpoints for rich content
GET /api/content/{storyId}/{language}/metadata
GET /api/chapters/{storyId}/{chapterId}/content
```

### 3. **Asset Loading**
```typescript
// ✅ Direct URLs from D1 metadata
coverImageUrl: "/api/content/{storyId}/assets/cover.jpg"
thumbnailUrl: "/api/content/{storyId}/assets/thumbnail.jpg"
```

## 🚀 API Integration Details

### **Story Listing & Discovery**

#### Get Stories with Language Support
```typescript
// Primary endpoint for story discovery
GET /api/stories?language=en&limit=20&page=1

// Response
{
  "stories": [
    {
      "id": "future-flavors-unveiled",
      "title": "Future Flavors Unveiled",
      "author": "AI Story Weaver", 
      "description": "In the bustling metropolis of Neo-Haven...",
      "genre": "Sci-Fi",
      "tags": ["adventure"],
      "originLanguage": "en",
      "supportedLanguages": ["en", "es", "fr", "de", "zh", "hi", "ru", "ja", "ko", "ar", "pt", "id"],
      "totalChapters": 8,
      "readingTime": 5,
      "coverImageUrl": "/api/content/future-flavors-unveiled/assets/cover.jpg",
      "thumbnailUrl": "/api/content/future-flavors-unveiled/assets/thumbnail.jpg",
      "status": "published",
      "createdAt": "2025-08-31T15:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

#### Advanced Filtering
```typescript
// Language-specific queries
GET /api/stories?language=es                    // Spanish stories
GET /api/stories?languages=es,fr               // Stories with BOTH Spanish AND French
GET /api/stories?language=es&audio_language=es // Spanish stories with Spanish audio

// Genre and tag filtering  
GET /api/stories?genre=Sci-Fi&tags=adventure
GET /api/stories?author=AI%20Story%20Weaver

// Sorting and pagination
GET /api/stories?sort=newest&page=2&limit=10
GET /api/stories?sort=popularity&featured=true
```

### **Individual Story Details**

#### Get Complete Story Metadata
```typescript
GET /api/stories/{storyId}

// Response - Enhanced with full metadata
{
  "id": "future-flavors-unveiled",
  "title": "Future Flavors Unveiled",
  "author": "AI Story Weaver",
  "description": "Complete story description...",
  "genre": "Sci-Fi",
  "originLanguage": "en",
  "supportedLanguages": ["en", "es", "fr", "de", "zh", "hi", "ru", "ja", "ko", "ar", "pt", "id"],
  "totalChapters": 8,
  "readingTime": 5,
  "tags": ["adventure"],
  "coverImageUrl": "/api/content/future-flavors-unveiled/assets/cover.jpg",
  "thumbnailUrl": "/api/content/future-flavors-unveiled/assets/thumbnail.jpg", 
  "status": "published",
  "chapters": [
    {
      "chapterNumber": 1,
      "title": "A Taste of Misunderstanding",
      "duration": 531,
      "audioUrl": "/api/content/future-flavors-unveiled/audio/en/chapter_01.mp3",
      "contentUrl": "/api/chapters/future-flavors-unveiled/chapter_dd439e6a/content"
    }
    // ... more chapters
  ]
}
```

### **Story Content & Reading**

#### Get Language-Specific Metadata
```typescript
// Get story metadata for a specific language
GET /api/content/{storyId}/{language}/metadata

// Example: Spanish metadata
GET /api/content/future-flavors-unveiled/es/metadata

// Response
{
  "title": "Future Flavors Unveiled", 
  "description": "En la bulliciosa metrópoli de Neo-Haven...",
  "language": "es",
  "totalChapters": 8,
  "chapters": [
    {
      "id": "chapter_dd439e6a", 
      "title": "Un Sabor a Malentendido",
      "chapterNumber": 1,
      "duration": 531,
      "audioUrl": "/api/content/future-flavors-unveiled/audio/es/chapter_01.mp3",
      "contentUrl": "/api/chapters/future-flavors-unveiled/chapter_dd439e6a/content"
    }
    // ... more chapters with Spanish titles
  ]
}
```

#### Get Chapter Content (Rich Content Blocks)
```typescript
// Get rich content blocks for reading
GET /api/chapters/{storyId}/{chapterId}/content

// Example
GET /api/chapters/future-flavors-unveiled/chapter_dd439e6a/content

// Response - Rich content blocks from R2
{
  "chapterId": "chapter_dd439e6a",
  "title": "A Taste of Misunderstanding",
  "chapterNumber": 1,
  "blocks": [
    {
      "id": "75b0401d-7b32-497a-bc3a-4404d5b315dc",
      "type": "heading_2", 
      "order": 0,
      "content": {
        "text": "A Taste of Misunderstanding",
        "level": 2,
        "style": "heading_2"
      }
    },
    {
      "id": "415133df-6d81-4536-9808-73089265f53e",
      "type": "paragraph",
      "order": 1, 
      "content": {
        "text": "In the sprawling city of Neo-Haven, where skyscrapers glinted...",
        "style": "paragraph"
      }
    },
    {
      "id": "image-block-001",
      "type": "image",
      "order": 2,
      "content": {
        "url": "/api/content/future-flavors-unveiled/assets/chapter1_img01.webp",
        "description": "Chapter 1 illustration", 
        "placement": "inline"
      }
    }
    // ... more content blocks
  ]
}
```

### **Asset URLs (Images & Audio)**

#### Direct Asset Access
```typescript
// Cover images (from D1 metadata)
coverImageUrl: "/api/content/{storyId}/assets/cover.jpg"
thumbnailUrl: "/api/content/{storyId}/assets/thumbnail.jpg"

// Chapter images (from content blocks or R2 metadata) 
chapterImageUrl: "/api/content/{storyId}/assets/chapter1_img01.webp"

// Audio files (language-specific)
audioUrl: "/api/content/{storyId}/audio/{language}/chapter_01.mp3"

// Examples
const coverUrl = "/api/content/future-flavors-unveiled/assets/cover.jpg";
const audioUrl = "/api/content/future-flavors-unveiled/audio/es/chapter_01.mp3";
const chapterImg = "/api/content/future-flavors-unveiled/assets/chapter1_img01.webp";
```

## 📋 UI Implementation Patterns

### **Story Card Component**
```typescript
interface StoryCardProps {
  story: {
    id: string;
    title: string;
    author: string; 
    description: string;
    coverImageUrl: string;
    thumbnailUrl: string;
    genre: string;
    readingTime: number;
    supportedLanguages: string[];
  }
}

function StoryCard({ story }: StoryCardProps) {
  return (
    <div className="story-card">
      {/* Use direct URLs from API */}
      <img src={story.coverImageUrl} alt={story.title} />
      <h3>{story.title}</h3>
      <p>{story.author}</p>
      <p>{story.description}</p>
      
      {/* Language indicator */}
      <div className="languages">
        {story.supportedLanguages.map(lang => (
          <span key={lang} className="language-tag">{lang}</span>
        ))}
      </div>
    </div>
  );
}
```

### **Story Reader Component**
```typescript
function StoryReader({ storyId, language }: { storyId: string; language: string }) {
  const [chapters, setChapters] = useState([]);
  const [currentChapter, setCurrentChapter] = useState(null);

  // Load story metadata for the selected language
  useEffect(() => {
    fetch(`/api/content/${storyId}/${language}/metadata`)
      .then(res => res.json())
      .then(data => setChapters(data.chapters));
  }, [storyId, language]);

  // Load specific chapter content
  const loadChapter = async (chapterId: string) => {
    const response = await fetch(`/api/chapters/${storyId}/${chapterId}/content`);
    const chapter = await response.json();
    setCurrentChapter(chapter);
  };

  return (
    <div className="story-reader">
      {/* Chapter selector */}
      <select onChange={(e) => loadChapter(e.target.value)}>
        {chapters.map(ch => (
          <option key={ch.id} value={ch.id}>{ch.title}</option>
        ))}
      </select>

      {/* Content blocks rendering */}
      {currentChapter?.blocks.map(block => (
        <ContentBlock key={block.id} block={block} />
      ))}
    </div>
  );
}

function ContentBlock({ block }: { block: any }) {
  switch (block.type) {
    case 'heading_2':
      return <h2>{block.content.text}</h2>;
    case 'paragraph': 
      return <p>{block.content.text}</p>;
    case 'image':
      return <img src={block.content.url} alt={block.content.description} />;
    default:
      return <div>{block.content.text}</div>;
  }
}
```

### **Language Switching**
```typescript
function LanguageSelector({ storyId, supportedLanguages, currentLanguage, onLanguageChange }) {
  return (
    <select 
      value={currentLanguage} 
      onChange={(e) => onLanguageChange(e.target.value)}
    >
      {supportedLanguages.map(lang => (
        <option key={lang} value={lang}>
          {getLanguageName(lang)} {/* Convert 'es' to 'Español' */}
        </option>
      ))}
    </select>
  );
}

// Usage: When language changes, refetch content
const handleLanguageChange = (newLanguage: string) => {
  setCurrentLanguage(newLanguage);
  // This will automatically refetch metadata and content for the new language
};
```

## 🔧 Performance Optimizations

### **Caching Strategy**
```typescript
// Cache story lists aggressively (change infrequently)
const storyListCache = new Map();

// Cache chapter content (read multiple times)  
const chapterCache = new Map();

// Preload next chapter in background
const preloadNextChapter = (storyId: string, currentChapterIndex: number) => {
  const nextChapterIndex = currentChapterIndex + 1;
  // Preload next chapter content
};
```

### **Image Loading**
```typescript
// Use thumbnail for lists, full cover for details
<img 
  src={story.thumbnailUrl}           // Fast loading in lists
  onMouseOver={() => preload(story.coverImageUrl)} // Preload full image
/>

// Progressive loading for chapter images
<img 
  src={`${chapterImageUrl}?w=400`}   // Smaller version first
  onLoad={() => loadFullSize()}      // Then full resolution
/>
```

## 🌐 Multi-language Best Practices

### **URL Structure**
```typescript
// Use language parameter in routes
/story/{storyId}?lang=es
/story/{storyId}/chapter/{chapterId}?lang=fr

// Default to user's preferred language
const userLanguage = getUserPreferredLanguage();
const availableLanguage = getFirstSupportedLanguage(story.supportedLanguages, userLanguage);
```

### **Content Fallbacks**
```typescript
// Fallback hierarchy for content
const loadStoryContent = async (storyId: string, preferredLanguage: string) => {
  try {
    // Try preferred language
    return await fetch(`/api/content/${storyId}/${preferredLanguage}/metadata`);
  } catch {
    // Fall back to story's origin language
    return await fetch(`/api/content/${storyId}/${story.originLanguage}/metadata`);
  }
};
```

## ⚡ Migration from Legacy System

### **API Endpoint Changes**
```diff
// OLD: Complex unified content endpoint
- GET /api/content/{storyId}/unified/{language}

// NEW: Separate optimized endpoints
+ GET /api/stories/{storyId}                           // Fast metadata
+ GET /api/content/{storyId}/{language}/metadata      // Language-specific metadata  
+ GET /api/chapters/{storyId}/{chapterId}/content     // Rich chapter content
```

### **Data Structure Changes**
```diff
// OLD: Everything in one large response
- { story, chapters, content, assets, metadata }

// NEW: Optimized separate responses
+ D1 Metadata: { id, title, author, description, coverImageUrl, supportedLanguages }
+ R2 Content: { chapters: [{ blocks: [...] }] }
+ Direct Assets: coverImageUrl, thumbnailUrl, audioUrl
```

This architecture provides optimal performance with fast story discovery via D1 and rich content delivery via R2. The UI can now load story lists instantly and fetch detailed content on demand.