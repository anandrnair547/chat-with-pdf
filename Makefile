.PHONY: clean build test-release release bump tag

# Remove previous build artifacts
clean:
	@rm -rf dist/ build/ *.egg-info

# Build package artifacts (wheel and sdist)
build:
	@poetry build

# Upload to TestPyPI for a dry run
test-release: clean build
	@twine upload --repository testpypi dist/*
	@echo "✅ Test release done. Install via: pip install --index-url https://test.pypi.org/simple/ chat-with-pdf"

# Create & push Git tag, then upload to real PyPI
release: clean build tag
	@twine upload dist/*
	@echo "🚀 Released version $(poetry version --short) to PyPI!"

# Prompt for new version, update pyproject.toml, and commit
bump:
	@current=$$(poetry version --short); \
	echo "Current version: $$current"; \
	read -p "New version: " new; \
	poetry version $$new; \
	git add pyproject.toml CHANGELOG.md; \
	git commit -m "feat: bump version to $$new"

# Create & push a Git tag for the current version
tag:
	@version=$$(poetry version --short); \
	git tag v$$version; \
	git push origin v$$version; \
	echo "Tagged version v$$version"
