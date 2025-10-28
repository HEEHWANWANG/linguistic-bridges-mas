# Environment Configuration Guide

## Overview

The Linguistic Bridges Multi-Agent System can be fully configured through environment variables in the `.env` file. This allows you to customize system behavior without modifying code.

## Quick Setup

1. Copy the template:
```bash
cp .env.template .env
```

2. Edit `.env` with your settings:
```bash
nano .env  # or your preferred editor
```

3. Run the system:
```bash
python main.py
```

## Configuration Reference

### API Keys (Required/Optional)

#### ANTHROPIC_API_KEY (Required)
- **Type**: String
- **Description**: API key for Claude models
- **Get it from**: https://console.anthropic.com/
- **Example**: `ANTHROPIC_API_KEY=sk-ant-api03-xxx`

#### GOOGLE_API_KEY (Optional)
- **Type**: String
- **Description**: API key for Gemini models
- **Get it from**: https://makersuite.google.com/app/apikey
- **Example**: `GOOGLE_API_KEY=AIzaSyXXX`

#### TAVILY_API_KEY (Optional)
- **Type**: String
- **Description**: API key for web search
- **Get it from**: https://tavily.com/
- **Example**: `TAVILY_API_KEY=tvly-xxx`

### System Configuration

#### MAX_PARALLEL_AGENTS
- **Type**: Integer
- **Default**: 10
- **Range**: 1-50
- **Description**: Maximum number of agents that can run concurrently
- **Usage**:
  - Lower (1-5): More sequential, less memory, slower
  - Medium (5-15): Balanced performance
  - Higher (15+): Parallel processing, requires more resources
- **Example**: `MAX_PARALLEL_AGENTS=10`

#### DEFAULT_MODEL
- **Type**: String
- **Default**: `claude-sonnet-4-5`
- **Options**:
  - `claude-sonnet-4-5`: Fast, efficient (recommended)
  - `claude-opus-4`: Most capable, slower, expensive
  - `gemini-2.0-flash`: Google's model (requires GOOGLE_API_KEY)
- **Description**: Default LLM model for all agents
- **Example**: `DEFAULT_MODEL=claude-sonnet-4-5`

#### WORKSPACE_PATH
- **Type**: Path
- **Default**: `.claude/workspace`
- **Description**: Directory for agent operations and temporary files
- **Example**: `WORKSPACE_PATH=.claude/workspace`

#### MAX_EVOLUTION_ITERATIONS
- **Type**: Integer
- **Default**: 3
- **Range**: 1-10
- **Description**: Number of hypothesis evolution rounds in Research Guild
- **Impact**:
  - Lower (1-2): Faster, less refined hypotheses
  - Medium (3-5): Balanced quality
  - Higher (6+): Better hypotheses, slower, more API calls
- **Example**: `MAX_EVOLUTION_ITERATIONS=3`

#### HYPOTHESIS_GENERATION_COUNT
- **Type**: Integer
- **Default**: 7
- **Range**: 1-20
- **Description**: Number of hypotheses to generate in each batch
- **Impact**:
  - Lower (3-5): Focused exploration
  - Medium (7-10): Balanced diversity
  - Higher (10+): Broad exploration, slower
- **Example**: `HYPOTHESIS_GENERATION_COUNT=7`

#### MAX_TOKENS
- **Type**: Integer
- **Default**: 8000
- **Range**: 1000-200000 (model-dependent)
- **Description**: Maximum tokens per LLM request
- **Example**: `MAX_TOKENS=8000`

#### TEMPERATURE
- **Type**: Float
- **Default**: 0.7
- **Range**: 0.0-2.0
- **Description**: LLM generation temperature
- **Values**:
  - 0.0-0.3: Deterministic, focused
  - 0.4-0.8: Balanced creativity
  - 0.9-2.0: Very creative, less predictable
- **Example**: `TEMPERATURE=0.7`

#### HUMAN_APPROVAL_TIMEOUT
- **Type**: Integer
- **Default**: 3600 (1 hour)
- **Unit**: Seconds
- **Special**: Set to 0 for no timeout
- **Description**: How long to wait for human approval before timing out
- **Example**: `HUMAN_APPROVAL_TIMEOUT=3600`

