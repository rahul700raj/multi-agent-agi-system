"""
Researcher Agent - Information gathering and knowledge extraction
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, Message
from loguru import logger
import json


class ResearcherAgent(BaseAgent):
    """
    Agent 1: Researcher
    
    Responsibilities:
    - Web search and information gathering
    - Knowledge extraction from sources
    - Fact verification and validation
    - Source credibility assessment
    """
    
    def __init__(
        self,
        agent_id: str = "researcher",
        model_name: str = "gpt-4",
        search_depth: int = 3,
        verification_threshold: float = 0.8
    ):
        super().__init__(
            agent_id=agent_id,
            agent_type="researcher",
            model_name=model_name
        )
        
        self.search_depth = search_depth
        self.verification_threshold = verification_threshold
        self.research_history: List[Dict[str, Any]] = []
    
    def process_message(self, message: Message) -> Optional[Message]:
        """
        Process incoming research requests.
        
        Handles:
        - research_request: Initiate new research
        - verify_fact: Verify specific claim
        - expand_knowledge: Deep dive on topic
        """
        logger.info(f"Researcher processing: {message.message_type}")
        
        if message.message_type == "research_request":
            return self._handle_research_request(message)
        
        elif message.message_type == "verify_fact":
            return self._handle_fact_verification(message)
        
        elif message.message_type == "expand_knowledge":
            return self._handle_knowledge_expansion(message)
        
        return None
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute research task.
        
        Args:
            task: {
                "query": str,
                "depth": int,
                "sources": List[str],
                "verification_required": bool
            }
        
        Returns:
            Research results with findings and sources
        """
        self.update_state(status="researching", current_task=task.get("task_id"))
        
        query = task.get("query", "")
        depth = task.get("depth", self.search_depth)
        
        logger.info(f"Researching: {query}")
        
        # Step 1: Initial search
        search_results = self._perform_search(query, depth)
        
        # Step 2: Extract information
        findings = self._extract_information(search_results)
        
        # Step 3: Verify facts
        if task.get("verification_required", True):
            findings = self._verify_findings(findings)
        
        # Step 4: Assess source credibility
        credibility_scores = self._assess_credibility(search_results)
        
        result = {
            "query": query,
            "findings": findings,
            "sources": search_results,
            "credibility_scores": credibility_scores,
            "confidence": self._calculate_confidence(findings, credibility_scores),
            "timestamp": self.state.last_updated
        }
        
        # Store in research history
        self.research_history.append(result)
        self.add_to_working_memory(result)
        
        self.update_state(status="idle")
        
        return result
    
    def self_evaluate(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate research quality.
        
        Metrics:
        - Information completeness
        - Source diversity
        - Fact verification rate
        - Confidence level
        """
        findings = result.get("findings", [])
        sources = result.get("sources", [])
        confidence = result.get("confidence", 0.0)
        
        evaluation = {
            "completeness": len(findings) / max(len(sources), 1),
            "source_diversity": len(set(s.get("domain") for s in sources)),
            "verification_rate": sum(1 for f in findings if f.get("verified", False)) / max(len(findings), 1),
            "confidence": confidence,
            "quality_score": 0.0
        }
        
        # Calculate overall quality score
        evaluation["quality_score"] = (
            evaluation["completeness"] * 0.3 +
            evaluation["verification_rate"] * 0.4 +
            evaluation["confidence"] * 0.3
        )
        
        logger.info(f"Research quality: {evaluation['quality_score']:.2f}")
        
        return evaluation
    
    def _handle_research_request(self, message: Message) -> Message:
        """Handle research request from planner"""
        query = message.payload.get("query")
        depth = message.payload.get("depth", self.search_depth)
        
        task = {
            "task_id": message.message_id,
            "query": query,
            "depth": depth,
            "verification_required": True
        }
        
        result = self.execute_task(task)
        
        return self.send_message(
            receiver=message.sender,
            message_type="research_complete",
            payload=result,
            priority=message.priority,
            context=message.context
        )
    
    def _handle_fact_verification(self, message: Message) -> Message:
        """Verify specific fact or claim"""
        claim = message.payload.get("claim")
        
        # Search for supporting/contradicting evidence
        evidence = self._perform_search(claim, depth=2)
        
        verification_result = {
            "claim": claim,
            "verified": self._verify_claim(claim, evidence),
            "evidence": evidence,
            "confidence": self._calculate_verification_confidence(evidence)
        }
        
        return self.send_message(
            receiver=message.sender,
            message_type="verification_complete",
            payload=verification_result,
            context=message.context
        )
    
    def _handle_knowledge_expansion(self, message: Message) -> Message:
        """Deep dive into specific topic"""
        topic = message.payload.get("topic")
        aspects = message.payload.get("aspects", [])
        
        expanded_knowledge = {}
        
        for aspect in aspects:
            query = f"{topic} {aspect}"
            results = self._perform_search(query, depth=self.search_depth)
            expanded_knowledge[aspect] = self._extract_information(results)
        
        return self.send_message(
            receiver=message.sender,
            message_type="knowledge_expanded",
            payload={
                "topic": topic,
                "expanded_knowledge": expanded_knowledge
            },
            context=message.context
        )
    
    def _perform_search(self, query: str, depth: int) -> List[Dict[str, Any]]:
        """
        Perform web search (placeholder - integrate with actual search API)
        
        In production, integrate with:
        - DuckDuckGo Search
        - Google Custom Search
        - Wikipedia API
        - ArXiv for research papers
        """
        # Placeholder implementation
        logger.debug(f"Searching: {query} (depth={depth})")
        
        # Simulated search results
        results = [
            {
                "title": f"Result {i+1} for {query}",
                "url": f"https://example.com/result{i+1}",
                "snippet": f"Information about {query}...",
                "domain": f"source{i+1}.com",
                "relevance_score": 0.9 - (i * 0.1)
            }
            for i in range(depth)
        ]
        
        return results
    
    def _extract_information(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract structured information from search results.
        
        Uses LLM to:
        - Identify key facts
        - Extract entities and relationships
        - Summarize findings
        """
        findings = []
        
        for result in search_results:
            # Placeholder - use LLM for actual extraction
            finding = {
                "fact": result.get("snippet"),
                "source": result.get("url"),
                "relevance": result.get("relevance_score", 0.5),
                "verified": False
            }
            findings.append(finding)
        
        return findings
    
    def _verify_findings(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Verify findings through cross-referencing.
        
        Verification methods:
        - Cross-source validation
        - Fact-checking databases
        - Logical consistency checks
        """
        for finding in findings:
            # Placeholder verification logic
            # In production: cross-reference with multiple sources
            finding["verified"] = finding.get("relevance", 0) > self.verification_threshold
        
        return findings
    
    def _verify_claim(self, claim: str, evidence: List[Dict[str, Any]]) -> bool:
        """Verify specific claim against evidence"""
        # Placeholder - use LLM for semantic verification
        supporting_evidence = sum(1 for e in evidence if e.get("relevance_score", 0) > 0.7)
        return supporting_evidence >= 2
    
    def _assess_credibility(self, sources: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Assess source credibility.
        
        Factors:
        - Domain authority
        - Publication date
        - Author credentials
        - Citation count
        """
        credibility = {}
        
        for source in sources:
            domain = source.get("domain", "unknown")
            
            # Placeholder credibility scoring
            # In production: use domain authority APIs, fact-check databases
            score = 0.8 if "edu" in domain or "gov" in domain else 0.6
            
            credibility[domain] = score
        
        return credibility
    
    def _calculate_confidence(
        self,
        findings: List[Dict[str, Any]],
        credibility_scores: Dict[str, float]
    ) -> float:
        """Calculate overall confidence in research results"""
        if not findings:
            return 0.0
        
        verified_count = sum(1 for f in findings if f.get("verified", False))
        avg_credibility = sum(credibility_scores.values()) / max(len(credibility_scores), 1)
        
        confidence = (
            (verified_count / len(findings)) * 0.6 +
            avg_credibility * 0.4
        )
        
        return min(confidence, 1.0)
    
    def _calculate_verification_confidence(self, evidence: List[Dict[str, Any]]) -> float:
        """Calculate confidence in fact verification"""
        if not evidence:
            return 0.0
        
        avg_relevance = sum(e.get("relevance_score", 0) for e in evidence) / len(evidence)
        return avg_relevance
    
    def get_research_summary(self) -> Dict[str, Any]:
        """Get summary of all research conducted"""
        return {
            "total_queries": len(self.research_history),
            "avg_confidence": sum(r.get("confidence", 0) for r in self.research_history) / max(len(self.research_history), 1),
            "recent_research": self.research_history[-5:] if self.research_history else []
        }
