bl_info = {
    "name": "3D Viewport Screenshot (Free)",
    "author": "mashitaya",
    "version": (1, 0, 0),
    "blender": (3, 2, 0),
    "location": "View3D > Header / Sidebar (N) > Capture",
    "description": "3Dビューポートをサイドメニューなしの状態で1枚保存します（無料・お試し版）",
    "category": "3D View",
}

# ---------------------------------------------------------------------------
# 無料（お試し）版の機能
#   できること : 3Dビューポートの撮影 / PNG保存 / Windows標準Screenshotsへ保存
#                サイドバー・ツールバー・ヘッダーを隠して撮影
#   製品版のみ : 他のパネルの撮影 / クリックでパネル選択 / サイドバーのみ撮影
#                JPEG・BMP保存 / ファイル名・プリフィックス・サフィックス・連番
#                保存先フォルダの指定 / クリップボードへコピー / ギズモ・オーバーレイ非表示
# ---------------------------------------------------------------------------

import os
import re
import time
import platform
import subprocess
from datetime import datetime
import bpy
from bpy.types import Operator, Panel
from bpy.props import BoolProperty


# 製品版の案内ページのURL。設定するとパネルに「製品版を見る」ボタンが出ます（空なら非表示）
PRO_URL = ""

# 製品版で使える機能（パネルにロック表示します）
PRO_FEATURES = (
    "3Dビュー以外のパネル（UV / ノード / タイムライン等）の撮影",
    "画面のパネルをクリックして撮影",
    "サイドバーのみの撮影",
    "JPEG / BMP 形式での保存",
    "ファイル名・プリフィックス・サフィックス・連番",
    "保存先フォルダの自由な指定",
    "クリップボードにコピー (Ctrl+V)",
    "ギズモ / オーバーレイを隠す",
)

# 撮影前にUIが消えて再描画されるのを待つ回数（0.1秒 x 回数）。まだ黒い場合は増やす
WAIT_TICKS = 4
# 連打防止(秒)
DEBOUNCE_SEC = 1.2

_LAST_EXEC = 0.0


def get_windows_screenshots_dir():
    """Windowsの標準Screenshotsフォルダパスを取得（OneDrive環境対応）"""
    home = os.path.expanduser("~")
    default_path = os.path.join(home, "Pictures", "Screenshots")

    onedrive = os.environ.get("OneDrive") or os.environ.get("OneDriveConsumer")
    if onedrive and os.path.exists(onedrive):
        for sub in ("Pictures", "画像"):
            candidate = os.path.join(onedrive, sub, "Screenshots")
            if os.path.exists(candidate):
                return candidate

    try:
        os.makedirs(default_path, exist_ok=True)
    except Exception:
        pass
    return default_path


def open_directory_in_explorer(folder_path):
    """指定フォルダをエクスプローラー等で開く（撮影は一切行わない）"""
    try:
        os.makedirs(folder_path, exist_ok=True)
        system = platform.system()
        if system == "Windows":
            os.startfile(folder_path)
        elif system == "Darwin":
            subprocess.run(["open", folder_path], check=False)
        else:
            subprocess.run(["xdg-open", folder_path], check=False)
    except Exception:
        pass


def safe_set_attr(obj, attr, value):
    """読み取り専用チェックと例外ガードを行い、(変更有無, 元の値) を返す"""
    if obj is None or not hasattr(obj, attr):
        return False, None
    try:
        if hasattr(obj, "bl_rna") and attr in obj.bl_rna.properties:
            if obj.bl_rna.properties[attr].is_readonly:
                return False, None

        orig_val = getattr(obj, attr)
        if orig_val == value:
            return False, orig_val

        setattr(obj, attr, value)
        return True, orig_val
    except Exception:
        return False, None


def wait_for_file(path, timeout=5.0):
    """スクリーンショットの書き込み完了（ファイルサイズが安定）を待つ"""
    deadline = time.time() + timeout
    last_size = -1
    while time.time() < deadline:
        if os.path.isfile(path):
            size = os.path.getsize(path)
            if size > 0 and size == last_size:
                return True
            last_size = size
        time.sleep(0.05)
    return False


def resolve_view3d_area(context):
    """撮影対象の3Dビューを決める（操作中の3Dビュー、無ければ最大の3Dビュー）"""
    if context.area and context.area.type == 'VIEW_3D':
        return context.area
    if context.screen:
        areas = [a for a in context.screen.areas if a.type == 'VIEW_3D']
        if areas:
            return max(areas, key=lambda a: a.width * a.height)
    return None


