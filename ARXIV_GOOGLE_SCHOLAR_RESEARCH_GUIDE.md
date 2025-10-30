# ArXiv and Google Scholar MCP - Research Guide for Linguistic Bridges

Comprehensive guide for using ArXiv MCP and Google Scholar MCP as your default research literature tools.

---

## Quick Start

### Installation

**ArXiv MCP (Easy)**:
```bash
npx -y @smithery/cli install arxiv-mcp-server --client claude
```

**Google Scholar MCP (Manual)**:
```bash
git clone https://github.com/JackKuo666/Google-Scholar-MCP-Server.git
cd Google-Scholar-MCP-Server
pip install -r requirements.txt
```

### Basic Usage

```
1. Start session: /sc:load

2. Academic research mode:
   /sc:research "music visual alignment" --academic
   → Auto-activates Google Scholar + ArXiv

3. Deep literature review:
   /sc:research "multimodal learning" --deep-academic
   → Full workflow with rate limiting

4. Find author papers:
   /sc:research --author "Michael Wooldridge" --scholar

5. End session: /sc:save
```

---

## Tool Comparison

### Google Scholar MCP
**Perfect for**: Foundation research, citation analysis, author discovery

| Aspect | Details |
|--------|---------|
| **Strength** | Citation metrics (h-index), comprehensive, foundational |
| **Search Speed** | 3-6s + **10-15s mandatory wait** |
| **Rate Limit** | STRICT: 5-10 req/min (one of strictest MCPs) |
| **Max/Session** | 3-5 searches maximum |
| **Best For** | Starting research, finding key authors, citation analysis |
| **Access** | All disciplines, published works |

**Tools**:
1. `search_google_scholar_keywords` - Basic search
2. `search_google_scholar_advanced` - Author/year filters
3. `get_author_info` - Author h-index, publications

**Example Workflow**:
```
Query: "multimodal learning music"
↓ [WAIT 15s]
→ Get top 10 papers with citations

For each top author:
  Query: get_author_info(author_name)
  ↓ [WAIT 15s]
  → Review h-index and publication history
```

---

### ArXiv MCP
**Perfect for**: Latest research, technical details, PDF access

| Aspect | Details |
|--------|---------|
| **Strength** | Latest preprints (same day), PDF downloads, generous rate limits |
| **Search Speed** | 2-4 seconds |
| **Rate Limit** | GENEROUS: 1 req/3s (~1200 req/hour) |
| **Max/Session** | 20-30 papers (unlimited searches) |
| **Best For** | Latest research, downloading papers, category filtering |
| **Access** | Preprints, open access |

**Tools**:
1. `search_arxiv` - Search with category/date filters
2. `get_paper` - Download PDF by arXiv ID
3. `list_papers` - View downloaded papers
4. `read_paper` - Access paper content

**Example Workflow**:
```
Query: cs.MA + abs:communication + recent 6 months
↓ [2s wait]
→ Get latest multiagent papers

For each relevant paper:
  Download PDF
  ↓ [5-20s wait]
  → Store locally

Analyze with deep-paper-analysis
```

---

## Recommended Research Phases

### Phase 1: Hypothesis Foundation (Week 1-2)

**Goal**: Identify foundational concepts and key researchers

**Tools**: Google Scholar PRIMARY

**Workflow**:
```
1. Start with broad academic searches:

   Scholar Search 1: "music perception visual features"
   [WAIT 15s]
   → Papers: 5-10 top results
   → Review: citation counts, key authors

   Scholar Search 2: "multimodal representation learning"
   [WAIT 15s]
   → Papers: 5-10 top results
   → Analyze: methods and approaches

   Scholar Search 3: Key author analysis
   [WAIT 15s]
   → get_author_info("Author Name")
   → Review h-index (>20 = influential)

2. Build knowledge map:
   - Identify 3-5 key researchers
   - Note 5-10 seminal papers
   - Understand core concepts

3. Save results:
   /sc:save → Persist findings
```

**Expected Results**:
- 10-15 foundational papers identified
- 5-10 key authors identified
- Understanding of field landscape
- 30-45 minutes elapsed

---

### Phase 2: Latest Developments (Week 3-4)

**Goal**: Discover cutting-edge research and recent advances

**Tools**: ArXiv PRIMARY + Google Scholar SECONDARY

