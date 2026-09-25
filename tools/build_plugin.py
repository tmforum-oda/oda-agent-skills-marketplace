"""Reads: skills/**, knowledge/**.
Writes: dist/consumer/** and dist/creator/** (each a self-contained Claude
Code plugin: skills/ subset with knowledge/ path references rewritten to
${CLAUDE_PLUGIN_ROOT}/knowledge/..., a full verbatim copy of knowledge/, and
.claude-plugin/plugin.json).
Track: n/a -- packaging step, not part of either refresh track. Run after
any change to skills/ or knowledge/ to regenerate both distributable plugin
bundles in dist/.

tools/build_plugin.py -- package skills/ + knowledge/ as two separate
Claude Code plugins in dist/consumer/ and dist/creator/, published through
the oda-agent-skills-marketplace repo. The user explicitly chose to bundle
knowledge/ inside each plugin, accepting that it breaks the norm that
plugins should be small/fast (and that knowledge/ is duplicated a third
time, once per plugin, on top of the repo's own top-level copy), so each
plugin has zero dependency on any project-specific clone or directory
layout.

Two plugins, not one, because the skill set has two distinct audiences that
rarely overlap in a single install: consumers building a product using ODA
don't want the drafting/correction skills cluttering their skill list, and
vice versa for people extending ODA itself. Splitting them keeps each
plugin's skill list focused on what that audience actually invokes.

The one non-mechanical step this script exists to do: skills/*/SKILL.md
are authored with plain relative paths (knowledge/use-cases/...) so they
work unmodified for a direct clone, where the agent's cwd contains
knowledge/ as a sibling. A plugin installs to
~/.claude/plugins/cache/... instead -- NOT the user's project cwd -- so a
bare relative path would silently resolve against the wrong directory
there. Claude Code substitutes ${CLAUDE_PLUGIN_ROOT} to the plugin's real
install directory, but ONLY inside plugin skills, so baking that syntax
into the canonical skills/*/SKILL.md would make it inert (literal,
unsubstituted text) for the direct-clone case. Resolved by
keeping one canonical source (plain paths) and mechanically rewriting
`knowledge/` -> `${CLAUDE_PLUGIN_ROOT}/knowledge/` only in the copies
under dist/, the same "generate the packaged form, never hand-maintain
two versions" pattern this repo already uses for knowledge/ itself
(generated from references/).

Must be idempotent (spec.md principle 7): dist/ is deleted and rebuilt
from scratch every run, so two consecutive runs with no source changes
produce an identical file set and identical file content.

Every skill directory under skills/ must appear in exactly one of
CONSUMER_SKILLS, CREATOR_SKILLS, or INTERNAL_ONLY_SKILLS below -- main()
fails loudly if a skill is unclassified (new skill added, not sorted into
a bucket yet) or double-classified, rather than silently dropping it from
both plugins or shipping it in both.

Usage:
    python build_plugin.py
"""
import json
import os
import shutil

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
SKILLS_SRC = os.path.join(REPO_ROOT, "skills")
KNOWLEDGE_SRC = os.path.join(REPO_ROOT, "knowledge")
DIST_DIR = os.path.join(REPO_ROOT, "dist")

# Builds a product using ODA -- reads knowledge/, never writes it.
CONSUMER_SKILLS = {
    "check-usecase-maturity",
    "explain-etom-process",
    "recommend-oda-components-for-requirement",
    "decompose-requirement-against-oda",
    "capture-requirements-from-usecase",
    "generate-test-cases-from-usecase",
    "generate-api-conformance-tests",
    "generate-api-mocks-from-usecase",
    "generate-implementation-scaffold-from-usecase",
    "implement-oda-component",
    "draft-architecture-diagram-from-usecase",
    "draft-event-design-for-component",
    "validate-design-against-oda",
    "review-architecture-against-oda",
    "assess-change-impact",
    "audit-implementation-against-usecase",
    "audit-implementation-against-component",
    "deliver-oda-requirement",
}

# Extends/corrects ODA itself -- drafts new use cases, components, API
# extensions, and matrix corrections for submission back to TM Forum.
CREATOR_SKILLS = {
    "feedback-harvest-gaps-from-lessons-learned",
    "feedback-propose-matrix-correction",
    "draft-new-usecase-from-scenario",
    "propose-component-or-api-extension",
    "lint-usecase-draft",
}

# Repo-maintenance skill that writes to this repo's own knowledge/ (spec.md
# 12) -- not for external distribution in either plugin: a consumer or
# creator installing a plugin to build against/extend this corpus has no
# use for a skill that edits it in place, and shipping it invites someone
# running it against a knowledge/ they don't actually maintain (e.g. a
# sparse clone with no way to push changes back). Stays in skills/ -- and
# in this repo's own git history -- just never copied into dist/.
INTERNAL_ONLY_SKILLS = {"process-usecase-media", "process-component-media"}

