# Changelog

## [1.4] - 2026-02-06
### Added
- Added support for NVDA 2026.1 with updated minimum version requirement.
- Enhanced CI/CD workflow with Pandoc automatic download and testing.
- Implemented workflow caching for pre-commit hooks and scons builds.
- Added gettext tools installation to Windows CI runner.

### Changed
- Updated minimum NVDA version from 2019.3 to 2024.1.
- Updated last tested NVDA version to 2026.1.
- Updated author information to Adil Shaikh.
- Optimized GitHub Actions workflow with concurrency controls and performance improvements.

### Fixed
- Fixed test case execution in CI/CD pipeline with proper PowerShell syntax.
- Fixed cache path handling for Windows runners in workflow.

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
