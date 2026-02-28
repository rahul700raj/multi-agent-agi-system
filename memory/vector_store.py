"""
Vector Store - Long-term memory with semantic search
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from loguru import logger
import json
from datetime import datetime


class VectorStore:
    """
    Vector database interface for semantic memory storage and retrieval.
    
    Supports:
    - FAISS (local, fast)
    - Pinecone (cloud, scalable)
    - Chroma (local, persistent)
    """
    
    def __init__(
        self,
        backend: str = "faiss",
        dimension: int = 1536,
        index_type: str = "IVF",
        persist_directory: Optional[str] = None
    ):
        self.backend = backend
        self.dimension = dimension
        self.index_type = index_type
        self.persist_directory = persist_directory
        
        self.index = None
        self.metadata_store: Dict[str, Dict[str, Any]] = {}
        self.id_counter = 0
        
        self._initialize_backend()
        
        logger.info(f"VectorStore initialized with {backend} backend")
    
    def _initialize_backend(self) -> None:
        """Initialize vector database backend"""
        if self.backend == "faiss":
            self._initialize_faiss()
        elif self.backend == "pinecone":
            self._initialize_pinecone()
        elif self.backend == "chroma":
            self._initialize_chroma()
        else:
            raise ValueError(f"Unsupported backend: {self.backend}")
    
    def _initialize_faiss(self) -> None:
        """Initialize FAISS index"""
        try:
            import faiss
            
            if self.index_type == "IVF":
                # IVF index for large-scale search
                quantizer = faiss.IndexFlatL2(self.dimension)
                self.index = faiss.IndexIVFFlat(
                    quantizer,
                    self.dimension,
                    100  # number of clusters
                )
                self.index.nprobe = 10
            else:
                # Flat index for exact search
                self.index = faiss.IndexFlatL2(self.dimension)
            
            logger.info("FAISS index initialized")
            
        except ImportError:
            logger.warning("FAISS not installed, using in-memory fallback")
            self.index = None
    
    def _initialize_pinecone(self) -> None:
        """Initialize Pinecone index"""
        try:
            import pinecone
            import os
            
            api_key = os.getenv("PINECONE_API_KEY")
            environment = os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp")
            
            if not api_key:
                raise ValueError("PINECONE_API_KEY not set")
            
            pinecone.init(api_key=api_key, environment=environment)
            
            index_name = "agi-memory"
            
            if index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    index_name,
                    dimension=self.dimension,
                    metric="cosine"
                )
            
            self.index = pinecone.Index(index_name)
            logger.info("Pinecone index initialized")
            
        except ImportError:
            logger.warning("Pinecone not installed")
            self.index = None
    
    def _initialize_chroma(self) -> None:
        """Initialize ChromaDB"""
        try:
            import chromadb
            
            if self.persist_directory:
                client = chromadb.PersistentClient(path=self.persist_directory)
            else:
                client = chromadb.Client()
            
            self.index = client.get_or_create_collection(
                name="agi_memory",
                metadata={"dimension": self.dimension}
            )
            
            logger.info("ChromaDB initialized")
            
        except ImportError:
            logger.warning("ChromaDB not installed")
            self.index = None
    
    def store(
        self,
        text: str,
        embedding: Optional[np.ndarray] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store text with embedding in vector database.
        
        Args:
            text: Text content to store
            embedding: Pre-computed embedding (if None, will generate)
            metadata: Additional metadata
            
        Returns:
            Unique ID of stored item
        """
        if embedding is None:
            embedding = self._generate_embedding(text)
        
        item_id = f"mem_{self.id_counter}"
        self.id_counter += 1
        
        # Store metadata
        self.metadata_store[item_id] = {
            "text": text,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat(),
            "id": item_id
        }
        
        # Store in vector index
        if self.backend == "faiss" and self.index is not None:
            self._store_faiss(item_id, embedding)
        elif self.backend == "pinecone" and self.index is not None:
            self._store_pinecone(item_id, embedding, metadata)
        elif self.backend == "chroma" and self.index is not None:
            self._store_chroma(item_id, text, embedding, metadata)
        
        logger.debug(f"Stored item: {item_id}")
        
        return item_id
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Semantic search for similar items.
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Metadata filters
            
        Returns:
            List of matching items with scores
        """
        query_embedding = self._generate_embedding(query)
        
        if self.backend == "faiss" and self.index is not None:
            results = self._search_faiss(query_embedding, top_k)
        elif self.backend == "pinecone" and self.index is not None:
            results = self._search_pinecone(query_embedding, top_k, filter_metadata)
        elif self.backend == "chroma" and self.index is not None:
            results = self._search_chroma(query, top_k, filter_metadata)
        else:
            # Fallback: simple similarity search
            results = self._fallback_search(query_embedding, top_k)
        
        return results
    
    def _store_faiss(self, item_id: str, embedding: np.ndarray) -> None:
        """Store in FAISS index"""
        if not self.index.is_trained:
            # Train index if needed (for IVF)
            if hasattr(self.index, 'train'):
                dummy_data = np.random.random((1000, self.dimension)).astype('float32')
                self.index.train(dummy_data)
        
        self.index.add(embedding.reshape(1, -1).astype('float32'))
    
    def _store_pinecone(
        self,
        item_id: str,
        embedding: np.ndarray,
        metadata: Optional[Dict[str, Any]]
    ) -> None:
        """Store in Pinecone"""
        self.index.upsert(
            vectors=[(item_id, embedding.tolist(), metadata or {})]
        )
    
    def _store_chroma(
        self,
        item_id: str,
        text: str,
        embedding: np.ndarray,
        metadata: Optional[Dict[str, Any]]
    ) -> None:
        """Store in ChromaDB"""
        self.index.add(
            ids=[item_id],
            embeddings=[embedding.tolist()],
            documents=[text],
            metadatas=[metadata or {}]
        )
    
    def _search_faiss(
        self,
        query_embedding: np.ndarray,
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Search FAISS index"""
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1).astype('float32'),
            top_k
        )
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.metadata_store):
                item_id = list(self.metadata_store.keys())[idx]
                item = self.metadata_store[item_id].copy()
                item["score"] = float(1 / (1 + distance))  # Convert distance to similarity
                results.append(item)
        
        return results
    
    def _search_pinecone(
        self,
        query_embedding: np.ndarray,
        top_k: int,
        filter_metadata: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Search Pinecone index"""
        response = self.index.query(
            vector=query_embedding.tolist(),
            top_k=top_k,
            filter=filter_metadata,
            include_metadata=True
        )
        
        results = []
        for match in response.matches:
            results.append({
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            })
        
        return results
    
    def _search_chroma(
        self,
        query: str,
        top_k: int,
        filter_metadata: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Search ChromaDB"""
        response = self.index.query(
            query_texts=[query],
            n_results=top_k,
            where=filter_metadata
        )
        
        results = []
        for i in range(len(response['ids'][0])):
            results.append({
                "id": response['ids'][0][i],
                "text": response['documents'][0][i],
                "score": 1 - response['distances'][0][i],  # Convert distance to similarity
                "metadata": response['metadatas'][0][i]
            })
        
        return results
    
    def _fallback_search(
        self,
        query_embedding: np.ndarray,
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Fallback similarity search using numpy"""
        results = []
        
        for item_id, item_data in self.metadata_store.items():
            # Generate embedding for stored text
            text_embedding = self._generate_embedding(item_data["text"])
            
            # Calculate cosine similarity
            similarity = np.dot(query_embedding, text_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(text_embedding)
            )
            
            item_copy = item_data.copy()
            item_copy["score"] = float(similarity)
            results.append(item_copy)
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def _generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for text.
        
        In production, use:
        - OpenAI text-embedding-ada-002
        - Sentence Transformers
        - Custom embedding model
        """
        # Placeholder: random embedding
        # In production: use actual embedding model
        np.random.seed(hash(text) % (2**32))
        embedding = np.random.randn(self.dimension)
        embedding = embedding / np.linalg.norm(embedding)  # Normalize
        
        return embedding
    
    def delete(self, item_id: str) -> bool:
        """Delete item from vector store"""
        if item_id in self.metadata_store:
            del self.metadata_store[item_id]
            logger.debug(f"Deleted item: {item_id}")
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        return {
            "backend": self.backend,
            "total_items": len(self.metadata_store),
            "dimension": self.dimension,
            "index_type": self.index_type
        }
    
    def save(self, filepath: str) -> None:
        """Save metadata to file"""
        with open(filepath, 'w') as f:
            json.dump(self.metadata_store, f, indent=2)
        logger.info(f"Saved metadata to {filepath}")
    
    def load(self, filepath: str) -> None:
        """Load metadata from file"""
        with open(filepath, 'r') as f:
            self.metadata_store = json.load(f)
        self.id_counter = len(self.metadata_store)
        logger.info(f"Loaded metadata from {filepath}")