def begin_capture(context, area, operator_instance):
    """UIを一時的に隠し、撮影に必要な情報を返す（撮影はまだしない）"""
    if not area:
        operator_instance.report({'ERROR'}, "3Dビューポートが見つかりませんでした。")
        return None

    region = None
    for r in area.regions:
        if r.type == 'WINDOW':
            region = r
            break
    if not region:
        operator_instance.report({'ERROR'}, "3Dビューの描画領域が見つかりませんでした。")
        return None

    scene = context.scene
    space = area.spaces.active

    output_dir = get_windows_screenshots_dir()
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        operator_instance.report({'ERROR'}, f"保存先フォルダを作成できませんでした: {e}")
        return None

    blend_name = "Untitled"
    if bpy.data.filepath:
        blend_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{blend_name}_{timestamp}.png"

    attrs = []
    if getattr(scene, "vpssf_hide_sidebar", True):
        attrs.append("show_region_ui")           # 右側サイドバー (Nキー)
    if getattr(scene, "vpssf_hide_toolbar", True):
        attrs.extend((
            "show_region_toolbar",               # 左側ツールバー (Tキー)
            "show_region_hud",                   # 左下オペレーター履歴パネル
            "show_region_asset_shelf",           # 下部アセットシェルフ
            "show_region_channels",
        ))
    if getattr(scene, "vpssf_hide_header", True):
        attrs.extend((
            "show_region_header",                # メインヘッダー
            "show_region_tool_header",           # ツール設定バー
            "show_region_footer",                # フッター
        ))

    orig_attrs = {}
    if space:
        for attr in attrs:
            changed, orig_val = safe_set_attr(space, attr, False)
            if changed:
                orig_attrs[attr] = orig_val

    area.tag_redraw()

    return {
        "win": context.window,
        "scr": context.screen,
        "area": area,
        "region": region,
        "space": space,
        "orig_attrs": orig_attrs,
        "changed": bool(orig_attrs),
        "output_dir": output_dir,
        "blend_name": blend_name,
        "filename": filename,
        "filepath": os.path.join(output_dir, filename),
    }


def restore_ui(state):
    """隠していたUI表示を元に戻す"""
    try:
        if state["space"]:
            for attr, val in state["orig_attrs"].items():
                safe_set_attr(state["space"], attr, val)
        state["area"].tag_redraw()
    except Exception:
        pass


def finish_capture(context, state, operator_instance):
    """描画が反映された状態で撮影し、UIを復元する"""
    try:
        with context.temp_override(
            window=state["win"],
            screen=state["scr"],
            area=state["area"],
            region=state["region"],
        ):
            bpy.ops.screen.screenshot_area(filepath=state["filepath"], check_existing=False)
    except Exception as e:
        operator_instance.report({'ERROR'}, f"撮影に失敗しました: {e}")
        return {'CANCELLED'}
    finally:
        restore_ui(state)

    if not wait_for_file(state["filepath"]):
        operator_instance.report({'ERROR'}, "画像を保存できませんでした。")
        return {'CANCELLED'}

    # 無料版は常に最新1枚のみ残す（同じシーンの古い画像を削除）
    try:
        pattern = re.compile(rf"^{re.escape(state['blend_name'])}_\d{{8}}_\d{{6}}\.png$", re.IGNORECASE)
        out = state["output_dir"]
        for fname in os.listdir(out):
            if fname != state["filename"] and pattern.match(fname):
                old_path = os.path.join(out, fname)
                if os.path.isfile(old_path):
                    os.remove(old_path)
    except Exception:
        pass

    operator_instance.report({'INFO'}, f"3Dビューポートを保存しました: {state['filename']}")
    return {'FINISHED'}


class VIEW3D_OT_capture_viewport_free(Operator):
    """3Dビューポートをサイドメニューなしの状態で1枚保存"""
    bl_idname = "view3d.capture_viewport_free"
    bl_label = "3Dビューをキャプチャ"
    bl_options = {'INTERNAL'}

    _timer = None
    _state = None
    _ticks = 0

    def invoke(self, context, event):
        global _LAST_EXEC
        now = time.time()
        if now - _LAST_EXEC < DEBOUNCE_SEC:
            return {'CANCELLED'}
        _LAST_EXEC = now

        state = begin_capture(context, resolve_view3d_area(context), self)
        if state is None:
            return {'CANCELLED'}

        # 何も隠していない場合は待たずに即撮影
        if not state["changed"]:
            return finish_capture(context, state, self)

        self._state = state
        self._ticks = 0
        self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def _remove_timer(self, context):
        if self._timer is not None:
            try:
                context.window_manager.event_timer_remove(self._timer)
            except Exception:
                pass
            self._timer = None

    def modal(self, context, event):
        if event.type in {'ESC', 'RIGHTMOUSE'}:
            self._remove_timer(context)
            restore_ui(self._state)
            self._state = None
            self.report({'INFO'}, "キャプチャをキャンセルしました。")
            return {'CANCELLED'}

        if event.type == 'TIMER':
            self._ticks += 1
            for a in context.screen.areas:
                a.tag_redraw()
            if self._ticks >= WAIT_TICKS:
                self._remove_timer(context)
                state, self._state = self._state, None
                return finish_capture(context, state, self)

        return {'RUNNING_MODAL'}


