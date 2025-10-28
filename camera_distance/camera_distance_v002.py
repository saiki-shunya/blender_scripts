import bpy, math
from mathutils import Vector

# ── Edit these names if needed ─────────────────────────────
CAM_NAME = "Camera"
FLOOR_POINT_NAME = "Empty"
# ───────────────────────────────────────────────────────────

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

# UP-POSITIVE for filmmakers: 0°=level, +90°=straight up, negative=down
# Inverted sign from previous version so that "up" reads positive for your setup.
tilt_up_deg = -math.degrees(math.atan2(fwd.z, max(1e-8, xy_len)))

# Print for copy/paste
print(f"3D distance: {dist_m:.3f} m  ({dist_bu:.3f} BU)")
print(f"Vertical height (Z): {abs(height_m):.3f} m  ({abs(height_bu):.3f} BU)  "
      f"[signed: {height_m:+.3f} m]")
print(f"Tilt (up +): {tilt_up_deg:+.1f}°")

# Store on Camera as custom properties (visible in Item > Custom Properties)
cam['distance_to_bridge_m'] = float(dist_m)
cam['height_to_bridge_m']   = float(abs(height_m))   # absolute height
cam['tilt_up_deg']          = float(tilt_up_deg)     # filmmakers: up is +
