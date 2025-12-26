# Denver Broncos Research Project

This repository tracks and analyzes information about the Denver Broncos organization, including players, management, and sponsor relationships.

## Research Goals

- **Source**: [Denver Broncos Official Website](https://www.denverbroncos.com)
- **Topic**: Players, management and sponsor mapping
- **Update Frequency**: Weekly
- **LLM Model**: gpt-4o

## Overview

This project systematically collects, parses, and analyzes data from the Denver Broncos official website to build a comprehensive knowledge graph of:

- **Players**: Current roster, statistics, and profiles
- **Management**: Coaching staff, executives, and organizational structure
- **Sponsors**: Partnership and sponsorship relationships

## Getting Started

### Prerequisites

- Python 3.8+
- GitHub Personal Access Token (for automated workflows)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Usage

The `main.py` CLI provides tools for document parsing, entity extraction, and workflow automation:

```bash
# Parse web content from the source
python -m main parse web https://www.denverbroncos.com

# Scan and process evidence directory
python -m main parse scan --recursive

# Run agent workflows
python -m main run-agent
```

## Project Structure

- **`evidence/`**: Source documents and raw data
- **`knowledge-graph/`**: Extracted entities and relationships
- **`reports/`**: Analysis reports and summaries
- **`dev_data/`**: Development and testing artifacts
- **`config/manifest.json`**: Project configuration

## Workflows

This repository uses automated GitHub Actions workflows to:

- Monitor the Denver Broncos website for updates (weekly)
- Parse new content into structured data
- Extract entities and build the knowledge graph
- Generate reports and summaries

## Contributing

This is a research repository. Updates are primarily automated through the configured workflows. Manual contributions to enhance analysis or fix data quality issues are welcome.

## License

Research data is collected from public sources. See individual source citations for usage rights.