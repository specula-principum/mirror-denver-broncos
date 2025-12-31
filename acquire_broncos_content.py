#!/usr/bin/env python3
"""Script to acquire content from Denver Broncos official website.

This script:
1. Fetches content from https://www.denverbroncos.com using WebParser
2. Stores the content to evidence/parsed/denverbroncos.com/ via GitHub API
3. Updates the source registry with content hash and timestamp
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from src.integrations.github.storage import get_github_storage_client
from src.knowledge.storage import SourceRegistry
from src.parsing.base import ParseTarget
from src.parsing.web import WebParser
from src import paths


def main() -> int:
    """Execute the content acquisition workflow."""
    source_url = "https://www.denverbroncos.com"
    
    print(f"Starting acquisition for: {source_url}")
    print("-" * 60)
    
    # Initialize GitHub storage client (may be None if not in proper Actions environment)
    github_client = get_github_storage_client()
    if github_client:
        print("✓ GitHub storage client initialized")
    else:
        print("⚠ GitHub storage client not available - using local filesystem")
        print("  (Files will be committed via report_progress tool)")
    
    # Step 1: Fetch content using WebParser
    print(f"\nStep 1: Fetching content from {source_url}")
    print("  - Using WebParser with rendering enabled for JavaScript support")
    
    try:
        parser = WebParser(enable_rendering=True)
        target = ParseTarget(source=source_url, is_remote=True)
        
        # Check if parser can handle this target
        if not parser.detect(target):
            print(f"ERROR: WebParser cannot handle target: {source_url}")
            return 1
        
        # Extract content
        document = parser.extract(target)
        print(f"  ✓ Content fetched successfully")
        print(f"    - Checksum: {document.checksum}")
        print(f"    - Segments: {len(document.segments)}")
        print(f"    - Parser: {document.parser_name}")
        
        # Check for warnings
        if document.warnings:
            print(f"    - Warnings: {len(document.warnings)}")
            for warning in document.warnings:
                print(f"      • {warning}")
        
        # Convert to markdown
        markdown = parser.to_markdown(document)
        print(f"    - Markdown length: {len(markdown)} characters")
        
    except Exception as e:
        error_msg = str(e)
        
        # Check if this is a firewall block
        if "firewall" in error_msg.lower() or "blocked" in error_msg.lower():
            print(f"\n⚠️  BLOCKED BY FIREWALL")
            print(f"    Domain 'denverbroncos.com' is not on the firewall allowlist.")
            print(f"    Error: {error_msg}")
            print(f"\nNext steps:")
            print(f"  1. Add comment to issue about firewall block")
            print(f"  2. Add 'blocked-by-firewall' label")
            print(f"  3. Close issue (will be reopened after domain allowlisted)")
            return 2
        
        print(f"ERROR: Failed to fetch content: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Step 2: Store content via GitHub API
    print(f"\nStep 2: Storing content to filesystem")
    
    # Parse domain from URL for directory structure
    parsed_url = urlparse(source_url)
    domain = parsed_url.netloc
    
    # Create directory structure: evidence/parsed/{domain}/
    project_root = Path.cwd()
    base_dir = project_root / "evidence" / "parsed" / domain
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Store content.md
    content_path = base_dir / "content.md"
    print(f"  - Storing markdown to: {content_path.relative_to(project_root)}")
    
    try:
        if github_client:
            github_client.commit_file(
                path=str(content_path.relative_to(project_root)),
                content=markdown,
                message=f"Acquire content from {source_url}",
            )
        else:
            content_path.write_text(markdown, encoding="utf-8")
        print(f"    ✓ Stored content.md")
    except Exception as e:
        print(f"ERROR: Failed to store content.md: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Store metadata.json
    metadata = {
        "source_url": source_url,
        "acquired_at": datetime.now(timezone.utc).isoformat(),
        "content_hash": document.checksum,
        "parser": document.parser_name,
        "segments_count": len(document.segments),
        "metadata": document.metadata,
    }
    
    metadata_path = base_dir / "metadata.json"
    print(f"  - Storing metadata to: {metadata_path.relative_to(project_root)}")
    
    try:
        if github_client:
            github_client.commit_file(
                path=str(metadata_path.relative_to(project_root)),
                content=json.dumps(metadata, indent=2),
                message=f"Store metadata for {source_url}",
            )
        else:
            metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        print(f"    ✓ Stored metadata.json")
    except Exception as e:
        print(f"ERROR: Failed to store metadata.json: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Step 3: Update source registry
    print(f"\nStep 3: Updating source registry")
    
    try:
        kb_root = paths.get_knowledge_graph_root()
        registry = SourceRegistry(
            root=kb_root,
            github_client=github_client,
            project_root=Path.cwd(),
        )
        
        # Get existing source entry
        source_entry = registry.get_source(source_url)
        if not source_entry:
            print(f"ERROR: Source entry not found for {source_url}")
            return 1
        
        print(f"  - Found source entry: {source_entry.name}")
        
        # Update with acquisition metadata
        source_entry.last_content_hash = document.checksum
        source_entry.last_checked = datetime.now(timezone.utc)
        
        # Save updated entry
        registry.save_source(source_entry)
        print(f"    ✓ Updated source registry")
        print(f"      - last_content_hash: {document.checksum[:16]}...")
        print(f"      - last_checked: {source_entry.last_checked.isoformat()}")
        
    except Exception as e:
        print(f"ERROR: Failed to update source registry: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Success summary
    print(f"\n{'=' * 60}")
    print(f"✓ Acquisition completed successfully!")
    print(f"{'=' * 60}")
    print(f"Source: {source_url}")
    print(f"Content hash: {document.checksum[:16]}...")
    print(f"Stored at: evidence/parsed/{domain}/")
    print(f"  - content.md ({len(markdown)} chars)")
    print(f"  - metadata.json")
    print(f"\nSource registry updated:")
    print(f"  - last_content_hash: {document.checksum[:16]}...")
    print(f"  - last_checked: {datetime.now(timezone.utc).isoformat()}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
