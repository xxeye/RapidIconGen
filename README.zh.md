# RapidIconGen

[English Version](README.md)

**RapidIconGen** 是一個能夠一鍵生成多尺寸、多語言圖標的工具，專為大批量重複製造場景設計。該工具允許配置完成後，自動化生成圖標，並產生預覽圖，方便檢視最終效果。

## 功能

- 支援批量生成多尺寸、多語言的圖標。
- 可根據 CSV 內容選擇性套用遮罩。
- 生成圖標後自動生成預覽圖。
- 透過 `\modules\config_loader.py` 進行設置語言、尺寸、文字框架管理。

## 先決條件

- Python 3.x
- 需要的 Python 庫：
  - `PIL` (Pillow)
  - `os`
  - `csv`

## 使用方法

1. **克隆專案**

   ```bash
   git clone https://github.com/xxeye/RapidIconGen.git
   ```

2. **安裝 Pillow**

   由於本專案使用了 `Pillow` 進行圖像處理，請使用以下指令安裝該python庫：

   ```bash
   pip install Pillow
   ```

3. **準備數據**

   請將所有圖片資源、`text_data.csv`、專案編號，以及遮罩配置檔 `prefix_mask_data.csv` 放置在相應的資產目錄中，確保文件結構與專案要求一致。

4. **運行腳本**

   腳本會提示您選擇包含資產和 CSV 檔案的資料夾。處理完後，它將生成 ICON 和預覽圖。
   
   ```bash
   python main.py
   ```

## 專案資源

本專案附帶了兩個資源資料夾 "RhythmMirage" 和 "RhythmMirage_B" 供用戶測試，並參考其完整的資料夾結構和檔案配置。


==**注意事項**== 
本專案內附帶的測試資料夾包含字形檔案，這些字形檔案僅供測試使用，並非由本專案製作或擁有。請勿將這些字形檔案用於商業用途或其他非測試用途。如需正式使用，請參考字形的原始授權條款。

## 生成結果

- 將會生成兩個資料夾，分別為`nas_data_list"_"ENU_text`、`資料集名稱_layers`。
- 各尺寸ICON 將會儲存在所選資料夾內的 `"nas_data_list"_"ENU_text"/ICON/PNG` 目錄下。
- 繪製過程的圖層將保留在`資料集名稱_layers`。
- 預覽圖（`資料集名稱_Preview.png`）也會保存，用來快速查看生成的圖標效果。

## 預覽圖

以下是生成的圖標預覽圖：

![預覽圖](RhythmMirage_Preview.png)

## 授權

此專案使用 MIT 授權。詳情請參見 [LICENSE](LICENSE) 文件。