**Workflow**:
```
1. ArXiv searches for latest papers:

   ArXiv Search 1: cs.MA category, last 6 months
   Query: "multimodal communication"
   → 50+ papers returned
   → Download top 5-10 PDFs

   ArXiv Search 2: cs.LG category, last 6 months
   Query: "disentangled representation learning"
   → 100+ papers returned
   → Download top 5-10 PDFs

   ArXiv Search 3: By known authors
   Query: au:"Michael Wooldridge" AND ti:agent
   → Recent papers by key authors
   → Download relevant PDFs

2. Deep analysis:
   For each downloaded paper:
   - Run deep-paper-analysis
   - Note novel approaches
   - Identify citations to Phase 1 papers

3. Google Scholar verification:
   Scholar Search 4: "citation count to top paper"
   [WAIT 15s]
   → Confirm paper importance
   → Find citing papers
```

**Expected Results**:
- 20-30 latest papers downloaded
- 3-5 breakthrough papers identified
- Understanding of latest methods
- New research directions identified

---

### Phase 3: Deep Dive Implementation (Week 5-6)

**Goal**: Understand implementation approaches and datasets

**Tools**: ArXiv + Tavily + Context7

**Workflow**:
```
1. Implementation-focused ArXiv searches:

   ArXiv Search 5: Datasets and benchmarks
   Query: "music dataset" OR "benchmark evaluation"
   → Download dataset papers

   ArXiv Search 6: Implementation details
   Query: "code implementation neural network music"
   → Download method papers

2. Find practical implementations:
   Tavily: GitHub repos, tutorials, benchmarks

3. Reference official documentation:
   Context7: PyTorch, TensorFlow patterns
```

---

## Critical Rules

### ⚠️ GOOGLE SCHOLAR - ESSENTIAL

These rules prevent IP blocking (24+ hour bans):

1. **ALWAYS add 10-15 second delays** between requests
   ```python
   time.sleep(random.uniform(10, 15))  # Between each query
   ```

2. **Maximum 5 searches per session**
   - Not per hour, per session
   - Plan searches carefully before starting

3. **Never do rapid-fire searches**
   - This is #1 way to get blocked
   - Even 1 second delay is not enough

4. **Use simpler queries**
   - Fewer AND/OR operators
   - Broader terms sometimes better

5. **If blocked**:
   - Wait 24+ hours
   - Use VPN (different IP)
   - Don't try again soon

### ✅ ARXIV - VERY SAFE

1. **Can do rapid searches** (2-3s delay only)
2. **Can download many papers** (generous limits)
3. **Can use complex queries** with field operators
4. **Generally no blocking** issues

---

## Search Queries for Linguistic Bridges

### Google Scholar Queries

```
Query 1: "music perception" AND "visual features"
Goal: Foundation papers on music-visual alignment

Query 2: "multimodal learning" AND "representation"
Goal: Representation learning for multiple modalities

Query 3: "cognitive architecture" AND "language"
Goal: How agents understand language and multimodal concepts

Query 4: Search by author
Author: "Michael Wooldridge" (Multiagent systems expert)

Query 5: Citation analysis of top papers
Analyze h-index and i10-index of key researchers
```

### ArXiv Queries

**Category Filter**: cs.MA (Multiagent), cs.LG (Machine Learning), cs.CL (NLP)

```
Query 1: Field-specific searches
ti:multiagent AND abs:communication

Query 2: Recent developments (last 6 months)
cat:cs.MA submittedDate:[202401010000 TO 202412312359]

Query 3: Known author papers
au:"Yoav Shoham" AND ti:agent

Query 4: Combined topics
ti:"representation learning" AND abs:music

Query 5: Disentanglement focus
ti:disentangled AND abs:learning
```

---

## Complete Research Workflow

### Session Structure

```
START SESSION: /sc:load
│
├─ Phase 1: FOUNDATION (Google Scholar)
│  ├─ Scholar Search 1: "music visual alignment"
│  │  [WAIT 15s]
│  ├─ Scholar Search 2: "multimodal learning"
│  │  [WAIT 15s]
│  ├─ Scholar Search 3: "cognitive architecture language"
│  │  [WAIT 15s]
│  └─ Author Analysis: get_author_info (top 3 authors)
│     [WAIT 15s]
│
├─ CHECKPOINT: /sc:save
│
├─ Phase 2: LATEST (ArXiv)
│  ├─ ArXiv Search 1: cs.MA + "multimodal"
│  ├─ ArXiv Search 2: cs.LG + "representation learning"
│  ├─ ArXiv Search 3: By known authors
│  └─ Download PDFs: 10-15 papers
│
├─ Phase 3: ANALYSIS
│  ├─ Deep paper analysis on key papers
│  ├─ Run Sequential reasoning on findings
│  └─ Build knowledge graph
│
├─ Phase 4: PRACTICAL (Tavily)
│  ├─ Find implementations
│  ├─ Identify datasets
│  └─ Locate benchmarks
│
└─ CHECKPOINT: /sc:save
   END SESSION
```

---

