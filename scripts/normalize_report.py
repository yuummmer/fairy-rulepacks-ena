#!/usr/bin/env python3
import json
import sys
from copy import deepcopy
from pathlib import Path

def _rel(p: str, repo_root: Path) -> str:
    try:
        pp = Path(p)
        # If it's inside repo_root, make it relative
        return str(pp.relative_to(repo_root))
    except Exception:
        return p

def normalize(report: dict, repo_root: Path) -> dict:
    r = deepcopy(report)

    # Remove or stabilize nondeterministic fields that would make goldens noisy.
    att = r.get("attestation", {})
    if isinstance(att, dict):
        att.pop("timestamp", None)          # changes every run
        att.pop("core_version", None)       # changes when fairy-core bumps

        # attestation.inputs[].path
        if isinstance(att.get("inputs"), list):
            for inp in att["inputs"]:
                if isinstance(inp, dict) and isinstance(inp.get("path"), str):
                    inp["path"] = _rel(inp["path"], repo_root)
        
        # attestation.rulepack.path
        rp = att.get("rulepack")
        if isinstance(rp, dict) and isinstance(rp.get("path"), str):
            rp["path"] = _rel(rp["path"], repo_root)

    # metadata.inputs.{name: path}
    meta = r.get("metadata", {})
    if isinstance(meta, dict):
        ins = meta.get("inputs")
        if isinstance(ins,dict):
            for k, v in list(ins.items()):
                if isinstance(v, str):
                    ins[k] = _rel(v, repo_root)

    # resources[].path
    resources = r.get("resources")
    if isinstance(resources, list):
        for res in resources:
            if isinstance(resources, list):
                for res in resources:
                    if isinstance(res, dict) and isinstance(res.get("path"), str):
                        res["path"] = _rel(res["path"], repo_root)

    # Sort rule/resource outputs can sometimes be stable already; we rely on json dump sort_keys.
    return r

def main():
    if len(sys.argv) != 3:
        print("Usage: normalize_report.py <in.json> <out.json>", file=sys.stderr)
        sys.exit(2)

    in_path, out_path = sys.argv[1], sys.argv[2]

    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # repo root = parent of scripts/
    repo_root = Path(__file__).resolve().parents[1] 

    norm = normalize(data, repo_root)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(norm, f, indent=2, sort_keys=True)
        f.write("\n")

if __name__ == "__main__":
    main()
