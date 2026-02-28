# Contributing to Multi-Agent AGI System

Thank you for your interest in contributing! This project aims to advance AGI research through collaborative development.

## 🎯 How to Contribute

### 1. Code Contributions

#### Setting Up Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/multi-agent-agi-system.git
cd multi-agent-agi-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

#### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow PEP 8 style guide
   - Add docstrings to all functions/classes
   - Include type hints
   - Write tests for new features

3. **Run tests**
   ```bash
   pytest tests/ -v
   pytest --cov=agents --cov=core --cov=memory
   ```

4. **Format code**
   ```bash
   black .
   flake8 .
   mypy .
   ```

5. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

   **Commit Message Format**:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `test:` Test additions/changes
   - `refactor:` Code refactoring
   - `perf:` Performance improvements

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### 2. Research Contributions

We welcome research contributions including:

- **New Algorithms**: Implement novel planning, reasoning, or learning algorithms
- **Benchmarks**: Create evaluation benchmarks for AGI capabilities
- **Experiments**: Conduct experiments and share results
- **Papers**: Write research papers using this system

#### Research Contribution Process

1. Open an issue describing your research idea
2. Discuss approach with maintainers
3. Implement and document your research
4. Submit PR with:
   - Code implementation
   - Experimental results
   - Documentation
   - (Optional) Research paper

### 3. Documentation Contributions

Help improve documentation:

- Fix typos and clarify explanations
- Add examples and tutorials
- Translate documentation
- Create video tutorials

### 4. Bug Reports

**Before submitting a bug report**:
- Check existing issues
- Verify it's reproducible
- Collect relevant information

**Bug Report Template**:
```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10]
- Package version: [e.g., 0.1.0]

## Additional Context
Any other relevant information
```

### 5. Feature Requests

**Feature Request Template**:
```markdown
## Feature Description
Clear description of the proposed feature

## Motivation
Why is this feature needed?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches you've considered

## Additional Context
Any other relevant information
```

## 📋 Code Style Guidelines

### Python Style

```python
# Good
def calculate_confidence(
    findings: List[Dict[str, Any]],
    credibility_scores: Dict[str, float]
) -> float:
    """
    Calculate overall confidence in research results.
    
    Args:
        findings: List of research findings
        credibility_scores: Source credibility scores
        
    Returns:
        Confidence score between 0 and 1
    """
    if not findings:
        return 0.0
    
    verified_count = sum(1 for f in findings if f.get("verified", False))
    avg_credibility = sum(credibility_scores.values()) / len(credibility_scores)
    
    confidence = (verified_count / len(findings)) * 0.6 + avg_credibility * 0.4
    
    return min(confidence, 1.0)
```

### Documentation Style

- Use Google-style docstrings
- Include type hints
- Provide examples for complex functions
- Document all public APIs

### Testing Guidelines

```python
# Good test structure
def test_researcher_confidence_calculation():
    """Test confidence calculation with various inputs"""
    # Arrange
    findings = [
        {"verified": True},
        {"verified": True},
        {"verified": False}
    ]
    credibility = {"source1": 0.9, "source2": 0.8}
    
    # Act
    confidence = calculate_confidence(findings, credibility)
    
    # Assert
    assert 0.0 <= confidence <= 1.0
    assert confidence > 0.5  # Majority verified
```

## 🏗️ Architecture Guidelines

### Adding New Agents

1. Inherit from `BaseAgent`
2. Implement required methods:
   - `process_message()`
   - `execute_task()`
   - `self_evaluate()`
3. Add comprehensive docstrings
4. Include unit tests
5. Update documentation

**Example**:
```python
from agents.base_agent import BaseAgent, Message

class NewAgent(BaseAgent):
    """
    Description of agent's role and responsibilities.
    """
    
    def __init__(self, agent_id: str = "new_agent", **kwargs):
        super().__init__(
            agent_id=agent_id,
            agent_type="new_agent",
            **kwargs
        )
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming messages"""
        # Implementation
        pass
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent-specific task"""
        # Implementation
        pass
    
    def self_evaluate(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate own performance"""
        # Implementation
        pass
```

### Adding New Tools

1. Create tool class in `tools/` directory
2. Implement `execute()` method
3. Register in `ToolRegistry`
4. Add tests and documentation

## 🧪 Testing Requirements

### Test Coverage

- Minimum 80% code coverage
- Test all public APIs
- Include edge cases
- Test error handling

### Test Categories

1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test component interactions
3. **System Tests**: Test end-to-end workflows
4. **Performance Tests**: Benchmark critical paths

## 📊 Performance Considerations

- Profile code before optimizing
- Document performance characteristics
- Include benchmarks for critical operations
- Consider memory usage

## 🔒 Security Guidelines

- Validate all inputs
- Sanitize user-provided data
- Use secure defaults
- Document security considerations

## 📝 Documentation Requirements

### Code Documentation

- Docstrings for all public functions/classes
- Type hints for all parameters and returns
- Examples for complex functionality
- Architecture diagrams for new components

### User Documentation

- Update README.md if needed
- Add examples to `examples/` directory
- Update ARCHITECTURE.md for structural changes
- Add research notes to RESEARCH.md

## 🎓 Research Standards

### Experimental Rigor

- Document experimental setup
- Report all metrics (not just best results)
- Include error bars/confidence intervals
- Make experiments reproducible

### Code Quality for Research

- Clean, readable code
- Comprehensive logging
- Configurable hyperparameters
- Reproducible random seeds

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on ideas, not individuals

### Communication

- Use GitHub issues for discussions
- Tag issues appropriately
- Respond to feedback promptly
- Ask questions when unclear

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Acknowledged in release notes
- Co-authors on research papers (if applicable)

## 📞 Getting Help

- **Questions**: Open a GitHub issue with `question` label
- **Discussions**: Use GitHub Discussions
- **Chat**: Join our Discord server (coming soon)

## 🗺️ Roadmap

See [RESEARCH.md](RESEARCH.md) for planned features and research directions.

---

**Thank you for contributing to advancing AGI research!** 🚀
