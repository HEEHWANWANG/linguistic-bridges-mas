# Designer Agent Implementation Guide

**Purpose**: Practical code examples and integration instructions
**Status**: Ready for Forge Guild implementation (Q1 2026)

---

## Part 1: Designer Agent Class Structure

### 1.1 Basic Implementation

```python
# agents/designer_agent.py

from agents.base_agent import BaseAgent
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime

class DesignSpecialty(Enum):
    """Designer agent specialties"""
    NARRATIVE = "narrative"           # Story-driven visuals
    MOOD = "mood"                     # Emotional/atmospheric
    STYLE = "style"                   # Aesthetic coherence
    CONCEPTUAL = "conceptual"         # Abstract/metaphorical
    COMMERCIAL = "commercial"         # Market appeal


@dataclass
class ReferenceImage:
    """Structured reference image representation"""
    url: str
    title: str
    source: str                        # unsplash, pexels, pinterest, behance
    relevance_score: float             # 0.0-1.0
    novelty_score: float               # 0.0-1.0
    quality_score: float               # 0.0-1.0
    design_patterns: Dict[str, Any]   # Extracted patterns
    license: str                       # CC0, CC-BY, etc.
    upload_date: datetime
    view_count: int


class DesignerAgent(BaseAgent):
    """
    Designer Agent orchestrates visual design through reference discovery
    """

    def __init__(
        self,
        name: str,
        agent_id: str,
        specialty: DesignSpecialty,
        config: Dict[str, Any],
        shared_memory: Any,
        mcp_manager: Any
    ):
        super().__init__(name, agent_id, config, shared_memory)
        self.specialty = specialty
        self.mcp_manager = mcp_manager
        self.logger = logging.getLogger(f"DesignerAgent-{specialty.value}")

        # Initialize sub-components
        self.reference_searcher = ReferenceSearcher(mcp_manager)
        self.design_analyzer = DesignAnalyzer(mcp_manager)
        self.prompt_generator = PromptGenerator(mcp_manager)
        self.image_generator = ImageGenerator(mcp_manager)
        self.evaluator = DesignEvaluator(mcp_manager)

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Route task to appropriate handler"""
        task_type = task.get("type")

        handlers = {
            "search_references": self.search_references,
            "analyze_design": self.analyze_design_patterns,
            "generate_guidelines": self.generate_design_guidelines,
            "generate_images": self.generate_images,
            "evaluate_designs": self.evaluate_and_iterate
        }

        handler = handlers.get(task_type)
        if not handler:
            return {"status": "error", "message": f"Unknown task: {task_type}"}

        try:
            return await handler(task)
        except Exception as e:
            self.logger.error(f"Task execution failed: {e}")
            return {"status": "error", "message": str(e)}

    async def search_references(
        self,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Search for novel reference images"""
        self.logger.info(f"🔍 Searching references (specialty: {self.specialty.value})")

        narrative = task.get("narrative")
        mood = task.get("mood")
        num_references = task.get("num_references", 5)

        # Generate search queries for this specialty
        queries = await self._generate_queries(narrative, mood)

        # Search across platforms
        self.logger.info(f"Searching with queries: {queries}")
        all_results = await self.reference_searcher.search_multi_platform(
            queries=queries,
            platforms=["unsplash", "pexels"],
            limit_per_query=15
        )

        # Filter for copyright compliance
        filtered = [r for r in all_results if r.license in ["CC0", "CC-BY"]]
        self.logger.info(f"Filtered to {len(filtered)} copyright-compliant results")

        # Score for novelty
        scored = await self._score_novelty(filtered, queries)

        # Select diverse top references
        references = scored[:num_references]

        self.logger.info(f"✅ Selected {len(references)} novel references")

        return {
            "status": "success",
            "references": references,
            "count": len(references),
            "queries_used": queries
        }

    async def analyze_design_patterns(
        self,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract design patterns from references"""
        self.logger.info("📊 Analyzing design patterns...")

        references = task.get("references", [])

        patterns = {
            "color_palettes": [],
            "compositions": [],
            "moods": [],
            "technical": [],
            "aesthetics": []
        }

        for ref in references:
            analysis = await self.design_analyzer.analyze_image(ref.url)
            patterns["color_palettes"].append(analysis.get("colors"))
            patterns["compositions"].append(analysis.get("composition"))
            patterns["moods"].append(analysis.get("mood"))
            patterns["technical"].append(analysis.get("technical"))
            patterns["aesthetics"].append(analysis.get("aesthetic"))

        # Synthesize patterns
        synthesized = await self._synthesize_patterns(patterns)

        self.logger.info("✅ Design patterns analyzed")

        return {
            "status": "success",
            "patterns": synthesized,
            "references_analyzed": len(references)
        }

    async def generate_design_guidelines(
        self,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive design guidelines"""
        self.logger.info("📝 Generating design guidelines...")

        references = task.get("references", [])
        patterns = task.get("patterns", {})
        narrative = task.get("narrative")
        mood = task.get("mood")

        guidelines = {
            "visual_identity": await self._create_visual_identity(
                patterns, narrative, mood
            ),
            "composition_rules": await self._create_composition_rules(patterns),
            "color_strategy": await self._create_color_strategy(patterns),
            "forbidden_elements": await self._identify_forbidden(patterns),
            "encouraged_elements": await self._identify_encouraged(patterns),
            "generation_prompts": await self._generate_prompts(
                patterns, narrative, mood, references
            )
        }

        self.logger.info("✅ Design guidelines created")

        return {
            "status": "success",
            "guidelines": guidelines,
            "specialty": self.specialty.value
        }

    async def generate_images(
        self,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate images guided by reference patterns"""
        self.logger.info("🤖 Generating images...")

        guidelines = task.get("guidelines")
        references = task.get("references", [])
        sections = task.get("sections", [])
        num_per_section = task.get("num_per_section", 3)

        generated = {}

        for section in sections:
            section_id = section.get("id")
            self.logger.info(f"Generating images for section: {section_id}")

            # Generate prompts for this section
            prompts = await self.prompt_generator.generate_for_section(
                guidelines=guidelines,
                section=section,
                specialty=self.specialty.value,
                count=num_per_section
            )

            # Generate images
            images = []
            for prompt in prompts:
                img = await self.image_generator.generate(
                    prompt=prompt.get("positive"),
                    negative_prompt=prompt.get("negative"),
                    guidance=guidelines,
                    references=references
                )
                images.append(img)

            generated[section_id] = {
                "section": section,
                "prompts": prompts,
                "images": images
            }

        self.logger.info(f"✅ Generated images for {len(sections)} sections")

        return {
            "status": "success",
            "generated_images": generated,
            "sections_processed": len(sections)
        }

    async def evaluate_and_iterate(
        self,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate images and iteratively refine"""
        self.logger.info("✅ Evaluating images...")

        images = task.get("images", {})
        guidelines = task.get("guidelines")
        max_iterations = task.get("max_iterations", 3)

        history = []

        for iteration in range(max_iterations):
            self.logger.info(f"Evaluation iteration {iteration + 1}/{max_iterations}")

            # Evaluate all images
            evaluations = {}
            for section_id, section_data in images.items():
                evals = await self.evaluator.evaluate_section(
                    images=section_data.get("images"),
                    guidelines=guidelines,
                    section_id=section_id
                )
                evaluations[section_id] = evals

            # Calculate average quality
            all_scores = [
                e.get("quality_score", 0)
                for section_evals in evaluations.values()
                for e in section_evals
            ]
            avg_quality = sum(all_scores) / len(all_scores) if all_scores else 0

            history.append({
                "iteration": iteration + 1,
                "avg_quality": avg_quality,
                "evaluations": evaluations
            })

            self.logger.info(f"Quality score: {avg_quality:.2f}")

            # Check if acceptable
            if avg_quality >= 0.80:
                self.logger.info("✅ Acceptable quality reached")
                break

            # Refine if needed and iterations remain
            if iteration < max_iterations - 1:
                images = await self._refine_and_regenerate(
                    evaluations, images, guidelines
                )

        return {
            "status": "success",
            "final_images": images,
            "evaluation_history": history,
            "final_quality_score": avg_quality
        }

    # Helper methods

    async def _generate_queries(
        self,
        narrative: Dict[str, Any],
        mood: Dict[str, Any]
    ) -> List[str]:
        """Generate search queries based on specialty"""

        if self.specialty == DesignSpecialty.NARRATIVE:
            return [
                f"{narrative.get('main_character', 'character')} {narrative.get('setting', 'place')}",
                f"{narrative.get('central_conflict', 'conflict')} cinematic",
                f"{narrative.get('theme', 'story')} visual metaphor",
                f"dramatic {narrative.get('emotional_arc', 'journey')}"
            ]

        elif self.specialty == DesignSpecialty.MOOD:
            return [
                f"{mood.get('primary_emotion', 'emotion')} atmosphere",
                f"{mood.get('color_scheme', 'blue')} mood lighting",
                f"{mood.get('energy_level', 'calm')} abstract",
                f"{mood.get('tone', 'tone')} environment"
            ]

        elif self.specialty == DesignSpecialty.STYLE:
            return [
                f"{mood.get('visual_style', 'minimalist')} aesthetic",
                f"contemporary {mood.get('design_trend', 'design')}",
                f"{mood.get('art_movement', 'modern')} visual",
                f"{mood.get('style_reference', 'reference')} inspiration"
            ]

        elif self.specialty == DesignSpecialty.CONCEPTUAL:
            return [
                f"abstract {narrative.get('theme', 'concept')}",
                f"surreal {mood.get('primary_emotion', 'emotion')} visualization",
                f"metaphorical {narrative.get('central_conflict', 'concept')}",
                f"experimental conceptual art"
            ]

        elif self.specialty == DesignSpecialty.COMMERCIAL:
            return [
                f"trending {mood.get('genre', 'pop')} design 2024",
                f"viral aesthetic {narrative.get('theme', 'theme')}",
                f"instagram popular {mood.get('color_scheme', 'color')} visual",
                f"modern commercial design {narrative.get('target_audience', 'youth')}"
            ]

        return []

    async def _score_novelty(
        self,
        results: List[Dict[str, Any]],
        queries: List[str]
    ) -> List[ReferenceImage]:
        """Score images for novelty"""

        scored = []

        for result in results:
            # Recency: newer images preferred
            age_days = (datetime.now() - result.get("upload_date", datetime.now())).days
            recency = max(0, 1.0 - (age_days / 365))  # Decay over 1 year

            # Rarity: unpopular images preferred
            view_count = result.get("view_count", 1)
            rarity = 1.0 / (1.0 + view_count / 10000)  # Logarithmic scale

            # Uniqueness: different from query terms (LLM semantic distance)
            uniqueness = result.get("semantic_distance", 0.5)

            # Quality: composition and technical quality
            quality = result.get("quality_score", 0.5)

            # Combined novelty score
            novelty = (
                recency * 0.15 +
                rarity * 0.25 +
                uniqueness * 0.25 +
                quality * 0.35
            )

            ref_img = ReferenceImage(
                url=result.get("url"),
                title=result.get("title"),
                source=result.get("source"),
                relevance_score=result.get("relevance", 0.5),
                novelty_score=novelty,
                quality_score=quality,
                design_patterns=result.get("patterns", {}),
                license=result.get("license"),
                upload_date=result.get("upload_date", datetime.now()),
                view_count=view_count
            )
            scored.append(ref_img)

        # Sort by novelty score
        scored.sort(key=lambda x: x.novelty_score, reverse=True)
        return scored

    async def _synthesize_patterns(
        self,
        patterns: Dict[str, List[Any]]
    ) -> Dict[str, Any]:
        """Synthesize patterns from multiple references"""

        return {
            "dominant_colors": self._extract_dominant_colors(patterns["color_palettes"]),
            "common_compositions": self._extract_common_compositions(patterns["compositions"]),
            "shared_mood": self._extract_shared_mood(patterns["moods"]),
            "technical_consensus": self._extract_technical_consensus(patterns["technical"]),
            "aesthetic_style": self._extract_aesthetic_consensus(patterns["aesthetics"])
        }

    async def _create_visual_identity(
        self,
        patterns: Dict[str, Any],
        narrative: Dict[str, Any],
        mood: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create cohesive visual identity from patterns"""

        return {
            "primary_aesthetic": patterns.get("aesthetic_style", "contemporary"),
            "color_scheme": patterns.get("dominant_colors", []),
            "mood_descriptors": [
                mood.get("primary_emotion"),
                mood.get("secondary_emotion"),
                mood.get("tone")
            ],
            "visual_references": [
                narrative.get("visual_style"),
                mood.get("style_inspiration")
            ]
        }

    async def _create_composition_rules(
        self,
        patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract composition guidelines"""

        return {
            "layout_preference": patterns.get("common_compositions", {}).get("preferred_layout"),
            "focal_point_guidance": patterns.get("common_compositions", {}).get("focal_point"),
            "depth_strategy": patterns.get("common_compositions", {}).get("depth"),
            "perspective": patterns.get("common_compositions", {}).get("perspective")
        }

    async def _create_color_strategy(
        self,
        patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract color guidelines"""

        return {
            "primary_colors": patterns.get("dominant_colors", {}).get("primary", []),
            "accent_colors": patterns.get("dominant_colors", {}).get("accent", []),
            "saturation_level": patterns.get("dominant_colors", {}).get("saturation", "medium"),
            "brightness_level": patterns.get("dominant_colors", {}).get("brightness", "medium")
        }

    async def _identify_forbidden(self, patterns: Dict[str, Any]) -> List[str]:
        """Identify clichéd elements to avoid"""
        return [
            "generic sunset",
            "overused bokeh",
            "stock photo aesthetic",
            "Instagram filter look",
            "clichéd composition"
        ]

    async def _identify_encouraged(self, patterns: Dict[str, Any]) -> List[str]:
        """Identify elements that work well"""
        return [
            "unique perspective",
            "natural lighting",
            "environmental storytelling",
            "subtle emotion in details",
            "unexpected juxtaposition"
        ]

    async def _generate_prompts(
        self,
        patterns: Dict[str, Any],
        narrative: Dict[str, Any],
        mood: Dict[str, Any],
        references: List[ReferenceImage]
    ) -> Dict[str, Any]:
        """Create detailed generation prompts"""

        return {
            "primary": f"""Create a {mood.get('visual_style', 'cinematic')} image of {narrative.get('central_idea', 'scene')}
            Color scheme: {patterns.get('dominant_colors', {}).get('primary', 'natural')}
            Mood: {mood.get('primary_emotion', 'neutral')}
            Style: {patterns.get('aesthetic_style', 'contemporary')}
            Composition: {patterns.get('common_compositions', {}).get('layout', 'balanced')}""",

            "negative_prompt": "cliché, generic, stock photo, artificial, overused",

            "style_modifiers": [
                "professional photography",
                f"{mood.get('lighting_style', 'natural')} lighting",
                f"{mood.get('camera_style', 'standard')} perspective"
            ],

            "reference_guidance": f"Reference style from: {', '.join([r.title for r in references[:3]])}"
        }

    async def _refine_and_regenerate(
        self,
        evaluations: Dict[str, Any],
        current_images: Dict[str, Any],
        guidelines: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Refine prompts based on evaluation feedback"""

        # Analyze which sections scored low
        low_performing = {
            section_id: evals
            for section_id, evals in evaluations.items()
            if any(e.get("quality_score", 0) < 0.75 for e in evals)
        }

        # Refine prompts for low-performing sections
        for section_id in low_performing:
            feedback = evaluations[section_id]
            current_images[section_id]["feedback"] = feedback
            # Prompts would be regenerated with refinements

        return current_images

    # Helper analysis methods
    def _extract_dominant_colors(self, palettes: List[List[str]]) -> Dict[str, Any]:
        """Extract most common colors from reference palettes"""
        # Implementation: analyze color frequency, return dominant
        pass

    def _extract_common_compositions(self, compositions: List[Dict]) -> Dict[str, Any]:
        """Extract most common composition patterns"""
        pass

    def _extract_shared_mood(self, moods: List[Dict]) -> Dict[str, Any]:
        """Extract shared emotional tone"""
        pass

    def _extract_technical_consensus(self, technical: List[Dict]) -> Dict[str, Any]:
        """Extract agreed-upon technical characteristics"""
        pass

    def _extract_aesthetic_consensus(self, aesthetics: List[Dict]) -> Dict[str, Any]:
        """Extract shared aesthetic style"""
        pass
```

