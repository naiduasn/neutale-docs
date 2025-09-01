# Specification for Book Review Feature in Neutale App

## 1. Introduction

### Overview
This document outlines the specification for introducing a comprehensive book review system in the Neutale app, an audiobook platform. The feature allows users to submit detailed reviews for books (stories), including separate ratings for the book content and audio quality. This separation ensures that audio production issues do not unfairly impact the perceived quality of the book's content.

The feature builds on the existing simple feedback system (thumbs up/down via `/api/feedback`), which will be extended or phased into this more robust system. The goal is to enhance user engagement, provide valuable feedback to creators, and improve content discovery through aggregated ratings.

### Objectives
- Enable users to rate books on a 5-star scale for content (e.g., story, writing) and audio (e.g., narration, sound quality).
- Allow optional text reviews for more detailed feedback.
- Display aggregated ratings and reviews on book detail pages to influence user decisions.
- Collect data for analytics and content improvement without mixing content and audio feedback.

### Scope
- **In Scope**: User-submitted reviews, separate ratings, display of averages and reviews, basic moderation flags.
- **Out of Scope**: Advanced moderation (e.g., AI review filtering), social sharing of reviews, editing existing reviews (initial version).

### Assumptions
- Based on codebase analysis, the app uses Flutter for the frontend (Neutale) and a backend API (Audiobook project) with endpoints like `/api/feedback`.
- Users must be authenticated to submit reviews.
- Books are referred to as "stories" in the codebase (e.g., storyId).
- Integration with existing story metadata (e.g., from UNIFIED-CONTENT-SPEC.md).

## 2. Product Requirements

### User Stories
- **As a user**, I want to rate a book's content and audio separately so that I can provide targeted feedback.
- **As a user**, I want to write an optional text review to share detailed thoughts.
- **As a user**, I want to see average ratings and reviews for a book before listening to decide if it's worth my time.
- **As a content creator/admin**, I want aggregated ratings to identify high-quality content and areas for improvement (e.g., poor audio).
- **As a user who finished a book**, I want to be prompted to review it to encourage feedback.

### Key Features
- **Separate Ratings**: 1-5 stars for "Content Quality" (story, plot, characters) and "Audio Quality" (narration, sound effects, production).
- **Text Review**: Optional free-text field (up to 1000 characters).
- **Submission Rules**: Users can review a book only once; must have listened to at least 50% of the book (tracked via existing progress APIs).
- **Display**: On book detail page, show average content rating, average audio rating, total review count, and a list of recent reviews (paginated).
- **Prompting**: After completing a book (100% progress), show a non-intrusive prompt to review.
- **Analytics**: Track submission rates, average ratings per book/genre.
- **Edge Cases**:
  - Anonymous users can view reviews but not submit.
  - Handle low review counts (e.g., display "No ratings yet").
  - Prevent spam: Rate-limit submissions per user.

### Success Metrics
- 20% of completed books receive a review within the first month of launch.
- Average rating >4.0 for content/audio on popular books.
- User engagement: Increase in time spent on book detail pages by 10%.

## 3. UX Design

### High-Level Flow
1. **Viewing Ratings/Reviews**:
   - Navigate to Book Detail Screen.
   - Scroll to "Reviews" section (below description and chapters).
   - See summary: "Content: 4.5/5 (based on 120 ratings)" | "Audio: 4.2/5 (based on 120 ratings)".
   - List of reviews: Each shows username (or anonymous), content/audio stars, text excerpt, date.
   - "Load More" button for pagination.

2. **Submitting a Review**:
   - From Book Detail Screen, tap "Write a Review" button (visible if eligible).
   - Or, post-completion prompt: Modal dialog with "Rate this book?" and quick links to review.
   - Review Submission Screen:
     - Two star rating widgets: "Rate the Content" (1-5 stars) and "Rate the Audio" (1-5 stars, optional).
     - Text area: "Share your thoughts (optional)".
     - Submit button: Disabled until content rating is selected.
   - Success: Toast message "Thanks for your review!" and refresh book detail page.

