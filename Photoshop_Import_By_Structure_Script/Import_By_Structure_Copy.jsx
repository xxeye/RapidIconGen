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
        if (file instanceof Folder) {
            // 檢查資料夾名稱，若為 "0gameicon" 則跳過
            if (file.name.toLowerCase() === "0gameicon") {
                continue;  // 略過該資料夾
            }
            
            var newGroup = parentGroup.layerSets.add();
            newGroup.name = file.name;
            importFolderContents(file, newGroup);
        } else if (file instanceof File && file.name.match(/\.(jpg|jpeg|png|gif|tiff|bmp)$/i)) {
            importImage(file, parentGroup);
        }
    }
}

function importImage(imageFile, parentGroup) {
    // 打開圖像文件
    var imageDoc = app.open(imageFile);

    // 將圖像文件的圖層複製到新文檔的群組中
    app.activeDocument = imageDoc;
    var imageLayer = imageDoc.activeLayer.duplicate(parentGroup, ElementPlacement.PLACEATBEGINNING);

    // 設置圖層名稱
    app.activeDocument = doc;
    parentGroup.artLayers.getByName(imageLayer.name).name = imageFile.name;

    // 關閉圖像文件，不保存更改
    imageDoc.close(SaveOptions.DONOTSAVECHANGES);
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
