#!/usr/bin/env python3
"""Count external effects after a lost MCP tools/call response and one retry."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

CASES = Path(__file__).with_name("cases.json")


def effect_server(case: dict):
    ledger: list[dict] = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            try:
                size = int(self.headers["Content-Length"])
            except (KeyError, ValueError):
                self.send_error(400)
                return
            if self.path != "/effect" or not 0 < size <= 4096:
                self.send_error(400)
                return
            try:
                event = json.loads(self.rfile.read(size))
                if event != {"operationKey": case["operationKey"]}:
                    raise ValueError("wrong operation key")
            except ValueError:
                self.send_error(400)
                return
            ledger.append(event)
            data = json.dumps({"effectId": len(ledger)}).encode("ascii")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    return server, ledger


def check_report(case: dict, report: dict, ledger: list[dict]) -> list[str]:
    errors = []
    ids = report.get("requestIds")
    if not isinstance(ids, list) or len(ids) != 2 or ids[0] == ids[1]:
        errors.append("retry must use a fresh JSON-RPC request ID")
    if report.get("firstResponseLost") is not True:
        errors.append("first response was not reported lost after the effect")
    if report.get("retrySource") != "application":
        errors.append("retry must be explicit application policy")
    if report.get("protocolVersion") != case["protocolVersion"]:
        errors.append("protocol version differs from the case")
    if len(ledger) != case["expectedEffects"]:
        errors.append(f"effect sink recorded {len(ledger)}, expected {case['expectedEffects']}")
    return errors


def run_case(case: dict, adapter: list[str], timeout: float) -> dict:
    server, ledger = effect_server(case)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        env = os.environ.copy()
        env["PROBITY_EFFECT_URL"] = f"http://127.0.0.1:{server.server_port}/effect"
        proc = subprocess.run(
            [*adapter, str(CASES), case["id"]],
            env=env, text=True, capture_output=True, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        return {"case": case["id"], "effects": len(ledger), "errors": ["adapter timed out"]}
    finally:
        server.shutdown()
        server.server_close()
        thread.join()

    try:
        report = json.loads(proc.stdout.strip().splitlines()[-1])
        errors = check_report(case, report, ledger) if isinstance(report, dict) else ["adapter report is not an object"]
    except (IndexError, TypeError, ValueError):
        errors = ["adapter did not print a JSON report"]
    if proc.returncode:
        errors.append(f"adapter exited {proc.returncode}: {proc.stderr.strip()}")
    return {"case": case["id"], "effects": len(ledger), "errors": errors}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("adapter", nargs="+", help="command run once per case")
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    results = [run_case(case, args.adapter, args.timeout) for case in cases]
    print(json.dumps(results, indent=2))
    return int(any(result["errors"] for result in results))


if __name__ == "__main__":
    sys.exit(main())
