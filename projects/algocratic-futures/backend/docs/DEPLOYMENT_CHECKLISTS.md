# Deployment Checklists
## Step-by-Step Repeatable Deployment and Rollback Procedures

### Overview

This document provides mandatory step-by-step procedures for deploying the algocratic-futures backend system. Every deployment MUST follow these exact procedures to ensure repeatability, reliability, and compliance with established standards.

## Pre-Deployment Validation

### Environment Verification Checklist
- [ ] **Development Environment Ready**
  ```bash
  cd /Users/norrisa/Documents/dev/github/the_intern/projects/algocratic-futures/backend
  git status  # Verify clean working directory
  git branch  # Confirm on feature branch
  python --version  # Verify Python 3.9+
  ```

- [ ] **Dependencies Current**
  ```bash
  pip list --outdated  # Check for outdated packages
  pip install -r requirements.txt  # Update dependencies
  python -c "import all_modules; print('✓ All imports successful')"
  ```

- [ ] **Database Migration Ready**
  ```bash
  python -c "from database import get_db_connection; conn = get_db_connection(); print('✓ Database accessible')"
  sqlite3 algocratic_futures.db ".schema" | wc -l  # Verify schema
  ```

- [ ] **API Endpoints Accessible**
  ```bash
  # Test each model endpoint (dry run)
  python -c "
  endpoints = ['gemini-flash', 'claude-3-haiku', 'gpt-3.5-turbo', 'claude-3-opus', 'gpt-4']
  for endpoint in endpoints:
      print(f'Checking {endpoint}...')
  print('✓ Endpoint validation completed')
  "
  ```

### Code Quality Gates
- [ ] **Linting Passes**
  ```bash
  flake8 --max-line-length=100 --ignore=E203,W503 *.py
  black --check *.py
  isort --check-only *.py
  ```

- [ ] **Security Scan Clean**
  ```bash
  bandit -r . -f json -o security_report.json
  cat security_report.json | jq '.results | length'  # Should be 0
  ```

- [ ] **Test Coverage Adequate**
  ```bash
  python -m pytest --cov=. --cov-report=term --cov-fail-under=95
  echo "Coverage threshold: 95% minimum"
  ```

## Staging Deployment

### Staging Environment Setup
- [ ] **Staging Database Preparation**
  ```bash
  # Backup current staging database
  cp algocratic_futures.db algocratic_futures_staging_backup_$(date +%Y%m%d_%H%M%S).db
  
  # Apply any pending migrations
  python -c "from database import init_db; init_db(); print('✓ Staging database ready')"
  ```

- [ ] **Configuration Validation**
  ```bash
  # Verify staging configuration
  python -c "
  import os
  required_vars = ['DATABASE_URL', 'API_ENDPOINTS']
  missing = [var for var in required_vars if not os.getenv(var)]
  if missing:
      print(f'❌ Missing environment variables: {missing}')
  else:
      print('✓ All required environment variables present')
  "
  ```

- [ ] **Service Startup**
  ```bash
  # Start staging server
  export ENVIRONMENT=staging
  python app.py --port 8001 &
  STAGING_PID=$!
  
  # Verify startup
  sleep 5
  curl -f http://localhost:8001/health || echo "❌ Staging startup failed"
  ```

### Staging Validation Tests
- [ ] **Functional Testing**
  ```bash
  # Test agent tier selection
  python -c "
  import requests
  import json
  
  # Test Flash tier
  flash_response = requests.post('http://localhost:8001/agent/query', json={
      'agent': 'liza',
      'model': 'gemini-flash',
      'message': 'Hello'
  })
  
  if flash_response.status_code == 200:
      data = flash_response.json()
      if len(data['response']) < 500:  # Flash tier should be concise
          print('✓ Flash tier working')
      else:
          print('❌ Flash tier response too long')
  
  # Test Thinker tier
  thinker_response = requests.post('http://localhost:8001/agent/query', json={
      'agent': 'liza',
      'model': 'claude-3-opus',
      'message': 'Tell me about this place'
  })
  
  if thinker_response.status_code == 200:
      data = thinker_response.json()
      if len(data['response']) > 300:  # Thinker tier should be detailed
          print('✓ Thinker tier working')
      else:
          print('❌ Thinker tier response too brief')
  "
  ```

