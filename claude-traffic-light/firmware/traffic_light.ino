// ============================================================
//  Claude 红绿灯 · Arduino 固件
//  作用：监听 USB 串口，收到字符就点亮对应的灯（每次只亮一个）
//  字符约定： R=红  Y=黄  G=绿  O=全灭
//
//  接线（按你的实际接线设置，改了线就改这里的数字）：
//    红 R  -> D5
//    黄 Y  -> D3
//    绿 G  -> D7
//    GND   -> GND
// ============================================================

const int RED    = 5;   // 红灯 -> D5
const int YELLOW  = 3;   // 黄灯 -> D3
const int GREEN  = 7;   // 绿灯 -> D7

// 只点亮一个灯，其余熄灭
void show(char c) {
  digitalWrite(RED,    LOW);
  digitalWrite(YELLOW, LOW);
  digitalWrite(GREEN,  LOW);
  switch (c) {
    case 'R': digitalWrite(RED,    HIGH); break;
    case 'Y': digitalWrite(YELLOW, HIGH); break;
    case 'G': digitalWrite(GREEN,  HIGH); break;
    case 'O': /* 全灭，什么都不做 */        break;
  }
}

void setup() {
  pinMode(RED,    OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(GREEN,  OUTPUT);
  Serial.begin(9600);

  // 开机自检：红 -> 黄 -> 绿 各亮 300ms。
  // 如果亮的顺序不是“红黄绿”，说明线色和上面的引脚对不上，
  // 把对应的数字（RED/YELLOW/GREEN）调一下即可，不用重新插线。
  digitalWrite(RED,    HIGH); delay(300); digitalWrite(RED,    LOW);
  digitalWrite(YELLOW, HIGH); delay(300); digitalWrite(YELLOW, LOW);
  digitalWrite(GREEN,  HIGH); delay(300); digitalWrite(GREEN,  LOW);
}

void loop() {
  if (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n' || c == '\r' || c == ' ') return;  // 忽略换行/空格
    show(c);
  }
}