# One or two realistic example prompts per skill, shown in the generated
# dist/{consumer,creator}/skills/README.md. Hand-maintained here (not
# derived from SKILL.md) because a good example needs a concrete
# TMFSxxx/TMFCxxx/TMFxxx id and phrasing a real caller would use, not a
# mechanical restatement of the frontmatter description.
SKILL_EXAMPLES = {
    "check-usecase-maturity": [
        "Is TMFS016 safe to build against right now?",
    ],
    "explain-etom-process": [
        "What is eTOM process 1.4.5, and which ODA components implement it?",
    ],
    "recommend-oda-components-for-requirement": [
        "We need to let customers manage their own SIM swaps online -- what ODA components and APIs should this be built on?",
    ],
    "decompose-requirement-against-oda": [
        "We need to let customers reserve specific network resources in advance so they're guaranteed available before the service order is placed -- nothing in the use-case corpus matches this closely, break it down against ODA anyway.",
    ],
    "capture-requirements-from-usecase": [
        "Turn TMFS030 into user stories and acceptance criteria for the delivery team.",
    ],
    "generate-test-cases-from-usecase": [
        "Generate Gherkin/BDD test scenarios for TMFS003.",
    ],
    "generate-api-conformance-tests": [
        "Generate conformance tests for TMF620 v4.0.0's Category resource -- required fields, declared operations, and status codes.",
    ],
    "generate-api-mocks-from-usecase": [
        "Scaffold mock API responses for TMFS003's dependencies so we can start integration testing before the real backend exists.",
    ],
    "generate-implementation-scaffold-from-usecase": [
        "Generate Python/FastAPI typed models and route stubs for TMFS020's linked API (TMF679) -- scaffolding only, no business logic.",
    ],
    "implement-oda-component": [
        "Build a complete TMFC009 Service Qualification Management implementation -- Node.js source and a Helm chart, following TM Forum's own reference stack.",
    ],
    "draft-architecture-diagram-from-usecase": [
        "Draw a sequence diagram for TMFS028's design phase service discovery. Save it as a .puml file",
    ],
    "draft-event-design-for-component": [
        "TMFC012 Resource Inventory now exposes TMF716 Resource Reservation but has no published event for it yet -- draft the eventNotification entry it needs.",
    ],
    "validate-design-against-oda": [
        "Check whether our design's assumption that Party Management (TMF632) exposes a loyaltyPoints field actually holds.",
    ],
    "review-architecture-against-oda": [
        "We're planning a new InventoryTracker service that owns resource inventory records, a BillingBridge that reads its database directly, and a ReservationManager that calls it with a custom reservation endpoint -- review this against ODA before we build it.",
    ],
    "assess-change-impact": [
        "We're deprecating TMF632 v4.0.0 - which use cases break, and how badly?",
    ],
    "audit-implementation-against-usecase": [
        "Does our current order-capture service actually implement TMFS030 the way the use case describes?",
    ],
    "audit-implementation-against-component": [
        "Does our TMFC012 implementation actually conform to its Core Function and Supporting Function contract, not just the flow one specific use case exercises?",
    ],
    "deliver-oda-requirement": [
        "We want customers to browse our product catalogue online and check whether fiber service is technically available at their address before they order -- take this all the way from requirement to a validated implementation.",
    ],
    "feedback-harvest-gaps-from-lessons-learned": [
        "What capability gaps has the use-case corpus already identified that nobody's aggregated into one place yet?",
    ],
    "feedback-propose-matrix-correction": [
        "Turn the logged use-case/matrix disagreements into submittable corrections for the next IG1228 revision.",
    ],
    "draft-new-usecase-from-scenario": [
        "Draft a new TMFS-shaped use case for satellite-to-ground handover billing -- nothing existing covers it.",
    ],
    "propose-component-or-api-extension": [
        "Design a fix for the 'Delegate Component' gap logged in the gaps backlog.",
    ],
    "lint-usecase-draft": [
        "Check my draft use-case DOCX for anything that will convert badly before I submit it to TM Forum.",
    ],
}

PLUGINS = {
    "consumer": {
        "name": "tm-forum-oda-consumer",
        "version": "1.0.0",
        "description": "TM Forum ODA use cases, components, and Open APIs as a provenance-tracked knowledge base, queryable via Agent Skills -- for building a product against ODA.",
        "author": {"name": "Lester Thomas"},
        "skills": CONSUMER_SKILLS,
    },
    "creator": {
        "name": "tm-forum-oda-creator",
        "version": "1.0.0",
        "description": "TM Forum ODA use cases, components, and Open APIs as a provenance-tracked knowledge base, queryable via Agent Skills -- for drafting and extending ODA itself.",
        "author": {"name": "Lester Thomas"},
        "skills": CREATOR_SKILLS,
    },
}


