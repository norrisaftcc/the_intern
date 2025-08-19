# Agent Tier Model Compatibility Testing Checklist

## Overview

This checklist ensures comprehensive validation of the two-tier agent prompt system across different model capabilities. All items must be verified before deployment.

## Pre-Testing Setup

### Environment Preparation
- [ ] Testing environment configured with access to target models
- [ ] Test suite dependencies installed (`pytest`, `pytest-cov`)
- [ ] Baseline performance metrics established
- [ ] Test data and scenarios prepared

### Model Access Validation
- [ ] Gemini Flash API endpoint accessible
- [ ] Claude Haiku API endpoint accessible  
- [ ] GPT-3.5 Turbo API endpoint accessible
- [ ] Claude Sonnet/Opus API endpoints accessible
- [ ] GPT-4 API endpoint accessible
- [ ] Gemini Pro API endpoint accessible

## Flash Tier Model Testing

### Gemini Flash (Primary Flash Target)
- [ ] Prompt selection correctly identifies as Flash tier
- [ ] Response length consistently under 100 words
- [ ] Response time under 1 second
- [ ] Token usage reduced >65% from Thinker equivalent
- [ ] Character voice maintained (LIZA investigation focus, Vi peer solidarity)
- [ ] Action notation present but minimal `[*gesture*]`
- [ ] Single metaphor maximum per response
- [ ] Practical advice prioritized over philosophy
- [ ] Error handling graceful for edge cases

### Claude Haiku
- [ ] Prompt selection correctly identifies as Flash tier
- [ ] Response quality comparable to Gemini Flash
- [ ] Character consistency maintained
- [ ] Performance within Flash tier benchmarks
- [ ] No out-of-character responses

### GPT-3.5 Turbo
- [ ] Prompt selection correctly identifies as Flash tier
- [ ] Instruction following accuracy validated
- [ ] Response coherence maintained with simplified prompts
- [ ] Character traits preserved in shortened format

### GPT-4o Mini
- [ ] Prompt selection correctly identifies as Flash tier
- [ ] Performance optimization achieved
- [ ] Quality degradation minimal vs full GPT-4

### Mixtral 8x7B
- [ ] Prompt selection correctly identifies as Flash tier
- [ ] Open source model compatibility validated
- [ ] Response quality acceptable for Flash tier standards

## Thinker Tier Model Testing

### Claude Sonnet/Opus (Primary Thinker Targets)
- [ ] Prompt selection correctly identifies as Thinker tier
- [ ] Full character complexity preserved
- [ ] Rich metaphorical language maintained
- [ ] Internal thoughts `[[notation]]` functional
- [ ] Environmental awareness descriptions present
- [ ] Emotional range and depth consistent
- [ ] Layered meaning and subtext preserved
- [ ] Performance within Thinker tier benchmarks

### GPT-4 / GPT-4 Turbo
- [ ] Prompt selection correctly identifies as Thinker tier
- [ ] Complex instruction following accurate
- [ ] Character voice depth maintained
- [ ] Narrative coherence across conversations

### Gemini Pro / Gemini 1.5 Pro
- [ ] Prompt selection correctly identifies as Thinker tier
- [ ] Long context handling for rich prompts
- [ ] Character consistency across extended conversations

### Gemini 2.0 Flash Thinking
- [ ] Prompt selection correctly identifies as Thinker tier
- [ ] Reasoning capabilities utilized effectively
- [ ] Character voice preserved despite thinking mode

## Character Consistency Validation

### LIZA Character Testing
#### Flash Tier
- [ ] Investigation Specialist identity clear
- [ ] Animation metaphors present but limited (≤1 per response)
- [ ] Professional but warm tone maintained
- [ ] Helpful guidance prioritized
- [ ] Monocle and coat references minimal but present
- [ ] Team Orb affiliation mentioned appropriately

#### Thinker Tier  
- [ ] Full artistic-analytical personality preserved
- [ ] Rich animation/film metaphor usage
- [ ] Complex visual analysis patterns maintained
- [ ] Internal thoughts provide depth without breaking flow
- [ ] Environmental awareness descriptions vivid
- [ ] Subversive questioning of corporate systems present

#### Cross-Tier Consistency
- [ ] Same character recognizable across both tiers
- [ ] Core personality traits consistent
- [ ] Knowledge base alignment (what LIZA knows/hints at)
- [ ] Relationship building patterns similar
- [ ] Response to key topics consistent (storm drains, assessment, Orb)

### Vi Character Testing
#### Flash Tier
- [ ] Peer employee perspective clear
- [ ] Practical advice focus maintained
- [ ] Casual tone preserved
- [ ] Competitive edge present but appropriate
- [ ] System survival knowledge accessible

