#!/usr/bin/env bash
set -euo pipefail

# Locally build and push the Quanty image
# Use this script to manually upload the Quanty image
# You must have logged into to github package repo using:
# podman login ghcr.io

# Location of latest download file
ZIP=/scratch/grp66007/software/quanty/2024_spring_version_0.81/quanty_lin.zip
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_CONTEXT=$SCRIPT_DIR

# Repository info
OWNER='diamondlightsource'
REPO='magnetic-materials-workflows'
TAG='latest'
# IMAGE_REF="ghcr.io/diamondlightsource/magnetic-materials-workflows/quanty:latest"
IMAGE_REF="ghcr.io/${OWNER}/${REPO}/quanty:${TAG}"

# Validate ZIP quickly (avoid mounting a bad file)
if ! file "$ZIP" | grep -qi 'zip archive'; then
  echo "ERROR: $ZIP does not look like a ZIP archive."
  file "$ZIP" || true
  exit 1
fi

#--------------------------------------------------------------
# Build Image
#--------------------------------------------------------------
echo "==> podman build ${IMAGE_REF}"
podman build \
  --tag "$IMAGE_REF" \
  --secret id=quanty_zip,src="$ZIP" \
  "$BUILD_CONTEXT"


#--------------------------------------------------------------
# Publish to GHCR
#--------------------------------------------------------------
# podman tag localhost/quanty:latest ghcr.io/diamondlightsource/magnetic-materials-workflows/quanty:latest
# podman push ghcr.io/diamondlightsource/magnetic-materials-workflows/quanty:latest
echo
echo "==> Pushing $IMAGE_REF"
podman push "$IMAGE_REF"

echo
echo "✅ Done. Pushed $IMAGE_REF"
# podman pull ghcr.io/diamondlightsource/magnetic-materials-workflows/quanty

