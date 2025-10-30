# ArXiv and Google Scholar MCP Servers - Configuration Guide

Permanent configuration for academic literature research using ArXiv MCP and Google Scholar MCP servers.

---

## Overview

Two specialized MCP servers for comprehensive academic literature research:

1. **ArXiv MCP Server** - Latest preprints and cutting-edge research
2. **Google Scholar MCP Server** - Citation analysis and foundational papers

Together they provide complete academic research capabilities.

---

## 1. ARXIV MCP SERVER

### Purpose
Access latest research papers from arXiv.org through Claude, including PDF downloads and automated paper analysis.

### Installation

**Easiest Method (Smithery)**:
```bash
npx -y @smithery/cli install arxiv-mcp-server --client claude
```

**Manual Installation**:
```bash
# Clone the repository
git clone https://github.com/blazickjp/arxiv-mcp-server.git
cd arxiv-mcp-server

# Install with uv
uv sync
```

### Configuration for claude_desktop_config.json

Add to your MCP servers section:
```json
"arxiv": {
  "command": "uv",
  "args": ["run", "arxiv-mcp-server"],
  "env": {
    "ARXIV_PAPERS_DIR": "/path/to/papers/storage"
  }
}
```

### Available Tools

1. **search_arxiv**
   - Search arXiv papers by keywords
   - Filter by date range and categories
   - Returns metadata and arXiv IDs

2. **get_paper**
   - Download full paper by arXiv ID
   - Stores locally for quick access
   - Returns paper content

3. **list_papers**
   - View all downloaded papers
   - Shows metadata and storage info

4. **read_paper**
   - Access downloaded paper content
   - Analyze with deep-paper-analysis workflow

### Search Parameters

**Basic Search**:
```
query: "quantum computing"
max_results: 10
```

**Advanced Search with Filters**:
```
query: "machine learning AND neural networks"
categories: "cs.LG"  # Computer Science - Machine Learning
from_date: "2023-01-01"
to_date: "2024-12-31"
max_results: 20
```

**Field-Specific Searches**:
- `ti:` - Title (e.g., `ti:quantum computing`)
- `au:` - Author (e.g., `au:Hinton`)
- `abs:` - Abstract (e.g., `abs:reinforcement learning`)
- `all:` - All fields (default)

### Rate Limiting

- **Limit**: ~1 request per 3 seconds (very generous)
- **Strategy**: Safe to use for rapid searches
- **Recommendation**: 2-3 second delays for courtesy

### Best Practices

✅ **Do**:
- Use field-specific queries for precision
- Combine multiple operators: `ti:multiagent AND au:Jennings`
- Download papers to local storage for quick access
- Run deep-paper-analysis workflow on relevant papers

❌ **Don't**:
- Ignore category filtering (narrows results significantly)
- Download entire databases unnecessarily
- Run queries without date filters for broad topics

### Example Workflow

```
1. Search for recent papers:
   query: "ti:multiagent AND abs:communication"
   categories: "cs.MA,cs.AI"
   from_date: "2023-01-01"

2. Download 5 most relevant papers

3. Run deep-paper-analysis on each:
   - Executive summary
   - Methodology overview
   - Key results
   - Implications for Linguistic Bridges
```

---

## 2. GOOGLE SCHOLAR MCP SERVER

### Purpose
Access comprehensive academic databases with citation metrics, author information, and foundational research discovery.

### Installation

**Option 1: Smithery (Automated)**:
```bash
npx -y @smithery/cli install google-scholar-mcp-server --client claude
```

**Option 2: Manual Installation**:
```bash
# Clone the repository
git clone https://github.com/JackKuo666/Google-Scholar-MCP-Server.git
cd Google-Scholar-MCP-Server

# Install Python dependencies
pip install -r requirements.txt
```

### Configuration for claude_desktop_config.json

Add to your MCP servers section:
```json
"google-scholar": {
  "command": "python",
  "args": ["-m", "google_scholar_mcp.server"],
  "env": {
    "PYTHONPATH": "/path/to/Google-Scholar-MCP-Server"
  }
}
```

### Available Tools

1. **search_google_scholar_keywords**
   - Basic search by keywords
   - Returns ranked results with citations

2. **search_google_scholar_advanced**
   - Author filtering
   - Year range filtering
   - Combined with keywords

3. **get_author_info**
   - Author h-index (career impact)
   - i10-index (recent impact)
   - Publication history
   - Affiliation information

### Search Parameters

**Basic Search**:
```
query: "cognitive architectures"
count: 10
```

**Advanced Search with Filters**:
```
query: "BDI agent architecture"
author: "Michael Wooldridge"
year_from: 1995
year_to: 2023
count: 20
```

**Author Profile**:
```
author_name: "Yoav Shoham"
```

### Rate Limiting (CRITICAL)

⚠️ **Google Scholar is Very Strict**:
- **Limit**: 5-10 requests per minute maximum
- **Enforcement**: IP blocking for excessive requests
- **Solution**: Add 10-15 second delays between searches
- **Recommendation**: Plan searches before execution

