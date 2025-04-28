# 📜 Changelog

All notable changes to this project will be documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added

- Support for passing PDF as file path, URL, or binary bytes in PDFChat constructor.
- Environment variable support for model, chunk size, and embedding model.
- Initial project structure with clean modular design.
- CI/CD integration using GitHub Actions.
- Test cases for file path, URL, and bytes input handling.
- Makefile for easy build, upload, and test management.

### Changed

- Improved flexibility of PDFChat initialization to handle multiple input types.

### Fixed

- Retriever now returns text chunks instead of embeddings, fixing TypeError when joining context in ask method.

---

## [0.1.0] - 2025-04-28

### Added

- First release to TestPyPI.
- Support for PDF parsing, embedding, retrieval, and OpenAI GPT answering.
- MIT License and full documentation.