---

## Part 2: Integration with Supervisor

```python
# agents/supervisor.py - Add to existing class

async def _coordinate_visual_generation_phase(
    self,
    research_result: Dict[str, Any],
    implementation_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Phase 2.5: Visual Design & Reference-Driven Generation
    Uses Designer Agents to search references and guide image generation
    """

    self.logger.info("🎨 Phase 2.5: Visual Design with Designer Agents")

    try:
        # Extract narrative and mood from previous phases
        narrative = research_result.get("song_narrative", {})
        mood = implementation_result.get("emotion_trajectory", {})
        sections = narrative.get("sections", [])

        # Initialize Designer Agents (one per specialty)
        designers = [
            DesignerAgent(
                name=f"designer_narrative",
                agent_id=f"dag_narrative_{self.agent_id}",
                specialty=DesignSpecialty.NARRATIVE,
                config=self.config,
                shared_memory=self.shared_memory,
                mcp_manager=self.mcp_manager
            ),
            DesignerAgent(
                name=f"designer_mood",
                agent_id=f"dag_mood_{self.agent_id}",
                specialty=DesignSpecialty.MOOD,
                config=self.config,
                shared_memory=self.shared_memory,
                mcp_manager=self.mcp_manager
            ),
            DesignerAgent(
                name=f"designer_style",
                agent_id=f"dag_style_{self.agent_id}",
                specialty=DesignSpecialty.STYLE,
                config=self.config,
                shared_memory=self.shared_memory,
                mcp_manager=self.mcp_manager
            ),
        ]

        design_results = {}

        # Run each Designer Agent in parallel
        for designer in designers:
            self.logger.info(f"Running {designer.specialty.value} designer...")

            # Task 1: Search references
            search_task = {
                "type": "search_references",
                "narrative": narrative,
                "mood": mood,
                "num_references": 5
            }
            search_result = await designer.execute_task(search_task)

            if search_result.get("status") != "success":
                self.logger.warning(f"Reference search failed for {designer.specialty.value}")
                continue

            references = search_result.get("references", [])

            # Task 2: Analyze design patterns
            analyze_task = {
                "type": "analyze_design",
                "references": references
            }
            analysis_result = await designer.execute_task(analyze_task)

            patterns = analysis_result.get("patterns", {})

            # Task 3: Generate design guidelines
            guidelines_task = {
                "type": "generate_guidelines",
                "references": references,
                "patterns": patterns,
                "narrative": narrative,
                "mood": mood
            }
            guidelines_result = await designer.execute_task(guidelines_task)

            guidelines = guidelines_result.get("guidelines", {})

            # Task 4: Generate images for all sections
            image_task = {
                "type": "generate_images",
                "guidelines": guidelines,
                "references": references,
                "sections": sections,
                "num_per_section": 3
            }
            images_result = await designer.execute_task(image_task)

            # Task 5: Evaluate and iterate
            eval_task = {
                "type": "evaluate_designs",
                "images": images_result.get("generated_images", {}),
                "guidelines": guidelines,
                "max_iterations": 3
            }
            eval_result = await designer.execute_task(eval_task)

            design_results[designer.specialty.value] = {
                "references": references,
                "patterns": patterns,
                "guidelines": guidelines,
                "generated_images": images_result.get("generated_images", {}),
                "evaluation": eval_result,
                "quality_score": eval_result.get("final_quality_score", 0)
            }

        # Task 6: Synthesize designs from multiple agents
        final_designs = await self._synthesize_designer_outputs(design_results)

        self.logger.info("✅ Visual generation phase complete")

        return {
            "success": True,
            "design_results": design_results,
            "final_designs": final_designs,
            "phases_completed": len(design_results)
        }

    except Exception as e:
        self.logger.error(f"Visual generation phase failed: {e}")
        return {"success": False, "error": str(e)}

async def _synthesize_designer_outputs(
    self,
    design_results: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Synthesize outputs from multiple Designer Agents
    Similar to HarmonicVisuals outlier preservation
    """

    synthesized = {}

    # For each section, select best images from each designer
    all_sections = set()
    for results in design_results.values():
        for section_id in results.get("generated_images", {}).keys():
            all_sections.add(section_id)

    for section_id in all_sections:
        images_by_designer = {}

        for designer_name, results in design_results.items():
            section_images = results.get("generated_images", {}).get(section_id, {})
            images_by_designer[designer_name] = section_images

        # Select best images and preserve creative outliers
        synthesized[section_id] = await self._select_best_images(
            images_by_designer=images_by_designer,
            consensus_weight=0.7,
            outlier_weight=0.3
        )

    return synthesized

async def _select_best_images(
    self,
    images_by_designer: Dict[str, Any],
    consensus_weight: float = 0.7,
    outlier_weight: float = 0.3
) -> Dict[str, Any]:
    """
    Select images: 70% consensus + 30% creative outliers
    """

    # Find images with highest quality across all designers (consensus)
    consensus_images = []
    for designer_name, images in images_by_designer.items():
        best_image = max(
            images.get("images", []),
            key=lambda x: x.get("quality_score", 0)
        )
        consensus_images.append(best_image)

    # Find most creative/unique image (outlier)
    all_images = [
        img
        for images in images_by_designer.values()
        for img in images.get("images", [])
    ]

    creative_image = max(
        all_images,
        key=lambda x: x.get("creativity_score", 0)
    )

    return {
        "consensus_image": consensus_images[0],  # Best quality
        "alternative_images": consensus_images[1:],
        "creative_outlier": creative_image
    }
```

