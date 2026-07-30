# 相机内参与畸变标定

## 标定板

照片上印刷的参数为：

- 类型：AprilGrid，`tag36h11`
- 排列：6 行 × 6 列，共 36 个标签
- ID：0–35
- 标签黑色方块边长：5.5 cm（0.055 m）
- 标签间净间距：1.65 cm（0.0165 m）
- 相邻标签起点节距：7.15 cm（0.0715 m）
- Kalibr 的无量纲 `tagSpacing`：0.3

这里的 `spacing=1.65cm` 是绝对间隙，不是 Kalibr YAML 中的比例值。

## 运行

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe calibrate_aprilgrid.py `
  DAS-Finger_20260731181932_sub_right_97aac4_37cdaa4b.mcap `
  --output-dir calibration_output
```

脚本也接受 OpenCV 能读取的 MP4/AVI/MOV 等普通视频。默认每 5 帧取一帧、最多使用
100 个有效视角；可用 `--stride`、`--max-views` 和 `--min-tags` 调整。

## 输出

- `calibration_results.yaml/json`：完整结果、误差和标定板参数
- `opencv_rational.yaml`：OpenCV rational pinhole，系数顺序
  `[k1,k2,p1,p2,k3,k4,k5,k6]`
- `opencv_fisheye.yaml`：OpenCV fisheye，系数顺序 `[k1,k2,k3,k4]`
- `opencv_fisheye_from_recorded_ds.yaml`：把 MCAP 内记录的 Double-Sphere 模型在
  全画幅对角视场内拟合为 OpenCV fisheye；本录像推荐在 Isaac Sim/Lab 中使用这一组
- `isaaclab_camera_config.py`：Isaac Lab `CameraCfg` 与 Isaac Sim 原生 OpenCV 畸变参数
- `debug_detections/`：检测点叠加图
- `undistorted_preview.jpg`：首个有效视角的去畸变预览

对于广角镜头，不要在两个模型之间混用 `K` 或 `D`。Isaac Lab 的 `CameraCfg` 负责
相机 prim 和理想内参；真实镜头畸变需要 RTX/Isaac Sim 的原生 OpenCV lens schema。
脚本保留视频独立求得的 pinhole/fisheye 两组结果。若 MCAP 同时包含 Double-Sphere
`camera_info`，还会生成覆盖整个画幅的 OpenCV fisheye 近似，并优先写入 Isaac 配置；
这样不会把只覆盖标定板出现区域的多项式盲目外推到约 200° 的完整视场。
