# Blender (Headless) 🧊

Run Blender in headless mode with Python scripts for 3D modeling, rendering, and GLB export. No GUI needed — write a Python script, run it through Blender's built-in `bpy` API, get your 3D assets out.

## Setup

**Requirements:**
- [Blender](https://www.blender.org/download/) (3.6+ recommended, 4.x works)

**Install Blender:**

macOS:
```bash
brew install --cask blender
# Binary ends up at /Applications/Blender.app/Contents/MacOS/Blender
```

Linux:
```bash
sudo snap install blender --classic
# Or download from blender.org
```

Windows:
```
Download from https://www.blender.org/download/
```

## Usage

### Using the wrapper script

```bash
bash scripts/run_blender.sh /path/to/your_script.py
```

With arguments passed to your script:
```bash
bash scripts/run_blender.sh /path/to/your_script.py -- --output /tmp/model.glb --resolution 2048
```

### Direct invocation

```bash
blender --background --factory-startup --python /path/to/your_script.py -- [script args]
```

- `--background` — No GUI
- `--factory-startup` — Ignore user preferences for deterministic results
- `--` — Separates Blender args from your script's args

### Accessing script arguments

```python
import sys

argv = sys.argv
if "--" in argv:
    argv = argv[argv.index("--") + 1:]
else:
    argv = []
```

## Example: Build geometry, render, and export

```python
import bpy

# Clear default scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Create a cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object

# Add material
mat = bpy.data.materials.new(name="MyMaterial")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.8, 0.2, 0.1, 1.0)
cube.data.materials.append(mat)

# Export GLB
bpy.ops.export_scene.gltf(
    filepath="/tmp/output.glb",
    export_format='GLB',
    use_selection=False,
    export_yup=True,
    export_apply=True,
)

# Add camera + light for preview render
bpy.ops.object.camera_add(location=(4, -4, 3))
cam = bpy.context.active_object
cam.rotation_euler = (1.1, 0, 0.8)
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type='SUN', location=(5, -5, 8))

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024
scene.render.filepath = "/tmp/preview.png"
bpy.ops.render.render(write_still=True)
```

## Tips

- Always use `--factory-startup` for reproducible builds
- Scripts should be idempotent — clean up named objects before creating them
- For GLB export: use Principled BSDF nodes (glTF compatible)
- Set Emission Color + Emission Strength on materials for glow effects
- Shape keys require stable topology — no booleans after adding shape keys
- Render a preview PNG in your script, then delete camera/light before GLB export if you don't want them in the model

## Use with AI Agents

See [`AGENTS.md`](./AGENTS.md) for instructions you can paste into any AI agent's context.