## Performance & Rate Limiting

### Time Estimates

**Google Scholar** (strict rate limiting):
```
Query execution: 3-6 seconds
Mandatory wait: 10-15 seconds
Total per search: 15-20 seconds
5 searches: 75-100 seconds (1.25-1.67 minutes)
```

**ArXiv** (generous rate limiting):
```
Query execution: 2-4 seconds
Optional wait: 2-3 seconds
Total per search: 4-7 seconds
20 searches: 80-140 seconds (1.3-2.3 minutes)
PDF download: 5-20 seconds each
10 PDFs: 50-200 seconds
Total with downloads: 2-4 minutes
```

**Total for Complete Research Session**:
- Phase 1 (Scholar): ~2 minutes
- Phase 2 (ArXiv): ~3-4 minutes
- Phase 3 (Analysis): ~10-15 minutes
- Phase 4 (Tavily): ~5-10 minutes
- **Total**: 20-30 minutes for thorough literature review

### Rate Limiter Implementation

```python
import asyncio
import time
import random

class AcademicResearchRateLimiter:
    def __init__(self):
        self.scholar_last = 0
        self.arxiv_last = 0

    async def wait_scholar(self):
        """10-15s delay for Google Scholar"""
        elapsed = time.time() - self.scholar_last
        delay = random.uniform(10, 15)
        if elapsed < delay:
            await asyncio.sleep(delay - elapsed)
        self.scholar_last = time.time()

    async def wait_arxiv(self):
        """2-3s delay for ArXiv"""
        elapsed = time.time() - self.arxiv_last
        delay = random.uniform(2, 3)
        if elapsed < delay:
            await asyncio.sleep(delay - elapsed)
        self.arxiv_last = time.time()
```

---

## Integration with SuperClaude Framework

### Automatic Activation

When you use research commands:

```bash
/sc:research "topic" --academic
→ Automatically:
  1. Start with Google Scholar (foundation)
  2. Implement 15s delays
  3. Download 5 papers with
  4. Add ArXiv to workflow
  5. Enable caching
```

### Flags for Control

```bash
# Use Scholar only (foundational research)
/sc:research "topic" --scholar

# Use ArXiv only (latest papers)
/sc:research "topic" --arxiv

# Full academic workflow
/sc:research "topic" --deep-academic

# Combined with other tools
/sc:research "topic" --academic --tavily --sequential
```

---

## Troubleshooting

### Google Scholar Blocked (403 errors)

**Problem**: IP address blocked for excessive requests

**Solutions**:
1. Wait 24+ hours for automatic unblock
2. Use VPN with different IP address
3. Reduce request frequency
4. Add longer delays (15-20s)

**Prevention**:
- Always use 10-15s minimum delays
- Max 5 searches per session
- Plan searches before executing
- Never rapid-fire requests

### ArXiv No Results

**Problem**: Query returns empty results

**Solutions**:
1. Try broader search terms
2. Remove category restrictions
3. Extend date range
4. Use different field operators (ti: vs au:)

### PDF Download Fails

**Problem**: ArXiv PDF download fails

**Solutions**:
1. Check arXiv ID validity
2. Verify storage directory permissions
3. Try different PDF quality (if available)
4. Manually download from arXiv.org

---

## Best Practices

### ✅ DO

- Plan searches before execution
- Use Google Scholar first (foundation)
- Follow ArXiv with latest papers
- Add Tavily for practical examples
- Cache results locally
- Analyze with Sequential reasoning
- Document key papers and findings
- Review author h-index for authority

### ❌ DON'T

- Rapid-fire Scholar searches (causes blocking)
- Ignore rate limiting (especially Scholar)
- Use ArXiv for citation counts (not available)
- Forget to wait 10-15s between Scholar queries
- Try to scrape bulk data
- Use Scholar for latest papers (ArXiv better)
- Ignore author h-index/credibility

---

## Summary

**Google Scholar MCP**:
- Foundation research, citations, author analysis
- Rate limit: 10-15s delays mandatory
- Max: 5 searches per session
- Best: Start here

**ArXiv MCP**:
- Latest research, PDFs, technical depth
- Rate limit: 2-3s delays (safe)
- Unlimited searches
- Best: Follow Scholar

**Combined Workflow**:
1. Scholar → Foundation (2 min)
2. ArXiv → Latest (4 min)
3. Analysis → Synthesis (15 min)
4. Tavily → Practical (10 min)
5. Total: 30 min comprehensive review

**Key Rule**: Always respect Google Scholar's strict rate limits to avoid 24+ hour IP blocks.

---

*Configuration Date: October 28, 2025*
*Status: Ready for production use*
*Default Setting: Academic research literature search*
