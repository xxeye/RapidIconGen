# 安裝 Python 與建置工作環境

1. **安裝 Python**(若已經有安裝可跳過到步驟3，安裝依賴套件Pillow)
   - 前往 https://www.python.org/downloads/，點擊「Download Python」下載安裝程式。
   - 安裝時需選中「Add Python to PATH」，然後完成安裝。

2. **打開命令提示字元**
   - 按 `Win + R`，輸入 `cmd`，按下「確定」。

3. **安裝套件**
   - 命令提示字元輸入 `python --version`，確認有無版本號，有則代表 Python 已成功安裝。沒有請解除安裝重裝，安裝時需確定有選中「Add Python to PATH」。
   - cmd輸入以下指令，安裝依賴套件：

     pip install Pillow

4. **將壓縮工具pngquant加入環境變數**
   - 執行資料夾內的`pngquant壓縮工具加入環境變數.bat`腳本，將自動把資料夾內pngquant壓縮工具加入環境變數。
   - 或者自行編輯將pngquant位置加入window系統環境變數。


5. **運行專案**

   - 運行資料夾內的`main.bat`
   - 或者，使用命令提示字元導航到該目錄運行主程序：

     python main.py


# 工具使用說明

1. **製作資源文件**
   - 可參考資料夾內附文件`SlotBigKingKong`與`TurboMultiplayerMines`資料結構。
   - 視專案各語言標題、nas歸檔編號、symbol是否要使用mask(y=使用mask，n=不使用mask)...等等。依照範例文件填寫`text_data.csv`與`prefix_mask_data.csv`內容。
   - 替換`symbol`資料夾內圖標，只需要400x581、500x300、500x500，三個尺寸，其他尺寸目前預設使用這三個尺寸自動編排縮放。
   - 將資源文件夾放在腳本所在資料夾內。

2. **運行**
   - 運行`main.bat`，輸入數字選擇要使用哪一個資料集，可單選與多選，若多選使用`,`分隔，enter運行，等待創建完畢。
   - 會產生全局預覽圖片與三個文件夾，分別為:
   
     1.`nas編號_專案英文名稱`
     2.`0gameicon`
     3.`資料集名稱_layers`
   
     1、2用於nas歸檔，圖片已自動壓縮。

3. **layers文件夾導入ps**
   - 開啟ps->指令碼->瀏覽，選擇文件夾內->photoshop_導入腳本內的`導入_複製圖片版本`或`導入_置入圖片版本`jsx格式腳本，選擇`資料集名稱_layers`運行，會依照所選資料夾結構導入圖層並關閉特定名稱的圖層組。

     備註.`導入_置入圖片`腳本尚在測試中，目前導入因智慧型圖片運算問題可能會有像素些微偏移的情形。

4. **進階設置**

   - 繪製所需圖片指定、字型指定、要產生哪幾種語言、壓縮選項、文字漸層顏色、文字陰影顏色，各語言文字基線微調。皆撰寫在:modules->config_loader.py，可依需求自行修改。