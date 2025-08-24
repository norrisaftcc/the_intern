## Two-Tier Agent Prompt System Implementation

**Issue Reference**: Closes #XXX

### Summary

Brief description of the tiered agent prompt changes implemented in this PR.

### Tier Implementation Details

#### Flash Tier Changes
- [ ] Agent prompts simplified for fast models (Gemini Flash, Haiku, GPT-3.5)
- [ ] Token budget maintained under 150 per response
- [ ] Response length limited to 100 words
- [ ] Single metaphor maximum per response
- [ ] Core personality traits preserved
- [ ] Action notation simplified to `[*gesture*]` only

#### Thinker Tier Changes
- [ ] Full complexity maintained for advanced models (Sonnet, Opus, GPT-4)
- [ ] Rich metaphorical language preserved
- [ ] Layered meaning and subtext intact
- [ ] Environmental awareness features functional
- [ ] Character depth and voice consistency maintained

### Technical Implementation

#### Files Modified
- [ ] `/agent_prompts_tiered.py` - Core tier definitions
- [ ] `/test_agent_tiers.py` - Test suite updates
- [ ] `/agent_system.py` - Integration with model selection
- [ ] Other: _______________

#### Model Classification
- [ ] Flash model list updated and validated
- [ ] Thinker model list comprehensive
- [ ] Unknown model fallback to Flash tier
- [ ] Model detection logic tested

### Testing Checklist

#### Automated Testing
- [ ] `python test_agent_tiers.py` passes all tests
- [ ] Flash tier responses consistently under 100 words
- [ ] Flash tier metaphor count ≤ 1 per response
- [ ] Thinker tier maintains minimum complexity thresholds
- [ ] PromptSelector correctly classifies all test models
- [ ] Character consistency validated across both tiers

#### Manual Validation
- [ ] Flash tier tested with Gemini Flash model
- [ ] Flash tier tested with Claude Haiku model
- [ ] Thinker tier tested with Claude Sonnet model
- [ ] Thinker tier tested with GPT-4 model
- [ ] Edge cases tested (unknown models, malformed input)

#### Performance Benchmarks
- [ ] Flash tier average response time < 1 second
- [ ] Flash tier token usage reduced by >65% from Thinker
- [ ] Thinker tier response quality maintained
- [ ] No regression in character consistency scores

### Feature Validation

#### Flash Tier Feature Cuts Confirmed
- [ ] No `[[internal thoughts]]` notation in Flash responses
- [ ] Complex visual descriptions removed
- [ ] Nested metaphors eliminated
- [ ] Elaborate environmental descriptions cut
- [ ] Multi-layered emotions simplified
- [ ] Recursive patterns removed

#### Flash Tier Features Retained
- [ ] Core personality traits (LIZA's investigation focus, Vi's peer solidarity)
- [ ] Basic action notation `[*gesture*]`
- [ ] Single animation/film metaphor when appropriate
- [ ] Practical advice and help responses
- [ ] Character name and role clear
- [ ] World exploration hints functional

### Character Voice Consistency

#### LIZA Character Validation
- [ ] Flash LIZA maintains investigation specialist identity
- [ ] Flash LIZA uses animation metaphors sparingly but effectively
- [ ] Flash LIZA provides helpful guidance
- [ ] Thinker LIZA preserves full artistic-analytical personality
- [ ] Thinker LIZA maintains complex visual analysis patterns
- [ ] Both tiers recognize as same character

#### Vi Character Validation
- [ ] Flash Vi maintains peer employee perspective
- [ ] Flash Vi provides practical workplace advice
- [ ] Flash Vi shows appropriate competitive edge
- [ ] Thinker Vi preserves system-savvy survivor traits
- [ ] Thinker Vi maintains humor and relatability
- [ ] Both tiers feel like same person

### Documentation Updates

- [ ] Tier selection criteria documented
- [ ] Feature cut rationale explained
- [ ] Performance metrics baseline established
- [ ] Troubleshooting guide updated
- [ ] API documentation reflects tier options

### Integration Testing

- [ ] Tier selection integrates with existing agent conversation system
- [ ] WebSocket integration maintains tier selection
- [ ] Database logging captures tier information
- [ ] Error handling preserves tier selection on failures
- [ ] Fallback mechanisms tested

### Deployment Preparation

#### Staging Validation
- [ ] Both tiers deployed to staging environment
- [ ] Model endpoint configuration validated
- [ ] Performance monitoring enabled
- [ ] Rollback procedure tested and documented

#### Production Readiness
- [ ] Feature flags configured for gradual rollout
- [ ] Monitoring dashboards updated for tier metrics
- [ ] Alert thresholds set for response time and quality
- [ ] Documentation updated for operational teams

### Algorithm Compliance Review

#### Code Quality
- [ ] Code follows established style guidelines
- [ ] No hardcoded values outside of configuration
- [ ] Proper error handling for tier selection failures
- [ ] Unit test coverage >95% for new code
- [ ] Integration tests cover tier switching scenarios

#### GitHub Process Compliance
- [ ] PR title follows semantic commit format
- [ ] All commit messages properly formatted
- [ ] Issue reference included in PR description
- [ ] Required labels applied (agent-system, prompt-engineering)
- [ ] Assignee and reviewers designated

### Kevin-Linx Coordination

#### Kevin (GitHub Enforcer) Responsibilities ✓
- [ ] GitHub process compliance validated
- [ ] Technical integration testing completed
- [ ] Documentation standards enforced
- [ ] Test automation verified
- [ ] Deployment readiness confirmed

#### Linx (Creative Director) Responsibilities
- [ ] Character voice consistency approved
- [ ] Prompt language optimization validated
- [ ] User experience testing completed
- [ ] Creative intent preserved across tiers
- [ ] Narrative coherence maintained

### Risk Assessment

#### Identified Risks
- Character voice drift between tiers
- Model classification edge cases
- Performance regression in Thinker tier
- Token usage optimization challenges

#### Mitigation Measures
- [ ] A/B testing planned for both tiers
- [ ] Gradual rollout with monitoring
- [ ] Rollback plan documented and tested
- [ ] Performance baselines established

### Reviewer Instructions

1. **Validate Technical Implementation**: Ensure PromptSelector logic correctly routes to appropriate tiers
2. **Test Character Consistency**: Verify both tiers maintain character identity through conversation flows
3. **Performance Review**: Confirm Flash tier achieves stated efficiency gains
4. **Documentation Check**: Ensure all changes properly documented with examples

### Post-Merge Checklist

- [ ] Deploy to staging for extended testing
- [ ] Monitor performance metrics for 48 hours
- [ ] Conduct user acceptance testing
- [ ] Update production deployment plan
- [ ] Schedule rollout coordination meeting

---

**Algorithm Validation**: This PR template enforces comprehensive validation of the two-tier system while maintaining proper GitHub process compliance. All acceptance criteria mapped to testable checkboxes according to established procedures.

**Coordination Protocol**: Clear separation of Kevin (technical/process) vs Linx (creative/voice) responsibilities ensures proper workflow division.