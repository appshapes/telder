"""Unit tests for plugin/scripts/tldr-hook. `make test` runs them; no network, no claude: the nested call is a fake."""
import importlib.machinery
import importlib.util
import io
import json
import os
import subprocess
import tempfile
import sys
import unittest
from unittest import mock

# Never drop a __pycache__ under plugin/: the plugin tree is an allowlist, and --plugin-dir would ship the cache.
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "plugin", "scripts", "tldr-hook")


def load_script():
    loader = importlib.machinery.SourceFileLoader("tldr_hook", SCRIPT)
    spec = importlib.util.spec_from_loader("tldr_hook", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


hook = load_script()

LONG = " ".join(f"word{i}" for i in range(400))
SHORT = "Done. Two files changed."


def fake_run(stdout, returncode=0, stderr=""):
    calls = []

    def run(cmd, **kwargs):
        calls.append((cmd, kwargs))
        return subprocess.CompletedProcess(cmd, returncode, stdout=stdout, stderr=stderr)

    run.calls = calls
    return run


class ProseWords(unittest.TestCase):
    def test_counts_words(self):
        self.assertEqual(hook.prose_words("one two  three\nfour"), 4)

    def test_empty(self):
        self.assertEqual(hook.prose_words(""), 0)
        self.assertEqual(hook.prose_words(None), 0)

    def test_fenced_code_does_not_count(self):
        text = "intro words here\n```sh\nmake test plugin-check\necho done\n```\nafter"
        self.assertEqual(hook.prose_words(text), 4)

    def test_tilde_fence_and_table_rows_do_not_count(self):
        text = "a b\n~~~\nx y z\n~~~\n| h1 | h2 |\n| --- | --- |\n| c d | e f |\nend"
        self.assertEqual(hook.prose_words(text), 3)


class Options(unittest.TestCase):
    def test_defaults(self):
        opts = hook.options({})
        self.assertEqual(opts["model"], hook.DEFAULTS["model"])
        self.assertEqual(opts["min_words"], 300)
        self.assertEqual(opts["max_points"], 10)
        self.assertEqual(opts["heading"], "TL;DR")
        self.assertEqual(opts["timeout"], 90)

    def test_from_environment(self):
        env = {"CLAUDE_PLUGIN_OPTION_MODEL": " claude-sonnet-5-5 ", "CLAUDE_PLUGIN_OPTION_MIN_WORDS": "40",
               "CLAUDE_PLUGIN_OPTION_MAX_POINTS": "3", "CLAUDE_PLUGIN_OPTION_HEADING": "Summary",
               "CLAUDE_PLUGIN_OPTION_TIMEOUT": "20"}
        opts = hook.options(env)
        self.assertEqual(opts["model"], "claude-sonnet-5-5")
        self.assertEqual(opts["min_words"], 40)
        self.assertEqual(opts["max_points"], 3)
        self.assertEqual(opts["heading"], "Summary")
        self.assertEqual(opts["timeout"], 20)

    def test_bounds_and_garbage(self):
        env = {"CLAUDE_PLUGIN_OPTION_MAX_POINTS": "99", "CLAUDE_PLUGIN_OPTION_MIN_WORDS": "-5",
               "CLAUDE_PLUGIN_OPTION_TIMEOUT": "9999", "CLAUDE_PLUGIN_OPTION_MODEL": "   ", "CLAUDE_PLUGIN_OPTION_HEADING": ""}
        with mock.patch.object(hook, "warn"):
            opts = hook.options(env)
        self.assertEqual(opts["max_points"], 10)
        self.assertEqual(opts["min_words"], 0)
        self.assertEqual(opts["timeout"], hook.MAX_TIMEOUT)
        self.assertEqual(opts["model"], hook.DEFAULTS["model"])
        self.assertEqual(opts["heading"], "TL;DR")
        with mock.patch.object(hook, "warn") as warn:
            opts = hook.options({"CLAUDE_PLUGIN_OPTION_MIN_WORDS": "many"})
        self.assertEqual(opts["min_words"], 300)
        warn.assert_called_once()


class ChildEnv(unittest.TestCase):
    def test_strips_by_prefix_and_keeps_config_dir(self):
        env = {"PATH": "/usr/bin", "CLAUDECODE": "1", "CLAUDE_PID": "7", "CLAUDE_CODE_SESSION_ID": "x",
               "CLAUDE_EFFORT": "high", "AI_AGENT": "claude", "AI_AGENT_X": "y", "CLAUDE_CONFIG_DIR": "/cfg", "HOME": "/h"}
        out = hook.child_env(env)
        self.assertEqual(sorted(out), ["CLAUDE_CONFIG_DIR", "HOME", "PATH", hook.INNER_MARK])
        self.assertEqual(out["CLAUDE_CONFIG_DIR"], "/cfg")
        self.assertEqual(out[hook.INNER_MARK], "1")

    def test_claude_command_prefers_the_running_executable(self):
        with tempfile.TemporaryDirectory() as folder:
            exe = os.path.join(folder, "claude")
            with open(exe, "w") as f:
                f.write("#!/bin/sh\n")
            os.chmod(exe, 0o755)
            self.assertEqual(hook.claude_command({"CLAUDE_CODE_EXECPATH": exe}), exe)
            self.assertEqual(hook.claude_command({"CLAUDE_CODE_EXECPATH": os.path.join(folder, "missing")}), "claude")
            self.assertEqual(hook.claude_command({}), "claude")

    def test_command_shape(self):
        opts = hook.options({})
        cmd = hook.summarize_command({}, opts, hook.instructions_text(hook.instruction_parts(opts, None)))
        self.assertEqual(cmd[:2], ["claude", "-p"])
        self.assertIn("--no-session-persistence", cmd)
        self.assertIn("--strict-mcp-config", cmd)
        self.assertEqual(cmd[cmd.index("--tools") + 1], "")
        self.assertEqual(cmd[cmd.index("--setting-sources") + 1], "")
        self.assertEqual(cmd[cmd.index("--model") + 1], hook.DEFAULTS["model"])
        self.assertNotIn("--bare", cmd)
        system = cmd[cmd.index("--system-prompt") + 1]
        self.assertIn("at most 10 points", system)
        self.assertIn("simple and concise language", system)
        self.assertTrue(system.endswith("single word NONE."))


class CleanSummary(unittest.TestCase):
    def test_bullets_kept_and_capped(self):
        text = "TL;DR\n- one\n* two\n• three\n1. four\n2) five\n- six\n"
        self.assertEqual(hook.clean_summary(text, 5), "- one\n- two\n- three\n- four\n- five")

    def test_heading_lines_dropped(self):
        self.assertEqual(hook.clean_summary("**TL;DR**\n\nSummary:\n- a\n", 5), "- a")

    def test_none_marker(self):
        self.assertIsNone(hook.clean_summary("NONE", 5))
        self.assertIsNone(hook.clean_summary("  none.\n", 5))
        self.assertIsNone(hook.clean_summary("", 5))
        self.assertIsNone(hook.clean_summary("\n\n", 5))

    def test_plain_lines_become_points(self):
        self.assertEqual(hook.clean_summary("first thing\nsecond thing", 5), "- first thing\n- second thing")


class Summarize(unittest.TestCase):
    def test_runs_claude_with_the_text_on_stdin(self):
        run = fake_run("- a\n- b\n")
        with mock.patch.object(hook, "warn"):
            out = hook.summarize(LONG, hook.options({}), {"PATH": "/usr/bin", "CLAUDECODE": "1"}, run=run)
        self.assertEqual(out, "- a\n- b")
        cmd, kwargs = run.calls[0]
        self.assertEqual(kwargs["input"], LONG)
        self.assertEqual(kwargs["timeout"], 90)
        self.assertNotIn("CLAUDECODE", kwargs["env"])
        self.assertEqual(kwargs["env"][hook.INNER_MARK], "1")

    def test_failure_paths_return_none(self):
        with mock.patch.object(hook, "warn") as warn:
            self.assertIsNone(hook.summarize(LONG, hook.options({}), {}, run=fake_run("", returncode=1, stderr="boom")))
            self.assertIn("exited 1", warn.call_args[0][0])

            def timeout(cmd, **kwargs):
                raise subprocess.TimeoutExpired(cmd, kwargs["timeout"])
            self.assertIsNone(hook.summarize(LONG, hook.options({}), {}, run=timeout))

            def missing(cmd, **kwargs):
                raise FileNotFoundError("claude")
            self.assertIsNone(hook.summarize(LONG, hook.options({}), {}, run=missing))
            self.assertIsNone(hook.summarize(LONG, hook.options({}), {}, run=fake_run("NONE\n")))


class StopEvent(unittest.TestCase):
    def run_hook(self, data, env, run):
        out = io.StringIO()
        with mock.patch.object(hook.subprocess, "run", run), mock.patch.object(hook, "warn"):
            code = hook.main([], io.StringIO(json.dumps(data)), out, env)
        return code, out.getvalue()

    def env(self, folder):
        return {"PATH": "/usr/bin", "CLAUDE_PLUGIN_DATA": folder}

    def test_long_reply_gets_a_system_message(self):
        with tempfile.TemporaryDirectory() as folder:
            data = {"hook_event_name": "Stop", "stop_reason": "end_turn", "last_assistant_message": LONG}
            code, out = self.run_hook(data, self.env(folder), fake_run("- first\n- second\n"))
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"systemMessage": "TL;DR\n- first\n- second"})

    def test_short_reply_and_error_stops_get_nothing(self):
        with tempfile.TemporaryDirectory() as folder:
            run = fake_run("- x")
            code, out = self.run_hook({"hook_event_name": "Stop", "stop_reason": "end_turn", "last_assistant_message": SHORT}, self.env(folder), run)
            self.assertEqual((code, out), (0, ""))
            code, out = self.run_hook({"hook_event_name": "Stop", "stop_reason": "overloaded"}, self.env(folder), run)
            self.assertEqual((code, out), (0, ""))
            self.assertEqual(run.calls, [])

    def test_inner_mark_and_mute_and_unknown_event(self):
        with tempfile.TemporaryDirectory() as folder:
            run = fake_run("- x")
            data = {"hook_event_name": "Stop", "stop_reason": "end_turn", "last_assistant_message": LONG}
            env = self.env(folder)
            self.assertEqual(self.run_hook(data, dict(env, TLDR_INNER="1"), run), (0, ""))
            hook.main(["off"], None, io.StringIO(), env)
            self.assertEqual(self.run_hook(data, env, run), (0, ""))
            hook.main(["on"], None, io.StringIO(), env)
            self.assertEqual(self.run_hook(dict(data, hook_event_name="PreToolUse"), env, run), (0, ""))
            self.assertEqual(run.calls, [])
            code, out = self.run_hook(data, env, run)
            self.assertEqual(json.loads(out)["systemMessage"], "TL;DR\n- x")

    def test_bad_input_is_not_an_error(self):
        out = io.StringIO()
        with mock.patch.object(hook, "warn"):
            self.assertEqual(hook.main([], io.StringIO("not json"), out, {}), 0)
            self.assertEqual(hook.main([], io.StringIO("[1, 2]"), out, {}), 0)
        self.assertEqual(out.getvalue(), "")


