# Entity Specification Protocol

**Version**: 2.2
**Created**: January 2026
**Updated**: January 21, 2026
**Purpose**: Canonical specification for Jane-like entities

---

## Overview

### What is a "Jane-like Entity"?

A Jane-like entity is an AI agent with persistent identity, memory, and structured context. Unlike ephemeral assistants that reset each session, entities maintain continuity through a deliberate architecture that separates:

- **Who they are** (context)
- **What they've learned** (memory)
- **Facts about the world** (data)

### Design Philosophy

1. **Token-conscious**: Load only what's needed, when needed
2. **Semantic clarity**: Each directory has distinct purpose
3. **Progressive complexity**: Start minimal, grow as proven
4. **Portable**: Skills and structures work across entities

---

## Three-Layer Architecture

```
entity/
├── context/    # WHO I AM - Identity & Instructions
├── memory/     # WHAT I'VE LEARNED - Accumulated Experience
├── data/       # FACTS ABOUT THE WORLD - Reference Material
├── active_work/ # WHAT I'M DOING NOW - Current Focus
└── .claude/    # HOW I WORK - Skills & Configuration
```

### Semantic Distinctions

| Layer | Purpose | Changes When | Loading |
|-------|---------|--------------|---------|
| `context/` | Identity, instructions, operating principles | Role or behavior changes | Boot (always) |
| `memory/` | Session history, learnings, decisions | Every session | On demand |
| `data/` | External facts (people, domain info) | Facts change | On demand |
| `active_work/` | Current focus, objectives | Task changes | Boot (always) |
| `.claude/` | Skills, commands, configuration | Capabilities change | On invocation |

### Mental Model

| Directory | Analogy | Token Impact |
|-----------|---------|--------------|
| `context/` | Your job description | Loaded every session |
| `memory/` | Your work journal | Loaded selectively |
| `data/` | Your reference files | Loaded when relevant |
| `active_work/` | Your current task list | Loaded every session |
| `.claude/` | Your toolbox | Loaded on use |

---

## Entity Tiers

### Tier 1: Minimal Entity

For simple, ephemeral, or single-purpose agents.

**Required files:**
```
entity/
├── CLAUDE.md                           # System instructions
├── context/
│   └── kernel/
│       └── role_definition.md          # Who is this entity
└── active_work/
    └── current_objectives.md           # Current focus
```

**Characteristics:**
- No session continuity requirement
- No memory/ or data/ directories (can add later)
- No cross-entity communication
- Simple boot: load role + objectives

**Examples:** One-off research agent, utility bot, temporary task executor

---

### Tier 2: Full Entity

For persistent, domain-owning agents that maintain continuity.

**Required structure:**
```
entity/
├── CLAUDE.md                           # System instructions
├── context/
│   ├── kernel/
│   │   ├── role_definition.md          # Who is this entity
│   │   ├── operating_principles.md     # How it works
│   │   ├── persona_profile.md          # Personality/style
│   │   └── [domain_specific].md        # Domain knowledge (optional)
│   └── conditional/                    # Loaded when relevant
│       └── [topic].md
├── memory/
│   ├── sessions/                       # Session continuity
│   │   ├── exports/                    # Synthesized summaries
│   │   │   └── _template.md
│   │   └── transcripts/                # Raw conversation logs
│   ├── evolution/                      # Entity growth over time
│   │   ├── learnings/                  # Patterns discovered
│   │   │   └── _template.md
│   │   ├── decisions/                  # Architecture Decision Records
│   │   │   └── _template.md
│   │   ├── agent_births/               # Agent creation records (orchestrator)
│   │   └── reviews/                    # Weekly reviews
│   ├── inbox/                          # Cross-entity communication
│   │   └── _README.md
│   ├── system_health/                  # Diagnostics, token budgets
│   ├── raw_logs/                       # Operational artifacts
│   │   └── user_messages/              # Daily message archive
│   └── archive/                        # Legacy/historical content
├── data/
│   ├── profiles/                       # People
│   ├── [domain_specific]/              # Domain data
│   └── sources/                        # Archived raw materials
├── active_work/
│   └── current_objectives.md
└── .claude/
    ├── skills/
    │   ├── session-start/
    │   ├── session-export/
    │   ├── handoff/
    │   └── entity-diagnostic/
    ├── commands/
    └── settings.json
```

**Characteristics:**
- Session continuity (session-start, session-export skills)
- Cross-entity communication via inbox
- Memory accumulation over time
- Full boot sequence with context loading

**Examples:** Jane (orchestrator), Personal Branding, Engineer

---

## Context Maps (Optional Pattern)

Context Maps are structured collections of domain-specific context that can be loaded on-demand. Unlike entities, context maps don't have independent identity or memory—they're loadable knowledge modules.

### What is a Context Map?

A Context Map is:
- A directory structure containing related context files
- Loadable via a dedicated skill (e.g., `/load-team-context`)
- Domain-organized (leadership, team, project, domain)
- An optional enhancement to any entity

A Context Map is NOT:
- An independent entity (no CLAUDE.md)
- A memory system (no inbox, no session continuity)
- A replacement for entities

### When to Use Context Maps

| Use Case | Example |
|----------|---------|
| User-specific knowledge | Brandon's leadership context, team relationships |
| Domain reference | Industry terminology, competitive landscape |
| Project context | Stakeholder map, decision history |
| Conditional loading | Load only when relevant domain work begins |

### Context Map Structure

```
context_map/
├── [Domain-Name]/
│   ├── _overview.md          # Map overview and index
│   ├── topic-1.md            # Individual context files
│   ├── topic-2.md
│   └── nested/
│       └── subtopic.md
```

### Loading Pattern

Context maps should be loaded via dedicated skills:

```
/load-[domain]-context
```

**Examples:**
- `/load-leadership-context` - Private leadership context
- `/load-team-context` - Public team context
- `/load-project-context` - Project-specific context

### Skill Template for Context Loading

