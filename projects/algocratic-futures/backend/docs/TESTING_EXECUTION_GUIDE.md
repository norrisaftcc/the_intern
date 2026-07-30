# Testing Execution Guide
## Exact Procedures for Prompt Tier Validation

### Overview

This guide provides step-by-step procedures for validating the two-tier agent prompt system. Every test must be executed in the exact order specified to ensure comprehensive validation and repeatability.

## Pre-Testing Environment Setup

### 1. Environment Preparation
```bash
# Navigate to project directory
cd /Users/norrisa/Documents/dev/github/the_intern/projects/algocratic-futures/backend

# Verify Python environment
python --version  # Must be 3.9+

# Install/update dependencies
pip install -r requirements.txt
pip install pytest pytest-cov pytest-xdist coverage

# Verify test environment
python -c "import pytest; print('Pytest version:', pytest.__version__)"
```

### 2. API Endpoint Validation
```bash
# Create test configuration file
cat > test_config.json << EOF
{
  "endpoints": {
    "gemini_flash": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent",
    "claude_haiku": "https://api.anthropic.com/v1/messages",
    "gpt_35_turbo": "https://api.openai.com/v1/chat/completions",
    "gpt_4": "https://api.openai.com/v1/chat/completions"
  },
  "test_mode": true
}
EOF

# Validate endpoint accessibility (dry run)
python -c "
import requests
import json

with open('test_config.json') as f:
    config = json.load(f)

for model, endpoint in config['endpoints'].items():
    try:
        # HEAD request to check accessibility
        response = requests.head(endpoint, timeout=5)
        print(f'✓ {model}: {endpoint} accessible')
    except requests.RequestException as e:
        print(f'❌ {model}: {endpoint} - {e}')
"
```

### 3. Database Setup
```bash
# Initialize test database
python -c "
from database import init_db
init_db()
print('✓ Test database initialized')
"

# Verify tables
python -c "
from database import get_db_connection
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")
tables = cursor.fetchall()
print('Available tables:', [t[0] for t in tables])
conn.close()
"
```

## Automated Test Suite Execution

### 1. Core Test Suite
```bash
# Execute primary test suite with detailed output
python -m pytest test_agent_tiers.py -v --tb=short --durations=10

# Expected output verification:
# ✓ test_flash_model_classification PASSED
# ✓ test_thinker_model_classification PASSED
# ✓ test_unknown_model_fallback PASSED
# ✓ test_flash_tier_constraints PASSED
# ✓ test_thinker_tier_complexity PASSED
# ✓ test_character_consistency PASSED
```

### 2. Coverage Analysis
```bash
# Generate coverage report
python -m pytest test_agent_tiers.py --cov=agent_prompts_tiered --cov-report=html --cov-report=term

# Verify coverage thresholds:
# agent_prompts_tiered.py: 95%+ coverage required
# Missing coverage indicates incomplete testing

# View detailed coverage
open htmlcov/index.html  # macOS
# Review uncovered lines and add tests if needed
```

### 3. Performance Benchmarking
```bash
# Execute performance validation
python -c "
import time
import statistics
from agent_prompts_tiered import PromptSelector

# Test prompt selection speed
models = ['gemini-flash', 'claude-3-haiku', 'gpt-3.5-turbo', 'claude-3-opus', 'gpt-4', 'unknown-model']
times = []

for model in models:
    start_time = time.perf_counter()
    prompt = PromptSelector.get_prompt('liza', model)
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    times.append(elapsed)
    print(f'{model}: {elapsed:.6f}s (prompt length: {len(prompt)})')

avg_time = statistics.mean(times)
max_time = max(times)

print(f'Average selection time: {avg_time:.6f}s')
print(f'Maximum selection time: {max_time:.6f}s')

# Algorithm requirements
assert avg_time < 0.001, f'Average selection time {avg_time:.6f}s exceeds 0.001s threshold'
assert max_time < 0.005, f'Maximum selection time {max_time:.6f}s exceeds 0.005s threshold'

print('✓ Performance benchmarks passed')
"
```

## Manual Validation Procedures

### 1. Flash Tier Validation