class MessageDisplayEvent(unittest.TestCase):
    def run_hook(self, data, env, run):
        out = io.StringIO()
        with mock.patch.object(hook.subprocess, "run", run), mock.patch.object(hook, "warn"):
            code = hook.main([], io.StringIO(json.dumps(data)), out, env)
        self.assertEqual(code, 0)
        return out.getvalue()

    def test_chunks_accumulate_and_the_final_chunk_carries_the_summary(self):
        with tempfile.TemporaryDirectory() as folder:
            env = {"CLAUDE_PLUGIN_DATA": folder}
            run = fake_run("- point one\n- point two\n")
            base = {"hook_event_name": "MessageDisplay", "session_id": "s1", "message_id": "m1"}
            half = " ".join(LONG.split()[:100])
            self.assertEqual(self.run_hook(dict(base, delta=half + " ", final=False), env, run), "")
            self.assertEqual(self.run_hook(dict(base, delta=" ".join(LONG.split()[100:]), final=False), env, run), "")
            self.assertEqual(run.calls, [])
            out = self.run_hook(dict(base, delta="", final=True), env, run)
            reply = json.loads(out)
            self.assertEqual(reply["hookSpecificOutput"]["hookEventName"], "MessageDisplay")
            self.assertEqual(reply["hookSpecificOutput"]["displayContent"], "---\n**TL;DR**\n- point one\n- point two")
            self.assertEqual(run.calls[0][1]["input"].split(), LONG.split())
            self.assertEqual(os.listdir(os.path.join(folder, "chunks")), [])

    @unittest.skipIf(os.name == "nt", "POSIX file modes")
    def test_the_pieces_are_readable_by_this_user_only(self):
        with tempfile.TemporaryDirectory() as folder:
            env = {"CLAUDE_PLUGIN_DATA": folder}
            chunks = os.path.join(folder, "chunks")
            os.makedirs(chunks, mode=0o755)  # as an earlier version left it
            os.chmod(chunks, 0o755)
            data = {"hook_event_name": "MessageDisplay", "session_id": "s", "message_id": "m", "delta": "a piece ", "final": False}
            self.assertEqual(self.run_hook(data, env, fake_run("- x")), "")
            self.assertEqual(os.stat(chunks).st_mode & 0o777, 0o700)
            self.assertEqual(os.stat(os.path.join(chunks, "s-m")).st_mode & 0o777, 0o600)

    def test_headless_shape_one_final_chunk_with_the_whole_message(self):
        with tempfile.TemporaryDirectory() as folder:
            env = {"CLAUDE_PLUGIN_DATA": folder}
            data = {"hook_event_name": "MessageDisplay", "session_id": "s", "message_id": "m", "delta": LONG, "final": True}
            out = self.run_hook(data, env, fake_run("- only\n"))
            shown = json.loads(out)["hookSpecificOutput"]["displayContent"]
            self.assertTrue(shown.startswith(LONG + "\n\n---\n**TL;DR**\n- only"))

    def test_short_message_shows_nothing_and_leaves_no_file(self):
        with tempfile.TemporaryDirectory() as folder:
            env = {"CLAUDE_PLUGIN_DATA": folder}
            run = fake_run("- x")
            data = {"hook_event_name": "MessageDisplay", "session_id": "s", "message_id": "m", "delta": SHORT, "final": True}
            self.assertEqual(self.run_hook(data, env, run), "")
            self.assertEqual(run.calls, [])
            self.assertEqual(os.listdir(os.path.join(folder, "chunks")), [])

    def test_stale_chunk_files_are_swept(self):
        with tempfile.TemporaryDirectory() as folder:
            env = {"CLAUDE_PLUGIN_DATA": folder}
            chunks = os.path.join(folder, "chunks")
            os.makedirs(chunks)
            stale = os.path.join(chunks, "old")
            with open(stale, "w") as f:
                f.write("x")
            os.utime(stale, (1, 1))
            data = {"hook_event_name": "MessageDisplay", "session_id": "s", "message_id": "m", "delta": SHORT, "final": True}
            self.run_hook(data, env, fake_run("- x"))
            self.assertFalse(os.path.exists(stale))


