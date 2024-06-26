bl_info = {
    "name": "DirectCam",
    "author": "Manning",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "3D Viewport Header",
    "description": "Add a camera at the current viewer location",
    "category": "Object"
}


import bpy
from mathutils import Matrix


def get_viewer_location_and_rotation():
    viewer_loc = None
    viewer_rot = None

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    space = area.spaces.active
                    if space.type == 'VIEW_3D':
                        region_3d = space.region_3d
                        view_matrix = region_3d.view_matrix
                        viewer_loc = view_matrix.inverted().translation
                        viewer_rot = view_matrix.to_3x3().inverted()
                        return viewer_loc, viewer_rot
    return None, None

def create_camera_at_viewer_location(viewer_loc, viewer_rot):
    bpy.ops.object.camera_add(location=viewer_loc)
    new_camera = bpy.context.object
    new_camera.rotation_euler = viewer_rot.to_euler()

    bpy.context.scene.camera = new_camera

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.camera = new_camera
                    space.region_3d.view_perspective = 'CAMERA'

    print("New camera added at viewer location and rotation and view set to the new camera.")

class OBJECT_OT_add_camera_at_viewer(bpy.types.Operator):
    bl_idname = "object.add_camera_at_viewer"
    bl_label = ""
    bl_description = "Add a camera at the current viewer location and set view to the new camera"
    bl_icon = "CON_CAMERASOLVER"

    def execute(self, context):
        viewer_loc, viewer_rot = get_viewer_location_and_rotation()
        icon = 'CON_CAMERASOLVER'
        if viewer_loc and viewer_rot:
            create_camera_at_viewer_location(viewer_loc, viewer_rot)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "3D View not found or viewer location/rotation could not be determined.")
            return {'CANCELLED'}
        self.layout.operator(OBJECT_OT_add_camera_at_viewer.bl_idname, icon=icon)

def draw_header_button(self, context):
    layout = self.layout
    layout.operator(OBJECT_OT_add_camera_at_viewer.bl_idname, icon="CON_CAMERASOLVER")

def register():
    bpy.utils.register_class(OBJECT_OT_add_camera_at_viewer)
    bpy.types.VIEW3D_HT_header.append(draw_header_button)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_camera_at_viewer)
    bpy.types.VIEW3D_HT_header.remove(draw_header_button)

if __name__ == "__main__":
    register()
