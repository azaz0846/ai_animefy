# Poster
<img width="100%" alt="Poster" src="https://imgur.com/p8Zl5mG.jpg"/>

## 摘要  
  
　　最近在社群網路上出現了一些能把人臉變成動畫風格的濾鏡，如ToonMe、Voila、PhotoLab等，其中運用到的神經網路—StyleGAN就是運用了生成對抗網路(GAN)技術從訓練資料中學習輸入圖片的特徵，找到Latent space中不同風格對應的分布，就能產生同一張照片的不同風格，用來把人臉變成各種不同風格，但這些濾鏡都只能改變人臉部分，因此我們想到可以連背景一起轉變風格，並提供不同的動畫風格供選擇，讓整張圖經過我們的程式轉換後就猶如動畫中的圖片。  
　　ai_animefy能輸入人像照片或影片，並可以選擇不同動畫風格及處理方式，程式會自動偵測圖片中的人物，把人臉和身體從畫面中分割成不同圖片和遮罩，並分別以不同神經網路處裡人臉，身體及背景，再以影像處理自動合成一張使用者所選擇的動畫風格的圖片。
<div align="center">
    <img width="50%" alt="風格轉換輸出範例" src="https://github.com/azaz0846/ai_animefy/blob/main/.figures/demo.gif"/><br>
    風格轉換輸出範例
</div>

## 整體架構  

<div align="center">
    <img width="100%" alt="整體架構系統圖" src="https://imgur.com/S3kIYGN.jpg"/><br>
    圖1. 整體架構系統圖
</div>
  
　　本專題的系統架構如下(圖1)：在原始影片的部分，我們透過ffmpeg將照片從影片中提取出來，預設為30FPS，並且依照先後順序將影片編號，以方便之後的流程。接著分別使用Mask R-CNN以及face-seg將照片中人像以及臉部的部分輸出成mask檔案，接著使用mask將人像與人臉分別切割出來並透過U-GAT-IT進行動漫化，而背景則是使用AnimeGANv2進行不同風格的動漫化。  
　　在三個部位都成功轉換後，都採用Real-RSRGAN增加照片的解析度以及銳利度並縮放至相對於原始照片的正確大小，最後則是將三個部位依照最初切割時留下的座標，透過OpenCV函式庫中的柏松融合將三個部位結合成一張完整的動漫化照片，最後再使用Real-RSRGAN進行一次解析度的提升，就完成了動漫化照片的流程，最後則再次使用ffmpeg將連續的照片合併成可播放的影片。

## 研究方法

　　起初規劃為先透過物件辨識，將照片切割成三個部分，背景、身體以及臉部，接著將各個部分使用不同的GAN與模型將其風格轉換，轉換後再依據切割時所留下的各部位座標資訊，將轉換後的圖片再次融合，組成一張新的照片。  
　　身體的部分我們採用Mask R-CNN，可以一起完成辨識以及切割出人體區塊的工作，實作時的模型我們採用以MS COCO資料集預先訓練好的模型，MS COCO資料集中收錄了許多日常生活可見的物體，其中也包括了"人"這個種類，其精確度也很高，這讓我們不用再自己訓練一次模型。
由於Mask R-CNN只能辨識出人體的外框，無法切割出人臉的部分，所以我們另外找了其他兩個函式庫，分別處理辨識以及切割人臉的任務，首先我們使用以dlib為基礎的函式庫，將人臉從整張照片中定位出來，並且輸出人臉的座標中心點，我們就可以以中心點大概框出人臉的位置，接著使用另外一個函式庫face-seg，將確切的人臉mask切割出來。  
　　經過以上的步驟，我們可以將原圖切割出四張圖檔，分別是透過Mask R-CNN，以身體的bounding box切割出來的人體圖片、人體的mask遮罩圖片、dlib辨識出的人臉bounding box圖片，最後是人臉的mask遮罩圖片。並且也同時將切割圖片相對於整個原始圖片的座標位置儲存下來，另外我們也儲存了臉部在原圖中的座標、身體切割圖片的大小、臉部切割圖片的大小以供之後合併時使用。流程如圖2所示。  
<div align="center">
    <img width="100%" alt="裁切流程" src="https://imgur.com/gWpw1Da.jpg"/><br>
    圖2. 裁切流程
