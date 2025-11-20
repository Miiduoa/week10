# TMDB 電影資料庫查詢系統

這是一個使用 Python 和 Tkinter 開發的電影資料庫查詢應用程式，整合了 The Movie Database (TMDB) API。

## 功能特色

- 🎬 **電影搜尋**：支援繁體中文、英文電影名稱或 Movie ID 查詢
- 💰 **收入查詢**：顯示電影的票房收入資訊
- 🖼️ **海報顯示**：自動下載並顯示電影海報
- 🌐 **多語言支援**：支援中文和英文電影名稱搜尋
- 📊 **詳細資訊**：顯示電影標題、原文標題、上映日期和收入

## 檔案說明

- `tmdb_0583404.py` - 主程式（GUI 應用程式）
- `tmdb_prediction.ipynb` - Jupyter Notebook（電影推薦系統）
- `run_gui.sh` - 使用 Python 3.12 啟動腳本
- `run_gui_conda.sh` - 使用 Conda 環境啟動腳本

## 安裝需求

### Python 套件
```bash
pip install requests pillow
```

### 系統需求
- Python 3.9+ 或 Python 3.12（推薦）
- tkinter（通常隨 Python 安裝）
- Pillow（PIL）用於圖片處理

## 使用方法

### 方法 1：使用啟動腳本（推薦）
```bash
./run_gui.sh
```

### 方法 2：使用 Conda 環境
```bash
./run_gui_conda.sh
```

### 方法 3：直接執行
```bash
python3 tmdb_0583404.py
```

## API 金鑰設定

在使用前，請在 `tmdb_0583404.py` 中設定你的 TMDB API 金鑰：

```python
api_key = '你的_API_金鑰'
```

取得 API 金鑰：https://www.themoviedb.org/settings/api

## 使用範例

1. 輸入電影名稱（繁體中文）：
   - 蜘蛛人
   - 復仇者聯盟
   - 星際大戰

2. 輸入電影名稱（英文）：
   - Spider-Man
   - The Avengers
   - Star Wars

3. 輸入 Movie ID：
   - 550 (Fight Club)
   - 11 (Star Wars)
   - 278 (The Shawshank Redemption)

## 功能說明

### Print 按鈕
在終端機顯示輸入的 Movie ID

### Revenue 按鈕
- 自動搜尋電影（如果輸入的是名稱）
- 顯示電影海報
- 顯示電影詳細資訊（標題、原文標題、上映日期、收入）

## 注意事項

- 需要網路連線才能使用 API 和下載海報
- 首次載入海報可能需要一些時間
- 如果找不到電影，請嘗試使用英文名稱或 Movie ID

## 授權

此專案僅供學習使用。

