# AI Code Review Setup

*Three steps to intelligent code reviews*

## Quick Start

### 1. Add Your API Key
```bash
# Repository Settings → Secrets → Add secret
ANTHROPIC_API_KEY=your_key_here
```

### 2. Create a Pull Request
```bash
git checkout -b feature/your-change
git commit -m "your changes"
git push -u origin feature/your-change
gh pr create
```

### 3. Get AI Review
Your PR triggers automatic AI review within minutes. Claude analyzes:
- Code quality and patterns
- Security considerations  
- Performance implications
- Algorithmic compliance

*That's it. The AI reviewer becomes part of your workflow.*

---

**Note**: This is Kevin's prototype AI review system. Feedback shapes the future.