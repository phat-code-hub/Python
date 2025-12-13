# languages.py

#Check License
LICENSE ={
    "English": {"Title": "Valid License Check",
                "Prompt": "Enter your license key:",
                "Display": "Show/Hide",
                "Button": "Check"
                },
    "Japanese": {"Title": "ライセンスキー確認",
                "Prompt": "ライセンスキーを入力下さい:",
                "Display": "表示/非表示",
                "Button": "確認"
                },
    "Vietnamese": {"Title": "Kiểm tra bản quyền",
                "Prompt": "Vui lòng nhập số bản quyền:",
                "Display": "Hiện/Ẩn",
                "Button": "Kiểm tra"
                }
}
ERROR ={
    "English": {"Title": "Error",
                "Message": "Invalid license key!",
                "Open":"Failed to open folder!",
                },
    "Japanese": {"Title": "エラー",
                "Message": "不正なライセンスキー!",
                "Open":"フォルダを開けません!",
                },
    "Vietnamese": {"Title": "Lỗi",
                "Message": "Bản quyền không hợp lệ!",
                "Open":"Không thể truy cập thư mục!",
                },
}
REG_KEY = "FileSearch"
APP_ID  =""
MAPPING = {
            "en_US": "English",
            "en-EN": "English",
            "ja_JP": "Japanese",
            "vi_VN": "Vietnamese",
        }
#Title
TITLE = {
    "English":"Search File",
    "Japanese": "ファイル検索",
    "Vietnamese": "Tìm Tập Tin"
}
# Language Radio Button
LANGUAGES ={"English":{"ENG":"English","JP":"Japanese","VN"  :"Vietnamese"},
            "Japanese":{"ENG":"英語","JP":"日本語","VN"  :"ベトナム語"},
            "Vietnamese":{"ENG":"Tiếng Anh","JP":"Tiếng Nhật","VN"  :"Tiếng Việt"}}
LABELS = {
    "English": {
        "Title": "File Search",
        "SearchPath": "Search Path:",
        "SearchKeyword": "Search keyword:",
        "FileType": "File Type:",
        "Folders": "Folders:",
        "Files": "Files:",
        "SearchButton": "Search",
        "SelectFolder": "Select Folder",
        "Info": "File Information:",
        "message": "Searching, please wait...",
        "finish": "Search finished!",
        "Cancel": "Cancel"
    },
    "Japanese": {
        "Title": "ファイル検索",
        "SearchPath": "検索パス:",
        "SearchKeyword": "検索キーワード:",
        "FileType": "ファイルタイプ:",
        "Folders": "フォルダ:",
        "Files": "ファイル:",
        "SearchButton": "検索",
        "SelectFolder": "フォルダを選択",
        "Info": "ファイル情報:",
        "message": "検索中、お待ちください...",
        "finish": "検索完了!",
        "Cancel": "キャンセル"
    },
    "Vietnamese": {
        "Title": "Tìm kiếm tập tin",
        "SearchPath": "Đường dẫn:",
        "SearchKeyword": "Từ Khóa:",
        "FileType": "Kiểu tập tin:",
        "Folders": "Thư mục:",
        "Files": "Tập tin:",
        "SearchButton": "Tìm kiếm",
        "SelectFolder": "Chọn thư mục",
        "Info": "Chi tiết tập tin:",
        "message": "Đang tìm, vui lòng đợi...",
        "finish": "Hoàn Thành tìm kiếm!",
        "Cancel": "Hủy"
    }
}
TYPES ={
    0:{"English": 'All', 'Japanese': '全て',"Vietnamese": "Tất cả"},
    1:{"English": 'VectorWorks Files', 'Japanese': 'VectorWorks ファイル',  "Vietnamese": "Tập tin VectorWorks"},
    2:{"English": 'CAD Files', 'Japanese': 'CAD ファイル',  "Vietnamese": "Tập tin CAD"},
    3:{"English": 'Excel Files', 'Japanese': 'Excel ファイル',  "Vietnamese": "Tập tin Excel"},
    4:{"English": 'PDF Files', 'Japanese': 'PDF ファイル',  "Vietnamese": "Tập tin PDF"},
    5:{"English": 'DXF Files', 'Japanese': 'DXF ファイル',  "Vietnamese": "Tập tin DXF"},
    6:{"English": 'Image Files', 'Japanese': '画像 ファイル',"Vietnamese": "Tập tin hình ảnh"},
    7:{"English": 'Video Files', 'Japanese': '動画 ファイル',"Vietnamese": "Tập tin video"},
    8:{"English": 'Word Files', 'Japanese': 'Word ファイル',  "Vietnamese": "Tập tin Word"},
    9:{"English": 'Text Files', 'Japanese': 'テキスト ファイル',"Vietnamese": "Tập tin text"},
    10:{"English": 'Audio Files', 'Japanese': '音声 ファイル',"Vietnamese": "Tập tin âm thanh"},
    11:{"English": 'Program Files', 'Japanese': 'プログラム ファイル', "Vietnamese": "Tập tin chương trình"},
    12:{"English": 'Executable Files', 'Japanese': '実行可能 ファイル', "Vietnamese": "Tập tin thực thi"}
    }