---

## Part 3: Reference Searcher Component

```python
# components/reference_searcher.py

import aiohttp
import asyncio
from typing import List, Dict, Any
from datetime import datetime

class ReferenceSearcher:
    """Search for reference images across multiple platforms"""

    def __init__(self, mcp_manager: Any):
        self.mcp_manager = mcp_manager
        self.unsplash_api_key = mcp_manager.get_config("unsplash_api_key")
        self.pexels_api_key = mcp_manager.get_config("pexels_api_key")

    async def search_multi_platform(
        self,
        queries: List[str],
        platforms: List[str],
        limit_per_query: int = 10
    ) -> List[Dict[str, Any]]:
        """Search across multiple platforms"""

        all_results = []

        # Search in parallel across platforms
        tasks = []
        for platform in platforms:
            for query in queries:
                if platform == "unsplash":
                    tasks.append(self._search_unsplash(query, limit_per_query))
                elif platform == "pexels":
                    tasks.append(self._search_pexels(query, limit_per_query))

        results = await asyncio.gather(*tasks)
        all_results.extend([r for result in results for r in result])

        return all_results

    async def _search_unsplash(
        self,
        query: str,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Search Unsplash API"""

        url = "https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "per_page": limit,
            "client_id": self.unsplash_api_key,
            "order_by": "relevant"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status != 200:
                    return []

                data = await resp.json()
                results = []

                for photo in data.get("results", []):
                    results.append({
                        "url": photo.get("urls", {}).get("regular"),
                        "title": photo.get("description", photo.get("alt_description", "Untitled")),
                        "source": "unsplash",
                        "upload_date": datetime.fromisoformat(
                            photo.get("created_at", "2024-01-01").replace("Z", "+00:00")
                        ),
                        "view_count": photo.get("likes", 0),
                        "license": "CC0",
                        "relevance": 0.7  # Unsplash is relevant by default
                    })

                return results

    async def _search_pexels(
        self,
        query: str,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Search Pexels API"""

        url = "https://api.pexels.com/v1/search"
        params = {
            "query": query,
            "per_page": limit
        }
        headers = {"Authorization": self.pexels_api_key}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as resp:
                if resp.status != 200:
                    return []

                data = await resp.json()
                results = []

                for photo in data.get("photos", []):
                    results.append({
                        "url": photo.get("src", {}).get("original"),
                        "title": f"Photo by {photo.get('photographer', 'Unknown')}",
                        "source": "pexels",
                        "upload_date": datetime.fromisoformat(
                            photo.get("avg_color", "2024-01-01")[:10]
                        ),
                        "view_count": 100,  # Pexels doesn't provide view count
                        "license": "CC0",
                        "relevance": 0.7
                    })

                return results
```

