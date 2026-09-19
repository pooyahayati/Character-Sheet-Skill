# Final Release Checklist

Before publishing a release:

- [ ] VERSION matches package-manifest.json and CHANGELOG.md.
- [ ] SKILL.md has valid name/description frontmatter.
- [ ] No private/user reference photographs are committed.
- [ ] No character-output/ or workspaces/ data is committed.
- [ ] All schemas validate.
- [ ] All structured examples validate.
- [ ] All cross-file references validate.
- [ ] Scenario IDs are unique.
- [ ] Pose-readiness P0-P5 coverage is present.
- [ ] Multi-view anchor source of truth is unique.
- [ ] Camera state is not duplicated in Pose Contract.
- [ ] Deterministic compositor smoke test passes.
- [ ] Installable ZIP package builds.
- [ ] Installable ZIP contains SKILL.md at the skill root.
- [ ] Installable ZIP excludes .github/, tests/, dist/, local data and developer-only scripts.
- [ ] GitHub Actions is green.
- [ ] Clean-room ChatGPT test completed with a fresh Project/chat.
- [ ] At least one pose-readiness sequence has been visually reviewed.
