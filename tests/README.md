# Test Artifacts

This directory contains verifyable evidence of your test runs.

## Structure

- **`videos/`**: Full browser session recordings (.webm)
- **`screenshots/`**: Screenshots captured during errors or step-by-step exeuction
- **`downloads/`**: Files downloaded during test execution
- **`reports/`**: JSON, HTML, and PDF reports (if configured to save here)
- **`selector_cache.json`**: Persistent cache for AI selector healing

## Usage

- **Videos**: Open in any browser or VLC player
- **Screenshots**: Helpful for debugging "Element Not Found" errors
- **Cache**: Delete `selector_cache.json` to force fresh AI healing
