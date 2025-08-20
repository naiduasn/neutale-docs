# Development Setup Guide

Multi-repository development workflow for the Neutale ecosystem.

## 📋 Overview

This guide covers setting up a complete development environment across all Neutale projects with shared documentation submodules.

## 🔧 Prerequisites

### Required Software
- **Git**: Version 2.25+ (for submodule support)
- **Node.js**: 18+ (for audiobook backend)
- **Python**: 3.11+ (for storygen)
- **Flutter**: 3.19+ (for neutale mobile app)
- **GitHub CLI**: For repository management

### Development Tools
- **VS Code**: Recommended IDE with extensions
- **Docker**: For containerized development (optional)
- **Postman**: For API testing

## 🚀 Quick Start

### 1. Repository Setup

```bash
# Create workspace directory
mkdir neutale-workspace && cd neutale-workspace

# Clone all repositories
git clone https://github.com/naiduasn/storygen
git clone https://github.com/naiduasn/audiobook
git clone https://github.com/naiduasn/neutale

# Initialize documentation submodules
cd storygen && git submodule update --init --recursive
cd ../audiobook && git submodule update --init --recursive  
cd ../neutale && git submodule update --init --recursive
```

### 2. Environment Configuration

**Create master environment file:**
```bash
# neutale-workspace/.env
OPENAI_API_KEY=your_openai_api_key_here
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
AUTH0_DOMAIN=audbook.us.auth0.com
AUTH0_CLIENT_ID=cysVRLo9SjMLkg5nwsX6veb240ghMjEE
```

### 3. Service Setup

**Terminal 1 - Storygen (Story Generation):**
```bash
cd storygen
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
python continuous_story_generator.py
```

**Terminal 2 - Audiobook Backend:**
```bash
cd audiobook
npm install
npm run preview  # Starts on http://localhost:8787
```

**Terminal 3 - Neutale Mobile App:**
```bash
cd neutale/app
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
flutter run -d chrome  # Or -d ios / -d android
```

## 📚 Documentation Submodule Management

### Initial Setup
```bash
# Add submodule to existing project
git submodule add https://github.com/naiduasn/neutale-docs docs

# Configure submodule to track main branch
cd docs
git config branch.main.remote origin
git config branch.main.merge refs/heads/main
cd ..

# Commit submodule configuration
git add .gitmodules docs
git commit -m "Add neutale-docs submodule"
```

### Daily Workflow
```bash
# Update documentation to latest
git submodule update --remote docs

# Check for documentation changes
cd docs && git status && cd ..

# Commit documentation updates
git add docs
git commit -m "Update documentation to latest"
```

### Documentation Development
```bash
# Make changes to documentation
cd docs
git checkout -b feature/update-api-spec
# Edit files...
git add .
git commit -m "Update API specification"
git push origin feature/update-api-spec

# Create pull request
gh pr create --title "Update API specification" --body "Description of changes"

# After merge, update all projects
cd ../storygen && git submodule update --remote docs
cd ../audiobook && git submodule update --remote docs
cd ../neutale && git submodule update --remote docs
```

## 🔄 Development Workflow

### 1. Content Development Cycle

**Story Creation → Backend → Mobile:**
```bash
# 1. Generate story in Storygen
cd storygen
python continuous_story_generator.py
# Select story and export

# 2. Upload to backend
python upload_to_audiobook.py --story-id new-story --validate

# 3. Test in mobile app
cd ../neutale/app
flutter run -d chrome
# Navigate to story and test
```

### 2. API Development Cycle

**Backend Changes → Mobile Integration:**
```bash
# 1. Update backend API
cd audiobook
# Make changes to backend/api/
npm run preview

# 2. Test API endpoints
curl http://localhost:8787/api/content/test-story/metadata/en

# 3. Update mobile app
cd ../neutale/app
# Update API service calls
flutter hot reload
```

### 3. Cross-Repository Testing

**Full Pipeline Test:**
```bash
# 1. Generate test content
cd storygen
python test_complete_pipeline.py

# 2. Verify backend storage
cd ../audiobook
curl http://localhost:8787/api/stories

# 3. Test mobile consumption
cd ../neutale/app
flutter test integration_test/content_flow_test.dart
```

## 🛠️ IDE Configuration

### VS Code Workspace Setup

**Create `neutale-workspace.code-workspace`:**
```json
{
  "folders": [
    {
      "name": "Storygen",
      "path": "./storygen"
    },
    {
      "name": "Audiobook Backend", 
      "path": "./audiobook"
    },
    {
      "name": "Neutale Mobile",
      "path": "./neutale"
    },
    {
      "name": "Documentation",
      "path": "./storygen/docs"
    }
  ],
  "settings": {
    "python.defaultInterpreterPath": "./storygen/venv/bin/python",
    "typescript.preferences.includePackageJsonAutoImports": "auto"
  },
  "extensions": {
    "recommendations": [
      "ms-python.python",
      "bradlc.vscode-tailwindcss",
      "dart-code.flutter",
      "ms-vscode.vscode-typescript-next"
    ]
  }
}
```

### Recommended Extensions
- **Python**: Python development (storygen)
- **Flutter**: Dart and Flutter support (neutale)
- **TypeScript**: Backend development (audiobook)
- **GitLens**: Git integration and history
- **Better Comments**: Documentation annotations

## 🔍 Testing Strategy

### Unit Testing
```bash
# Storygen
cd storygen && python -m pytest tests/

# Audiobook Backend
cd audiobook && npm test

# Neutale Mobile
cd neutale/app && flutter test
```

### Integration Testing
```bash
# End-to-end content pipeline
cd storygen && python test_complete_integration.py

# API integration
cd audiobook && npm run test:e2e

# Mobile app integration
cd neutale/app && flutter test integration_test/
```

### Documentation Validation
```bash
# Validate all projects reference docs correctly
cd neutale-workspace
grep -r "docs/UNIFIED-CONTENT-SPEC.md" */
grep -r "neutale-docs" */README.md
```

## 🐛 Troubleshooting

### Common Issues

**Submodule Not Updating:**
```bash
# Force update submodule
git submodule update --remote --force docs

# Re-initialize if needed
git submodule deinit docs
git submodule update --init docs
```

**Flutter Build Issues:**
```bash
# Clean and regenerate
cd neutale/app
flutter clean
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

**Backend Connection Issues:**
```bash
# Check backend is running
curl http://localhost:8787/api/health

# Restart with logs
cd audiobook
npm run preview -- --local --log-level debug
```

**Content Upload Failures:**
```bash
# Validate content format
cd storygen
python validate_story_upload.py --story-id problematic-story

# Check R2 permissions
cd audiobook
npx wrangler r2 object list audiobook-content
```

### Development Tips

1. **Use Documentation Reference**: Always check `docs/` first for specifications
2. **Validate Early**: Run validation scripts before cross-project integration
3. **Test Incrementally**: Test each component before full pipeline
4. **Monitor Logs**: Keep terminal windows open for all services
5. **Version Control**: Commit frequently with clear messages

## 📊 Development Metrics

### Performance Targets
- **Story Generation**: < 5 minutes for 10-chapter story
- **Backend API**: < 500ms response time for metadata
- **Mobile App**: < 3 seconds cold start time
- **Content Upload**: < 30 seconds for typical story

### Quality Gates
- All tests pass before commits
- Documentation stays in sync
- API contracts maintained
- Mobile app builds successfully on all platforms

---

**Version**: 1.0.0  
**Last Updated**: August 20, 2025  
**Status**: ✅ Ready for Use