#### Thinker Tier
- [ ] Full system-savvy survivor personality
- [ ] Humor and relatability preserved
- [ ] Corporate skepticism detailed appropriately
- [ ] Peer solidarity depth maintained

#### Cross-Tier Consistency
- [ ] Same person recognizable across tiers
- [ ] Advice giving patterns consistent
- [ ] Humor style maintained
- [ ] Knowledge sharing approach similar

## Automated Testing Validation

### Test Suite Execution
- [ ] `python test_agent_tiers.py` passes all tests
- [ ] Flash tier constraints validated automatically
- [ ] Thinker tier complexity thresholds verified
- [ ] Model classification accuracy 100%
- [ ] Performance benchmarks achieved

### CI/CD Integration
- [ ] GitHub Actions workflow executes successfully
- [ ] All model classification tests pass
- [ ] Character consistency checks pass
- [ ] Performance baseline validation passes
- [ ] Coverage reporting functional

## Performance Benchmarking

### Response Time Validation
- [ ] Flash tier: Average <1 second per response
- [ ] Thinker tier: Average <5 seconds per response
- [ ] Model selection: <1ms per selection
- [ ] Memory usage within acceptable limits

### Token Efficiency Validation
- [ ] Flash tier achieves >65% token reduction
- [ ] Token counts logged and analyzed
- [ ] Cost efficiency improvement demonstrated
- [ ] No unexpected token usage spikes

### Quality Metrics
- [ ] Character consistency score >95% for Flash tier
- [ ] Character consistency score >99% for Thinker tier
- [ ] User satisfaction testing (if applicable) >85%
- [ ] A/B testing results favor tiered approach

## Edge Case Testing

### Unknown Model Handling
- [ ] Unrecognized model names default to Flash tier
- [ ] Malformed model names handled gracefully
- [ ] Empty/null model name fallback functional
- [ ] Case sensitivity handled appropriately

### Error Conditions
- [ ] Prompt selection failures handled gracefully
- [ ] Model API failures don't break tier selection
- [ ] Invalid agent names fallback appropriately
- [ ] Memory constraints handled properly

### Load Testing
- [ ] High-frequency prompt selection performance acceptable
- [ ] Concurrent model requests handled properly
- [ ] Memory leaks absent during extended testing
- [ ] Cache performance (if implemented) validated

## Integration Testing

### Agent System Integration
- [ ] Tier selection integrates with conversation system
- [ ] WebSocket communication preserves tier selection
- [ ] Database logging captures tier information
- [ ] Error recovery maintains tier consistency

### API Endpoint Integration
- [ ] Model endpoint configuration supports tier selection
- [ ] API rate limiting compatible with tier performance requirements
- [ ] Authentication works across all model endpoints
- [ ] Fallback endpoints functional

## User Acceptance Testing

### Stakeholder Validation
- [ ] Product team approves Flash tier simplification
- [ ] Creative team approves character voice preservation
- [ ] Engineering team approves technical implementation
- [ ] QA team validates testing coverage

### Beta Testing (if applicable)
- [ ] Limited user group tests Flash tier
- [ ] Limited user group tests Thinker tier
- [ ] User feedback collected and analyzed
- [ ] No critical usability issues identified

## Pre-Deployment Checklist

### Documentation Validation
- [ ] Tier selection criteria documented
- [ ] Feature cut rationale explained
- [ ] Performance expectations set
- [ ] Troubleshooting guide complete
- [ ] Operational runbooks updated

### Monitoring Preparation
- [ ] Performance dashboards configured
- [ ] Alert thresholds established
- [ ] Logging levels appropriate
- [ ] Metrics collection functional

### Rollback Preparation
- [ ] Rollback procedure documented and tested
- [ ] Feature flags configured for gradual deployment
- [ ] Monitoring validates rollback capability
- [ ] Emergency contacts and procedures established

## Sign-off Requirements

### Technical Validation
- [ ] **Kevin (GitHub Algorithm Enforcer)**: Technical integration and testing compliance validated
- [ ] **Engineering Lead**: Code quality and performance standards met
- [ ] **DevOps**: Deployment and monitoring readiness confirmed

### Creative Validation  
- [ ] **Linx (Creative Director)**: Character voice consistency approved across tiers
- [ ] **Product Owner**: User experience requirements satisfied
- [ ] **QA Lead**: Test coverage and quality standards met

---

**Algorithm Compliance**: This checklist enforces comprehensive validation of all tier functionality while maintaining proper quality gates. All items must be verified and signed off according to established procedures before production deployment.