**Rate Limiter Class**:
```python
import time

class GoogleScholarRateLimiter:
    def __init__(self, min_delay=10, max_delay=15):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request = 0

    async def wait(self):
        elapsed = time.time() - self.last_request
        delay = random.uniform(self.min_delay, self.max_delay)
        if elapsed < delay:
            await asyncio.sleep(delay - elapsed)
        self.last_request = time.time()
```

### Best Practices

✅ **Do**:
- Start with Google Scholar for foundational papers
- Use author filters to find key researchers
- Analyze h-index and i10-index for authority
- Cache results locally
- Plan 5-10 searches maximum per session
- Add 10-15 second delays between queries

❌ **Don't**:
- Rapid-fire searches (causes IP blocking)
- Run more than 10 searches in quick succession
- Ignore rate limiting
- Try to scrape extensive datasets
- Use for automated bulk analysis

### Example Workflow

```
1. Search for foundational papers:
   query: "language grounding multimodal"
   count: 5
   [WAIT 15 seconds]

2. Analyze top authors:
   For each author:
     - get_author_info
     - Review h-index and publications
     [WAIT 15 seconds]

3. Advanced search by author + year:
   author: "Top researcher name"
   year_from: 2015
   [WAIT 15 seconds]

4. Identify seminal papers and download from ArXiv
```

---

## 3. COMBINED WORKFLOW

### Complementary Capabilities

| Need | Use | Reason |
|------|-----|--------|
| Latest papers | ArXiv | Same-day preprints |
| Citation count | Google Scholar | Comprehensive metrics |
| Author ranking | Google Scholar | h-index, i10-index |
| PDF access | ArXiv | Direct downloads |
| Historical context | Google Scholar | Full publication history |
| Field trends | ArXiv | Category filtering |

### Recommended Research Pattern

**Phase 1: Foundation (Google Scholar)**
```
Goal: Identify foundational papers and key authors

1. Search seminal papers:
   "multimodal learning music visual"
   → Get citation counts and key authors

2. Analyze top authors:
   get_author_info for each
   → Identify impact (h-index)

3. Identify research directions:
   Look at citation patterns
```

**Phase 2: Latest Developments (ArXiv)**
```
Goal: Find cutting-edge research

1. Search by category + date:
   cs.MA (Multiagent), cs.LG (Learning)
   Recent 6-12 months

2. Download relevant papers:
   By same authors found in Phase 1
   New methodologies in field

3. Deep analysis:
   Run deep-paper-analysis workflow
```

**Phase 3: Integration (Tavily + Sequential)**
```
Goal: Connect academic findings to implementation

1. Use Tavily for implementations
2. Use Sequential for reasoning/synthesis
3. Build knowledge base
```

### Rate-Limited Search Workflow

```python
async def research_literature(query_plan):
    """
    Execute planned searches with proper rate limiting

    query_plan = [
        {"type": "scholar", "query": "...", "author": "..."},
        {"type": "arxiv", "query": "...", "category": "..."},
        ...
    ]
    """

    scholar_limiter = GoogleScholarRateLimiter()
    arxiv_limiter = ArXivRateLimiter()

    results = []

    for step in query_plan:
        if step["type"] == "scholar":
            await scholar_limiter.wait()
            result = search_google_scholar(**step)
        else:
            await arxiv_limiter.wait()
            result = search_arxiv(**step)

        results.append(result)

    return results
```

---

## 4. CONFIGURATION FOR LINGUISTIC BRIDGES RESEARCH

### Phase 1: Hypothesis Development

**Search Sequence**:
1. Google Scholar: "multimodal learning", "music visual alignment"
2. Google Scholar: Key authors (h-index analysis)
3. ArXiv: Recent papers by identified authors
4. Tavily: Implementations and practical examples

**Key Searches**:
- Scholar: `"music perception" AND "visual features"`
- Scholar: `"cognitive architecture" AND "multimodal"`
- ArXiv: `ti:multimodal abs:learning` (cs.LG category)
- ArXiv: `au:Wooldridge ti:agent` (known multiagent expert)

### Phase 2: Implementation Research

**Search Sequence**:
1. ArXiv: Technical approaches and datasets
2. Google Scholar: Citations to validate importance
3. Tavily: Code, tutorials, benchmarks

**Key Searches**:
- ArXiv: `ti:representation learning AND abs:disentangled`
- ArXiv: `ti:sequence model AND abs:music`
- Scholar: Authors of top ArXiv papers
- Tavily: Dataset descriptions and benchmarks

### Phase 3: Evaluation and Comparison

**Search Sequence**:
1. Google Scholar: Benchmark papers and comparison studies
2. ArXiv: Latest evaluation methods
3. Tavily: Online benchmarks and leaderboards

**Key Searches**:
- Scholar: `"benchmark" AND "music generation"`
- ArXiv: `ti:evaluation AND abs:multimodal`