3. **Wireframe Sketches** (Text-Based Description)
   - **Book Detail Screen**:
     ```
     [Book Cover] [Title] [Author]
     [Play Button] [Description]
     --- Reviews Section ---
     Content Rating: ★★★★☆ 4.3/5 (45 ratings)
     Audio Rating: ★★★★☆ 4.1/5 (45 ratings)
     [Write a Review Button]
     --- Recent Reviews ---
     User123: ★★★★★ (Content) ★★★★☆ (Audio) "Great story, but narration was slow." [Date]
     [Load More]
     ```
   - **Review Submission Screen**:
     ```
     Rate [Book Title]
     Content Quality: [Star Rating Picker]
     Audio Quality: [Star Rating Picker] (Optional)
     Your Review: [Text Field]
     [Submit Button]
     ```

### Design Principles
- **Mobile-First**: Responsive for iOS/Android (Flutter-based).
- **Accessibility**: ARIA labels for stars, high contrast.
- **Theming**: Use existing app styles (e.g., from app/lib/themes/).
- **Error Handling**: If submission fails, show "Try again" with retry.
- **Localization**: Support multi-language strings (e.g., via Flutter's intl).

## 4. Backend Design

### Database Schema Changes
- Extend existing schema (based on migrations/*.sql and schema/*.sql).
- New Table: `reviews` (assuming PostgreSQL-like from backend/db/).
  ```
  CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    story_id UUID NOT NULL REFERENCES stories(id),
    content_rating INTEGER NOT NULL CHECK (content_rating BETWEEN 1 AND 5),
    audio_rating INTEGER CHECK (audio_rating BETWEEN 1 AND 5),  -- Optional
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, story_id)  -- One review per user per story
  );
  ```
- Update `stories` table: Add cached fields for quick access.
  ```
  ALTER TABLE stories ADD COLUMN avg_content_rating DECIMAL(3,1) DEFAULT 0;
  ALTER TABLE stories ADD COLUMN avg_audio_rating DECIMAL(3,1) DEFAULT 0;
  ALTER TABLE stories ADD COLUMN review_count INTEGER DEFAULT 0;
  ```
- Trigger: After insert/update on reviews, recalculate averages for the story.

### API Endpoints
- Build on existing `/api/feedback` (from backend/api/stories.ts and api-spec.yaml).
- **POST /api/reviews** (Submit review)
  - Request Body: `{ storyId: UUID, contentRating: 1-5, audioRating: 1-5 (optional), comment: string (optional) }`
  - Response: 201 Created { message: "Review submitted" }
  - Validation: Zod schema (e.g., extend existing in backend/api/progressive-upload.ts).
  - Logic: Check eligibility (e.g., progress >50% via existing tracking), insert to DB, update story averages.

- **GET /api/stories/:id/reviews** (Get reviews for a story)
  - Query Params: `page: int (default 1), limit: int (default 10)`
  - Response: { reviews: [{ userName, contentRating, audioRating, comment, createdAt }], total: int }
  - Anonymize userName if privacy settings apply.

- **GET /api/stories/:id/ratings** (Get aggregated ratings)
  - Response: { avgContent: 4.3, avgAudio: 4.1, count: 45 }

- Deprecate or integrate existing `/api/feedback`: Map thumbs up/down to 5/1 contentRating if needed.

### Security & Performance
- Authentication: Required for POST (use existing auth from auth0).
- Rate Limiting: Max 1 review per story per user; global limit of 5/day.
- Caching: Use Redis (if integrated) for aggregates to avoid frequent DB queries.
- Error Handling: 400 for invalid ratings, 403 if not eligible, 429 for rate limits.

## 5. Implementation Plan
- **Phase 1**: Backend (1-2 weeks) - Schema migration, API endpoints, tests (extend tests/ in both projects).
- **Phase 2**: Frontend (1-2 weeks) - Update book detail screen (app/lib/screens/book_title_view.dart), new review screen, integrate with api_service.dart.
- **Phase 3**: Testing & Launch (1 week) - E2E tests (tests/e2e/), beta rollout, monitor metrics.
- **Dependencies**: Update api-spec.yaml and UNIFIED-CONTENT-SPEC.md.
- **Risks**: Data migration for existing feedback; ensure averages don't break on low counts.