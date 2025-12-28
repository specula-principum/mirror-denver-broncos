# Content Acquisition Files

This directory contains files related to the Denver Broncos website acquisition attempt.

## Status: BLOCKED - Network Access Required

The content acquisition task could not be completed due to network access limitations in the Copilot Agent sandbox environment.

## Files in This Directory

### 📋 Documentation

- **`NEXT_STEPS.md`** - Comprehensive guide for completing the acquisition
- **`ACQUISITION_BLOCKED.md`** - Detailed analysis of the network limitation
- **`scripts/README.md`** - Documentation for acquisition scripts
- **`.github/workflows/manual-acquire-content.yml.example`** - Sample workflow for manual acquisition

### 🔧 Implementation

- **`scripts/acquire_denver_broncos.py`** - Ready-to-use acquisition script
  - ✓ Fully implemented using existing parsing infrastructure
  - ✓ Supports both local and GitHub Actions execution
  - ✓ Handles persistence via GitHub API or filesystem
  - ✗ Requires network access to run

## Quick Start (For Repository Owner)

### Option 1: GitHub Actions (Recommended)

1. Rename the example workflow:
   ```bash
   mv .github/workflows/manual-acquire-content.yml.example \
      .github/workflows/manual-acquire-content.yml
   ```

2. Commit and push:
   ```bash
   git add .github/workflows/manual-acquire-content.yml
   git commit -m "Add manual content acquisition workflow"
   git push
   ```

3. Run the workflow:
   - Go to Actions tab on GitHub
   - Select "Acquire Content (Manual)"
   - Click "Run workflow"
   - Wait for completion

4. Verify results:
   - Check `evidence/parsed/` for new content
   - Check `knowledge-graph/sources/` for updated registry

### Option 2: Local Execution

```bash
# Clone and setup
git clone <repository-url>
cd mirror-denver-broncos
pip install -r requirements.txt

# Run acquisition
python scripts/acquire_denver_broncos.py

# Commit results
git add evidence/ knowledge-graph/
git commit -m "Acquire Denver Broncos website content"
git push
```

## What Happens When You Run It

The acquisition script will:

1. **Fetch** content from https://www.denverbroncos.com
2. **Parse** HTML to markdown using trafilatura
3. **Store** parsed content in `evidence/parsed/2025/denverbroncos.com-{hash}/`
4. **Update** manifest with entry and checksum
5. **Update** source registry with `last_content_hash`
6. **Commit** all changes (if in GitHub Actions with token)

## Expected Output

```
evidence/parsed/
└── 2025/
    └── denverbroncos.com-{hash}/
        ├── index.md           # Main content
        ├── segment-001.md     # Content segments
        └── segment-002.md

knowledge-graph/sources/
├── 0b899913b1fab003.json  # Updated with content hash
└── registry.json           # Registry index
```

## After Successful Acquisition

1. Close issue #XX with success summary
2. Add label `acquisition-complete`
3. Optionally: Run entity extraction on the parsed content

## Need Help?

- See `NEXT_STEPS.md` for detailed instructions
- See `ACQUISITION_BLOCKED.md` for technical details about the network issue
- See `scripts/README.md` for script documentation

## Technical Notes

- **Source Registry**: Confirmed present at `knowledge-graph/sources/0b899913b1fab003.json`
- **Source Status**: Active, awaiting content
- **Network Test**: All external domains blocked in Copilot sandbox
- **Script Validation**: ✓ Syntax valid, imports successful, registry accessible
- **Environment**: Requires standard GitHub Actions runner or local machine with internet