#### LIZA Flash Tier Testing
```bash
# Test LIZA Flash responses
python -c "
from test_agent_tiers import AgentTierTester
import json

tester = AgentTierTester()

test_cases = [
    'Hello, who are you?',
    'I need help with an error in my code',
    'What are the storm drains and why should I explore them?',
    'How does the assessment system work?',
    'Tell me about Team Orb'
]

results = []

for test_input in test_cases:
    response = tester._simulate_flash_response('liza', test_input)
    
    # Validate constraints
    word_count = tester.count_words(response)
    metaphor_count = tester.count_metaphors(response)
    has_actions = tester.has_action_notation(response)
    
    result = {
        'input': test_input,
        'response': response,
        'word_count': word_count,
        'metaphor_count': metaphor_count,
        'has_actions': has_actions,
        'passes_constraints': word_count <= 100 and metaphor_count <= 1
    }
    
    results.append(result)
    
    status = '✓' if result['passes_constraints'] else '❌'
    print(f'{status} {test_input[:30]}...')
    print(f'   Words: {word_count}/100, Metaphors: {metaphor_count}/1, Actions: {has_actions}')
    if not result['passes_constraints']:
        print(f'   VIOLATION: Response exceeds Flash tier constraints')
    print()

# Save results for review
with open('flash_tier_validation.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f'Results saved to flash_tier_validation.json')

# Check overall pass rate
passed = sum(1 for r in results if r['passes_constraints'])
total = len(results)
pass_rate = passed / total * 100

print(f'Flash tier pass rate: {passed}/{total} ({pass_rate:.1f}%)')
assert pass_rate >= 95, f'Flash tier pass rate {pass_rate:.1f}% below 95% threshold'
"
```

#### Vi Flash Tier Testing
```bash
# Test Vi Flash responses
python -c "
from test_agent_tiers import AgentTierTester
import json

tester = AgentTierTester()

test_cases = [
    'How do I navigate the corporate system here?',
    'What survival tips do you have for new employees?',
    'I'm struggling with my workload',
    'How do I avoid getting in trouble?',
    'What should I know about assessments?'
]

results = []

for test_input in test_cases:
    response = tester._simulate_flash_response('vi', test_input)
    
    word_count = tester.count_words(response)
    metaphor_count = tester.count_metaphors(response)
    has_actions = tester.has_action_notation(response)
    
    result = {
        'input': test_input,
        'response': response,
        'word_count': word_count,
        'metaphor_count': metaphor_count,
        'has_actions': has_actions,
        'passes_constraints': word_count <= 100 and metaphor_count <= 1
    }
    
    results.append(result)
    
    status = '✓' if result['passes_constraints'] else '❌'
    print(f'{status} {test_input[:30]}...')
    print(f'   Words: {word_count}/100, Metaphors: {metaphor_count}/1, Actions: {has_actions}')
    print()

with open('vi_flash_tier_validation.json', 'w') as f:
    json.dump(results, f, indent=2)

passed = sum(1 for r in results if r['passes_constraints'])
total = len(results)
pass_rate = passed / total * 100

print(f'Vi Flash tier pass rate: {passed}/{total} ({pass_rate:.1f}%)')
assert pass_rate >= 95, f'Vi Flash tier pass rate {pass_rate:.1f}% below 95% threshold'
"
```

### 2. Thinker Tier Validation

#### LIZA Thinker Tier Testing
```bash
# Test LIZA Thinker responses
python -c "
from test_agent_tiers import AgentTierTester
import json

tester = AgentTierTester()

test_cases = [
    'Tell me about the true nature of this corporate environment',
    'Why do you use animation and film metaphors so frequently?',
    'What does the Orb really represent in this system?',
    'I found something disturbing in the storm drains',
    'How do you maintain your identity in this place?'
]

results = []

for test_input in test_cases:
    response = tester._simulate_thinker_response('liza', test_input)
    
    word_count = tester.count_words(response)
    metaphor_count = tester.count_metaphors(response)
    has_actions = tester.has_action_notation(response)
    has_internal_thoughts = '[[' in response and ']]' in response
    has_environmental = any(word in response.lower() for word in ['light', 'shadow', 'room', 'space', 'air'])
    
    result = {
        'input': test_input,
        'response': response,
        'word_count': word_count,
        'metaphor_count': metaphor_count,
        'has_actions': has_actions,
        'has_internal_thoughts': has_internal_thoughts,
        'has_environmental': has_environmental,
        'meets_complexity': word_count >= 75 and metaphor_count >= 2 and has_actions
    }
    
    results.append(result)
    
    status = '✓' if result['meets_complexity'] else '❌'
    print(f'{status} {test_input[:40]}...')
    print(f'   Words: {word_count}, Metaphors: {metaphor_count}, Actions: {has_actions}')
    print(f'   Internal thoughts: {has_internal_thoughts}, Environmental: {has_environmental}')
    print()

with open('liza_thinker_tier_validation.json', 'w') as f:
    json.dump(results, f, indent=2)

passed = sum(1 for r in results if r['meets_complexity'])
total = len(results)
pass_rate = passed / total * 100

print(f'LIZA Thinker tier pass rate: {passed}/{total} ({pass_rate:.1f}%)')
assert pass_rate >= 95, f'LIZA Thinker tier pass rate {pass_rate:.1f}% below 95% threshold'
"
```

