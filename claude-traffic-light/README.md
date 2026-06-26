# Claude 红绿灯 🚦

一个物理交通灯，实时映射 Claude Code 的工作状态：

| 灯 | 含义 |
|---|---|
| 🟢 绿 | Claude 正在干活（处理中 / 调用工具） |
| 🟡 黄 | Claude 在等你（需要授权 / 输入） |
| 🔴 红 | 空闲 / 已结束 / 刚启动 |

---

## 硬件 & 接线

- Arduino Nano（CH340，328P，已焊排针）
- YwRobot LED 真交通灯模块（含一分四杜邦线）

本项目按以下接线编写（已固定在固件里）：

| 模块线 | Arduino Nano |
|---|---|
| 红 R | **D5** |
| 黄 Y | **D3** |
| 绿 G | **D7** |
| GND | **GND** |

> 想换引脚？改 `firmware/traffic_light.ino` 顶部的 `RED / YELLOW / GREEN` 即可，软件迁就硬件。

---

## 目录

```
claude-traffic-light/
├── firmware/traffic_light.ino   # 烧进 Arduino 的固件
├── host/light.py                # 电脑端发灯脚本（自动找串口）
├── claude-hooks.json            # 合并进 ~/.claude/settings.json 的钩子配置
└── README.md
```

---

## 安装步骤

### 0. 装好环境
- **Arduino IDE**：https://www.arduino.cc/en/software
- **Python 3**，然后装串口库：
  ```bash
  pip install pyserial
  ```

### 1. 烧录固件
1. USB 线把 Nano 插到电脑
2. Arduino IDE 打开 `firmware/traffic_light.ino`
3. **工具 → 开发板** 选 `Arduino Nano`
4. **工具 → 处理器** 选 `ATmega328P`（若上传失败，改试 `ATmega328P (Old Bootloader)`）
5. **工具 → 端口** 选出现的那个口（记下来，排错时有用）
   - Windows: `COM3` 之类
   - Mac: `/dev/cu.usbserial-xxxx`
   - Linux: `/dev/ttyUSB0`
6. 点 **上传（→）**

✅ **上传成功后，红→黄→绿会依次闪一下（开机自检）。**
看到了说明接线和固件都 OK。若闪的顺序不对，说明线色和引脚对不上，改固件里的数字即可。

### 2. 手动测试（重要：先确认能点亮，再接钩子）
```bash
python3 host/light.py G   # 绿灯亮
python3 host/light.py Y   # 黄灯
python3 host/light.py R   # 红灯
python3 host/light.py O   # 全灭
```
脚本会**自动识别 CH340 串口**。如果没反应，见下方排错。

### 3. 接入 Claude Code 钩子
打开 `claude-hooks.json`，把里面 `hooks` 的内容合并进你的 `~/.claude/settings.json`，并：
- 把 `PATH_TO` 换成 `light.py` 的**绝对路径**
- Windows 用户：`python3` 改成 `python`，路径用正斜杠（如 `C:/Users/you/claude-traffic-light/host/light.py`）

事件映射：
- 你发消息 / Claude 调工具 → 🟢
- Claude 弹通知（等授权） → 🟡
- Claude 回答结束 / 会话启动 → 🔴

改完 **重启 Claude Code**，随便让它干个活，灯就会跟着变。完成！🎉

---

## 排错

| 现象 | 解决 |
|---|---|
| 上传失败 | 处理器在 `ATmega328P` 和 `Old Bootloader` 间换着试；确认是数据线不是纯充电线 |
| 自检顺序不对 | 线色和引脚对不上，改固件里 `RED/YELLOW/GREEN` 的数字 |
| 脚本点不亮 | 端口被占用？关掉 Arduino IDE 的“串口监视器”；或在 `light.py` 顶部手动填 `PORT` |
| 找不到串口 | 装了 CH340 驱动吗？`pip install pyserial` 装了吗？ |
| 灯每次都重新自检 | `light.py` 里 `dtr=False` 是治这个的，确认没被改掉 |
| Linux 权限不足 | `sudo usermod -a -G dialout $USER`，重新登录 |

---

## 让本地 Claude 帮你自动调试

把这个仓库拉到**插着灯的那台电脑**上，在该目录开一个 Claude Code 会话，对它说：

> 读一下 claude-traffic-light/README.md，帮我烧录固件、测试灯、并把钩子配好。

本地的 Claude Code 能直接访问 USB 串口，可以帮你跑测试、自动排错。