class CommandLine(unittest.TestCase):
    def test_off_on_status(self):
        with tempfile.TemporaryDirectory() as folder:
            out = io.StringIO()
            self.assertEqual(hook.main(["status", "--data-dir", folder], None, out, {}), 0)
            self.assertEqual(hook.main(["off", "--data-dir", folder], None, out, {}), 0)
            self.assertTrue(hook.muted({"CLAUDE_PLUGIN_DATA": folder}))
            self.assertEqual(hook.main(["status", "--data-dir", folder], None, out, {}), 0)
            self.assertEqual(hook.main(["on", "--data-dir", folder], None, out, {}), 0)
            self.assertFalse(hook.muted({"CLAUDE_PLUGIN_DATA": folder}))
            self.assertEqual(out.getvalue(), "tldr: on\ntldr: off. No summary is written until `tldr-hook on`.\ntldr: off\ntldr: on.\n")

    def test_usage_errors(self):
        with mock.patch.object(hook, "warn"):
            self.assertEqual(hook.main(["sideways"], None, io.StringIO(), {}), 2)
            self.assertEqual(hook.main(["off", "--data-dir"], None, io.StringIO(), {}), 2)
            self.assertEqual(hook.main(["instructions", "--mode"], None, io.StringIO(), {}), 2)
            self.assertEqual(hook.main(["instructions", "--sideways"], None, io.StringIO(), {}), 2)

    def test_data_dir_falls_back_to_a_temporary_directory(self):
        self.assertTrue(hook.data_dir({}).startswith(tempfile.gettempdir()))
        self.assertEqual(hook.data_dir({"CLAUDE_PLUGIN_DATA": "/d"}), "/d")