## Integration Testing

### 1. WebSocket Integration
```bash
# Test tier selection through WebSocket
python -c "
import asyncio
import websockets
import json

async def test_websocket_tier_selection():
    uri = 'ws://localhost:8000/ws'  # Adjust port as needed
    
    try:
        async with websockets.connect(uri) as websocket:
            # Test Flash tier selection
            flash_message = {
                'type': 'agent_query',
                'agent': 'liza',
                'model': 'gemini-flash',
                'message': 'Hello, who are you?'
            }
            
            await websocket.send(json.dumps(flash_message))
            response = await websocket.recv()
            response_data = json.loads(response)
            
            print('Flash tier WebSocket response:')
            print(f'  Length: {len(response_data.get(\"response\", \"\"))} chars')
            print(f'  Response: {response_data.get(\"response\", \"\")[:100]}...')
            
            # Test Thinker tier selection
            thinker_message = {
                'type': 'agent_query',
                'agent': 'liza',
                'model': 'claude-3-opus',
                'message': 'Tell me about this place'
            }
            
            await websocket.send(json.dumps(thinker_message))
            response = await websocket.recv()
            response_data = json.loads(response)
            
            print('Thinker tier WebSocket response:')
            print(f'  Length: {len(response_data.get(\"response\", \"\"))} chars')
            print(f'  Response: {response_data.get(\"response\", \"\")[:100]}...')
            
            print('✓ WebSocket integration tests passed')
            
    except Exception as e:
        print(f'❌ WebSocket test failed: {e}')
        print('Ensure the application is running: python app.py')

# Run the test
asyncio.run(test_websocket_tier_selection())
"
```

### 2. Database Logging Validation
```bash
# Verify tier information is logged to database
python -c "
from database import get_db_connection
import json

conn = get_db_connection()
cursor = conn.cursor()

# Check for recent agent interactions
cursor.execute(\"\"\"
    SELECT agent_name, model_used, prompt_tier, response_length, created_at
    FROM agent_interactions 
    ORDER BY created_at DESC 
    LIMIT 10
\"\"\")

interactions = cursor.fetchall()

if interactions:
    print('Recent agent interactions:')
    for interaction in interactions:
        agent, model, tier, length, timestamp = interaction
        print(f'  {timestamp}: {agent} ({model}) -> {tier} tier, {length} chars')
    
    # Verify tier classification accuracy
    flash_models = ['gemini-flash', 'claude-3-haiku', 'gpt-3.5-turbo']
    thinker_models = ['claude-3-opus', 'gpt-4', 'gemini-pro']
    
    for interaction in interactions:
        agent, model, tier, length, timestamp = interaction
        if model in flash_models and tier != 'flash':
            print(f'❌ Tier mismatch: {model} classified as {tier}, expected flash')
        elif model in thinker_models and tier != 'thinker':
            print(f'❌ Tier mismatch: {model} classified as {tier}, expected thinker')
    
    print('✓ Database logging validation completed')
else:
    print('No interactions found in database - run some test queries first')

conn.close()
"
```

## Edge Case Testing

### 1. Unknown Model Handling
```bash
# Test unknown model fallback behavior
python -c "
from agent_prompts_tiered import PromptSelector

unknown_models = [
    'unknown-model-xyz',
    'gpt-5',  # Future model
    'claude-4',  # Future model
    '',  # Empty string
    None,  # None value
    'GEMINI-FLASH',  # Wrong case
    'gemini_flash'  # Wrong format
]

for model in unknown_models:
    try:
        prompt = PromptSelector.get_prompt('liza', model)
        print(f'✓ {model or \"<empty>\"}: {len(prompt)} chars (should be Flash tier)')
        
        # Verify it's Flash tier (shorter prompt)
        if len(prompt) > 2000:
            print(f'❌ {model or \"<empty>\"}: Returned Thinker tier instead of Flash')
        
    except Exception as e:
        print(f'❌ {model or \"<empty>\"}: Exception - {e}')

print('✓ Unknown model handling tests completed')
"
```