OPTIONS ={"English":{"AND":"All matched","OR":"Contain","NOT"  :"Not contain"},
        "Japanese":{"AND":"全て一致","OR":"いずれか","NOT"  :"いずれか除外"},
        "Vietnamese":{"AND":"Tất cả","OR":"Bao hàm","NOT"  :"Không bao hàm"}}

PLACE_HOLDER={"English":"Input search keywords",
            "Japanese":"検索キーワードを入力",
            "Vietnamese":"Nhập từ khóa tìm kiếm"}

HINT ={
    "Dialog" :{"English":"Click to change search folder",
            "Japanese":"クリックして検索フォルダを変更",
            "Vietnamese":"Click để thay đổi đường dẫn tìm kiếm"},
    "Search":{"English":"Multiple keywords are separated by ',:;' or spaces, '*' for show all",
                "Japanese":"複数のキーワードは半角で英字、数字、記号とし',:;'または空白で区切って入力,'*'は全て表示",
                "Vietnamese":"Các từ khóa cách nhau bởi ',:;' hoặc khoảng trắng,'*' để hiển thị tất cả"},
    "Logic" : {"English":
                {
                0: "Any of the keywords matches",
                1: "All of the keywords matches, ignore order",
                2: "Not contain all keywords"
                },
            "Japanese":{
                0: "いずれかのキーワードに一致",
                1: "順番問わず、全てのキーワードに一致",
                2: "全てのキーワードに一致しない"
                },
            "Vietnamese":{
                0: "Có ít nhất một từ khóa ",
                1: "Tất cả đều tìm thấy , không cần thứ tự",
                2: "Không chứa tất cả các từ khóa này"
                }
            },
    
    "Type" : {"English":"Select file type",
            "Japanese":"ファイルタイプを選択",
            "Vietnamese":"Chọn Lodi tập tin"},

    "Folder" : {"English":"Double Click to change search folder",
                "Japanese":"ダブルクリックしてフォルダを選択、再検索",
                "Vietnamese":"Click đúp để chọn đường dẫn tìm kiếm, tìm kiếm lại"},

    "File" : {"English":"Double Click to go file location",
            "Japanese":"ダブルクリックしてファイルの場所を開く",
            "Vietnamese":"Click đúp để đi tới vị trí tập tin"}

}

EXTENSIONS ={
    0: [],
    1: [".vwx",".vwxp",".vwxw",".sta"],
    2: [".vwx",".sta",".mcd",".dwg", ".step", ".stp","dxf",
                ".CAT",".iges", ".igs", ".sldprt", ".sldasm", ".prt"],
    3: [".xls",".xlsx",".xlsm",".xlsb",".xltx",".xltm",".xlt",".csv",".numbers"],
    4: [".pdf"],
    5: ["dxf"],
    6: [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg","png"],
    7: [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    8: [ ".doc", ".docx", ".odt", ".rtf",".dot","docm","dotx"],
    9: [".txt", ".ini",".log" ,".csv" ,".md",".yml",".yaml",".json"],
    10: [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    11: [".py", ".java", ".js", ".c",".cpp",".php", ".rb", ".html", ".htm", ".css", ".cs",".frx","frm","bas","cls","vba"],
    12: [".exe", ".msi", ".bat", ".cmd",".pkg",".sh", ".app", ".jar",  ".pyw", ".pyc"],
    }
TEXT_EXT = [
        ".txt",
        ".ini",
        ".md",
        ".csv",
        ".yml",
        ".yaml",
        ".log",
        ".json"
    ]
VIEW_EXT = {
    "text":[3,4,6,8,9],
    "cad" :[1,2,5],
    "prog":[11],
    "media":[7,10],
    "other":[12]
}

CAD_EXT = ['.vwx', '.dwg', '.dxf']
LOGICS ={
    "OR":0,
    "AND":1,
    "NOT":2
}