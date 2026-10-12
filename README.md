# SquashFrame AI V0.1

壁球视频动作分析原型，Flutter 安卓优先、兼容 iOS，Python + MediaPipe 后端。

功能：视频导入、慢动作、逐帧步进、姿态检测、肘膝角度计算、CSV/JSON 导出。

当前版本为原型，不包含壁球击球识别、回 T 识别和球轨迹检测。

## 运行

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

手机端：`flutter create --platforms=android,ios . && flutter pub get && flutter run`。

请在 AndroidManifest 中增加 INTERNET 权限；开发时访问局域网 HTTP 需单独允许明文流量，正式发布应使用 HTTPS。

本项目独立开发，不包含动作帧原版私有代码或素材。