#### DEBUG_MODE
- **Type**: Boolean
- **Default**: false
- **Values**: `true`, `false`
- **Description**: Enable debug logging for detailed information
- **Example**: `DEBUG_MODE=false`

#### PROGRESS_CHECK_INTERVAL
- **Type**: Integer
- **Default**: 300 (5 minutes)
- **Unit**: Seconds
- **Description**: How often Supervisor checks guild progress
- **Example**: `PROGRESS_CHECK_INTERVAL=300`

#### MAX_RETRIES
- **Type**: Integer
- **Default**: 3
- **Range**: 0-10
- **Description**: Maximum retry attempts for failed operations
- **Example**: `MAX_RETRIES=3`

#### RETRY_BACKOFF_FACTOR
- **Type**: Integer
- **Default**: 2
- **Description**: Exponential backoff multiplier for retries
- **Example**: `RETRY_BACKOFF_FACTOR=2`

#### VECTOR_DB_PATH
- **Type**: Path
- **Default**: `./data/vector_db`
- **Description**: Directory for vector database persistence
- **Example**: `VECTOR_DB_PATH=./data/vector_db`

#### GRACEFUL_DEGRADATION
- **Type**: Boolean
- **Default**: true
- **Values**: `true`, `false`
- **Description**: Allow partial completion when some components fail
- **Example**: `GRACEFUL_DEGRADATION=true`

## Configuration Examples

### Fast Development (Minimal Resources)
```properties
MAX_PARALLEL_AGENTS=3
DEFAULT_MODEL=claude-sonnet-4-5
MAX_EVOLUTION_ITERATIONS=1
HYPOTHESIS_GENERATION_COUNT=3
TEMPERATURE=0.3
DEBUG_MODE=true
```

### Balanced Production (Recommended)
```properties
MAX_PARALLEL_AGENTS=10
DEFAULT_MODEL=claude-sonnet-4-5
MAX_EVOLUTION_ITERATIONS=3
HYPOTHESIS_GENERATION_COUNT=7
TEMPERATURE=0.7
DEBUG_MODE=false
```

### High Quality Research (More Thorough)
```properties
MAX_PARALLEL_AGENTS=15
DEFAULT_MODEL=claude-opus-4
MAX_EVOLUTION_ITERATIONS=5
HYPOTHESIS_GENERATION_COUNT=10
TEMPERATURE=0.8
DEBUG_MODE=false
MAX_TOKENS=16000
```

### Resource-Constrained (Minimal API Usage)
```properties
MAX_PARALLEL_AGENTS=1
DEFAULT_MODEL=claude-sonnet-4-5
MAX_EVOLUTION_ITERATIONS=2
HYPOTHESIS_GENERATION_COUNT=3
TEMPERATURE=0.5
MAX_TOKENS=4000
```

## Checking Your Configuration

Run the status command to see your current configuration:

```bash
python cli.py status
```

Output example:
```
System Status Check

✅ Environment file (.env)
✅ Anthropic API Key
⚠️  Google API Key (optional)
✅ Vector database

Current Configuration:
  Model: claude-sonnet-4-5
  Max Parallel Agents: 10
  Evolution Iterations: 3
  Hypothesis Count: 7
  Workspace: .claude/workspace
  Debug Mode: False
  Vector DB: ./data/vector_db
```

## Troubleshooting

### "ANTHROPIC_API_KEY is required"
- Ensure `.env` file exists
- Check that `ANTHROPIC_API_KEY=sk-ant-...` is set correctly
- No spaces around the `=` sign

### Configuration not taking effect
1. Restart the program after changing `.env`
2. Check for typos in variable names (case-sensitive)
3. Ensure values are valid (e.g., integers where expected)

### Performance Issues
- Reduce `MAX_PARALLEL_AGENTS` if running out of memory
- Lower `MAX_EVOLUTION_ITERATIONS` for faster completion
- Decrease `HYPOTHESIS_GENERATION_COUNT` to reduce API calls

## Best Practices

1. **Start with defaults** - They're well-tested
2. **Enable DEBUG_MODE** during development
3. **Use claude-sonnet-4-5** for cost-effectiveness
4. **Monitor API costs** when increasing batch sizes
5. **Backup your .env** but never commit it to git

## Security Note

⚠️ **Never commit your `.env` file to version control!**

The `.gitignore` file should include:
```
.env
*.env
```

Keep your API keys secure and rotate them regularly.