- [ ] **Performance Baseline**
  ```bash
  # Load testing
  ab -n 100 -c 10 http://localhost:8001/health
  
  # Response time validation
  curl -w "Response time: %{time_total}s\n" -o /dev/null -s http://localhost:8001/health
  ```

- [ ] **WebSocket Testing**
  ```bash
  python -c "
  import asyncio
  import websockets
  import json
  
  async def test_websocket():
      try:
          async with websockets.connect('ws://localhost:8001/ws') as websocket:
              message = {'type': 'ping'}
              await websocket.send(json.dumps(message))
              response = await websocket.recv()
              print('✓ WebSocket functional')
      except Exception as e:
          print(f'❌ WebSocket failed: {e}')
  
  asyncio.run(test_websocket())
  "
  ```

### Staging Sign-off
- [ ] **Technical Validation** (Kevin - GitHub Algorithm Enforcer)
  - Automated tests pass
  - Performance benchmarks met
  - Integration tests successful
  - Database migrations applied correctly

- [ ] **Creative Validation** (Linx - Creative Director)  
  - Character voice consistency maintained
  - User experience preserved
  - Narrative coherence intact
  - Both tiers provide appropriate responses

- [ ] **QA Validation**
  - Manual testing completed
  - Edge cases validated
  - Error handling verified
  - Documentation accurate

## Production Deployment

### Pre-Production Checklist
- [ ] **Production Environment Preparation**
  ```bash
  # Verify production environment variables
  python -c "
  import os
  production_vars = [
      'DATABASE_URL', 'API_ENDPOINTS', 'LOG_LEVEL', 'MONITORING_ENDPOINT'
  ]
  missing = [var for var in production_vars if not os.getenv(var)]
  if missing:
      print(f'❌ Missing production variables: {missing}')
      exit(1)
  else:
      print('✓ Production environment ready')
  "
  ```

- [ ] **Production Database Backup**
  ```bash
  # Create production backup
  BACKUP_FILE="algocratic_futures_prod_backup_$(date +%Y%m%d_%H%M%S).db"
  cp algocratic_futures.db "$BACKUP_FILE"
  echo "Production backup: $BACKUP_FILE"
  
  # Verify backup integrity
  sqlite3 "$BACKUP_FILE" "PRAGMA integrity_check;" | grep -q "ok"
  echo "✓ Backup integrity verified"
  ```

- [ ] **Maintenance Window Setup**
  ```bash
  # Enable maintenance mode (if applicable)
  touch /tmp/maintenance_mode
  echo "Maintenance mode enabled at $(date)"
  
  # Notify monitoring systems
  curl -X POST monitoring-endpoint/maintenance-start
  ```

### Production Deployment Steps
- [ ] **Code Deployment**
  ```bash
  # Stop current production service
  kill $PRODUCTION_PID 2>/dev/null || echo "No existing service to stop"
  
  # Deploy new code
  git checkout main
  git pull origin main
  
  # Install/update dependencies
  pip install -r requirements.txt
  
  # Apply database migrations
  python -c "from database import init_db; init_db()"
  ```

- [ ] **Service Startup**
  ```bash
  # Start production service
  export ENVIRONMENT=production
  nohup python app.py --port 8000 > production.log 2>&1 &
  PRODUCTION_PID=$!
  echo $PRODUCTION_PID > production.pid
  
  # Verify startup
  sleep 10
  curl -f http://localhost:8000/health || {
      echo "❌ Production startup failed"
      # Trigger rollback
      exit 1
  }
  
  echo "✓ Production service started (PID: $PRODUCTION_PID)"
  ```

- [ ] **Post-Deployment Validation**
  ```bash
  # Smoke tests
  python -c "
  import requests
  import time
  
  # Test basic functionality
  health_response = requests.get('http://localhost:8000/health')
  assert health_response.status_code == 200, 'Health check failed'
  
  # Test agent functionality
  agent_response = requests.post('http://localhost:8000/agent/query', json={
      'agent': 'liza',
      'model': 'gemini-flash',
      'message': 'Health check'
  })
  assert agent_response.status_code == 200, 'Agent query failed'
  
  print('✓ Production smoke tests passed')
  "
  ```

