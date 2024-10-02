#target photoshop

// 選擇資料夾
var inputFolder = Folder.selectDialog("選擇要導入的資料夾");

// 如果沒有選擇資料夾，終止腳本
if (inputFolder == null) {
    alert("沒有選擇資料夾。");
    exit();
}

// 使用當前打開的文檔
var doc = app.activeDocument;

// 遞歸導入圖片並保持資料夾結構
function importFolderContents(folder, parentGroup) {
    var files = folder.getFiles();
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        
        // 檢查是否為資料夾
        if (file instanceof Folder) {
            // 檢查資料夾名稱，若為 "0gameicon" 則跳過
            if (file.name.toLowerCase() === "0gameicon") {
                continue;  // 略過該資料夾
            }
            
            // 為每個資料夾創建一個新的圖層組
            var newGroup = parentGroup.layerSets.add();
            newGroup.name = file.name;  // 使用資料夾名稱命名群組
            importFolderContents(file, newGroup);  // 遞歸處理子資料夾
        } else if (file instanceof File && file.name.match(/\.(jpg|jpeg|png|gif|tiff|bmp)$/i)) {
            placeImage(file, parentGroup);  // 將圖像置入到當前的圖層組中
        }
    }
}

// 將圖像直接放入到指定的圖層組中
function placeImage(imageFile, parentGroup) {
    var idPlc = charIDToTypeID("Plc ");  // Place 命令
    var desc = new ActionDescriptor();
    desc.putPath(charIDToTypeID("null"), new File(imageFile));  // 圖片文件路徑
    desc.putEnumerated(charIDToTypeID("FTcs"), charIDToTypeID("QCSt"), charIDToTypeID("Qcsa"));  // 使用當前畫布
    executeAction(idPlc, desc, DialogModes.NO);
    
    // 將放入的圖像放入指定的父圖層組
    var placedLayer = doc.activeLayer;
    placedLayer.move(parentGroup, ElementPlacement.PLACEATBEGINNING);
}

// 隱藏指定名稱的圖層組
var groupsToHide = ["VND", "THB", "PTE", "ESP", "ENU", "CHT"];

function customIndexOf(arr, searchElement) {
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] === searchElement) {
            return i;
        }
    }
    return -1;
}

function setGroupVisibilityInvisible(layerSets) {
    for (var i = 0; i < layerSets.length; i++) {
        var group = layerSets[i];
        if (customIndexOf(groupsToHide, group.name) !== -1) {
            group.visible = false;
        }
        if (group.layerSets.length > 0) {
            setGroupVisibilityInvisible(group.layerSets);
        }
    }
}

// 初始化遞歸導入
importFolderContents(inputFolder, doc);

// 隱藏指定名稱的圖層組
setGroupVisibilityInvisible(doc.layerSets);

alert("導入完成");