class Instructions(unittest.TestCase):
    def parts(self, env=None, project=None):
        with mock.patch.object(hook, "warn") as warn:
            parts = hook.instruction_parts(hook.options(env or {}), project)
        return parts, warn

    def test_built_in_then_format_rules(self):
        parts, warn = self.parts()
        self.assertEqual([source for source, _ in parts], ["the plugin", "the format rules, fixed"])
        self.assertEqual(parts[0][1], hook.BUILT_IN)
        self.assertIn("at most 10 points", parts[1][1])
        warn.assert_not_called()

    def test_inline_option_is_added_after_the_built_in(self):
        parts, _ = self.parts({"CLAUDE_PLUGIN_OPTION_INSTRUCTIONS": "  Write it in French.  "})
        self.assertEqual([source for source, _ in parts][:2], ["the plugin", "your instructions option"])
        self.assertEqual(parts[1][1], "Write it in French.")
        text = hook.instructions_text(parts)
        self.assertLess(text.index(hook.BUILT_IN), text.index("Write it in French."))
        self.assertTrue(text.endswith("NONE."))

    def test_file_option_and_project_file_in_order(self):
        with tempfile.TemporaryDirectory() as folder:
            mine = os.path.join(folder, "mine.md")
            with open(mine, "w", encoding="utf-8") as f:
                f.write("\nSay what I must do next.\n")
            project = os.path.join(folder, "proj")
            os.makedirs(project)
            with open(os.path.join(project, hook.PROJECT_FILE), "w", encoding="utf-8") as f:
                f.write("Name the files that changed.")
            parts, warn = self.parts({"CLAUDE_PLUGIN_OPTION_INSTRUCTIONS_FILE": mine,
                                      "CLAUDE_PLUGIN_OPTION_INSTRUCTIONS": "Be brief."}, project)
            self.assertEqual([source for source, _ in parts],
                             ["the plugin", "your instructions option", mine, os.path.join(project, hook.PROJECT_FILE),
                              "the format rules, fixed"])
            self.assertEqual(parts[2][1], "Say what I must do next.")
            self.assertEqual(parts[3][1], "Name the files that changed.")
            warn.assert_not_called()

    def test_replace_drops_the_built_in_only(self):
        with tempfile.TemporaryDirectory() as folder:
            parts, warn = self.parts({"CLAUDE_PLUGIN_OPTION_INSTRUCTIONS_MODE": "REPLACE",
                                      "CLAUDE_PLUGIN_OPTION_INSTRUCTIONS": "Three words each."}, folder)
            self.assertEqual([source for source, _ in parts], ["your instructions option", "the format rules, fixed"])
            warn.assert_not_called()

    def test_replace_with_nothing_falls_back_with_a_warning(self):
        parts, warn = self.parts({"CLAUDE_PLUGIN_OPTION_INSTRUCTIONS_MODE": "replace"})
        self.assertEqual([source for source, _ in parts], ["the plugin", "the format rules, fixed"])
        self.assertIn("replace", warn.call_args[0][0])

    def test_bad_mode_keeps_add(self):
        with mock.patch.object(hook, "warn") as warn:
            opts = hook.options({"CLAUDE_PLUGIN_OPTION_INSTRUCTIONS_MODE": "sideways"})
        self.assertEqual(opts["instructions_mode"], "add")
        warn.assert_called_once()

    def test_missing_file_warns_missing_project_file_is_silent(self):
        with tempfile.TemporaryDirectory() as folder:
            parts, warn = self.parts({"CLAUDE_PLUGIN_OPTION_INSTRUCTIONS_FILE": os.path.join(folder, "none.md")}, folder)
            self.assertEqual([source for source, _ in parts], ["the plugin", "the format rules, fixed"])
            warn.assert_called_once()
            self.assertIn("not found", warn.call_args[0][0])

    def test_too_large_blank_and_binary_files_are_ignored(self):
        with tempfile.TemporaryDirectory() as folder:
            big = os.path.join(folder, "big.md")
            with open(big, "w") as f:
                f.write("x" * (hook.MAX_INSTRUCTIONS_BYTES + 1))
            blank = os.path.join(folder, "blank.md")
            with open(blank, "w") as f:
                f.write("  \n\n")
            binary = os.path.join(folder, "bin.md")
            with open(binary, "wb") as f:
                f.write(b"\xff\xfe\x00 not text")
            for path, warned in ((big, True), (blank, False), (binary, True)):
                with mock.patch.object(hook, "warn") as warn:
                    self.assertIsNone(hook.read_instructions_file(path))
                self.assertEqual(warn.called, warned, path)

    def test_summarize_sends_the_layered_instructions(self):
        with tempfile.TemporaryDirectory() as project:
            with open(os.path.join(project, hook.PROJECT_FILE), "w") as f:
                f.write("Mention the risk first.")
            run = fake_run("- a\n")
            env = {"CLAUDE_PLUGIN_OPTION_INSTRUCTIONS": "In Spanish."}
            with mock.patch.object(hook, "warn"):
                hook.summarize(LONG, hook.options(env), env, project_dir=project, run=run)
            cmd = run.calls[0][0]
            system = cmd[cmd.index("--system-prompt") + 1]
            self.assertLess(system.index(hook.BUILT_IN), system.index("In Spanish."))
            self.assertLess(system.index("In Spanish."), system.index("Mention the risk first."))
            self.assertTrue(system.endswith("NONE."))

    def test_hook_uses_project_dir_from_env_else_cwd(self):
        with tempfile.TemporaryDirectory() as folder:
            a = os.path.join(folder, "a")
            b = os.path.join(folder, "b")
            os.makedirs(a)
            os.makedirs(b)
            with open(os.path.join(a, hook.PROJECT_FILE), "w") as f:
                f.write("from a")
            with open(os.path.join(b, hook.PROJECT_FILE), "w") as f:
                f.write("from b")
            data = {"hook_event_name": "Stop", "stop_reason": "end_turn", "last_assistant_message": LONG, "cwd": b}
            for env, expected in (({"CLAUDE_PROJECT_DIR": a, "CLAUDE_PLUGIN_DATA": folder}, "from a"),
                                  ({"CLAUDE_PLUGIN_DATA": folder}, "from b")):
                run = fake_run("- x\n")
                out = io.StringIO()
                with mock.patch.object(hook.subprocess, "run", run), mock.patch.object(hook, "warn"):
                    hook.main([], io.StringIO(json.dumps(data)), out, env)
                system = run.calls[0][0][run.calls[0][0].index("--system-prompt") + 1]
                self.assertIn(expected, system)

    def test_instructions_command_reports_every_part(self):
        with tempfile.TemporaryDirectory() as folder:
            mine = os.path.join(folder, "mine.md")
            with open(mine, "w") as f:
                f.write("Say what to do next.")
            with open(os.path.join(folder, hook.PROJECT_FILE), "w") as f:
                f.write("Name the files.")
            out = io.StringIO()
            code = hook.main(["instructions", "--instructions-file", mine, "--mode", "add", "--max-points", "3",
                              "--project-dir", folder, "--instructions-stdin"], io.StringIO("Be brief.\n"), out, {})
            self.assertEqual(code, 0)
            report = out.getvalue()
            self.assertEqual(report.split("\n")[0], "From the plugin:")
            self.assertIn("From your instructions option:\nBe brief.", report)
            self.assertIn(f"From {mine}:\nSay what to do next.", report)
            self.assertIn(f"From {os.path.join(folder, hook.PROJECT_FILE)}:\nName the files.", report)
            self.assertIn("From the format rules, fixed:\nFormat: an unordered list only", report)
            self.assertIn("at most 3 points", report)

    def test_instructions_command_defaults(self):
        out = io.StringIO()
        self.assertEqual(hook.main(["instructions"], io.StringIO(""), out, {}), 0)
        self.assertEqual(out.getvalue().count("From "), 2)


if __name__ == "__main__":
    unittest.main()
