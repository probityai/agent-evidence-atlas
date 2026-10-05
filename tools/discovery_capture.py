#!/usr/bin/env python3
"""Capture private native JSONL without running or scoring a discovery study."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import selectors
import subprocess
import sys

import discovery_capture_journal as custody


def capture(manifest_path, prompt_path, directory, fault=lambda _: None, utc=None, monotonic=None):
    manifest_bytes = custody.read_small(manifest_path)
    manifest = custody.strict_json(manifest_bytes)
    custody.validate_manifest(manifest)
    prompt = custody.read_small(prompt_path)
    directory = Path(directory)
    directory.mkdir(mode=0o700)
    custody.sync_directory(directory.parent)
    custody.exclusive_write(directory / "invocation.json", manifest_bytes)
    custody.exclusive_write(directory / "prompt.txt", prompt)
    journal = custody.Journal(directory, utc, monotonic)
    source_directory = directory / "driver-source"
    source_directory.mkdir(mode=0o700)
    sources = {}
    for path in (Path(__file__), Path(custody.__file__)):
        custody.exclusive_write(source_directory / path.name, custody.read_small(path))
        sources[path.name] = custody.file_binding(source_directory / path.name)
    journal.append("prepared", {"invocation": custody.file_binding(directory / "invocation.json"),
                               "prompt": custody.file_binding(directory / "prompt.txt"), "driver_sources": sources})
    receiver = custody.EventReceiver(directory, journal, fault)
    stderr = custody.open_regular(directory / "native-stderr.txt", os.O_WRONLY | os.O_CREAT | os.O_EXCL)
    custody.sync_directory(directory)
    process = None
    interrupted = False
    try:
        process = subprocess.Popen(manifest["argv"], cwd=manifest["cwd"], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        journal.append("launched", custody.process_identity(process.pid))
        fault("after_launch_identity")
        with selectors.DefaultSelector() as selector:
            for stream, tag in ((process.stdout, "stdout"), (process.stderr, "stderr")):
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, selectors.EVENT_READ, tag)
            if prompt:
                os.set_blocking(process.stdin.fileno(), False)
                selector.register(process.stdin, selectors.EVENT_WRITE, "stdin")
            else:
                process.stdin.close()
            written = 0
            while selector.get_map():
                for key, _ in selector.select():
                    if key.data == "stdin":
                        try:
                            written += os.write(key.fd, prompt[written:written + 65536])
                        except BrokenPipeError:
                            written = len(prompt)
                        if written == len(prompt):
                            selector.unregister(key.fileobj)
                            key.fileobj.close()
                        continue
                    chunk = os.read(key.fd, 65536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        key.fileobj.close()
                    elif key.data == "stdout":
                        receiver.feed(chunk)
                    else:
                        stderr.write(chunk)
                        stderr.flush()
                        os.fsync(stderr.fileno())
        code = process.wait()
        fault("after_wait_before_observation")
        journal.append("native_wait", {"exit_code": code})
        fault("after_wait_observation_before_driver_close")
        journal.append("driver_closure", {"state": "completed"})
    except KeyboardInterrupt:
        interrupted = True
        if process is not None:
            process.terminate()
            code = process.wait()
            journal.append("native_wait", {"exit_code": code})
            journal.append("driver_closure", {"state": "interrupted"})
    finally:
        # Unexpected errors preserve unknown closure. Stop only our own child.
        if process is not None and process.poll() is None:
            process.terminate()
            process.wait()
        if process is not None:
            for stream in (process.stdin, process.stdout, process.stderr):
                stream.close()
        receiver.close()
        stderr.close()
        journal.close()
    record = custody.project(directory)
    custody.atomic_write(directory / "record.json", record, fault)
    return record, 130 if interrupted else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("capture", "project"))
    parser.add_argument("--attempt-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--prompt", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.operation == "capture":
            custody.require(args.manifest is not None and args.prompt is not None and args.output is None,
                            "capture requires manifest and prompt; output is record.json")
            _, code = capture(args.manifest, args.prompt, args.attempt_dir)
            return code
        custody.require(args.output is not None and args.manifest is None and args.prompt is None, "project requires only output and attempt directory")
        custody.atomic_write(args.output, custody.project(args.attempt_dir))
        return 0
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
