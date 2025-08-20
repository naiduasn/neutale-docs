# Neutale Ecosystem Documentation

Central documentation repository for the Neutale AI-powered audiobook platform ecosystem.

## 📚 Overview

This repository contains shared specifications, API contracts, and integration guides used across all Neutale projects:

- **[storygen](https://github.com/naiduasn/storygen)**: AI story generation service
- **[audiobook](https://github.com/naiduasn/audiobook)**: Backend API and content management
- **[neutale](https://github.com/naiduasn/neutale)**: Flutter mobile application

## 📋 Documentation Index

### Core Specifications
- **[UNIFIED-CONTENT-SPEC.md](./UNIFIED-CONTENT-SPEC.md)**: ⚠️ **MANDATORY** - Central content format specification
- **[API-CONTRACTS.md](./API-CONTRACTS.md)**: Backend API endpoint documentation
- **[INTEGRATION-GUIDE.md](./INTEGRATION-GUIDE.md)**: Cross-project integration guidelines

### Development Guides
- **[DEVELOPMENT-SETUP.md](./DEVELOPMENT-SETUP.md)**: Multi-repository development workflow
- **[CONTENT-PIPELINE.md](./CONTENT-PIPELINE.md)**: Story generation to mobile app pipeline

## 🔗 Usage as Git Submodule

This repository is included as a git submodule in all Neutale projects:

```bash
# Add to your project
git submodule add https://github.com/naiduasn/neutale-docs docs

# Initialize after cloning
git submodule update --init --recursive

# Update to latest
git submodule update --remote docs
```

## ⚠️ Important Notes

### Mandatory Reference
**ALL** projects in the Neutale ecosystem MUST reference this documentation:

1. **storygen**: MUST follow `docs/UNIFIED-CONTENT-SPEC.md` for content generation
2. **audiobook**: MUST implement API endpoints per `docs/API-CONTRACTS.md`
3. **neutale**: MUST integrate content using `docs/UNIFIED-CONTENT-SPEC.md`

### Updates and Versioning
- Changes to specifications require updates across all dependent projects
- Use semantic versioning for breaking changes
- Test all integrations before committing spec changes

## 🚀 Quick Start

### For New Developers
1. Read `UNIFIED-CONTENT-SPEC.md` first - this is the foundation
2. Review `API-CONTRACTS.md` for backend integration
3. Follow `DEVELOPMENT-SETUP.md` for multi-repo development

### For Content Updates
1. Update specifications in this repository
2. Test changes across all dependent projects
3. Update project-specific documentation as needed

## 📝 Contributing

When updating documentation:

1. **Test Impact**: Verify changes work across all projects
2. **Breaking Changes**: Update version and add migration notes
3. **Consistency**: Maintain consistent format and terminology
4. **Review Process**: Get approval from project maintainers

## 🔄 Version History

- **v1.0.0**: Initial unified specification (August 2025)
  - Consolidated content formats across ecosystem
  - Established API contracts
  - Created integration guidelines

---

**Last Updated**: August 20, 2025  
**Maintainers**: Neutale Development Team  
**License**: MIT