# ───────────────── Tilt HUD (up-positive) — Bottom-Right ────────────────
# Shows in any 3D View. Up (+) means tilting above the horizon.
import bpy, math, blf
from mathutils import Vector

CAM_NAME = "camera_test_002"   # or None to use scene.camera
ONLY_WHEN_IN_CAMERA_VIEW = False
_MARGIN = 20
_FONT_SIZE = 16

_TILT_HUD_HANDLE = getattr(bpy.types.Scene, "_TILT_HUD_HANDLE", None)

def _find_cam():
    if CAM_NAME:
        cam = bpy.data.objects.get(CAM_NAME)
        if cam and cam.type == 'CAMERA':
            return cam
    return bpy.context.scene.camera

def _tilt_up_deg(cam):
    fwd = cam.matrix_world.to_3x3() @ Vector((0.0, 0.0, -1.0))  # camera forward (world)
    xy_len = (fwd.x*fwd.x + fwd.y*fwd.y) ** 0.5
    return math.degrees(math.atan2(fwd.z, max(1e-8, xy_len)))   # 0=horizon, +up, -down

def _draw_tilt_hud():
    if ONLY_WHEN_IN_CAMERA_VIEW:
        rd = bpy.context.region_data
        if not (rd and rd.view_perspective == 'CAMERA'):
            return

    cam = _find_cam()
    if not cam:
        return

    tilt = _tilt_up_deg(cam)
    txt = f"Tilt (up +): {tilt:+.1f}°"

    region = bpy.context.region
    if not region:
        return

    font_id = 0
    blf.size(font_id, _FONT_SIZE)
    text_w, text_h = blf.dimensions(font_id, txt)

    # Bottom-right placement (origin is bottom-left)
    x = region.width  - text_w - _MARGIN
    y = _MARGIN

    blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
    blf.position(font_id, x, y, 0)
    blf.draw(font_id, txt)

def _toggle():
    global _TILT_HUD_HANDLE
    if _TILT_HUD_HANDLE:
        bpy.types.SpaceView3D.draw_handler_remove(_TILT_HUD_HANDLE, 'WINDOW')
        _TILT_HUD_HANDLE = None
        bpy.types.Scene._TILT_HUD_HANDLE = None
        print("Tilt HUD: OFF")
    else:
        _TILT_HUD_HANDLE = bpy.types.SpaceView3D.draw_handler_add(
            _draw_tilt_hud, (), 'WINDOW', 'POST_PIXEL'
        )
        bpy.types.Scene._TILT_HUD_HANDLE = _TILT_HUD_HANDLE
        print("Tilt HUD: ON (bottom-right, up +)")

_toggle()
# ─────────────────────────────────────────────────────────────────────────
