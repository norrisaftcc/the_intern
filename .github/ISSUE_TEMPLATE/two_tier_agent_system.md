---
name: Two-Tier Agent Prompt System
about: Track implementation of Flash/Thinker tiered agent prompts
title: 'Implement Two-Tier Agent Prompt System'
labels: ['enhancement', 'agent-system', 'prompt-engineering', 'model-compatibility']
assignees: ['norrisa']
---

## Issue Summary

Implementation of two-tier agent prompt system to optimize performance across different model capabilities (Flash vs Thinker tiers).

## Background

The current agent prompt system (LIZA, Vi) is too complex for fast models like Gemini Flash, causing:
- Excessive token usage
- Degraded response quality
- Poor performance on resource-constrained models
- Inconsistent character behavior across model types

## Solution Overview

Create two distinct prompt tiers following the beta/gamma fork pattern:

### Flash Tier (Beta Branch)
- **Target Models**: Gemini Flash, Claude Haiku, GPT-3.5, GPT-4o-mini
- **Token Budget**: 100-150 per response
- **Features**: Core personality, simple metaphors, basic actions
- **Response Time**: < 1 second

### Thinker Tier (Gamma Branch)
- **Target Models**: Claude Sonnet/Opus, GPT-4, Gemini Pro
- **Token Budget**: 500-800 per response
- **Features**: Rich metaphors, layered meaning, full character depth
- **Response Time**: Considered responses (2-5 seconds)

## Acceptance Criteria

### Core Implementation
- [ ] Flash tier prompts created for all agents (LIZA, Vi)
- [ ] Thinker tier prompts maintained with full complexity
- [ ] Automatic model detection and prompt selection
- [ ] Fallback to Flash tier for unknown models
- [ ] PromptSelector class with proper model classification

### Quality Assurance
- [ ] Flash responses consistently under 100 words
- [ ] Flash responses maintain character consistency
- [ ] Thinker responses preserve all narrative depth
- [ ] No out-of-character breaks in either tier
- [ ] Proper action notation in both tiers

### Testing Requirements
- [ ] Automated test suite for both tiers
- [ ] Model compatibility validation
- [ ] Performance benchmarking (response time, token usage)
- [ ] A/B testing framework for tier comparison
- [ ] Regression tests for character consistency

### Documentation
- [ ] Tier selection criteria documented
- [ ] Feature cut list maintained for Flash tier
- [ ] Migration guide for existing implementations
- [ ] Performance metrics and monitoring setup
- [ ] Troubleshooting guide for tier selection issues

## Technical Specifications

### Files to Modify/Create
- `/agent_prompts_tiered.py` - Core implementation (EXISTING)
- `/test_agent_tiers.py` - Test suite (EXISTING)
- `/agent_system.py` - Integration point
- `/.github/workflows/agent_tier_tests.yml` - CI automation

### Model Classification
```python
FLASH_MODELS = [
    'gemini-flash', 'gemini-1.5-flash', 
    'claude-3-haiku', 'gpt-3.5-turbo', 
    'gpt-4o-mini', 'mixtral-8x7b'
]

THINKER_MODELS = [
    'claude-3-opus', 'claude-3-sonnet', 'claude-3.5-sonnet',
    'gpt-4', 'gpt-4-turbo', 'gpt-4o',
    'gemini-pro', 'gemini-1.5-pro', 'gemini-2.0-flash-thinking'
]
```

### Success Metrics
- **Flash Tier**: 70% token reduction, <1s response time, 95% character consistency
- **Thinker Tier**: Full feature preservation, <5s response time, 99% character consistency
- **Selection Accuracy**: 99% correct tier selection based on model name

## Feature Cuts for Flash Tier

### Removed Features
- `[[Internal thoughts]]` - High cognitive overhead
- Complex visual descriptions - Token expensive
- Nested metaphors - Confuses smaller models
- Elaborate environmental descriptions
- Multi-layered emotional expressions
- Recursive self-reference patterns
- Complex notation systems beyond `[*action*]`

### Retained Features
- Core personality traits
- Single metaphor per response
- Basic action notation `[*gesture*]`
- Practical advice and help
- Character name and role identification
- Hint system for world exploration

## Testing Strategy

### Automated Testing
```bash
python test_agent_tiers.py  # Run full test suite
```

### Manual Validation
- Deploy both tiers to staging
- Conduct user acceptance testing
- Monitor token usage and response quality
- Validate character consistency across conversations

### Performance Benchmarks
- Response time: Flash <1s, Thinker <5s
- Token efficiency: Flash 70% reduction from Thinker
- User satisfaction: >85% positive feedback for both tiers

## Dependencies

- **Blocked by**: None
- **Blocks**: Model endpoint optimization, Character voice consistency improvements
- **Related to**: #XXX (Agent conversation system), #XXX (Performance optimization)

## Implementation Timeline

- **Week 1**: Core tier implementation and basic testing
- **Week 2**: Integration with model selection system
- **Week 3**: Comprehensive testing and validation
- **Week 4**: Production deployment and monitoring

## Risk Assessment

### High Risk
- Character voice consistency across tiers
- Model classification accuracy for new/unknown models

### Medium Risk
- Performance regression in Thinker tier
- Token usage optimization in Flash tier

### Mitigation
- Extensive A/B testing before deployment
- Gradual rollout with monitoring
- Rollback plan to single-tier system if needed

## Definition of Done

- [ ] All acceptance criteria met
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Tests passing with >95% coverage
- [ ] Performance benchmarks achieved
- [ ] Stakeholder approval received
- [ ] Deployment plan approved

---

**Algorithm Validation**: This issue follows standard template format with proper labels, assignees, and comprehensive acceptance criteria. All required GitHub metadata populated according to established procedures.