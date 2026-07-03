#!/usr/bin/env python3
"""
Gate E3 smoke test ("test_api.py chay duoc, co 1 output mau").

Adaptation note (disclosed in notes.md): the RBL-4 template assumes "the API" means
a remote LLM provider's HTTP endpoint (e.g. OpenAI). This project's approved LLM
invocation method is a **Claude Code isolated sub-agent call** (see env/tools.md),
not a scriptable HTTP client -- there is no per-call REST endpoint to smoke-test.
So "the API" this script tests is instead **the target REST APIs under test (the
3 SUTs)**, which is gate E3's real practical purpose: confirm the environment
actually answers requests before committing to a big batch run.

This script never fails hard: an unreachable SUT (not currently started) is a
normal, expected state between experiment runs, not an error. It always exits 0
and prints one sample request/response per SUT it *can* reach.
"""
import urllib.request
import urllib.error

SUTS = [
    {"name": "rest-ncs", "port": 8080, "sample_path": "/api/bessj/2/1.0"},
    {"name": "rest-scs", "port": 8083, "sample_path": "/api/calc/plus/1/2"},
    {"name": "features-service", "port": 8081, "sample_path": "/products/test"},
]


def probe(sut, timeout=3):
    url = f"http://localhost:{sut['port']}{sut['sample_path']}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            body = resp.read(500).decode("utf-8", errors="replace")
            return True, resp.status, body
    except urllib.error.HTTPError as e:
        # A 4xx/5xx still means the server answered -- it's REACHABLE.
        body = e.read(500).decode("utf-8", errors="replace")
        return True, e.code, body
    except Exception as e:
        return False, None, str(e)


def main():
    print("Gate E3 smoke test -- SUT liveness (see docstring for the API-type adaptation)\n")
    any_reachable = False
    for sut in SUTS:
        ok, status, body = probe(sut)
        if ok:
            any_reachable = True
            print(f"[REACHABLE]   {sut['name']:<18} port={sut['port']} "
                  f"GET {sut['sample_path']} -> HTTP {status}")
            print(f"              sample output: {body[:200]}")
        else:
            print(f"[UNREACHABLE] {sut['name']:<18} port={sut['port']} "
                  f"(not started, or not on this port) -- {body}")
    print(f"\n{'At least one SUT answered.' if any_reachable else 'No SUT currently running -- start via run_mutation.py / Maven before a batch run.'}")
    print("Exit 0 (diagnostic only, not a hard failure per gate E3 intent).")


if __name__ == "__main__":
    main()
