# Viewport Screenshot to Clipboard for Blender (Free Edition)

A lightweight Blender Python tool to capture the current 3D Viewport directly to your OS clipboard with a single click.

No saving temporary image files, no manual cropping—just hit **Ctrl + V** anywhere (Discord, Slack, Notion, PureRef, Photoshop, etc.).
 
> Check out the **Pro Edition** on [Gumroad](https://mashitaya.gumroad.com/l/tdgmq/LAUNCH) or [BOOTH](https://yworks.booth.pm/items/9112055).

---

## ⚡ Features (Free Edition)

- **Instant Clipboard Copy:** Copies the active 3D Viewport render straight to your OS clipboard.
- **Clean Viewport Output:** Automatically hides 3D gizmos, floor grid, origins, and overlays.
- **Zero External Dependencies:** Uses Blender's native Python API / GPU module (no pip packages required).
- **Lightweight & Portable:** Single `.py` file—runs immediately without any complex installer.
- **Compatibility:** Tested on **Blender 3.2, 3.3 LTS, 3.6 LTS, 4.0, 4.1, 4.2 LTS, 4.3, and 4.4+** (Windows / macOS / Linux).

---

## 🚀 How to Use (No Installer Required)

Since the Free Edition is provided as a standalone script (`viewport_screenshot_blender_free.py`), you can run or install it using either of the following methods:

### Method 1: Open & Execute via Text Editor (Direct Run)

1. Download [`viewport_screenshot_blender_free.py`](./viewport_screenshot_blender_free.py).
2. Open Blender and switch to the **Scripting** workspace (or open a **Text Editor** window).
3. In the Text Editor header menu, click **Text > Open...** (or press `Alt + O`).
4. Select the downloaded `viewport_screenshot_blender_free.py`.
5. Click **Run Script** (the play icon ▶ in the Text Editor header) or press `Alt + P`.
   - Your current 3D Viewport will be instantly copied to your clipboard!
   - *(Optional: Enable **Text > Register** in the header so the script automatically loads whenever you open this blend file).*

---

### Method 2: Install as a Single-File Add-on (Preferences)

1. In Blender, go to **Edit > Preferences > Add-ons**.
2. Click the top-right down arrow (or header menu) and select **Install from Disk...** (or **Install...** in Blender 4.1 and earlier).
3. Browse and select `viewport_screenshot_blender_free.py`.
4. Enable the checkbox for **"Generic: Viewport Screenshot to Clipboard"**.
5. Press `F3` in the 3D Viewport and search for **"Viewport Screenshot to Clipboard"** to execute anytime!

---

## ⚖️ Free vs. Pro Comparison

| Feature | Free Edition | Pro Edition |
| :--- | :---: | :---: |
| One-Click Clipboard Copy | ✅ | ✅ |
| Clean Viewport (Hide Overlays & Gizmos) | ✅ | ✅ |
| Dedicated N-Panel Sidebar UI | ❌ | ✅ |
| Customizable Hotkey Binding | Manual | ✅ One-Click Setup |
| Transparent Background (Alpha Cutout) | ❌ | ✅ |
| High-Res Multiplier (1x / 2x / 4K) | ❌ | ✅ |
| Render Region / Camera Framing Lock | ❌ | ✅ |
| Lifetime Updates & Priority Support | Community | ✅ Priority |

👉 **Upgrade to Pro:** [Gumroad](https://mashitaya.gumroad.com/l/tdgmq/LAUNCH) | [BOOTH (国内向け)](https://yworks.booth.pm/items/9112055)

---

## 📄 License & Terms

- **Usage:** Free for both non-commercial and commercial 3D modeling and animation workflows.
- **Restrictions:** Redistribution, resale, or sublicensing of this script/source code is strictly prohibited.

---
---

## 🇯🇵 日本語説明 (Japanese)

Blenderの3Dビューポート画面を**ワンクリックで直接クリップボードへ保存する**Pythonツールです。

一時ファイルの保存やキャプチャ画像のトリミング作業をすることなく、そのまま Discord / Slack / Notion / PureRef / Photoshop 等へ **`Ctrl + V`** で即座に貼り付け可能です。

> ⚡多機能な **Pro版** は [BOOTH](https://yworks.booth.pm/items/9112055) または [Gumroad](https://mashitaya.gumroad.com/l/tdgmq/LAUNCH) にて公開中です。

---

### ⚡ 主な特徴（無料版）

- **クリップボード直接コピー:** ファイル保存の手間なしに、チャットやドキュメントへ即貼り付け。
- **UI非表示クリーン出力:** グリッド、3Dカーソル、ギズモ、オーバーレイなどの余計な表示を自動で除外。
- **外部ライブラリ不要:** Blender標準のPython / GPUモジュールのみで動作（追加インストール不要）。
- **完全スタンドアロン:** 単体 `.py` スクリプト形式のため、専用インストーラー不要ですぐ利用可能。
- **対応バージョン:** Blender 3.2, 3.3 LTS, 3.6 LTS, 4.0, 4.1, 4.2 LTS, 4.3, 4.4以降（Windows / macOS / Linux）

---

### 🚀 インストールと使い方（インストーラーなし）

無料版は単体スクリプト（`viewport_screenshot_blender_free.py`）のみで動作します。以下のいずれかの方法でご利用いただけます。

#### 方法1：テキストエディターから開いて実行（手軽・即時実行）

1. 本リポジトリから [`viewport_screenshot_blender_free.py`](./viewport_screenshot_blender_free.py) をダウンロードします。
2. Blenderを起動し、上部タブの **「Scripting」** ワークスペースを選択するか、任意のエリアを **「テキストエディター (Text Editor)」** に切り替えます。
3. テキストエディターのメニューから **テキスト > 開く...**（または `Alt + O`）を選択します。
4. ダウンロードした `viewport_screenshot_blender_free.py` を選択して開きます。
5. 上部ツールバーの再生ボタン（**スクリプト実行** / `Alt + P`）をクリックします。
   - 現在の3Dビューポート画面がクリップボードへコピーされます。
   - *(※ 常時読み込みたい場合は、エディターメニューの「テキスト > 登録」にチェックを入れてスタートアップファイルに保存してください)*

---

#### 方法2：設定からアドオンとしてインストール（標準的な導入）

1. Blenderのトップメニューから **編集 > プリファレンス (Preferences)** を開きます。
2. 左メニューの **「アドオン」** を選択します。
3. 右上のドロップダウン矢印から **「ディスクからインストール... (Install from Disk...)」**（Blender 4.1以前では右上の「インストール...」ボタン）をクリックします。
4. ダウンロードした `viewport_screenshot_blender_free.py` を選択します。
5. リストに表示された **「Viewport Screenshot to Clipboard」** のチェックボックスをオンにして有効化します。
6. 3Dビューポート上で `F3` キーを押し、**「Viewport Screenshot to Clipboard」** と検索して実行できます。

---

### ⚖️ 無料版とPro版の違い

| 機能 | 無料版 (Free) | Pro版 (BOOTH / Gumroad) |
| :--- | :---: | :---: |
| ワンクリック・クリップボードコピー | ✅ | ✅ |
| UI/ギズモ/グリッドの自動非表示 | ✅ | ✅ |
| Nパネル（サイドバー）専用メニュー | ❌ | ✅ |
| ショートカットキーの簡単ワンクリック割当 | 手動設定 | ✅ 専用設定あり |
| 背景透過（アルファ切り抜き）キャプチャ | ❌ | ✅ |
| 高解像度スケーリング（1x / 2x / 4K） | ❌ | ✅ |
| レンダリング枠・カメラ画角ロック | ❌ | ✅ |
| アップデート＆優先サポート | コミュニティ | ✅ 優先対応 |

👉 **Pro版はこちら:** [BOOTH（国内向け）](https://yworks.booth.pm/items/9112055) | [Gumroad（海外向け）](https://mashitaya.gumroad.com/l/tdgmq/LAUNCH)

---

### 📄 ライセンス

- **利用許諾:** 個人・商用問わず、3Dモデル制作や日々の制作業務において無料で自由にご利用いただけます。
- **禁止事項:** 本ツールのスクリプト自体の再配布、転載、再販売は固く禁止します。
