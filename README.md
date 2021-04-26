# 音频文件处理工具
# Audio Editor
---

## 版本
### 0.1.0
使用[Open Unmix](https://github.com/sigsep/open-unmix-pytorch)模型实现了人声提取 \
## Version
### 0.1.0
Implements [Open Unmix](https://github.com/sigsep/open-unmix-pytorch) to extract vocal from songs

---
## 依赖
1. [FFmpeg](https://www.ffmpeg.org/download.html).
## Dependencies
1. [FFmpeg](https://www.ffmpeg.org/download.html).
---
## 功能
1. 人声提取
## functions
1. vocal extraction
---
## 敬请期待
2. T-Net （卷积神经网络类） 实现的人声提取， 或弥补Open-Unmix在较短时间的音频文件中提取人声的不足（这个问题也有可能是因为训练该模型的数据库都是3分钟左右的音乐文件）。
1. 风格迁移 （对抗生成网络类）
## TODO
2. Implements T-Net （CNN）to extract vocal. Open-Unmix works poorly on short audio files, and CNN might be solve that problem (This issue is probably due to the lengths of songs in musdb18 are all about 3 minutes).
1. Style Transfer (GAN)