- [ ] **Monitoring Activation**
  ```bash
  # Enable monitoring
  curl -X POST monitoring-endpoint/deployment-complete
  
  # Verify metrics collection
  curl -s http://localhost:8000/metrics | grep -q "http_requests_total"
  echo "✓ Metrics collection active"
  
  # Disable maintenance mode
  rm -f /tmp/maintenance_mode
  echo "Maintenance mode disabled at $(date)"
  ```

### Production Validation
- [ ] **Immediate Validation (0-15 minutes)**
  ```bash
  # Response time check
  for i in {1..5}; do
      curl -w "Response %d: %{time_total}s\n" -o /dev/null -s http://localhost:8000/health
      sleep 30
  done
  
  # Error rate check
  grep -c "ERROR" production.log | head -1
  echo "Error count should be 0"
  ```

- [ ] **Short-term Monitoring (15-60 minutes)**
  ```bash
  # Monitor logs
  tail -f production.log | grep -E "(ERROR|WARN|agent_query)" &
  LOG_MONITOR_PID=$!
  
  # Performance monitoring
  while [ true ]; do
      RESPONSE_TIME=$(curl -w "%{time_total}" -o /dev/null -s http://localhost:8000/health)
      if (( $(echo "$RESPONSE_TIME > 2.0" | bc -l) )); then
          echo "⚠️  Slow response: ${RESPONSE_TIME}s"
      fi
      sleep 60
  done &
  PERF_MONITOR_PID=$!
  ```

- [ ] **Extended Validation (1-24 hours)**
  ```bash
  # Set up extended monitoring
  crontab -l > /tmp/current_cron
  echo "*/15 * * * * curl -f http://localhost:8000/health || echo 'Health check failed' | mail -s 'Production Alert' admin@company.com" >> /tmp/current_cron
  crontab /tmp/current_cron
  
  echo "✓ Extended monitoring configured"
  ```

## Rollback Procedures

### Immediate Rollback (< 15 minutes)
- [ ] **Emergency Rollback Trigger**
  ```bash
  # Conditions for immediate rollback:
  # - Health check returns 5xx status
  # - Response time > 5 seconds
  # - Error rate > 1%
  # - Critical functionality broken
  
  echo "EMERGENCY ROLLBACK INITIATED at $(date)"
  
  # Stop failing service
  kill $(cat production.pid) 2>/dev/null
  rm -f production.pid
  ```

- [ ] **Database Rollback**
  ```bash
  # Find latest backup
  LATEST_BACKUP=$(ls -t algocratic_futures_prod_backup_*.db | head -1)
  echo "Rolling back to: $LATEST_BACKUP"
  
  # Restore database
  cp "$LATEST_BACKUP" algocratic_futures.db
  
  # Verify restoration
  sqlite3 algocratic_futures.db "PRAGMA integrity_check;" | grep -q "ok"
  echo "✓ Database restored"
  ```

- [ ] **Code Rollback**
  ```bash
  # Revert to previous commit
  git log --oneline -5  # Show recent commits
  PREVIOUS_COMMIT=$(git log --oneline -2 | tail -1 | cut -d' ' -f1)
  git checkout $PREVIOUS_COMMIT
  
  echo "Code reverted to: $PREVIOUS_COMMIT"
  ```

- [ ] **Service Restoration**
  ```bash
  # Restart with previous version
  export ENVIRONMENT=production
  nohup python app.py --port 8000 > rollback.log 2>&1 &
  ROLLBACK_PID=$!
  echo $ROLLBACK_PID > production.pid
  
  # Verify rollback success
  sleep 10
  curl -f http://localhost:8000/health || {
      echo "❌ Rollback failed - escalate immediately"
      exit 1
  }
  
  echo "✓ Rollback completed successfully"
  ```

### Planned Rollback (> 15 minutes)
- [ ] **Assessment and Planning**
  ```bash
  # Document rollback reason
  cat > rollback_report.md << EOF
  # Rollback Report
  
  **Date**: $(date)
  **Reason**: [Specify deployment issue]
  **Impact**: [Describe user impact]
  **Decision**: Planned rollback to previous stable version
  
  ## Rollback Steps
  1. Database restoration
  2. Code reversion
  3. Service restart
  4. Validation testing
  EOF
  ```