</div>  
  
　　取得各部位的圖片後，就進入到轉換動畫風格的步驟，在實作前我們預先尋找適合上述三個部分的GAN。並分別套用至不同部分，以達到最好的轉換效果。  
　　在背景的部分，我們找到名為animeGANv2的模型，其架構較適合將大片風景轉換成日式動畫風。使用此模型進行訓練時選用日本動畫以及具有日本動畫風格的遊戲畫面來當作訓練資料，分別有動畫蠟筆小新、遊戲原神以及遊戲邊緣禁地。我們採用與研究人員相同的訓練方法: 從遊戲遊玩影片或是動畫中抽取畫面，並將畫面切割成許多256x256圖片後進行訓練，圖3展示了從遊戲原神遊玩畫面中擷取出來的圖片。圖4則展示由原神資料集訓練出來的模型轉換效果。  
<div align="center">
    <img width="50%" alt="遊戲中截圖畫面" src="https://imgur.com/7J7GdEx.jpg"/><br>
    圖3. 遊戲中截圖畫面(原神)
</div>
<table align="center">
  <tr align="center">
    <td>
      <img width="100%" alt="test image" src="https://imgur.com/xaJkZbR.jpg"/>
    </td>
    <td>
      <img width="100%" alt="label image" src="https://imgur.com/PikqbUG.jpg"/>
    </td>
  </tr>
  <tr align="center">
    <td>圖4.1 原圖</td>
    <td>圖4.2 風格轉換圖(原神)</td>
  </tr>
</table>
　　而在臉部的部分，由於現實與動畫中的轉換頗大，例如眼睛的部分，動畫皆採取較誇大的畫法，所以我們採用的是U-GAT-IT以及其研究人員預先訓練的模型。經我們實驗過後，確實可將轉變較為巨大的眼睛和頭髮成功轉換至動畫風格。在身體的部分，我們也是同樣採取U-GAT-IT進行轉換，這樣可以避免人物身體以及臉部動畫效果差距過大。如圖5所示。  
<table align="center">
  <tr align="center">
    <td>
      <img width="50%" alt="test image" src="https://imgur.com/R99m08E.jpg"/>
    </td>
    <td>
      <img width="50%" alt="label image" src="https://imgur.com/tTMeNCe.jpg"/>
    </td>
  </tr>
  <tr align="center">
    <td>圖5.1 原圖</td>
    <td>圖5.2 風格轉換圖</td>
  </tr>
</table>
　　在確認個別實作方法後，接著是將各個部分轉換後的結果加以整合。首先是整合人臉以及身體的部分，使用人臉mask以及儲存起來的座標位置，將轉換後的人臉(圖5.2)整合至轉換後的身體上。此步驟如果單純使用mask圖片做切割後貼上，會使身體與人臉的邊界相交處非常明顯，這裡我們使用OpenCV函式庫中的柏松融合將人臉以及身體進行融合，讓交界處可以較平順的接合。接著將整合後的人物再使用柏松融合與背景進行融合。圖6展示了將三個部分整合後的轉換效果。可以觀察到各部位交界處皆無明顯邊界。動畫化流程如圖7所示。  
<table align="center">
  <tr align="center">
    <td>
      <img width="50%" alt="test image" src="https://imgur.com/28UXRmn.jpg"/>
    </td>
    <td>
      <img width="50%" alt="label image" src="https://imgur.com/UVrXKSa.jpg"/>
    </td>
  </tr>
  <tr align="center">
    <td>圖6.1 原圖</td>
    <td>圖6.2 風格轉換圖</td>
  </tr>
</table>
<div align="center">
    <img width="100%" alt="動畫化" src="https://imgur.com/pjN4rRs.jpg"/><br>
    圖7. 動畫化流程
</div> 