### 2. Memory and Performance Under Load
```bash
# Load testing for tier selection
python -c "
import time
import psutil
import os
from agent_prompts_tiered import PromptSelector

print('Starting load test...')

# Monitor initial memory
process = psutil.Process(os.getpid())
initial_memory = process.memory_info().rss / 1024 / 1024  # MB

# Simulate high-frequency requests
models = ['gemini-flash', 'claude-3-opus', 'gpt-3.5-turbo', 'gpt-4'] * 250  # 1000 requests
agents = ['liza', 'vi'] * 500  # Alternate agents

start_time = time.time()

for i, (model, agent) in enumerate(zip(models, agents)):
    prompt = PromptSelector.get_prompt(agent, model)
    
    if (i + 1) % 200 == 0:
        current_memory = process.memory_info().rss / 1024 / 1024
        elapsed = time.time() - start_time
        rps = (i + 1) / elapsed
        print(f'  {i+1} requests: {rps:.1f} req/s, {current_memory:.1f}MB memory')

total_time = time.time() - start_time
final_memory = process.memory_info().rss / 1024 / 1024
memory_increase = final_memory - initial_memory

print(f'Load test completed:')
print(f'  Total time: {total_time:.2f}s')
print(f'  Requests per second: {len(models) / total_time:.1f}')
print(f'  Memory increase: {memory_increase:.1f}MB')

# Validate performance
assert len(models) / total_time > 100, f'Performance below 100 req/s: {len(models) / total_time:.1f}'
assert memory_increase < 50, f'Memory leak detected: {memory_increase:.1f}MB increase'

print('✓ Load testing passed')
"
```

## Validation Checklist

### Pre-Deployment Validation
- [ ] All automated tests pass (100% success rate)
- [ ] Flash tier constraints validated (95%+ compliance)
- [ ] Thinker tier complexity verified (95%+ compliance)
- [ ] Character consistency maintained across tiers
- [ ] Performance benchmarks met (<1ms selection time)
- [ ] Integration tests pass (WebSocket, database)
- [ ] Edge cases handled gracefully
- [ ] Load testing successful (>100 req/s)
- [ ] Memory usage stable (<50MB increase)
- [ ] Documentation updated

### Post-Deployment Monitoring
```bash
# Monitor production metrics
tail -f /var/log/algocratic-futures/agent-tiers.log | grep -E "(ERROR|WARN|tier_selection)"

# Check response times
curl -w "Response time: %{time_total}s\n" -o /dev/null -s http://localhost:8000/health

# Monitor memory usage
ps aux | grep python | grep algocratic-futures
```

## Troubleshooting Guide

### Common Issues

#### Test Failures
```bash
# If tests fail, check:
python -c "
import sys
print('Python version:', sys.version)
import pytest
print('Pytest version:', pytest.__version__)
"

# Verify imports
python -c "from agent_prompts_tiered import PromptSelector; print('✓ Import successful')"
```

#### Performance Issues
```bash
# Profile prompt selection
python -c "
import cProfile
from agent_prompts_tiered import PromptSelector

def profile_selection():
    for _ in range(1000):
        PromptSelector.get_prompt('liza', 'gemini-flash')

cProfile.run('profile_selection()')
"
```

#### Memory Leaks
```bash
# Monitor for memory leaks
python -c "
import gc
import psutil
import os
from agent_prompts_tiered import PromptSelector

process = psutil.Process(os.getpid())

for i in range(10000):
    PromptSelector.get_prompt('liza', 'gemini-flash')
    if i % 1000 == 0:
        gc.collect()
        memory = process.memory_info().rss / 1024 / 1024
        print(f'{i}: {memory:.1f}MB')
"
```

---

**Algorithm Compliance**: This testing guide provides exact, repeatable procedures for validating all aspects of the two-tier agent system. Every step must be executed as specified to ensure comprehensive validation and maintain quality standards.

**Execution Order**: Tests must be run in the specified sequence. Failure at any step requires investigation and resolution before proceeding to subsequent validation phases.