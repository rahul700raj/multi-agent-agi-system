# Quick Start Guide

Get up and running with the Multi-Agent AGI System in 5 minutes!

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- (Optional) Virtual environment tool

### Step 1: Clone Repository

```bash
git clone https://github.com/rahul700raj/multi-agent-agi-system.git
cd multi-agent-agi-system
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Basic installation
pip install -r requirements.txt

# Or install as package
pip install -e .

# For full features (including RL, vector DBs)
pip install -e ".[full]"
```

### Step 4: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

**Required API Keys**:
- `OPENAI_API_KEY`: For LLM capabilities (get from https://platform.openai.com)
- (Optional) `PINECONE_API_KEY`: For cloud vector database

## 📝 Basic Usage

### Example 1: Simple Task

```python
from core.cognitive_loop import CognitiveSystem

# Initialize system
system = CognitiveSystem()

# Solve a task
result = system.solve_task(
    goal="Research recent advances in quantum computing"
)

# View results
print(f"Status: {result['status']}")
print(f"Confidence: {result['confidence']:.1%}")
print(f"Summary: {result['summary']}")
```

### Example 2: With Custom Configuration

```python
from core.cognitive_loop import CognitiveSystem
from agents.researcher import ResearcherAgent
from agents.planner import PlannerAgent

# Initialize with custom agents
system = CognitiveSystem(
    researcher=ResearcherAgent(
        model_name="gpt-4",
        search_depth=5,
        verification_threshold=0.9
    ),
    planner=PlannerAgent(
        planning_horizon=15,
        optimization_method="beam_search"
    ),
    max_iterations=10,
    convergence_threshold=0.85
)

# Solve complex task
result = system.solve_task(
    goal="Design a scalable microservices architecture",
    context={
        "domain": "software_engineering",
        "requirements": ["high_availability", "fault_tolerance"]
    },
    constraints={
        "budget": "moderate",
        "timeline": "3_months"
    }
)
```

### Example 3: Using Memory System

```python
from memory.vector_store import VectorStore

# Initialize vector store
vector_store = VectorStore(
    backend="faiss",  # or "pinecone", "chroma"
    dimension=1536
)

# Store knowledge
vector_store.store(
    text="Quantum computers use qubits that can be in superposition",
    metadata={
        "source": "research_paper",
        "domain": "quantum_computing",
        "confidence": 0.95
    }
)

# Retrieve relevant knowledge
results = vector_store.search(
    query="How do quantum computers work?",
    top_k=5
)

for result in results:
    print(f"Score: {result['score']:.2f}")
    print(f"Text: {result['text']}")
    print(f"Source: {result['metadata']['source']}")
    print()
```

## 🎯 Running Examples

### Pre-built Examples

```bash
# Simple task example
python examples/simple_task.py

# Complex reasoning example
python examples/complex_reasoning.py

# Self-learning demonstration
python examples/self_learning.py
```

## 🔧 Configuration

### Agent Configuration

Edit `config/agents.yaml`:

```yaml
researcher:
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 2000
  search_depth: 3

planner:
  model: "gpt-4"
  planning_horizon: 10
  optimization_method: "beam_search"
```

### Memory Configuration

Edit `config/memory.yaml`:

```yaml
vector_store:
  backend: "faiss"  # Options: faiss, pinecone, chroma
  dimension: 1536
  index_type: "IVF"

episodic_memory:
  max_episodes: 10000
  retention_policy: "importance_based"
```

## 📊 Monitoring & Logging

### Enable Logging

```python
from loguru import logger

# Configure logging
logger.add(
    "logs/agi_system.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO"
)
```

### View Metrics

```python
# Get system performance metrics
metrics = system.get_metrics()

print(f"Total tasks: {metrics['total_tasks']}")
print(f"Success rate: {metrics['metrics']['success_rate']:.1%}")
print(f"Avg iterations: {metrics['metrics']['avg_iterations']:.1f}")
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_agents.py -v

# Run with coverage
pytest --cov=agents --cov=core --cov=memory --cov-report=html
```

### View Coverage Report

```bash
# Open coverage report in browser
open htmlcov/index.html  # On Mac
xdg-open htmlcov/index.html  # On Linux
start htmlcov/index.html  # On Windows
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'agents'`

**Solution**:
```bash
# Install in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### 2. API Key Errors

**Problem**: `OpenAI API key not found`

**Solution**:
```bash
# Set environment variable
export OPENAI_API_KEY="your-key-here"

# Or add to .env file
echo "OPENAI_API_KEY=your-key-here" >> .env
```

#### 3. Memory Issues

**Problem**: `Out of memory when using FAISS`

**Solution**:
```python
# Use smaller index or switch to Pinecone
vector_store = VectorStore(
    backend="pinecone",  # Cloud-based, no local memory
    dimension=1536
)
```

#### 4. Slow Performance

**Problem**: Tasks taking too long

**Solution**:
```python
# Reduce max iterations
system = CognitiveSystem(
    max_iterations=5,  # Default is 10
    convergence_threshold=0.7  # Lower threshold
)

# Use faster model
researcher = ResearcherAgent(
    model_name="gpt-3.5-turbo"  # Faster than gpt-4
)
```

## 📚 Next Steps

### Learn More

1. **Architecture**: Read [ARCHITECTURE.md](../ARCHITECTURE.md) for system design
2. **Research**: Explore [RESEARCH.md](../RESEARCH.md) for advanced topics
3. **Contributing**: See [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute

### Advanced Topics

- **Custom Agents**: Create specialized agents for your domain
- **Tool Integration**: Add custom tools and capabilities
- **Reinforcement Learning**: Train agents with RL
- **Multi-Agent Collaboration**: Coordinate multiple agent instances

### Community

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions and share ideas
- **Discord**: Join our community (coming soon)

## 💡 Tips & Best Practices

### 1. Start Simple

Begin with simple tasks and gradually increase complexity:

```python
# Start with this
result = system.solve_task("What is Python?")

# Then try this
result = system.solve_task(
    "Compare Python and JavaScript for web development"
)

# Finally this
result = system.solve_task(
    "Design a full-stack web application architecture",
    context={"scale": "enterprise", "users": "millions"}
)
```

### 2. Monitor Performance

Track metrics to understand system behavior:

```python
# After each task
metrics = system.get_metrics()
print(f"Success rate: {metrics['metrics']['success_rate']:.1%}")

# Adjust if needed
if metrics['metrics']['success_rate'] < 0.7:
    system.convergence_threshold = 0.6  # Lower threshold
```

### 3. Use Appropriate Models

Choose models based on task complexity:

- **Simple tasks**: `gpt-3.5-turbo` (fast, cheap)
- **Complex reasoning**: `gpt-4` (slower, expensive, better)
- **Research**: `gpt-4` for Researcher, `gpt-3.5-turbo` for others

### 4. Leverage Memory

Store and reuse knowledge:

```python
# Store successful solutions
if result['status'] == 'completed':
    vector_store.store(
        text=f"Solution for {result['goal']}: {result['result']}",
        metadata={"confidence": result['confidence']}
    )

# Retrieve similar past solutions
similar = vector_store.search(new_goal, top_k=3)
```

### 5. Iterate and Improve

The system learns from experience:

```python
# Run multiple tasks
for task in task_list:
    result = system.solve_task(task)
    
    # System automatically improves over time
    # Check improvement
    metrics = system.get_metrics()
    print(f"Current success rate: {metrics['metrics']['success_rate']:.1%}")
```

## 🎓 Learning Resources

### Tutorials

1. **Basic Usage**: `examples/simple_task.py`
2. **Advanced Features**: `examples/complex_reasoning.py`
3. **Memory System**: `examples/memory_usage.py`
4. **Custom Agents**: `examples/custom_agent.py`

### Documentation

- [README.md](../README.md): Project overview
- [ARCHITECTURE.md](../ARCHITECTURE.md): System design
- [RESEARCH.md](../RESEARCH.md): Research directions
- [API Documentation](api/): Detailed API reference

### External Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)

---

**Ready to build AGI?** Start with `examples/simple_task.py` and explore from there! 🚀
