#!/bin/bash
# Makes emil-design-eng mandatory on every design run (carried over from Marhela, 2026-09-15).
#   PostToolUse(Skill): a design skill was just loaded -> require emil-design-eng alongside it.
#   UserPromptSubmit:   the prompt is about design/UI  -> require it before any design work.
input=$(cat)
event=$(jq -r '.hook_event_name // empty' <<<"$input")

design_skills='^(design|design-consultation|design-shotgun|design-html|design-review|plan-design-review|ios-design-review|frontend-design:frontend-design|transitions-dev|transitions-polish|better-ui|frontend-slides|autoplan)$'

msg='MANDATORY (project rule, CLAUDE.md §4 design): this is design work, so the emil-design-eng skill must be loaded. If it has not been invoked in this conversation yet, invoke Skill("emil-design-eng") NOW, passing the concrete design task as args (so it skips its canned greeting), and apply its principles (animation decision framework, custom easing, under-300ms UI motion, scale(0.97) press feedback, no scale(0) entries, reduced-motion, hover media query, and its Before/After/Why table for reviews) throughout this design run, on top of the gstack design skill. Massar rules still win on conflict (Arabic RTL, DESIGN.md tokens and the #2563EB accent, western numerals, src/dashboard.ts anchored edits only).'

emit() {
  jq -n --arg ev "$1" --arg ctx "$msg" '{hookSpecificOutput: {hookEventName: $ev, additionalContext: $ctx}}'
}

case "$event" in
  PostToolUse)
    skill=$(jq -r '.tool_input.skill // empty' <<<"$input" | sed 's#^/##')
    [[ "$skill" =~ $design_skills ]] && emit PostToolUse
    ;;
  UserPromptSubmit)
    prompt=$(jq -r '.prompt // empty' <<<"$input")
    if grep -qiE '(^|[^a-z])(/design|design|ui|ux|mockup|wireframe|css|layout|animation|transition|landing page|redesign|restyle|polish)([^a-z]|$)|تصميم|واجهة|شكل' <<<"$prompt"; then
      emit UserPromptSubmit
    fi
    ;;
esac
exit 0