class VIEW3D_OT_open_screenshots_folder_free(Operator):
    """撮影は行わず、保存先フォルダだけをエクスプローラーで開きます"""
    bl_idname = "view3d.open_screenshots_folder_free"
    bl_label = "保存先フォルダを開く"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        open_directory_in_explorer(get_windows_screenshots_dir())
        return {'FINISHED'}


class VIEW3D_PT_viewport_screenshot_free_panel(Panel):
    """3Dビューポートのサイドバー（Nキー）に表示されるパネル"""
    bl_label = "Viewport Capture (Free)"
    bl_idname = "VIEW3D_PT_viewport_screenshot_free"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Capture"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)
        col.scale_y = 1.35
        col.operator(
            "view3d.capture_viewport_free",
            text="3Dビューをキャプチャ (1枚保存)",
            icon='CAMERA_DATA'
        )

        hide_box = layout.box()
        hide_box.label(text="撮影時に隠すメニュー:", icon='HIDE_ON')
        hide_col = hide_box.column(align=True)
        hide_col.prop(scene, "vpssf_hide_sidebar", text="サイドバー (Nパネル) を隠す")
        hide_col.prop(scene, "vpssf_hide_toolbar", text="ツールバー / 操作履歴を隠す")
        hide_col.prop(scene, "vpssf_hide_header", text="上部ヘッダーを隠す")

        dir_box = layout.box()
        dir_box.label(text="保存先 (Windows標準 Screenshots):", icon='FILE_FOLDER')
        path_col = dir_box.column(align=True)
        path_col.scale_y = 0.75
        path_col.label(text=get_windows_screenshots_dir())
        dir_box.operator(
            "view3d.open_screenshots_folder_free",
            text="保存先フォルダを開く（撮影しない）",
            icon='DISK_DRIVE'
        )
        note_col = dir_box.column(align=True)
        note_col.scale_y = 0.75
        note_col.label(text="形式: PNG / 常に最新1枚のみ保存")

        pro_box = layout.box()
        pro_box.label(text="製品版で使える機能", icon='LOCKED')
        pro_col = pro_box.column(align=True)
        pro_col.scale_y = 0.8
        for text in PRO_FEATURES:
            pro_col.label(text=text, icon='DOT')
        if PRO_URL:
            op = pro_box.operator("wm.url_open", text="製品版を見る", icon='URL')
            op.url = PRO_URL


def draw_header_button_free(self, context):
    """3Dビューポート右上ヘッダーへのワンクリック撮影ボタン"""
    layout = self.layout
    layout.separator()
    layout.operator("view3d.capture_viewport_free", text="", icon='CAMERA_DATA')


SCENE_PROPS = (
    "vpssf_hide_sidebar",
    "vpssf_hide_toolbar",
    "vpssf_hide_header",
)

classes = (
    VIEW3D_OT_capture_viewport_free,
    VIEW3D_OT_open_screenshots_folder_free,
    VIEW3D_PT_viewport_screenshot_free_panel,
)


def register():
    try:
        bpy.types.VIEW3D_HT_header.remove(draw_header_button_free)
    except Exception:
        pass

    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass
        bpy.utils.register_class(cls)

    bpy.types.Scene.vpssf_hide_sidebar = BoolProperty(
        name="サイドバーを隠す",
        default=True,
        description="ONの場合、撮影の瞬間にサイドバー（Nキー）を非表示にして撮影し、直後に元へ戻します"
    )
    bpy.types.Scene.vpssf_hide_toolbar = BoolProperty(
        name="ツールバーを隠す",
        default=True,
        description="ONの場合、ツールバー（Tキー）と操作履歴パネルを非表示にして撮影します"
    )
    bpy.types.Scene.vpssf_hide_header = BoolProperty(
        name="ヘッダーを隠す",
        default=True,
        description="ONの場合、パネル上部のヘッダーやツール設定バーを非表示にして撮影します"
    )

    bpy.types.VIEW3D_HT_header.append(draw_header_button_free)


def unregister():
    try:
        bpy.types.VIEW3D_HT_header.remove(draw_header_button_free)
    except Exception:
        pass

    for prop in SCENE_PROPS:
        if hasattr(bpy.types.Scene, prop):
            delattr(bpy.types.Scene, prop)

    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass


if __name__ == "__main__":
    register()