## 風格比較
　　我們提供三種不同背景風格，分別有動畫"蠟筆小新"、遊戲"邊緣禁地"、及遊戲"原神"。蠟筆小新風格較平滑(圖8.2)，邊緣禁地風格的明暗對比明顯(圖8.3)，原神風格則是更鮮豔(圖8.4)，以上三種都有符合原作的背景美術特色。
<table align="center">
  <tr align="center">
    <td>
      <img width="100%" alt="原圖" src="https://imgur.com/PjvvMDC.jpg"/>
    </td>
    <td>
      <img width="100%" alt="蠟筆小新" src="https://imgur.com/tf7fdQb.jpg"/>
    </td>
  </tr>
  <tr align="center">
    <td>圖8.1 原圖</td>
    <td>圖8.2 蠟筆小新風格轉換圖</td>
  </tr>
  <tr align="center">
    <td>
      <img width="100%" alt="邊緣禁地" src="https://imgur.com/VupfzVY.jpg"/>
    </td>
    <td>
      <img width="100%" alt="原神" src="https://imgur.com/eOUXfNS.jpg"/>
    </td>
  </tr>
  <tr align="center">
    <td>圖8.3 邊緣禁地風格轉換圖</td>
    <td>圖8.4 原神風格轉換圖</td>
  </tr>
</table>

# Checkpoint & Dataset

ai_animefy/  
│── checkpoint/  
│　　│── [generator_borderland_weight](https://drive.google.com/file/d/1aq4y--VDNqEVKCbuSxfxpXxF5KrAYN_I/view?usp=sharing) (Please unzip)  
│　　│── [generator_genshin_weight](https://drive.google.com/file/d/1uXXy2A1QkNAUPpoMX0d8blfUG8ojw5gb/view?usp=sharing) (Please unzip)  
│　　│── [generator_shinchan_weight](https://drive.google.com/file/d/1jbYqt-J-bzlGbmR-N2fuoCmH1nYhcJ9j/view?usp=sharing) (Please unzip)  
│── dataset/  
│　　│── [data](https://drive.google.com/file/d/12YzB_rmaIlPTuaFAHN3Tta_E-rSHO4Ot/view?usp=sharing) (Please unzip)  
│── face-seg/  
│　　│── checkpoints/  
│　　│　　├── [model.pt](https://drive.google.com/file/d/1STG6TP7-aumzlLUBtYhFNpshHHwgtPv3/view?usp=sharing)  
│　　│── weights/  
│　　│　　│── [mobilenet_v2.pth.tar](https://drive.google.com/file/d/1OxKALyevphqvkWTLMpCOOziYKkZLipy3/view?usp=sharing)  
│── Mask_RCNN/  
│　　│── [mask_rcnn_coco.h5](https://drive.google.com/file/d/1VOkEjSRigWUiRyLDvUXJgllLe7JetQIM/view?usp=sharing)  
│── Real-ESRGAN/  
│　　│── experiments/  
│　　│　　│── pretrained_models/  
│　　│　　│　　│── [RealESRGAN_x4plus.pth](https://drive.google.com/file/d/1syut64M8ZshOz3gJim3Yot4p07Dkerks/view?usp=sharing)  
│　　│　　│　　│── [RealESRGAN_x4plus_anime_6B.pth](https://drive.google.com/file/d/13GTtyGLSztQyUs83MAxCiJxqCPr0M-TU/view?usp=sharing)  
│── UGATIT/  
│　　│── checkpoint/  
│　　│　　│── [UGATIT_temp_photos](https://drive.google.com/file/d/1Jh36ZOKdGHO5pZ34Q20tqOEY15nwcTQZ/view?usp=sharing) (Please unzip)  
│　　│── dataset/  
│　　│　　│── [data](https://drive.google.com/file/d/1QAkXasDLnB_vCaqsQ1zvyzbQ1gob60XC/view?usp=sharing) (Please unzip)  
  
# Acknowledge
感謝[Mask R-CNN](https://github.com/matterport/Mask_RCNN)、[Dlib](https://en.wikipedia.org/wiki/Dlib)、[AnimeGANv2](https://github.com/TachibanaYoshino/AnimeGANv2)、[U-GAT-IT](https://github.com/taki0112/UGATIT)、[Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)提供良好的工具與模型輔助此Project建構出更棒的應用。