def rewrite_knowledge_paths(text):
    return text.replace("knowledge/", "${CLAUDE_PLUGIN_ROOT}/knowledge/")


def check_classification():
    all_skills = {name for name in os.listdir(SKILLS_SRC) if os.path.isdir(os.path.join(SKILLS_SRC, name))}
    classified = CONSUMER_SKILLS | CREATOR_SKILLS | INTERNAL_ONLY_SKILLS
    unclassified = all_skills - classified
    unknown = classified - all_skills
    overlap = (CONSUMER_SKILLS & CREATOR_SKILLS) | (CONSUMER_SKILLS & INTERNAL_ONLY_SKILLS) | (CREATOR_SKILLS & INTERNAL_ONLY_SKILLS)
    if unclassified:
        raise SystemExit(f"build_plugin.py: unclassified skill(s), add to CONSUMER_SKILLS/CREATOR_SKILLS/INTERNAL_ONLY_SKILLS: {sorted(unclassified)}")
    if unknown:
        raise SystemExit(f"build_plugin.py: classified skill(s) no longer exist under skills/: {sorted(unknown)}")
    if overlap:
        raise SystemExit(f"build_plugin.py: skill(s) classified in more than one bucket: {sorted(overlap)}")


def copy_skills(plugin_dir, skill_names):
    dst = os.path.join(plugin_dir, "skills")
    os.makedirs(dst, exist_ok=True)
    rewritten = 0
    for name in sorted(skill_names):
        shutil.copytree(os.path.join(SKILLS_SRC, name), os.path.join(dst, name))
    for root, _, files in os.walk(dst):
        for name in files:
            if name != "SKILL.md":
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            new_text = rewrite_knowledge_paths(text)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
            rewritten += new_text.count("${CLAUDE_PLUGIN_ROOT}/knowledge/")
    return rewritten


def read_skill_frontmatter(skill_md_path):
    with open(skill_md_path, encoding="utf-8") as f:
        text = f.read()
    _, frontmatter, _ = text.split("---", 2)
    meta = {}
    for line in frontmatter.strip().splitlines():
        key, _, value = line.partition(": ")
        meta[key.strip()] = value.strip()
    return meta


def write_skills_readme(plugin_dir, spec, skill_names):
    lines = [
        f"# {spec['name']}",
        "",
        spec["description"],
        "",
        "Auto-generated by `tools/build_plugin.py` from `skills/*/SKILL.md` -- "
        "do not edit by hand; edit the source skill and rebuild.",
        "",
        f"This plugin bundles {len(skill_names)} Agent Skills. Claude Code invokes "
        "one automatically when your request matches what it does -- you "
        "don't need to name the skill directly, just describe what you want.",
        "",
        "## Skills",
        "",
    ]
    for name in sorted(skill_names):
        meta = read_skill_frontmatter(os.path.join(plugin_dir, "skills", name, "SKILL.md"))
        lines.append(f"### {meta['name']}")
        lines.append("")
        lines.append(meta["description"])
        lines.append("")
        examples = SKILL_EXAMPLES.get(name)
        if not examples:
            raise SystemExit(f"build_plugin.py: no SKILL_EXAMPLES entry for skill {name!r}")
        label = "Example" if len(examples) == 1 else "Examples"
        lines.append(f"**{label}:**")
        for example in examples:
            lines.append(f"> {example}")
        lines.append("")
    with open(os.path.join(plugin_dir, "skills", "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip("\n") + "\n")


def copy_knowledge(plugin_dir):
    shutil.copytree(KNOWLEDGE_SRC, os.path.join(plugin_dir, "knowledge"))


def write_manifest(plugin_dir, manifest):
    manifest_dir = os.path.join(plugin_dir, ".claude-plugin")
    os.makedirs(manifest_dir, exist_ok=True)
    with open(os.path.join(manifest_dir, "plugin.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")


def main():
    check_classification()

    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR)

    for key, spec in PLUGINS.items():
        plugin_dir = os.path.join(DIST_DIR, key)
        os.makedirs(plugin_dir)

        rewritten = copy_skills(plugin_dir, spec["skills"])
        write_skills_readme(plugin_dir, spec, spec["skills"])
        copy_knowledge(plugin_dir)
        write_manifest(plugin_dir, {
            "name": spec["name"],
            "version": spec["version"],
            "description": spec["description"],
            "author": spec["author"],
        })

        skill_count = len(spec["skills"])
        print(f"dist/{key}/skills/: {skill_count} skill(s), {rewritten} knowledge/ path reference(s) rewritten to ${{CLAUDE_PLUGIN_ROOT}}")
        print(f"dist/{key}/skills/README.md: written ({skill_count} skill(s) listed)")
        print(f"dist/{key}/knowledge/: copied from {KNOWLEDGE_SRC}")
        print(f"dist/{key}/.claude-plugin/plugin.json: written ({spec['name']})")


if __name__ == "__main__":
    main()