---

## Part 4: Usage Example

```python
# Example: Using Designer Agent in main workflow

async def main():
    # Initialize supervisor with Designer Agents support
    supervisor = SupervisorAgent(
        name="supervisor_harmonic",
        agent_id="sup_001",
        config=config,
        shared_memory=shared_memory,
        mcp_manager=mcp_manager
    )

    # Define project goal
    song_analysis = {
        "title": "Lonely Road",
        "narrative": {
            "main_character": "wanderer",
            "setting": "empty highway",
            "central_conflict": "self-discovery",
            "emotional_arc": "despair to hope"
        },
        "mood": {
            "primary_emotion": "melancholic",
            "energy_level": "medium",
            "color_scheme": "cool blues and warm golds"
        }
    }

    # Run orchestration with visual generation
    result = await supervisor.orchestrate_project(song_analysis)

    # Access generated designs
    designs = result.get("visual_design", {}).get("design_results", {})

    for specialty, design in designs.items():
        print(f"\n{specialty.upper()} DESIGNER:")
        print(f"  References found: {len(design.get('references', []))}")
        print(f"  Quality score: {design.get('quality_score', 0):.2f}")
        print(f"  Images generated: {len(design.get('generated_images', {}))}")
```

---

## Summary

This implementation provides:

✅ **Reference Search**: Multi-platform API integration
✅ **Novelty Filtering**: Avoid clichés while finding inspiring references
✅ **Design Analysis**: Extract patterns from references
✅ **Specialized Designers**: Different agents for different perspectives
✅ **Iterative Refinement**: Improve images based on evaluation
✅ **Multi-Agent Synthesis**: Combine outputs with creative preservation

Ready for Forge Guild implementation in Q1 2026.

