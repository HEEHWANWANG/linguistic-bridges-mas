"""
MCP (Model Context Protocol) Manager for Linguistic Bridges
Manages connections to various external services and APIs
"""
import os
from typing import Dict, Any, Optional, List
import logging
from abc import ABC, abstractmethod


class BaseMCP(ABC):
    """Base class for all MCP connections"""
    
    def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        self.config = config
        self.logger = logger or logging.getLogger(f"MCP.{self.__class__.__name__}")
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """Execute MCP-specific operation"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if MCP is healthy and accessible"""
        pass


class LLMProviderMCP(BaseMCP):
    """MCP for LLM API calls (Anthropic, Google)"""
    
    def __init__(self, config: Dict[str, Any], provider: str = "anthropic"):
        super().__init__(config)
        self.provider = provider
        self._client = None
        
    async def execute(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        **kwargs
    ) -> str:
        """Execute LLM completion"""
        if self.provider == "anthropic":
            return await self._call_anthropic(messages, system, **kwargs)
        elif self.provider == "google":
            return await self._call_google(messages, system, **kwargs)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    async def _call_anthropic(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        **kwargs
    ) -> str:
        """Call Anthropic API"""
        try:
            import anthropic
            
            if not self._client:
                api_key = os.getenv("ANTHROPIC_API_KEY")
                self._client = anthropic.AsyncAnthropic(api_key=api_key)
            
            response = await self._client.messages.create(
                model=self.config.get("model", "claude-sonnet-4-5-20250929"),
                max_tokens=kwargs.get("max_tokens", self.config.get("max_tokens", 8000)),
                temperature=kwargs.get("temperature", self.config.get("temperature", 0.7)),
                system=system or "",
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            self.logger.error(f"Anthropic API error: {e}")
            raise
    
    async def _call_google(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        **kwargs
    ) -> str:
        """Call Google Gemini API"""
        try:
            import google.generativeai as genai
            
            if not self._client:
                api_key = os.getenv("GOOGLE_API_KEY")
                genai.configure(api_key=api_key)
                self._client = genai.GenerativeModel(
                    self.config.get("model", "gemini-2.0-flash-001")
                )
            
            # Convert messages to Gemini format
            prompt = ""
            if system:
                prompt += f"System: {system}\n\n"
            
            for msg in messages:
                role = "User" if msg["role"] == "user" else "Assistant"
                prompt += f"{role}: {msg['content']}\n\n"
            
            response = await self._client.generate_content_async(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=kwargs.get("temperature", self.config.get("temperature", 0.7)),
                    max_output_tokens=kwargs.get("max_tokens", 8000),
                )
            )
            
            return response.text
            
        except Exception as e:
            self.logger.error(f"Google API error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if LLM API is accessible"""
        try:
            test_response = await self.execute(
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10
            )
            return bool(test_response)
        except:
            return False


class WebSearchMCP(BaseMCP):
    """MCP for web search (Tavily, Google)"""
    
    def __init__(self, config: Dict[str, Any], provider: str = "tavily"):
        super().__init__(config)
        self.provider = provider
        self._client = None
    
    async def execute(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Execute web search"""
        if self.provider == "tavily":
            return await self._search_tavily(query, max_results)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    async def _search_tavily(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search using Tavily API"""
        try:
            from tavily import TavilyClient
            
            if not self._client:
                api_key = os.getenv("TAVILY_API_KEY")
                self._client = TavilyClient(api_key=api_key)
            
            response = self._client.search(query=query, max_results=max_results)
            return response.get("results", [])
            
        except Exception as e:
            self.logger.error(f"Tavily search error: {e}")
            return []
    
    async def health_check(self) -> bool:
        """Check if search API is accessible"""
        try:
            results = await self.execute("test query", max_results=1)
            return len(results) > 0
        except:
            return False


class ArxivMCP(BaseMCP):
    """MCP for arXiv academic paper search"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._client = None
    
    async def execute(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search arXiv for papers"""
        try:
            import arxiv
            
            if not self._client:
                self._client = arxiv.Client()
            
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = []
            for paper in self._client.results(search):
                results.append({
                    "title": paper.title,
                    "authors": [author.name for author in paper.authors],
                    "summary": paper.summary,
                    "pdf_url": paper.pdf_url,
                    "published": paper.published.isoformat(),
                    "arxiv_id": paper.entry_id.split("/")[-1]
                })
            
            return results
            
        except Exception as e:
            self.logger.error(f"arXiv search error: {e}")
            return []
    
    async def health_check(self) -> bool:
        """Check if arXiv API is accessible"""
        try:
            results = await self.execute("machine learning", max_results=1)
            return len(results) > 0
        except:
            return False


class PDFParserMCP(BaseMCP):
    """MCP for parsing PDF documents"""
    
    async def execute(self, pdf_path: str) -> str:
        """Extract text from PDF"""
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(pdf_path)
            text = ""
            
            for page in doc:
                text += page.get_text()
            
            doc.close()
            return text
            
        except Exception as e:
            self.logger.error(f"PDF parsing error: {e}")
            return ""
    
    async def health_check(self) -> bool:
        """Check if PDF parser is available"""
        try:
            import fitz
            return True
        except:
            return False


class VectorDBMCP(BaseMCP):
    """MCP for Vector Database operations (ChromaDB)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._client = None
        self._collections = {}
    
    async def initialize(self):
        """Initialize ChromaDB client"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            persist_dir = self.config.get("persist_directory", "./data/vector_db")
            os.makedirs(persist_dir, exist_ok=True)
            
            self._client = chromadb.PersistentClient(
                path=persist_dir,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create default collection
            collection_name = self.config.get("collection", "linguistic_bridges_memory")
            self._collections[collection_name] = self._client.get_or_create_collection(
                name=collection_name
            )
            
            self.logger.info(f"Vector DB initialized: {persist_dir}")
            
        except Exception as e:
            self.logger.error(f"Vector DB initialization error: {e}")
            raise
    
    async def add(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
        collection_name: str = "linguistic_bridges_memory"
    ):
        """Add documents to collection"""
        if collection_name not in self._collections:
            self._collections[collection_name] = self._client.get_or_create_collection(
                name=collection_name
            )
        
        if ids is None:
            ids = [f"doc_{i}_{hash(doc)}" for i, doc in enumerate(documents)]
        
        self._collections[collection_name].add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    async def query(
        self,
        query_texts: List[str],
        n_results: int = 5,
        collection_name: str = "linguistic_bridges_memory",
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Query collection for similar documents"""
        if collection_name not in self._collections:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
        
        results = self._collections[collection_name].query(
            query_texts=query_texts,
            n_results=n_results,
            where=where
        )
        
        return results
    
    async def execute(self, operation: str, **kwargs) -> Any:
        """Execute generic vector DB operation"""
        if operation == "add":
            return await self.add(**kwargs)
        elif operation == "query":
            return await self.query(**kwargs)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    async def health_check(self) -> bool:
        """Check if Vector DB is accessible"""
        try:
            return self._client is not None
        except:
            return False


class MCPManager:
    """Central manager for all MCP connections"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger("MCPManager")
        self.mcps: Dict[str, BaseMCP] = {}
        
    async def initialize(self):
        """Initialize all MCP connections"""
        self.logger.info("Initializing MCP connections...")
        
        # LLM Providers
        self.mcps["llm_anthropic"] = LLMProviderMCP(
            self.config.get("apis", {}).get("anthropic", {}),
            provider="anthropic"
        )
        self.mcps["llm_google"] = LLMProviderMCP(
            self.config.get("apis", {}).get("google", {}),
            provider="google"
        )
        
        # Web Search
        search_provider = self.config.get("apis", {}).get("search", {}).get("provider", "tavily")
        self.mcps["web_search"] = WebSearchMCP(
            self.config.get("apis", {}).get("search", {}),
            provider=search_provider
        )
        
        # Academic Search
        self.mcps["arxiv"] = ArxivMCP(
            self.config.get("apis", {}).get("arxiv", {})
        )
        
        # PDF Parser
        self.mcps["pdf_parser"] = PDFParserMCP({})
        
        # Vector Database
        self.mcps["vector_db"] = VectorDBMCP(
            self.config.get("vector_db", {})
        )
        await self.mcps["vector_db"].initialize()
        
        # Git and GitHub
        from mcps.git_mcp import GitMCP, GitHubMCP
        
        git_config = self.config.get("git", {})
        self.mcps["git"] = GitMCP(git_config)
        await self.mcps["git"].initialize()
        
        github_config = self.config.get("github", {})
        self.mcps["github"] = GitHubMCP(github_config)
        
        self.logger.info(f"Initialized {len(self.mcps)} MCP connections")
    
    def get_mcp(self, name: str) -> BaseMCP:
        """Get MCP by name"""
        if name not in self.mcps:
            raise ValueError(f"MCP not found: {name}")
        return self.mcps[name]
    
    async def health_check_all(self) -> Dict[str, bool]:
        """Check health of all MCPs"""
        results = {}
        for name, mcp in self.mcps.items():
            try:
                results[name] = await mcp.health_check()
            except Exception as e:
                self.logger.error(f"Health check failed for {name}: {e}")
                results[name] = False
        return results
