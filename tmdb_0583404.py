import requests
import json
import tkinter as tk
from urllib.parse import quote
from PIL import Image, ImageTk
from io import BytesIO

api_key = '2328be5c7a405973d7c20449dbed9888'

root = tk.Tk()
root.title ('The Movie DataBase')
root.geometry ('700x700')
root.configure(bg='white')

# 創建海報顯示區域
poster_label = tk.Label(root, bg='white')
poster_label.pack(pady=10)

label_movie = tk.Label(root, text='電影名稱或 Movie ID (例如: 蜘蛛人, 550, Star Wars)', 
                       font=('Helvetica', 12, 'bold'), fg='black')
label_movie.pack(pady=(15,5))
entry_movie = tk.Entry(root, width = 25)
entry_movie.pack()

show_variable = tk.StringVar()
show_variable.set('請輸入電影名稱（繁體中文或英文）或 Movie ID\n\n範例：\n蜘蛛人\nStar Wars\n550 (Movie ID)')
show_area = tk.Label(root, 
     textvariable = show_variable,
     font = ('Helvetica', 11),
     bg = 'lightyellow',
     fg = 'black',
     wraplength = 380,
     justify = 'left')
show_area.pack(pady=10, padx=10)

def print_movie():
    movie_id = entry_movie.get()
    print ('Moive ID = ', movie_id)
    print ('-'*30)

button_print = tk.Button(root, text = 'Print', command = print_movie,
                         bg='lightblue', fg='black', font=('Helvetica', 10, 'bold'))
button_print.pack(pady=15)

def search_movie_by_name(query):
    """使用電影名稱搜索"""
    # URL 編碼查詢字串以支持中文
    encoded_query = quote(query)
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={encoded_query}&language=zh-TW'
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('results') and len(data['results']) > 0:
            # 返回第一個結果的 ID
            return data['results'][0]['id'], data['results']
        else:
            return None, []
    except:
        return None, []

def load_poster(poster_path):
    """載入並顯示電影海報"""
    if not poster_path:
        poster_label.config(image='', text='無海報')
        return
    
    try:
        # TMDB 海報 URL
        poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
        
        # 下載圖片
        response = requests.get(poster_url, timeout=10)
        response.raise_for_status()
        
        # 使用 PIL 處理圖片
        image = Image.open(BytesIO(response.content))
        
        # 調整圖片大小（最大寬度 300px，保持比例）
        max_width = 300
        if image.width > max_width:
            ratio = max_width / image.width
            new_height = int(image.height * ratio)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # 轉換為 tkinter 可用的格式
        photo = ImageTk.PhotoImage(image)
        
        # 顯示海報
        poster_label.config(image=photo, text='')
        poster_label.image = photo  # 保持引用，避免被垃圾回收
        
    except Exception as e:
        print(f'載入海報失敗: {str(e)}')
        poster_label.config(image='', text='無法載入海報')

def print_revenue():
    user_input = entry_movie.get().strip()
    
    if not user_input:
        error_msg = "錯誤：請輸入電影名稱或 Movie ID"
        print(error_msg)
        show_variable.set(error_msg)
        poster_label.config(image='', text='')
        return
    
    movie_id = None
    
    # 檢查輸入是否為數字（Movie ID）
    if user_input.isdigit():
        movie_id = int(user_input)
        print(f'使用 Movie ID: {movie_id}')
    else:
        # 使用電影名稱搜索
        print(f'搜索電影: {user_input}')
        show_variable.set(f'正在搜索：{user_input}...')
        root.update()  # 更新視窗顯示
        
        movie_id, search_results = search_movie_by_name(user_input)
        
        if movie_id is None:
            error_msg = f"找不到電影：{user_input}\n\n請嘗試：\n- 使用英文名稱\n- 使用 Movie ID\n- 檢查拼寫"
            print(error_msg)
            show_variable.set(error_msg)
            poster_label.config(image='', text='')
            return
        else:
            # 顯示找到的電影
            found_movie = search_results[0]
            print(f'找到電影: {found_movie.get("title", "未知")} (ID: {movie_id})')
            if len(search_results) > 1:
                print(f'共找到 {len(search_results)} 個結果，使用第一個結果')
    
    # 使用 Movie ID 獲取詳細資訊
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=zh-TW'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # 檢查是否有錯誤訊息
        if 'status_code' in data:
            error_msg = f"錯誤：{data.get('status_message', '找不到該電影')}"
            print(error_msg)
            show_variable.set(error_msg)
            poster_label.config(image='', text='')
            return
        
        revenue_value = data.get('revenue')
        title = data.get('title', '未知電影')
        original_title = data.get('original_title', '')
        release_date = data.get('release_date', '')
        poster_path = data.get('poster_path', '')
        
        # 載入海報
        load_poster(poster_path)
        
        # 構建結果訊息
        result_parts = [f"電影：{title}"]
        if original_title and original_title != title:
            result_parts.append(f"原文：{original_title}")
        if release_date:
            result_parts.append(f"上映日期：{release_date}")
        
        if revenue_value is None or revenue_value == 0:
            result_parts.append("收入：無資料")
        else:
            result_parts.append(f"收入：${revenue_value:,}")
        
        result = "\n".join(result_parts)
        
        print(f'Title = {title}')
        print(f'Revenue = {revenue_value}')
        print('-' * 30)
        show_variable.set(result)
        
    except requests.exceptions.RequestException as e:
        error_msg = f"網路錯誤：無法連接到 API\n{str(e)}"
        print(error_msg)
        show_variable.set(error_msg)
        poster_label.config(image='', text='')
    except Exception as e:
        error_msg = f"發生錯誤：{str(e)}"
        print(error_msg)
        show_variable.set(error_msg)
        poster_label.config(image='', text='')

button_revenue = tk.Button(root, text='Revenue', command=print_revenue,
                          bg='lightgreen', fg='black', font=('Helvetica', 10, 'bold'))
button_revenue.pack(pady=15)

root.mainloop()

