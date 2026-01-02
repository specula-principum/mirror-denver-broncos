# Extraction Report: Denver Broncos Podcasts Page

**Document Checksum:** `0e5b799c87eff69ff61a06748422d28c9452c9e4b51907701322d9784aa53055`  
**Source URL:** https://www.denverbroncos.com/podcasts/  
**Assessment Date:** 2026-01-02  
**Status:** ⚠️ **BLOCKED - Configuration Error**

## Document Assessment

### Content Type
Podcast directory/listing page from the official Denver Broncos website.

### Substantive Content Analysis

✅ **SUBSTANTIVE CONTENT CONFIRMED**

The document contains valuable extractable information:

**Podcast Shows Identified:**
1. **Altitude Advantage** - Primary Broncos analysis show
2. **Entre Amigos** - Spanish language analysis 
3. **Broncast** - Team-focused podcast series

**Episode Examples (with dates):**
- "How Broncos can earn key postseason advantage with win vs. Chargers" (Jan 01, 2026)
- "Broncos set sights on clinching No. 1 seed after AFC West title" (Dec 29, 2025)
- "Broncast | Análisis del juego de la Semana 17: Broncos vs. Chiefs" (Dec 26, 2025)
- "A closer look at the Broncos 2026 Pro Bowlers, Christmas Day game vs. Chiefs" (Dec 24, 2025)

**Extractable Entities:**
- **People**: Pro Bowl players, likely coaching staff mentioned in episodes
- **Organizations**: Denver Broncos, opponent teams (Chargers, Chiefs, Jaguars)
- **Concepts**: Playoff positioning, Pro Bowl, AFC West championship, game analysis
- **Events**: Specific games with dates, playoffs, Christmas Day game

**Content Quality:**
- Real substantive information, not just navigation
- Contains dates, names, and specific topics
- Multi-language content (English and Spanish)
- Recent and relevant (Dec 2025 - Jan 2026)

### Skip Criteria Check

❌ NOT a navigation page - Contains actual podcast content listings  
❌ NOT an error page - Valid content retrieved  
❌ NOT boilerplate - Real podcast metadata and descriptions  
❌ NOT duplicate - Unique podcast listing page  

**Conclusion:** This document should proceed to extraction.

## Extraction Status

### ❌ BLOCKED: Missing GitHub Token

**Error Encountered:**
```
Initialization error: GitHub token required. Set GH_TOKEN or GITHUB_TOKEN environment variable or pass api_key parameter.
```

**Root Cause:**
The extraction commands require access to the GitHub Models API (via `CopilotClient`) for LLM-based entity extraction. This requires a `GITHUB_TOKEN` or `GH_TOKEN` environment variable, which is not available in the current Copilot agent execution environment.

**Configuration Issue:**
All workflows in `.github/workflows/` reference `secrets.GH_TOKEN`, but this secret is not configured or not being injected into the Copilot agent environment.

**Required Fix:**
Repository owner must configure the `GH_TOKEN` repository secret with a GitHub Personal Access Token that has:
- Access to GitHub Models API
- Appropriate scopes for LLM inference

## Attempted Commands

### Command 1: Extract People
```bash
python main.py extract --checksum 0e5b799c87eff69ff61a06748422d28c9452c9e4b51907701322d9784aa53055
```
**Result:** Failed - Missing GITHUB_TOKEN

### Command 2: Extract Organizations
```bash
python main.py extract --checksum 0e5b799c87eff69ff61a06748422d28c9452c9e4b51907701322d9784aa53055 --orgs
```
**Result:** Not attempted (blocked by prerequisite failure)

### Command 3: Extract Concepts
```bash
python main.py extract --checksum 0e5b799c87eff69ff61a06748422d28c9452c9e4b51907701322d9784aa53055 --concepts
```
**Result:** Not attempted (blocked by prerequisite failure)

### Command 4: Extract Associations
```bash
python main.py extract --checksum 0e5b799c87eff69ff61a06748422d28c9452c9e4b51907701322d9784aa53055 --associations
```
**Result:** Not attempted (blocked by prerequisite failure)

## Recommendations

1. **Immediate Action Required**: Configure `GH_TOKEN` secret in repository settings
   - Navigate to Repository Settings → Secrets and variables → Actions
   - Add new repository secret named `GH_TOKEN`
   - Value should be a GitHub PAT with Models API access

2. **Verify Token Scope**: Ensure the token has access to GitHub Models API endpoint

3. **Re-queue Document**: Once token is configured, re-trigger extraction for this document

4. **Test Configuration**: Verify token works by running a test extraction locally or in Actions

## Expected Extraction Results

Once the configuration issue is resolved, this document should yield:

**People Entities:**
- Broncos players (especially 2026 Pro Bowlers)
- Podcast hosts
- Coaching staff mentioned in episodes

**Organization Entities:**
- Denver Broncos
- NFL teams (Chiefs, Chargers, Jaguars)
- AFC West

**Concept Entities:**
- Pro Bowl 2026
- AFC West Championship
- Playoff seeding (#1 seed)
- Game analysis
- Bilingual content/Spanish language coverage

**Associations:**
- Player ↔ Team relationships
- Game ↔ Date relationships
- Podcast ↔ Topic relationships

## Labels to Apply

According to extraction pipeline documentation:
- ⚠️ `extraction-error` - Extraction failed due to configuration issue
- 📌 Leave issue **OPEN** for retry after configuration fix

## Next Steps

1. **Repository Owner**: Configure `GH_TOKEN` secret
2. **Re-trigger**: Add `extraction-queue` label to this issue again
3. **Monitor**: Verify extraction completes successfully
4. **Cleanup**: Remove this report file after successful extraction
