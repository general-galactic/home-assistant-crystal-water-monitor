#!/usr/bin/env bash
set -euo pipefail

MANIFEST="custom_components/crystal_water_monitor/manifest.json"

current=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['version'])")
echo "Current version: $current"
echo -n "New version: "
read -r version

if [[ -z "$version" ]]; then
  echo "Aborted: no version entered."
  exit 1
fi

# Validate format: digits and dots, optional -suffix
if ! [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+|(\.[a-zA-Z][a-zA-Z0-9]*))?$ ]]; then
  echo "Invalid version format. Use semver e.g. 1.2.0 or 1.2.0.dev"
  exit 1
fi

# Ensure working tree is clean
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Working tree has uncommitted changes. Commit or stash them first."
  exit 1
fi

# Update manifest.json
python3 -c "
import json
with open('$MANIFEST') as f:
    m = json.load(f)
m['version'] = '$version'
with open('$MANIFEST', 'w') as f:
    json.dump(m, f, indent=2)
    f.write('\n')
"

echo "Updated $MANIFEST to $version"

git add "$MANIFEST"
git commit -m "Release $version"
git tag "v$version"

echo ""
echo "Tagged v$version. Push with:"
echo "  git push origin main && git push origin v$version"
echo ""
echo -n "Push now? [y/N] "
read -r push
if [[ "$push" =~ ^[Yy]$ ]]; then
  git push origin main
  git push origin "v$version"
  echo "Pushed. GitHub Actions will create the release automatically."
fi
