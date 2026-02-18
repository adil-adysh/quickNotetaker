# Changelog

## [1.5] - 2026-02-18

### Added
- **Create Note from Selection**: New NVDA+Alt+Shift+S shortcut to create a note directly from selected text in browse mode
- Selected text is automatically inserted as note content with optional window title prefilling
- Supports both virtual buffer selections (browse mode) and editable field selections

## [1.4] - 2026-02-18

### Major Features
- **Configurable Notes Data Path**: Implemented user-configurable notes data path with automatic migration support for existing notes
- **Enhanced Configuration Management**: Improved configuration handling with better initialization, validation, and error handling

### Breaking Changes
- **Renamed from Quick Notetaker to Quick Notes**: Updated all references, panel names, and configurations for consistency
- **Updated to 2025 Add-on Template**: Migrated to late 2025 NVDA add-on template edition with updated build system
- **Minimum NVDA Version**: Updated minimum NVDA version requirement from 2019.3 to 2024.1

### Added
- Migration logic for notes data when storage path changes
- User prompts during notes migration process with improved error handling
- Support for NVDA 2026.1 with updated last tested version to 2026.1
- Enhanced CI/CD workflow with Pandoc automatic download and testing
- Workflow caching for pre-commit hooks and scons builds
- Gettext tools installation to Windows CI runner
- Code quality automation with ruff and GitHub Actions
- Automated code formatting with Poetry for dependency management

### Changed
- Renamed QuickNotetakerPanel to QuickNotesPanel for consistency
- Updated notes path references to use 'quick_notes' directory structure
- Updated author information to Adil Shaikh
- Upgraded Python version to 3.13 in development workflows
- Updated Poetry installation method to use pipx for improved consistency
- Converted indentation from spaces to tabs (NVDA coding style compliance) across all files
- Improved lambda expressions and code formatting for better readability
- Optimized GitHub Actions workflow with concurrency controls and performance improvements

### Refactored
- Cleaned up imports across multiple files for better code organization
- Enhanced notes data path handling with improved logging
- Improved error handling and validation in settings configuration
- Updated BuildVars, SConstruct, manifest templates, and site_scons to 2025 add-on template standards

### Fixed
- Fixed test case execution in CI/CD pipeline with proper PowerShell syntax
- Fixed cache path handling for Windows runners in GitHub Actions workflow
- Resolved merge conflicts with spaces2tabs formatting

## [1.3] - 2025-07-18
### Added
- Integrated Pandoc download functionality into the add-on structure.
- Enhanced Pandoc extraction process to include MANUAL.html and clean up directories.
- Added comprehensive tests for Pandoc markdown to DOCX conversion.

### Changed
- Updated pandoc path retrieval to use a function for better maintainability.
- Updated version to 1.3 and adjusted last tested NVDA version to 2025.1.
- Upgraded dependency markdown2 and matched with latest NVDA API.
- Updated repo to match with latest add-on template.

### Removed
- Excluded pandoc.exe from the repository.
