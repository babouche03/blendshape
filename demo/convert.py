import bpy

ARKIT_NAME = "ARKit_Head"
TRIPO_NAME = "Tripo_Head"
EXPORT_PATH = "//tripo_with_blendshape.glb"

arkit = bpy.data.objects.get(ARKIT_NAME)
tripo = bpy.data.objects.get(TRIPO_NAME)

if not arkit or not tripo:
    raise Exception("❌ 找不到 ARKit_Head 或 Tripo_Head")

# 确保选中 Tripo
bpy.ops.object.select_all(action='DESELECT')
tripo.select_set(True)
bpy.context.view_layer.objects.active = tripo

# 应用所有变换
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# 添加 Surface Deform
surf = tripo.modifiers.new(name="SurfaceDeform_ARKit", type='SURFACE_DEFORM')
surf.target = arkit

bpy.ops.object.surfacedeform_bind(modifier=surf.name)

print("✅ Surface Deform 绑定完成")

# 烘焙为 Shape Keys
bpy.ops.object.modifier_apply_as_shapekey(
    keep_modifier=False,
    modifier=surf.name
)

print("✅ Shape Keys 已生成")

# 清理：删除 ARKit 模板
bpy.ops.object.select_all(action='DESELECT')
arkit.select_set(True)
bpy.ops.object.delete()

print("🧹 模板已删除，仅保留 Tripo")

# 导出 GLB
bpy.ops.export_scene.gltf(
    filepath=EXPORT_PATH,
    export_format='GLB',
    export_apply=True,
    export_morph=True,
    export_selected=False
)

print("🎉 导出完成:", EXPORT_PATH)