# Makefile for this repository
# Conventions: lowercase variable names; per-target `.PHONY`; `##` doc-comments scraped by `help`.
# Ported from appshapes/brigade and cut down to what a hooks-only plugin needs: no Go, no binaries, no checksums.

# ========== Variables (alphabetical) ==========

hook_script    := plugin/scripts/tldr-hook
plugin_json    := plugin/.claude-plugin/plugin.json
plugin_version := $(shell sed -nE 's/^[[:space:]]*"version":[[:space:]]*"([^"]+)".*/\1/p' $(plugin_json) | head -n 1)
python         ?= python3
version        ?= $(plugin_version)

# Strip the outer Claude Code session's variables from targets that launch claude: an inherited CLAUDECODE /
# CLAUDE_CODE_* set would make the nested session believe it is a child of this one. By PREFIX, never by
# enumeration (Brigade measured the enumerated list short by three names, and the next release can add more).
# CLAUDE_CONFIG_DIR is the single exception and must survive: it is how a second persona keeps its own login.
unclaude_keep  := CLAUDE_CONFIG_DIR
unclaude_vars  := $(filter-out $(unclaude_keep),$(shell env | sed -n -e 's/^\(CLAUDE[0-9A-Za-z_]*\)=.*/\1/p' -e 's/^\(AI_AGENT[0-9A-Za-z_]*\)=.*/\1/p'))
unclaude       := env $(patsubst %,-u %,$(unclaude_vars))

# ========== Help ==========

# A trailing ` (CI)` marks every target that a step of `.github/workflows/*.yml` invokes, and no other target.
.PHONY: help
help: ## Show this help message
	@grep -hE '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ========== Setup ==========

.PHONY: setup
setup: ## Check the tools the gates need (python3, shellcheck, claude, gh) and set push.autoSetupRemote
	@command -v $(python) >/dev/null || { echo "python3 is required (the hook is a Python 3 script)"; exit 1; }
	@$(python) -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' || { echo "python3 must be 3.9 or newer"; exit 1; }
	@command -v shellcheck >/dev/null || echo "WARNING: shellcheck is not installed (brew install shellcheck); make plugin-check will warn locally and fail in CI"
	@command -v claude >/dev/null || echo "WARNING: claude is not on PATH; make plugin-validate and make plugin-dev need it"
	@command -v gh >/dev/null || echo "WARNING: gh is not installed; make release needs it logged in"
	git config push.autoSetupRemote true
	@echo "setup: ok"

# ========== Gates ==========

.PHONY: test
test: ## Compile the hook script and run the unit tests (what `make commit` runs) (CI)
	$(python) -c 'import sys; compile(open(sys.argv[1]).read(), sys.argv[1], "exec")' $(hook_script)
	PYTHONDONTWRITEBYTECODE=1 $(python) -m unittest discover -s tests -t . -v

.PHONY: lint
lint: ## shellcheck every shell script in the repository (CI)
	shellcheck -s sh scripts/ci/*.sh scripts/*.sh

.PHONY: plugin-check
plugin-check: ## Static checks of plugin/: file allowlist, exec-form hooks, script mode, no bin/ or MCP, shellcheck, no secrets (CI)
	scripts/ci/plugin-check.sh
	scripts/ci/no-secrets.sh

.PHONY: plugin-validate
plugin-validate: ## claude plugin validate on the marketplace and the plugin root (CI)
	claude plugin validate .
	claude plugin validate ./plugin --strict

.PHONY: hook-smoke
hook-smoke: ## Run the hook script on the sample input in tests/fixtures and print its reply (needs a logged-in claude)
	$(unclaude) $(python) $(hook_script) < tests/fixtures/hook-input.json

# ========== Plugin dev loop ==========

# `opts` is the plugin's option object for this one session, e.g. opts='{"model":"claude-sonnet-5-5","min_words":40}'.
# The plugin id of a --plugin-dir load is <name>@inline.
.PHONY: plugin-dev
plugin-dev: ## Start Claude Code with the local plugin (usage: make plugin-dev [opts='{"model":"..."}'] [mode=default])
ifeq ($(opts),)
	$(unclaude) claude $(if $(mode),--permission-mode $(mode)) --plugin-dir ./plugin
else
	$(unclaude) claude $(if $(mode),--permission-mode $(mode)) --plugin-dir ./plugin --settings '{"pluginConfigs":{"tldr@inline":{"options":$(opts)}}}'
endif

# ========== Release ==========

.PHONY: print-version
print-version: ## Print the version the plugin manifest pins
	@echo $(plugin_version)

.PHONY: release
release: ## Bump the manifest to $(version), move the changelog's Unreleased section, commit as `$(card): Release $(version)`, tag v$(version) and push the tag (usage: make release version=0.1.0 card=<n>)
	@test -n "$(version)" && test -n "$(card)" || { echo "usage: make release version=X.Y.Z card=<n>"; exit 1; }
	card=$(card) scripts/release-prep.sh $(version)

# ========== Commit chain ==========

.PHONY: pull
pull: ## Merge origin into the current branch (plain merge — never rebase; no editor)
	git pull --no-edit

.PHONY: commit
commit: pull test plugin-check ## Pull, test, check the plugin tree, stage, commit (usage: make commit message="<card>: ...")
	@test -n "$(message)" || { echo "usage: make commit message=\"<card>: <Imperative summary>\""; exit 1; }
	git add --verbose :/ .
	git commit -m "$(message)"

.PHONY: push
push: commit ## commit + push
	git push
