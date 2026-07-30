# GitHub Community Learning - Prototype Guide

## Quick Setup (10 minutes)

1. **Create GitHub Organization**
   ```bash
   # Use GitHub web interface or CLI
   gh org create cs101-fall2024 --description "CS101 Learning Community"
   ```

2. **Basic Repository Structure**
   ```
   cs101-fall2024/
   ├── assignments/        # Starter code for each assignment
   ├── submissions/        # Student PRs go here
   └── help-desk/         # Issues for questions
   ```

3. **Add Students & Mentors**
   - Students: Fork assignments → Code → Submit PR
   - Mentors: Watch help-desk → Answer issues
   - Instructor: Review PRs → Grade

## Simple Example Workflow

### Week 1: Hello World Assignment

1. **Instructor creates assignment:**
   ```python
   # assignments/week1-hello/main.py
   def greet(name):
       """Make this function return 'Hello, {name}!'"""
       pass  # Student implements this
   
   # assignments/week1-hello/test.py
   def test_greet():
       assert greet("World") == "Hello, World!"
   ```

2. **Student workflow:**
   - Fork `assignments/week1-hello`
   - Fix the code
   - Push to their fork
   - Create PR to `submissions/week1`

3. **Getting help:**
   - Student creates issue in `help-desk`
   - Title: "Week 1 - Can't pass test"
   - Mentor responds with guidance

## Customize the Prompt

Edit `.github/ISSUE_TEMPLATE/help_request.md`:

```markdown
---
name: Help Request
about: Get help from mentors
---

**Assignment:** [Week X - Name]
**Problem:** [What's not working?]
**What I tried:** [Your attempts]
**Error message:** [If any]

```

Adjust for your course needs - add debugging steps, require code snippets, or include specific tags for different help types.

## That's It!

- No servers to manage
- No databases to configure  
- Students get real GitHub experience
- Mentors volunteer through existing GitHub features

Start with 5 students, 1 mentor. Scale when it works.