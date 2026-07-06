# Contributing to Posture Correction System

Thank you for your interest in contributing! Here's how you can help.

## Getting Started

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/my-feature`.
3. Make your changes.
4. Run linting: `ruff check src/ tests/`.
5. Run tests: `pytest --cov=src --cov-report=term`.
6. Push and open a pull request.

## Code Style

- This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.
- Type hints are required for all public functions.
- Follow existing patterns for consistency.

## Commit Messages

Use concise, descriptive commit messages in the imperative mood.

## Pull Request Process

1. Ensure CI passes (lint → test → docker).
2. Update docs/API.md if you change public interfaces.
3. Add tests for new functionality.
4. A maintainer will review your PR within a few days.

## Reporting Issues

Open a [bug report](https://github.com/amori27/posture-correction/issues/new?template=bug_report.md) or [feature request](https://github.com/amori27/posture-correction/issues/new?template=feature_request.md).

## Code of Conduct

Please note this project has a [Code of Conduct](CODE_OF_CONDUCT.md). By participating you agree to its terms.
