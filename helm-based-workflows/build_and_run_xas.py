#!/usr/bin/env python3
"""
Run the xas_notebook workflows script locally

Run with:

    python build_and_run_msmapper.py

Requires:
    python(any), podman

Steps:
1. Build the Dockerfile image locally using podman
2. Generate a run script from workflow template
3. Run the script in the container

All generated output is stored in `local-msmapper-output/`
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
WORKFLOW = ROOT / "templates" / "xas-notebook.yaml"
NOTEBOOK = ROOT / "notebooks" / "xas_notebook.ipynb"
LOCAL_IMAGE = "mmg_toolbox-local:test"
DOCKERFILE = ROOT / ".." / "images" / "base" / "Dockerfile"
BUILD_CONTEXT = DOCKERFILE.parent
IMAGE_FALLBACK = "ghcr.io/diamondlightsource/magnetic-materials-workflows/base:latest"

PARAMETERS: dict[str, str | float] = {
    "visitdir": "/dls/i10-1/data/2026/mm43353-1",
    "n_holes": 1,
    "background_ev_from_end": 5,
    "background_ev_from_start": 5,
    "peak_width_ev": 5,
    "background_subtraction": "linear",
    "sample_name": "none",
    "scan_numbers_str": "75759-75766",
    "edge_label": "none"
}


def build_image() -> None:
    """Build the local msmapper container image."""

    if not DOCKERFILE.is_file():
        raise FileNotFoundError(f"Dockerfile not found: {DOCKERFILE}")

    command = [
        "podman",
        "build",
        "--tag",
        LOCAL_IMAGE,
        "--file",
        str(DOCKERFILE),
        str(BUILD_CONTEXT),
    ]

    print("\n--- building local image ---")
    print(" ".join(command))
    print()

    subprocess.run(command, check=True)


def load_script_and_image() -> tuple[str, str]:
    with WORKFLOW.open(encoding="utf-8") as f:
        workflow = yaml.safe_load(f)

    templates = workflow["spec"]["templates"]
    template = next(t for t in templates if t["name"] == "run-xas-notebook")
    return template["script"]["source"], template["script"].get("image", IMAGE_FALLBACK)


def render_argo_parameters(script: str) -> str:
    """Replace {{ workflow.parameters.NAME }}, including Helm backtick wrappers."""
    for name, value in PARAMETERS.items():
        # Handles both {{ workflow.parameters.foo }} and
        # {{`{{ workflow.parameters.foo }}`}} as seen in the Helm YAML.
        patterns = (
            rf"\{{\{{`\{{\{{\s*workflow\.parameters\.{re.escape(name)}\s*\}}\}}`\}}\}}",
            rf"\{{\{{\s*workflow\.parameters\.{re.escape(name)}\s*\}}\}}",
        )
        for pattern in patterns:
            script = re.sub(pattern, str(value), script)
    return script


def replace_mount_files(script: str) -> str:
    """Replace the Helm .Files notebook extraction with the mounted local notebook."""
    lines = script.splitlines()
    output: list[str] = []
    for line in lines:
        if '.Files.Get "notebooks/xas_notebook.ipynb"' in line:
            output.append("cp /work/xas_notebook.ipynb /tmp/notebook.ipynb")
        else:
            output.append(line)
    return "\n".join(output)


def main(build_local_image: bool = True) -> None:
    visitdir = Path(str(PARAMETERS["visitdir"])).resolve()
    if not WORKFLOW.is_file():
        raise FileNotFoundError(WORKFLOW)
    if not NOTEBOOK.is_file():
        raise FileNotFoundError(NOTEBOOK)
    if not visitdir.is_dir():
        raise NotADirectoryError(visitdir)

    # Build the image we are about to test.
    if build_local_image:
        build_image()

    script, image = load_script_and_image()
    script = replace_mount_files(render_argo_parameters(script))

    # Preserve /tmp artefacts after the container exits by mapping host output
    # directly to /tmp, which is also how the workflow script addresses them.
    output_dir = ROOT / "local-xas-output"
    output_dir.mkdir(exist_ok=True)

    command = [
        "podman", "run", "--rm",
        "-v", f"{NOTEBOOK}:/work/xas_notebook.ipynb:ro",
        "-v", f"{visitdir}:{visitdir}",
        "-v", f"{output_dir}:/tmp:Z",
        LOCAL_IMAGE if build_local_image else image,
        "bash", "-c", script,
    ]

    print(f"Workflow: {WORKFLOW}")
    print(f"Image:    {image}")
    print("\n--- rendered workflow script ---")
    print(script)
    print("--- end script ---\n")

    print(f"subprocess command:\n{command}")

    subprocess.run(command, check=True)
    print(f"Outputs: {output_dir}")
    print("\n".join(('  ' + f.name for f in output_dir.iterdir() if f.is_file())))


if __name__ == "__main__":
    main(build_local_image=True)
