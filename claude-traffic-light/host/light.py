#!/usr/bin/env python3
# ============================================================
#  Claude 红绿灯 · 发灯脚本
#  用法:  python3 light.py G      (R=红 / Y=黄 / G=绿 / O=全灭)
#
#  特性:
#   - 自动探测 Arduino 串口(识别 CH340 芯片)，一般无需手动配置端口
#   - 打开串口时关闭 DTR，避免每次触发都让 Nano 复位重启
#   - 任何异常都静默退出，绝不会因为找不到灯而打断 Claude
# ============================================================
import sys, time

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    # 没装 pyserial 也别报错中断钩子，提示一次即可
    sys.stderr.write("[light] 需要先安装 pyserial:  pip install pyserial\n")
    sys.exit(0)

# 如需手动指定端口，把下面这行填上，例如:
#   Windows: "COM3"   Mac: "/dev/cu.usbserial-1420"   Linux: "/dev/ttyUSB0"
# 留空("")则自动探测。
PORT = ""
BAUD = 9600


def find_port():
    if PORT:
        return PORT
    candidates = list(list_ports.comports())
    # 优先匹配 CH340 (USB 厂商ID = 0x1A86)，或描述里带 CH340 / USB-SERIAL
    for p in candidates:
        desc = (p.description or "").upper()
        if p.vid == 0x1A86 or "CH340" in desc or "USB-SERIAL" in desc or "USB SERIAL" in desc:
            return p.device
    # 兜底：只有一个串口时直接用它
    if len(candidates) == 1:
        return candidates[0].device
    return None


def main():
    color = (sys.argv[1] if len(sys.argv) > 1 else "O").upper()[:1]
    if color not in ("R", "Y", "G", "O"):
        color = "O"

    port = find_port()
    if not port:
        # 没插灯 / 没找到设备：静默退出
        return

    try:
        ser = serial.Serial()
        ser.port = port
        ser.baudrate = BAUD
        ser.dtr = False          # 关键：防止开口时 Nano 自动复位
        ser.timeout = 1
        ser.open()
        ser.write(color.encode())
        ser.flush()
        time.sleep(0.05)
        ser.close()
    except Exception:
        # 串口被占用 / 拔了 / 权限问题等，一律静默
        pass


if __name__ == "__main__":
    main()