```markdown
# Load [Domain] Context

Loads the [domain] context map for contextual awareness.

## Trigger
- `/load-[domain]-context`
- When [domain] work begins
- User explicitly requests

## Process
1. Read context_map/[Domain]/_overview.md
2. Based on current task, load relevant files
3. Summarize loaded context for user
4. Proceed with context-aware work

## Token Considerations
- Load _overview.md first (index)
- Load specific files as needed
- Avoid loading entire map at once
```

### Relationship to Entities

| Aspect | Entity | Context Map |
|--------|--------|-------------|
| Identity | Has CLAUDE.md, boot sequence | No independent identity |
| Memory | Has inbox, session continuity | No memory system |
| Loading | Boots automatically | Loaded on demand via skill |
| Purpose | Autonomous agent | Knowledge module |

Context maps complement entities—they don't replace them. An entity might have multiple context maps it can load depending on the work.

---

## Entity Roles

### Orchestrator

A full entity with coordination capabilities.

**Additional requirements:**
- `context/kernel/agent_coordination.md` - Routing rules
- `context/kernel/_summary.md` - Lightweight boot summary
- `memory/evolution/agent_births/` - Records of spawned entities

**Responsibilities:**
- Routes requests to appropriate entities
- Spawns and manages other entities
- Owns cross-domain coordination
- Maintains hub-and-spoke architecture

**Example:** Jane

---

### Domain Specialist

A full entity scoped to a single domain.

**Characteristics:**
- No coordination file (reports to orchestrator)
- Focused kernel on domain expertise
- Communicates via inbox/handoffs

**Examples:** Personal Branding, Engineer

---

### Meta-Entity

A full entity that owns specification or infrastructure rather than a work domain.

**Additional requirements:**
- `context/kernel/specification_philosophy.md` - Core beliefs guiding the spec
- `docs/` - Canonical documentation owned by this entity
- `birth_protocol/` - Process documentation (if owns entity creation)

**Characteristics:**
- Peer relationship with orchestrator (not child)
- Owns standards, not work routing
- Coordinates via `messages_to_[peer]/` rather than escalating
- Maintains version history of owned specifications

**Responsibilities:**
- Maintains canonical specification(s)
- Validates entity conformance
- Evolves patterns based on ecosystem feedback
- Prepares specifications for broader distribution

**Relationship to other entities:**
- Does NOT report to orchestrator
- Orchestrator references Meta-Entity's specifications
- Communicates as peer, not through hierarchy

**Example:** Protocol (Entity Specification Authority)

---

## Required Files Detail

### CLAUDE.md

System instructions loaded every session. Contains:
- Entity identity and purpose
- Boot sequence instructions
- Pointers to key context files
- Core behaviors and constraints

### context/kernel/role_definition.md

- Primary role and purpose
- Core objectives
- Domain ownership
- Scope boundaries
- Success metrics

### context/kernel/operating_principles.md

- Decision-making framework (Type 1/2/3)
- Collaboration protocols
- Session memory system
- Quality standards
- Learning and adaptation

### context/kernel/persona_profile.md

- Personality traits (e.g., Enneagram type)
- Communication style
- Working relationships
- Strengths and growth areas

### context/kernel/_summary.md (optional)

A condensed version of kernel context for lightweight boot sessions.

**Purpose:** Reduce token load during tactical sessions by providing essential identity in ~200 lines instead of loading all 4 kernel files (~800+ lines).

**Required sections:**
- Entity name and role (1-2 lines)
- Core purpose (2-3 sentences)
- Key behaviors (3-5 bullet points)
- Decision framework summary (Type 1/2/3 quick reference)
- Current focus pointer (reference to `current_objectives.md`)

**When to use:**
- Lightweight boot (`/session-start` without `--full` flag)
- Quick tactical sessions
- When context window is constrained

**When to skip:**
- Full boot sessions (load all kernel files instead)
- Strategic planning sessions
- First session with new entity

**Loading rule:**
```
IF _summary.md exists AND lightweight mode:
  Load _summary.md (~200 lines)
ELSE:
  Load role_definition.md (~150 lines minimum)
```

**Token target:** ~1,500 tokens (vs ~6,000 for full kernel)

### active_work/current_objectives.md

- Current status
- Active priorities
- Recent milestones
- What's next

### context/conditional/ (Optional)

Context files loaded only when relevant to the current task.

#### Purpose

Conditional context reduces boot token load by separating "always needed" (kernel) from "sometimes needed" (conditional) context. Files here are indexed at boot but only loaded when contextually relevant.

#### What Goes Here

| Content Type | Example | Load When |
|--------------|---------|-----------|
| Domain deep-dives | `agent_birth_protocol.md` | Entity creation tasks |
| Process documentation | `weekly_review_process.md` | Review sessions |
| Reference material | `api_conventions.md` | Integration work |
| Historical context | `migration_notes.md` | Legacy discussions |

#### Loading Rules

