#!/usr/bin/env python3
"""
Run the msmapper workflows script locally

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
WORKFLOW = ROOT / "templates" / "msmapper-notebook.yaml"
NOTEBOOK = ROOT / "notebooks" / "msmapper_notebook.ipynb"
LOCAL_IMAGE = "msmapper-local:test"
DOCKERFILE = ROOT / ".." / "images" / "msmapper" / "Dockerfile"
BUILD_CONTEXT = DOCKERFILE.parent
IMAGE_FALLBACK = "ghcr.io/diamondlightsource/magnetic-materials-workflows/msmapper:latest"

PARAMETERS: dict[str, object] = {
    "visitdir": "/dls/i16/data/2026/nt46530-1",
    "normalisation": "rc",
    "region": "None",
    "start": "None",
    "scale_factor": 2,
    "splitter_parameter": 2,
    "shape": "None",
    "step": 0.002,
    "output_mode": "Volume_HKL",
    "correct_polarisation": 'false',  # must use json style string
    "azi_plane_normal": "None",
    "reduce_box": 'true',
    "third_axis": "None",
    "crystal_frame": 'false',
    "splitter_name": "nearest",
    "scan_numbers": 1161098
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
    template = next(t for t in templates if t["name"] == "run-msmapper-notebook")
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
        if '.Files.Get "notebooks/msmapper_notebook.ipynb"' in line:
            output.append("cp /work/msmapper_notebook.ipynb /tmp/notebook.ipynb")
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
    output_dir = ROOT / "local-msmapper-output"
    output_dir.mkdir(exist_ok=True)

    command = [
        "podman", "run", "--rm",
        "-v", f"{NOTEBOOK}:/work/msmapper_notebook.ipynb:ro",
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
