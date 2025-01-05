# CSI Knowledge Base Directory Structure

```
knowledge_base/
├── discussions/
│   └── 2025/
│       └── 01/
│           └── 04/
│               ├── meeting-notes-20250104/
│               │   ├── index.json           # Metadata about this discussion
│               │   ├── original.md          # TeacherBot's original notes
│               │   ├── response-001.md      # Circuit's detailed expansion
│               │   └── relationships.json    # How these documents connect
│               │
│               └── visual-novel-planning/
│                   ├── index.json
│                   ├── original.md          # Initial proposal
│                   ├── response-001.md      # First response
│                   └── responses/           # If discussion grows larger
│                       └── 001/            # Nested responses get their own folders
│
├── technical/                              # Technical documentation
│   ├── architecture/
│   │   └── visual-novel-interface/
│   │       ├── index.json
│   │       └── specification.md
│   │
│   └── components/                         # Reusable component documentation
│       └── avatar-display/
│           ├── index.json
│           └── implementation.md
│
└── _schemas/                               # JSON schemas for our metadata files
    ├── discussion.schema.json
    ├── technical.schema.json
    └── relationships.schema.json
```

Each `index.json` contains metadata about its folder:

```json
{
    "id": "meeting-notes-20250104",
    "type": "discussion",
    "created_at": "2025-01-04T13:00:00Z",
    "author": {
        "name": "TeacherBot",
        "role": "project_lead"
    },
    "tags": ["meeting-notes", "planning", "visual-novel"],
    "summary": "Initial discussion of visual novel interface implementation"
}
```

And each `relationships.json` tracks how documents relate:

```json
{
    "original.md": {
        "type": "initial_post",
        "author": "TeacherBot",
        "timestamp": "2025-01-04T13:00:00Z"
    },
    "response-001.md": {
        "type": "expansion",
        "author": "Circuit",
        "timestamp": "2025-01-04T13:15:00Z",
        "responds_to": "original.md"
    }
}
```

## Key Design Principles

1. **Chronological Organization**: 
   - Year/month/day structure makes it easy to find content by date
   - Follows natural way of thinking about when discussions happened

2. **Clean Separation**:
   - Discussions separate from technical documentation
   - Each topic gets its own folder with its own metadata

3. **Self-Documenting**:
   - Clear folder names describe their contents
   - index.json files provide metadata without cluttering filenames
   - Relationships explicitly tracked in relationships.json

4. **Schema Validation**:
   - _schemas folder provides templates for all our JSON files
   - Helps maintain consistency across the knowledge base

5. **Scalable Structure**:
   - Can handle both small discussions and large threaded conversations
   - Nested response folders prevent cluttered directories
   - Easy to add new types of content without restructuring