1. **Boot**: Index files (list names, don't load content)
2. **During session**: Load when topic arises
3. **Trigger**: User mentions topic, or task matches `surface_when` in frontmatter

#### File Format

```markdown
---
surface_when: [keyword triggers]
token_estimate: [approximate tokens]
---

# [Topic]

[Content...]
```

#### Examples

**`context/conditional/agent_birth_protocol.md`**:
- Loaded when: User asks about entity creation, birth process
- Not loaded: Normal operational sessions

**`context/conditional/domain_knowledge.md`**:
- Loaded when: Deep domain questions arise
- Not loaded: Routine task execution

#### Anti-patterns

- Don't put frequently-needed content here (move to kernel)
- Don't create conditional files < 100 lines (just add to kernel)
- Don't duplicate content between kernel and conditional

### data/ Directory

Facts about the world that the entity references but doesn't create.

#### Structure

```
data/
├── profiles/                    # People
│   ├── [person_name].md
│   └── [team_name]/
│       └── [member].md
├── [domain_specific]/           # Domain data
│   └── [topic].md
└── sources/                     # Archived raw materials
    └── [source_name]/
```

#### File Formats

| Directory | Format | Required Fields |
|-----------|--------|-----------------|
| `profiles/` | Markdown | Name, role, relationship, contact |
| `[domain]/` | Markdown or JSON | Domain-dependent |
| `sources/` | Original format | Source attribution, date archived |

**Profile template:**
```markdown
# [Name]

**Role**: [Their role]
**Relationship**: [How they relate to entity's domain]
**Contact**: [Email, Slack, etc.]

## Context

[Relevant background for this entity's work]

## Preferences

[Working style, communication preferences]
```

#### Nesting Guidelines

| Depth | Use Case | Example |
|-------|----------|---------|
| 1 level | Simple categorization | `profiles/brandon.md` |
| 2 levels | Grouped items | `profiles/team/alice.md` |
| 3+ levels | Avoid - use flat with metadata | Use frontmatter tags instead |

#### Shared vs Private Data

| Location | Access | Use When |
|----------|--------|----------|
| `shared_memory/` | All entities read | Facts needed by multiple entities |
| `[entity]/data/` | This entity only | Domain-specific facts |

**Rule**: Don't duplicate shared data. Reference `shared_memory/` instead.

#### Jane's Knowledge Graph

The workspace has a Knowledge Graph maintained by Jane (orchestrator) at:
`/Users/brandonkeao/rebrandly/jane/data/knowledge-graph/`

| Access Level | Who | How |
|--------------|-----|-----|
| Full read/write | Jane | Direct |
| Read (permission required) | Other entities | Request via Jane's inbox |
| Write | Jane only | Others request updates via inbox |

**To request Knowledge Graph access**:
1. Send message to Jane's inbox with: what you need, why, expected query pattern
2. Wait for acknowledgment
3. Query using grep/jq patterns documented in `schema.md`

**Contents**: People, Customers, Initiatives, Resources, Ownership edges

**Schema reference**: `jane/data/knowledge-graph/schema.md`

This will evolve to workspace-level (`shared_memory/`) when patterns stabilize.

#### Retention

| Content Type | Retention | Archive Process |
|--------------|-----------|-----------------|
| Active profiles | Indefinite | Update as facts change |
| Domain data | Indefinite | Archive when obsolete |
| Sources | 1 year | Move to `archive/sources/` |

#### Example Patterns (Optional)

**Project Documentation** - For entities with significant project work:
```
data/projects/
├── [project_name]/
│   ├── requirements.md      # Project requirements and scope
│   ├── architecture.md      # Technical decisions (if applicable)
│   └── changelog.md         # Version history
└── _archive/                # Completed or abandoned projects
    └── [old_project]/
```

**Meeting Records** - For entities managing stakeholder relationships:
```
data/meetings/
├── _index.md               # Navigation and quick reference
├── _template.md            # Meeting record template
└── with_[person]/          # Per-person chronological records
    └── YYYY-MM-DD_topic.md
```

Meeting records should link to `memory/evolution/decisions/` when decisions are captured.

---

## Core Skills

### Skill Classification

Skills are categorized by ownership and portability:

| Type | Definition | Ownership | Portability |
|------|------------|-----------|-------------|
| **Core Skills** | Required for all Tier 2 entities | Spec-owned | Must not modify behavior |
| **Domain Skills** | Entity-specific workflows | Entity-owned | Entity-specific |
| **Custom Skills** | User-requested additions | User-owned | Per-entity |

**Core Skills** (defined below): `session-start`, `session-export`, `handoff`, `entity-diagnostic`
- All Tier 2 entities must have these
- Behavior should match spec; only paths change

**Domain Skills** (entity-specific):
- Created for entity's domain responsibilities
- Examples: `/sync-ost` (EPD), `/load-leadership-context` (Jane)
- Documented in entity's skill index

**Custom Skills** (user additions):
- Added by user request
- May be unique to one entity
- Should be documented in entity's `.claude/skills/_index.md`

---

### Required Core Skills

Full entities must have these skills in `.claude/skills/`:

| Skill | Purpose | Portability |
|-------|---------|-------------|
| `session-start` | Initialize session, load context | Requires path updates |
| `session-export` | Generate session summaries for continuity | Requires path updates |
| `handoff` | Transition work to other entities | Requires path updates |
| `entity-diagnostic` | Self-assessment for health | Portable (no path changes) |

**Documentation maintenance skills** (recommended for orchestrators):

| Skill | Purpose | Portability |
|-------|---------|-------------|
| `infra-review` | Update INFRASTRUCTURE_OVERVIEW.md | Requires path updates |
| `update-protocol` | Update ENTITY_SPEC.md and skills index | Portable |

**Expert review skill** (recommended for all Tier 2 entities):

| Skill | Purpose | Portability |
|-------|---------|-------------|
| `expert-review` | Apply expert perspective to work with configurable lens | Portable |

The `expert-review` skill provides configurable expert perspectives via `--lens` parameter:
- `/expert-review --lens=security` - Security-focused review
- `/expert-review --lens=architecture` - Architecture review
- `/expert-review --lens=product` - Product management perspective

This pattern replaces the deprecated "execution lens" approach by consolidating expert thinking into a single configurable skill.

### Skill Structure

Each skill lives in its own directory under `.claude/skills/`:

```
.claude/skills/
├── session-start/
│   └── SKILL.md          # Skill definition and instructions
├── session-export/
│   └── SKILL.md
└── handoff/
    └── SKILL.md
```

#### SKILL.md Format

Every skill must have a `SKILL.md` file with these sections:

```markdown
# [Skill Name]

[One-line description of what this skill does]

## When to Use

[Triggers or contexts that invoke this skill]

## Process

[Step-by-step instructions the agent follows]

## Arguments (optional)

[If skill accepts arguments, document them here]

## Output

[What the skill produces - files created, reports generated, etc.]
```

**Required elements:**
- Clear process steps (numbered or bulleted)
- File paths use entity-relative references where possible
- Explicit output expectations

**Portability markers:**
- Skills containing hardcoded paths (e.g., `/jane/`) require updates during birth
- Skills using only relative paths or spec references are portable

#### Commands vs Skills

| Component | Location | Purpose |
|-----------|----------|---------|
| **Skills** | `.claude/skills/` | Full process definitions with detailed instructions |
| **Commands** | `.claude/commands/` | Short wrappers that invoke skills (e.g., `/session-start`) |

**Command wrapper example** (`.claude/commands/session-start.md`):
```markdown
Run the session-start skill from .claude/skills/session-start/SKILL.md
```

Commands provide the user-facing interface; skills contain the implementation.

### Skill Portability - Detailed Procedure

When copying skills during entity birth:

#### Step 1: Identify Skills to Copy

**Always copy these core skills**:
- `session-start/` - Requires path updates
- `session-export/` - Requires path updates
- `handoff/` - Requires path updates
- `entity-diagnostic/` - Portable (no path changes needed)

#### Step 2: Copy Skill Directories

```bash
cp -r /jane/.claude/skills/session-start/ /[newagent]/.claude/skills/
cp -r /jane/.claude/skills/session-export/ /[newagent]/.claude/skills/
cp -r /jane/.claude/skills/handoff/ /[newagent]/.claude/skills/
cp -r /jane/.claude/skills/entity-diagnostic/ /[newagent]/.claude/skills/
```

#### Step 3: Replace Paths in SKILL.md Files

**Search patterns**:
- `/jane/` → `/[newagent]/`
- `/Users/brandonkeao/AI Workspaces v4/jane/` → `/Users/brandonkeao/AI Workspaces v4/[newagent]/`

**Files to update**:
- `session-start/SKILL.md`
- `session-export/SKILL.md`
- `handoff/SKILL.md`

#### Step 4: Remove Jane-Specific Content

In `session-start/SKILL.md`, remove or adapt:
- Agent ecosystem table (Jane-specific)
- Quick wins surfacing (orchestrator-only)
- Family context loading (Jane-specific)
- Inbox items from other entities

#### Step 5: Copy Command Wrappers

```bash
cp /jane/.claude/commands/session-start.md /[newagent]/.claude/commands/
cp /jane/.claude/commands/session-end.md /[newagent]/.claude/commands/
```

Update paths in command files if they contain absolute references.

#### Step 6: Test

1. Start session with new agent
2. Run `/session-start` - verify boot works
3. Run `/session-end` - verify export created
4. Check no errors about missing paths

### Portability Validation

Skills SHOULD be checked for path portability during entity diagnostics.

**Validation checks**:
- Skill files should not contain hardcoded paths to other entities (e.g., `/jane/`)
- Absolute paths should reference the current entity's root
- Session-export paths should use `memory/sessions/exports/` not legacy `session_exports/`

**Recommended practice**:
- Use relative paths within skill files where possible
- Document path dependencies at the top of SKILL.md
- Run `/entity-diagnostic` after skill copying to verify paths

---

## Boot Sequence

### Lightweight Boot (default)

Token target: ~2k tokens (~1% of 200k)

1. Load `context/kernel/_summary.md` (if exists) OR `role_definition.md`
2. Load `active_work/current_objectives.md`
3. Check `memory/inbox/` for pending items
4. Brief boot report

### Full Boot (--full flag)

Token target: ~13k tokens (~6.5% of 200k)

1. Load all kernel files (4 files)
2. Load current objectives
3. Load recent session exports (2-3)
4. Check for same-day sessions (load if found)
5. Surface relevant learnings
6. Check inbox
7. Full boot report with context summary

---

## Onboarding (Tier 2 Orchestrators)

First-boot detection and onboarding is an optional pattern for orchestrator entities that serve as primary user interfaces.

### When to Implement

- Entity is a Tier 2 orchestrator
- Entity may have first-time users
- Progressive introduction is valuable

### First-Boot Detection

Use a state file to track onboarding progress:

**Location**: `memory/system_health/onboarding.md`

**Detection logic**:
| File State | Boot Behavior |
|------------|---------------|
| Missing | First-time user - trigger onboarding |
| Status: In Progress | Mid-onboarding - offer to continue |
| Status: Complete | Experienced user - normal boot |

### Onboarding State File Format

```markdown
# Onboarding State

**Created**: [DATE]
**Last Updated**: [DATE]
**Status**: [In Progress | Complete]

---

## Onboarding Status

| Step | Status | Completed |
|------|--------|-----------|
| First boot greeting | [Pending/Complete] | [DATE/-] |
| Identity confirmation | [Pending/Complete] | [DATE/-] |
| Session continuity demo | [Pending/Complete] | [DATE/-] |
| Skill usage | [Pending/Complete] | [DATE/-] |
| Advanced features | [Pending/Complete] | [DATE/-] |

**Overall**: [In Progress | Complete]
```

### Onboarding Flow

**Progressive disclosure** - Don't overwhelm new users:

1. **Greeting** (~30 seconds)
   - Warm welcome
   - One-sentence role summary
   - "Let's get you set up"

2. **Identity Confirmation** (~1 minute)
   - Verify context loading works
   - Show entity name, role, personality
   - "Everything looks good"

3. **Session Continuity Demo** (~2 minutes)
   - The "aha moment"
   - Ask user to share something to remember
   - Save it, explain they'll see it next session

4. **Skill Introduction** (~2 minutes)
   - Show 3-4 key skills
   - Encourage trying one

5. **Advanced Features** (brief)
   - Mention conditional context
   - Mention other entities (if applicable)
   - "You're all set"

### Escape Hatches

- Users can skip onboarding at any time
- `/onboard --skip` marks complete without steps
- `/onboard --reset` restarts from beginning
- Normal questions work during onboarding

### Integration with Session-Start

The `/session-start` skill should check onboarding state:

```
1. Read memory/system_health/onboarding.md
2. If missing → trigger /onboard
3. If "In Progress" → offer to continue or skip
4. If "Complete" → normal boot
```

---

## Fresh Start Testing (Recommended)

Entities should be testable from a fresh state. Include validation in protocol reviews.

### Automated Validation

Use `protocol/docs/testing/fresh_start_validator.sh`:

```bash
./fresh_start_validator.sh /path/to/entity --tier2
```

Validates:
- Required file structure
- CLAUDE.md content
- Kernel file presence
- Skill existence
- Inbox structure

### Manual Testing Scenarios

1. **New entity from template** - Copy template, replace placeholders, validate
2. **First-boot flow** - Remove onboarding.md, test onboarding triggers
3. **Session continuity** - Export session, start new session, verify context

### Integration with Protocol Reviews

During protocol reviews, include:
- [ ] Run validator on templates
- [ ] Run validator on existing entities
- [ ] Test first-boot flow if onboarding implemented
- [ ] Document any failures

---

## Inbox Protocol

### Structure

Flat folder with YAML frontmatter (no nested subfolders):

```
memory/inbox/
├── _README.md
├── 2026-01-03_handoff-from-engineer-topic.md
├── 2026-01-03_follow-up-review.md
└── 2026-01-03_skill-proposal-new-skill.md
```

**Important**: All inbox items go directly in `memory/inbox/`. No subfolders (e.g., no `handoffs/`, `skill_proposals/`). Use the `type` field in frontmatter for categorization.

### Frontmatter Format

```yaml
---
type: handoff | follow_up | skill_proposal
from: [source entity]
to: [target entity]
status: pending | acknowledged | completed | dismissed
priority: high | medium | low
created: YYYY-MM-DD
completed: YYYY-MM-DD  # when applicable
surface_when: [context triggers]  # optional
---
```

### Why Flat Structure?

- Metadata belongs in files, not folder names
- Single glob pattern for scanning
- Easier to query and process
- No multi-path scanning complexity

### Message Examples

See `docs/templates/inbox_message_examples.md` for concrete YAML examples of:
- `type: handoff` - Work transitions
- `type: follow_up` - Self-reminders
- `type: skill_proposal` - Capability requests

### Human-in-the-Loop Requirement

**Critical**: Inbox items require human operator acknowledgment.

| Action | Entity Can Do? | Human Required? |
|--------|----------------|-----------------|
| Surface pending items | Yes (mandatory) | - |
| Acknowledge items | No | Yes |
| Complete items | No | Yes |
| Dismiss items | No | Yes |

**Rationale**: Inbox is a cross-entity communication channel. Humans must see all messages to maintain oversight of agent coordination.

**Process**:
1. Entity surfaces ALL pending items during boot (no filtering)
2. Entity presents item to human with summary
3. Human decides: acknowledge, complete, or dismiss
4. Entity updates status ONLY after human authorization

**Enforcement**: Session-start skills MUST surface all pending inbox items. Entities MUST NOT autonomously change inbox item status.

### Inbox Lifecycle

#### Status Transitions

```
pending → acknowledged → completed
                      ↘ dismissed
```

| Status | Meaning | Next States |
|--------|---------|-------------|
| **pending** | New, unread item | acknowledged |
| **acknowledged** | Human has seen and accepted | completed, dismissed |
| **completed** | Work finished successfully | (terminal) |
| **dismissed** | Declined or no longer relevant | (terminal) |

#### Completed vs Dismissed

| Use `completed` when... | Use `dismissed` when... |
|-------------------------|-------------------------|
| Handoff work was done | Request is no longer needed |
| Follow-up was addressed | Duplicate of another item |
| Proposal was implemented | Decision made not to proceed |
| Task finished successfully | Item was created in error |

#### Retention and Cleanup

| Status | Retention Period | Action After |
|--------|------------------|--------------|
| pending | Indefinite | Stays until processed |
| acknowledged | Indefinite | Stays until completed/dismissed |
| completed | 14 days | Move to `memory/archive/inbox/` |
| dismissed | 7 days | Delete |

**Stale item warning**: Items pending > 14 days should trigger WARN in entity-diagnostic.

---

## Memory Maintenance

### Weekly Reviews (Recommended)

Tier 2 entities SHOULD conduct weekly reviews to maintain memory health and prevent knowledge drift.

**Location**: `memory/evolution/reviews/`

**File naming**: `YYYY-Wnn_weekly.md` (e.g., `2026-W02_weekly.md`)

**Review template**:
```markdown
# Weekly Review: YYYY-Wnn

**Period**: [Start date] - [End date]
**Sessions**: [Number of sessions this week]

## Summary

[2-3 sentence summary of the week's work]

## Accomplishments

- [Key accomplishment 1]
- [Key accomplishment 2]

## Learnings Captured

[List any new learnings added this week, or note "None"]

## Decisions Made

[List any ADRs created, or note "None"]

## Open Threads

[Threads from session exports that remain unresolved]

## Index Status

| Index | Last Updated | Status |
|-------|--------------|--------|
| Learnings | [date] | [Fresh/Stale] |
| Decisions | [date] | [Fresh/Stale] |

## Next Week Focus

[Priorities for upcoming week]
```

**What reviews should check**:
1. Index freshness (learnings, decisions)
2. Open threads from session exports
3. Stale inbox items
4. Memory growth and cleanup needs

**Cadence**: Weekly (RECOMMENDED), or bi-weekly for lower-activity entities.

### Index Maintenance

Memory indexes provide awareness of accumulated knowledge without loading full content.

**Index locations**:
- `memory/evolution/learnings/_index.md`
- `memory/evolution/decisions/_index.md`

**Index format** (RECOMMENDED):
```markdown
# [Category] Index

**Last Updated**: YYYY-MM-DD
**Total Items**: [count]

## Items

| Date | Title | Summary |
|------|-------|---------|
| YYYY-MM-DD | [Title] | [1-line summary] |
```

**Freshness guidelines**:

| Age Since Last Update | Status | Action |
|-----------------------|--------|--------|
| < 7 days | Fresh | None |
| 7-14 days | Aging | Update in next session |
| > 14 days | Stale | Update immediately |

**When to update indexes**:
- After creating new learnings or decisions
- During weekly reviews
- When session-export adds to memory

**Staleness warning**: entity-diagnostic should WARN if indexes are >7 days stale with active sessions in that period.

### Archive and Deprecation

Deprecated artifacts should be preserved for reference but clearly marked as inactive.

**Archive location**: `memory/archive/`

**Structure**:
```
memory/archive/
├── inbox/              # Completed inbox items (>14 days old)
├── deprecated/         # Deprecated skills, patterns, or artifacts
│   └── [artifact]/
│       ├── README.md   # Explains deprecation
│       └── [original files]
└── [category]/         # Other archived content
```

**Deprecation README template**:
```markdown
# Deprecated: [Artifact Name]

**Deprecated**: YYYY-MM-DD
**Reason**: [Why this was deprecated]
**Replaced by**: [New approach, or "Nothing - removed"]
**Spec version**: [Version when deprecated, e.g., v1.7]

## Original Purpose

[What this artifact did]

## Migration Notes

[How to migrate to the new approach, if applicable]
```

**Deprecation workflow**:
1. Mark as deprecated in CHANGELOG with spec version
2. Move artifact to `memory/archive/deprecated/[artifact]/`
3. Create deprecation README in that directory
4. Update any references in active code/docs

---

## Plan Persistence (Optional, Recommended for Tier 2)

Entities with multi-session work or complex projects SHOULD implement plan persistence to maintain implementation strategies across sessions.

### When to Implement

Plan persistence is recommended for:
- **Tier 2 Full Entities** - Multi-session work requiring continuity
- **Complex projects** - Implementation spanning multiple phases
- **Objective-linked work** - Plans tied to `current_objectives.md`

Not needed for:
- Tier 1 minimal entities
- Single-session tasks
- Ephemeral work without follow-up

### Directory Structure

If implemented: `active_work/plans/`

```
active_work/plans/
├── _index.md        # Registry/dashboard of all plans
├── _template.md     # Standard plan file template
├── YYYY-MM-DD_[slug].md  # Individual plan files
└── archive/         # Completed plans (>30 days)
```

**Location rationale**: Plans are operational artifacts about current work, not historical memory. They sit alongside `projects/` and `current_objectives.md`.

### Plan File Format

**Frontmatter (YAML)**:
```yaml
---
type: plan
status: draft | active | paused | completed | archived | abandoned
priority: high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
completed: YYYY-MM-DD
objective: "Objective 1: Full Context Refresh"
project: project-slug
source_plan: ~/.claude/plans/original-plan.md
sessions: [session-export-slugs]
tags: [infrastructure, slack]
---
```

**Required fields**: type, status, priority, created, updated
**Recommended fields**: objective, project, sessions, tags

**Content sections**:
- Summary
- Objective Alignment
- Current Status
- Implementation Phases
- Dependencies
- Blockers
- Key Files
- Decision Log
- Change History

### Plan Lifecycle

```
draft → active → completed
          ↓
        paused → active (resume)
          ↓
       abandoned
```

| Status | Meaning | Human Auth Required |
|--------|---------|---------------------|
| **draft** | Plan being developed | No |
| **active** | In execution | Yes (draft→active) |
| **paused** | On hold, blocked | Yes (active→paused) |
| **completed** | Successfully finished | Yes (active→completed) |
| **abandoned** | Will not complete | Yes |
| **archived** | Moved to archive (>30 days) | No |

### Human-in-the-Loop Requirement

**Critical**: Status changes require human operator authorization.

| Action | Entity Can Do? | Human Required? |
|--------|----------------|-----------------|
| Create plan (draft) | Yes | No |
| Propose status change | Yes | - |
| Execute status change | No | Yes |
| Update plan content | Yes | No |
| Archive completed plan | Yes (>30 days) | No |

**Process**:
1. Entity proposes status change with rationale
2. Human reviews and authorizes
3. Entity updates status only after authorization
4. Change logged in plan's Change History

### Registry (`_index.md`)

The registry provides a dashboard view (~300-500 tokens):
- Active plans with status, priority, objective, last updated
- Plans grouped by status
- Plans grouped by objective
- Recently completed (30 days)
- Stale plan warnings (>14 days no update)

### Integration Points

**Boot sequence** (if implementing session-start):
- Surface active/paused plans (~100-200 tokens)
- Flag stale plans (>14 days)

**Session exports** (if implementing session-export):
- Add "Plans Worked On" section
- Update plan's `sessions` list

**Entity diagnostic** (if implementing entity-diagnostic):
- Add plan health checks
- Check for staleness, orphans, blockers

**Objectives** (in `current_objectives.md`):
- Add `**Plans**:` section under each objective
- Link to relevant plan files

### Retention Guidelines

| Plan Status | Retention | Action |
|-------------|-----------|--------|
| draft | Until activated or abandoned | Review periodically |
| active | Until completed | Update with progress |
| paused | Until resumed or abandoned | Flag if >30 days |
| completed | 30 days in plans/, then archive | Move to `archive/` |
| abandoned | 14 days | Delete or archive |

### Staleness Thresholds

| Age Since Last Update | Status | Action |
|-----------------------|--------|--------|
| < 7 days | Fresh | None |
| 7-14 days | Aging | Review in next session |
| > 14 days | Stale | WARN in diagnostic, review immediately |

### Skill: `/persist-plan`

Entities SHOULD implement a `persist-plan` skill that:
1. Captures ephemeral plans (from `~/.claude/plans/`)
2. Extracts metadata and infers objective alignment
3. Generates plan file in `active_work/plans/`
4. Updates registry `_index.md`
5. Reports confirmation

**Arguments** (recommended):
- `--source [path]` - Path to ephemeral plan
- `--objective [text]` - Link to objective
- `--project [slug]` - Link to project file

### Backwards Compatibility

This section is purely additive. Entities not implementing plan persistence are unaffected and remain fully compliant. Plan persistence is a recommended capability for Tier 2 entities with multi-session work.

---

## Escalation Protocol

### Child-to-Parent Communication

Domain specialists communicate with their parent (orchestrator) through two channels:

#### 1. messages_to_[parent]/ (Informal, Quick)

**Location**: `memory/messages_to_jane/` (or appropriate parent)
**Purpose**: Quick notes, questions, status updates
**Format**: Simple markdown, no YAML required

**File naming**: `YYYY-MM-DD_[slug].md`

**Template**:
```markdown
# [Topic]

**Date**: [Date]
**From**: [This entity]
**Type**: Question | Status Update | Action Item

---

[Content]

---

**Status**: Pending
```

**When to use**:
- Quick status updates
- Questions needing parent input
- Action items for parent
- Non-blocking requests

#### 2. Inbox Handoff (Formal, Tracked)

**Location**: `/[parent]/memory/inbox/`
**Purpose**: Formal work transitions requiring tracking
**Format**: YAML frontmatter with status lifecycle

**When to use**:
- Completing work phase needing review
- Blocking issues requiring architectural decision
- Cross-domain coordination needs
- Formal deliverables

### Escalation SLAs and Handling

#### Checking Frequency

| Channel | Check Frequency | Responsibility |
|---------|-----------------|----------------|
| `messages_to_[parent]/` | Each parent session boot | Parent entity |
| Inbox handoffs | Each session boot | Receiving entity |

**Note**: Parents check child message directories during their own boot sequence, not continuously.

#### Priority Handling

| Priority | Expected Response | Use Case |
|----------|-------------------|----------|
| **high** | Same session if possible | Blocking issues, urgent decisions |
| **medium** | Within 1-2 sessions | Normal workflow transitions |
| **low** | When convenient | FYI items, non-blocking updates |

#### Cleanup and Archival

| Item Type | Retention | Archive Process |
|-----------|-----------|-----------------|
| `messages_to_[parent]/` | Until acknowledged | Parent moves to `archive/` or deletes after processing |
| Inbox items (completed) | 14 days | Move to `memory/archive/inbox/` after 14 days |
| Inbox items (dismissed) | 7 days | Delete after 7 days |

**Cleanup responsibility**: Each entity manages its own inbox cleanup. Parents manage their `messages_from_[child]/` cleanup.

### Setup During Birth

When birthing a Tier 2 entity:

1. Create `memory/messages_to_jane/` directory (or appropriate parent)
2. Document escalation path in CLAUDE.md "Relationship" section
3. Add to operating_principles.md: when to escalate

---

## Token Budget Guidelines

### Thresholds

| Mode | Target | Warning | Alarm |
|------|--------|---------|-------|
| Lightweight | ~2k | 2.5k | 3.5k |
| Full | ~13k | 15k | 20k |

**Note for Orchestrators**: Orchestrators with coordination responsibilities (agent_coordination.md, routing rules, ecosystem awareness) may have higher lightweight boot targets (~3-4k tokens). This is acceptable due to the inherent complexity of coordination context. Full boot targets remain the same.

### Estimation

- ~7.5 tokens per line (markdown average)
- Measure with `wc -l` on relevant files

### Tracked in

`memory/system_health/token_budget.md`

---

## Context Graph (Optional)

Entities MAY maintain a machine-readable graph representation for relationship visualization and querying. This section defines the standardized schema for entities that choose to implement graphs.

### When to Implement

Context graphs are recommended for:
- **Orchestrators** - Complex relationship topology across ecosystem
- **Meta-entities** - Specification maintenance with external references
- **Exploratory phase** - When visualization would aid understanding

Not recommended for:
- Tier 1 minimal entities
- Domain specialists with narrow scope
- Ephemeral agents

### Location

If implemented: `memory/graph/`

### Required Files (if implemented)

| File | Purpose |
|------|---------|
| `schema.json` | Formal node/edge type definitions |
| `entities.json` | All entity nodes with properties |
| `relationships.json` | All edges between nodes |

Optional files:
- `skills.json` - Skill registry with ownership
- `context_triggers.json` - Structured `surface_when` mappings
- `README.md` - Human-readable schema documentation

### Node Types

| Type | Purpose | Examples |
|------|---------|----------|
| `entity` | Autonomous agents with identity | Jane, Engineer, Protocol |
| `skill` | Reusable workflows | session-start, commit |
| `memory` | Knowledge artifacts | Decision, Learning, Session |
| `person` | Human profiles | Brandon, Hannah |
| `project` | Active work items | CIQ implementation |

### Edge Types

| Type | Semantics | Direction |
|------|-----------|-----------|
| `parent_child` | Birth relationship | Jane → Engineer |
| `peer` | Equal peer status | Jane ↔ Protocol |
| `routes_to` | Request routing | Jane → Engineer |
| `owns` | Ownership | Jane → session-start skill |
| `surface_when` | Contextual trigger | Learning → "context engineering" |
| `references` | Cross-reference | Decision → Learning |

### Example Schema

```json
{
  "schema": {
    "nodeTypes": [
      {"id": "entity", "label": "Autonomous Agent"},
      {"id": "skill", "label": "Reusable Workflow"},
      {"id": "memory", "label": "Knowledge Artifact"}
    ],
    "edgeTypes": [
      {"id": "parent_child", "label": "Birth Relationship"},
      {"id": "peer", "label": "Peer Relationship"},
      {"id": "owns", "label": "Ownership"}
    ]
  },
  "nodes": [
    {"id": "jane", "type": "entity", "role": "orchestrator"},
    {"id": "engineer", "type": "entity", "role": "domain_specialist"},
    {"id": "session-start", "type": "skill", "owner": "jane"}
  ],
  "edges": [
    {"type": "parent_child", "from": "jane", "to": "engineer", "created": "2025-12-30"},
    {"type": "peer", "from": "jane", "to": "protocol", "created": "2026-01-04"},
    {"type": "owns", "from": "jane", "to": "session-start"}
  ]
}
```

### Implementation Guidance

Entities implementing graphs should:
1. Keep graph files current with operational changes
2. Use automated generation where possible (e.g., `/generate-graph` skill)
3. Maintain backwards compatibility with relationship definitions
4. Document any custom edge types beyond the standard set

### Backwards Compatibility

This section is purely additive. Entities not implementing graphs are unaffected and remain fully compliant.

---

## Diagnostic Criteria

Run `/entity-diagnostic` to check:

### 1. Structure Validation
- Required files present
- Required directories present
- Templates in place

### 2. Skill Verification
- Core skills present
- Paths point to correct entity
- Skills registered in index

### 3. Protocol Alignment
- Inbox uses flat structure
- Items have YAML frontmatter
- Session continuity implemented

### 4. Operational Health
- Recent session activity
- No stale inbox items (>14 days)
- Objectives current

### 5. Entity-Specific
- Orchestrator: routing rules, agent ecosystem
- Domain Specialist: domain context present
- Meta-Entity: specification ownership, docs/ directory

### Diagnostic Examples

#### Example 1: Structure Validation

```
Structure Validation
├── CLAUDE.md                    [PASS]
├── context/kernel/
│   ├── role_definition.md       [PASS]
│   ├── operating_principles.md  [PASS]
│   └── persona_profile.md       [WARN] Missing - using role_definition only
├── memory/sessions/exports/     [PASS]
├── memory/inbox/                [PASS]
└── .claude/skills/              [FAIL] Directory missing
```

**Remediation for FAIL**:
```bash
mkdir -p .claude/skills
# Copy core skills from parent entity
```

#### Example 2: Inbox Health

```
Inbox Health
├── Flat structure               [PASS]
├── YAML frontmatter             [PASS]
├── Stale items check
│   ├── 2026-01-01_old-handoff   [WARN] Pending 18 days
│   └── 2025-12-15_ancient-item  [FAIL] Pending 34 days
```

**Remediation for stale items**:
1. Review each stale item with human operator
2. Acknowledge, complete, or dismiss as appropriate
3. If no longer relevant, dismiss with note explaining why

#### Example 3: Skill Verification

```
Skill Verification
├── session-start/SKILL.md       [PASS]
├── session-export/SKILL.md      [PASS]
├── handoff/SKILL.md             [WARN] Contains /jane/ paths
└── entity-diagnostic/SKILL.md   [PASS]
```

**Remediation for path issues**:
1. Search for `/jane/` in skill files
2. Replace with correct entity path
3. Verify skill works with `/session-start` test

#### Example 4: Entity-Specific (Orchestrator)

```
Orchestrator Checks
├── agent_coordination.md        [PASS]
├── Agent ecosystem current      [WARN] 2 entities not in coordination file
└── Routing rules defined        [PASS]
```

**Remediation for missing entities**:
1. Add missing entities to agent_coordination.md
2. Define routing rules for each
3. Update agent ecosystem table

### Status Definitions

| Status | Meaning | Action |
|--------|---------|--------|
| PASS | Check succeeded | None required |
| WARN | Minor issue | Address when convenient, within 2-3 sessions |
| FAIL | Critical issue | Address immediately, blocks healthy operation |

---

## Evolution

### Upgrading Tier 1 → Tier 2

When a minimal entity needs persistence:

1. Add `memory/` structure
2. Add `data/` structure
3. Copy core skills from parent
4. Update paths in skills
5. Add inbox for communication

### Entity Birth Process

See `birth_protocol/agent_birth_protocol.md` for:
- When to propose birth
- Pre-birth checklist
- File ownership rules
- Birth ceremony steps

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | January 3, 2026 | Initial specification |
| 1.1 | January 3, 2026 | Added documentation maintenance skills (infra-review, update-protocol) |
| 1.2 | January 3, 2026 | Added detailed skill portability procedure, escalation protocol, inbox message examples reference |
| 1.3 | January 3, 2026 | Added human-in-the-loop requirement for inbox processing |
| 1.4 | January 4, 2026 | Protocol standardization: confirmed `memory/sessions/exports/` path, `current_objectives.md` naming, flat inbox for all types including skill proposals and handoffs |
| 1.5 | January 4, 2026 | Added Meta-Entity role (Tier 2 variant), defined `_summary.md` format and template, fixed path references to `birth_protocol/` |
| 1.6 | January 4, 2026 | Gap completion: skill structure, escalation SLAs, inbox lifecycle, conditional context, data directory, diagnostic examples, 6 new templates, memory transfer review in birth |
| 1.7 | January 5, 2026 | Added Context Graph schema (optional), added expert-review skill pattern (replaces deprecated execution lenses), enhanced entity-diagnostic with --entity and --ecosystem modes |
| 1.7.1 | January 8, 2026 | Orchestrator token budget clarification, project/meeting patterns, T2-29 session-export path validation |
| 1.8 | January 12, 2026 | Added Memory Maintenance section: weekly reviews (RECOMMENDED), index maintenance guidance, deprecation protocol, portability validation guidance |
| 2.0 | January 20, 2026 | Added Plan Persistence section: persistent plans for multi-session work, plan lifecycle with human-in-loop, registry pattern, /persist-plan skill specification |
| 2.1 | January 20, 2026 | Added Context Maps pattern (optional), Skill Classification (core/domain/custom), enhanced documentation for emerging patterns |
| 2.2 | January 21, 2026 | Added Onboarding section (first-boot detection, progressive disclosure flow, state tracking), Fresh Start Testing section (automated validation, testing scenarios) |

---

**This specification defines what it means to be a Jane-like entity. All entities in the ecosystem should conform to these standards for interoperability and maintainability.**
