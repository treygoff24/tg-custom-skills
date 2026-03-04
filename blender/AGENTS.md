# Blender (Headless) — Agent Instructions

You have access to Blender for headless 3D modeling, rendering, and GLB export. Write Python scripts that use Blender's `bpy` API, then execute them in background mode.

## Prerequisites

- Blender must be installed
- Common paths: `/Applications/Blender.app/Contents/MacOS/Blender` (macOS), `blender` (Linux/Windows if on PATH)

## Running Scripts

Use the wrapper script (adjust the path to where this skill lives):

```bash
bash scripts/run_blender.sh /path/to/your_script.py -- [script args]
```

Or invoke directly:

```bash
blender --background --factory-startup --python /path/to/script.py -- [script args]
```

- `--background`: No GUI
- `--factory-startup`: Ignore user prefs for deterministic results
- `--`: Separates Blender args from script args

## Parsing Script Arguments

```python
import sys
argv = sys.argv
if "--" in argv:
    argv = argv[argv.index("--") + 1:]
else:
    argv = []
```

## Standard Workflow

Write a self-contained Python script that:

1. Clears the default scene or starts from factory settings
2. Builds geometry using `bpy` ops or direct mesh manipulation
3. Assigns materials (use Principled BSDF for glTF compatibility)
4. Exports GLB for web/game use
5. Optionally adds a temporary camera + light, renders a preview PNG, then removes them before GLB export

### GLB Export

```python
bpy.ops.export_scene.gltf(
    filepath="/path/to/output.glb",
    export_format='GLB',
    use_selection=False,
    export_yup=True,
    export_apply=True,
    export_animations=True,
    export_nla_strips=True,
    export_morph=True,
)
```

### Preview Render

```python
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024
scene.render.filepath = "/path/to/preview.png"
bpy.ops.render.render(write_still=True)
```

## Key Rules

- Always use `--factory-startup` for reproducible builds
- Scripts must be idempotent — clean up named objects before creating
- Use Principled BSDF node for materials (glTF compatible)
- Set Emission Color + Emission Strength for glow effects
- Shape keys require stable topology — no booleans after adding shape keys
- Preview renders: set up camera + light in script, render, then delete them before GLB export
