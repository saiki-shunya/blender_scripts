import bpy, math
from mathutils import Vector

# ── Edit these names if needed ─────────────────────────────
CAM_NAME = "Camera"
FLOOR_POINT_NAME = "Empty"
# ───────────────────────────────────────────────────────────

def clear_custom_props(obj):
    """Remove all custom properties from an object (cleans Item > Custom Properties)."""
    for k in list(obj.keys()):
        try:
            del obj[k]
        except Exception:
            pass
    if "_RNA_UI" in obj:
        try:
            del obj["_RNA_UI"]
        except Exception:
            pass

def zero_snap(v, eps=0.05):
    """Snap tiny values to exactly 0.0 to avoid showing -0.0/+0.0."""
    return 0.0 if abs(v) < eps else v

scene = bpy.context.scene
u = scene.unit_settings.scale_length  # meters per Blender Unit

cam = bpy.data.objects.get(CAM_NAME)
floor = bpy.data.objects.get(FLOOR_POINT_NAME)

if cam is None:
    raise ValueError(f"Object '{CAM_NAME}' not found.")
if floor is None:
    raise ValueError(f"Object '{FLOOR_POINT_NAME}' not found.")

cam_world = cam.matrix_world.translation
floor_world = floor.matrix_world.translation

vec = cam_world - floor_world
dist_bu = vec.length                            # 3D distance in BU
height_bu = vec.z                               # + if camera is above
dist_m = dist_bu * u
height_m = height_bu * u

# ── Camera tilt (pitch) convention ────────────────────────
# Forward vector in world space (camera looks along local -Z)
fwd = cam.matrix_world.to_3x3() @ Vector((0.0, 0.0, -1.0))
xy_len = (fwd.x*fwd.x + fwd.y*fwd.y) ** 0.5

# Up-positive: 0°=level, +90°=straight up, -90°=straight down (matches HUD)
base_tilt_deg = math.degrees(math.atan2(fwd.z, max(1e-8, xy_len)))
tilt_up_deg = zero_snap(base_tilt_deg, eps=0.05)

# Print for copy/paste
print(f"3D distance: {dist_m:.3f} m  ({dist_bu:.3f} BU)")
print(f"Vertical height (Z): {abs(height_m):.3f} m  ({abs(height_bu):.3f} BU)  "
      f"[signed: {height_m:+.3f} m]")
print(f"Tilt (up +): {tilt_up_deg:+.1f}°")

# Clear old custom props, then store fresh ones on Camera
clear_custom_props(cam)
cam['Distance to Empty (m)'] = float(dist_m)
cam['Height to Empty (m)']   = float(abs(height_m))   # absolute height
cam['Tilt (up +, deg)']      = float(tilt_up_deg)