---

## 5. AUTO-ACTIVATION RULES

### For SuperClaude Framework

Add to `.claude/CLAUDE.md`:

```yaml
mcp_activation_for_research:
  research_phase:
    primary_mcps: [tavily, sequential]
    academic_research_mcps: [google-scholar, arxiv]
    activation_triggers:
      - hypothesis_phase: google-scholar
      - implementation_phase: arxiv
      - literature_review: both

  execution_pattern:
    1. Google Scholar first (foundation)
    2. [WAIT 15+ seconds]
    3. ArXiv second (latest)
    4. Tavily third (practical)

  rate_limiting:
    google_scholar:
      min_delay: 10
      max_delay: 15
      max_per_session: 5

    arxiv:
      min_delay: 2
      max_delay: 3
      max_per_session: unlimited
```

### Commands for Research

```bash
# Search academic literature
/sc:research "query" --academic
→ Auto-activates Google Scholar + ArXiv

# Deep literature review
/sc:research "topic" --deep-academic
→ Runs full workflow with both MCPs

# Find author papers
/sc:research --author "Name" --scholar
→ Google Scholar for author analysis

# Get latest papers
/sc:research "topic" --arxiv-latest
→ ArXiv recent papers only
```

---

## 6. INTEGRATION WITH EXISTING MCP STACK

### Complete MCP Ecosystem

```
Research Literature:
├── Google Scholar MCP (foundation, citations)
├── ArXiv MCP (latest, PDFs)
└── Tavily (implementations, tutorials)

Code Understanding:
├── Serena (semantic code analysis)
└── Context7 (documentation patterns)

Complex Reasoning:
└── Sequential (hypothesis evolution, synthesis)

Code Transformation:
└── Morphllm (bulk editing)

Testing:
└── Playwright (validation)
```

### Workflow Integration

```
Research Phase:
  Google Scholar → Identify foundations
  ↓ [15s wait]
  ArXiv → Download latest
  ↓ [analyze with Sequential]
  Tavily → Find implementations

Implementation Phase:
  Serena → Code understanding
  ArXiv → Reference papers
  Context7 → Framework patterns
  Sequential → Design reasoning

Documentation Phase:
  Tavily → Related work links
  Google Scholar → Citation formatting
  ArXiv → Paper references
  Context7 → Academic standards
```

---

## 7. TROUBLESHOOTING

### ArXiv Issues

**Problem**: Search returns no results
- **Solution**: Try broader query, remove category filters, use different keywords

**Problem**: PDF download fails
- **Solution**: Check storage path permissions, verify arXiv ID validity

**Problem**: Slow searches
- **Solution**: Add category filters, narrow date range, reduce max_results

### Google Scholar Issues

**Problem**: IP Blocked (403 errors)
- **Solution**: Wait 24+ hours, use VPN/proxy, reduce request frequency
- **Prevention**: Always use 10-15 second delays

**Problem**: Timeouts
- **Solution**: Longer delays between requests, simpler queries

**Problem**: No author information returned
- **Solution**: Try different name format, use full name, check spelling

### Common Solutions

✅ **Always**:
- Plan searches before execution
- Use rate limiting properly (especially Scholar)
- Start with simple queries, add filters gradually
- Cache results locally

---

## 8. PERFORMANCE EXPECTATIONS

### ArXiv Speed
- **Search**: 2-4 seconds
- **PDF Download**: 5-20 seconds (depends on file size)
- **Analysis**: 10-30 seconds (with Sequential)
- **Total per paper**: ~20-50 seconds

### Google Scholar Speed
- **Search**: 3-6 seconds (+ 10-15s mandatory wait)
- **Author lookup**: 2-4 seconds (+ 10-15s mandatory wait)
- **Total per query**: ~15-20 seconds minimum

### Recommended Session Limits
- **ArXiv**: 20-30 papers per session
- **Google Scholar**: 3-5 searches per session
- **Combined**: 1-2 hours maximum

---

## 9. INSTALLATION CHECKLIST

For setting up both MCPs:

```
Installation:
☐ Install ArXiv MCP (Smithery or manual)
☐ Install Google Scholar MCP (manual)
☐ Configure claude_desktop_config.json
☐ Restart Claude Desktop

Verification:
☐ Test ArXiv search_arxiv tool
☐ Test Google Scholar search tool
☐ Test get_author_info tool
☐ Verify rate limiting works

Integration:
☐ Update .claude/CLAUDE.md
☐ Add to SuperClaude framework
☐ Create research workflows
☐ Document search patterns
```

---

## Summary

**ArXiv MCP**: Latest research, PDFs, technical focus, generous rate limits
**Google Scholar MCP**: Citations, authors, foundational papers, strict rate limits

**Together**: Complete academic research capability for Linguistic Bridges

**Key Rule**: Always use Google Scholar first (foundation) → ArXiv second (latest) → Tavily third (practical)

---

*Configuration Date: October 28, 2025*
*Status: Ready for deployment*