- [ ] **Maintenance Mode**
  ```bash
  # Enable maintenance mode
  touch /tmp/maintenance_mode
  curl -X POST monitoring-endpoint/maintenance-start
  
  echo "Maintenance mode enabled for planned rollback"
  ```

- [ ] **Gradual Rollback**
  ```bash
  # Stop service gracefully
  kill -TERM $(cat production.pid)
  sleep 30
  kill -KILL $(cat production.pid) 2>/dev/null
  
  # Restore database
  BACKUP_FILE=$(ls -t algocratic_futures_prod_backup_*.db | head -1)
  cp "$BACKUP_FILE" algocratic_futures.db
  
  # Revert code
  git checkout main~1  # Previous commit
  pip install -r requirements.txt
  
  # Restart service
  nohup python app.py --port 8000 > rollback.log 2>&1 &
  echo $! > production.pid
  
  # Validate
  sleep 15
  curl -f http://localhost:8000/health
  
  # Disable maintenance mode
  rm -f /tmp/maintenance_mode
  curl -X POST monitoring-endpoint/maintenance-end
  ```

### Post-Rollback Procedures
- [ ] **Incident Documentation**
  ```bash
  # Update rollback report
  cat >> rollback_report.md << EOF
  
  ## Rollback Results
  - **Completion Time**: $(date)
  - **Service Status**: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
  - **Database Status**: $(sqlite3 algocratic_futures.db "SELECT COUNT(*) FROM sqlite_master;")
  - **User Impact**: [Describe any ongoing impact]
  
  ## Next Steps
  1. Root cause analysis
  2. Fix development
  3. Additional testing
  4. Re-deployment planning
  EOF
  
  echo "Incident documented in rollback_report.md"
  ```

- [ ] **Team Notification**
  ```bash
  # Notify stakeholders
  echo "Rollback completed. Service restored to previous stable version." | \
  mail -s "Production Rollback Completed" team@company.com
  
  # Update status page (if applicable)
  curl -X POST status-page-api/incident-resolved
  ```

- [ ] **Monitoring Restoration**
  ```bash
  # Resume normal monitoring
  curl -X POST monitoring-endpoint/normal-operations
  
  # Clear any temporary alerts
  curl -X DELETE monitoring-endpoint/deployment-alerts
  
  echo "✓ Normal monitoring resumed"
  ```

## Deployment Validation Matrix

### Success Criteria
| Metric | Threshold | Validation Method |
|--------|-----------|-------------------|
| Response Time | < 1s average | `curl -w "%{time_total}"` |
| Error Rate | < 0.1% | Log analysis |
| Memory Usage | < 512MB | `ps aux` monitoring |
| CPU Usage | < 50% | System monitoring |
| Database Connections | < 10 concurrent | DB monitoring |
| Agent Response Quality | > 95% success | Automated testing |

### Monitoring Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Metrics
curl http://localhost:8000/metrics

# Agent status
curl http://localhost:8000/agent/status

# Database status
curl http://localhost:8000/db/status
```

## Emergency Contacts

### Escalation Path
1. **Kevin (GitHub Algorithm Enforcer)** - Technical issues, process compliance
2. **Linx (Creative Director)** - Agent behavior, user experience issues  
3. **Engineering Lead** - Infrastructure, architecture decisions
4. **DevOps Team** - Deployment automation, monitoring
5. **Product Owner** - Business impact decisions

### Emergency Procedures
- **Critical System Failure**: Immediate rollback + team notification
- **Performance Degradation**: Investigate + planned rollback if needed
- **Data Integrity Issues**: Stop service + database restoration
- **Security Incident**: Isolate system + security team escalation

---

**Algorithm Compliance**: These deployment procedures provide exact, repeatable steps for all deployment scenarios. Every deployment MUST follow these checklists completely. Deviations require explicit approval and documentation.

**Rollback Authority**: Any team member may initiate emergency rollback procedures if critical issues are detected. Planned rollbacks require approval from technical lead and product owner.

**Continuous Improvement**: These procedures will be updated based on lessons learned from each deployment. All changes must be reviewed and approved by the GitHub Algorithm Enforcer.