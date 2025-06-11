const int trigPin = 9;
const int echoPin = 10;
const int thresholdDistance = 100; // cm

unsigned long lastDetectionTime = 0;
bool personDetected = false;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

long measureDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 20000); // 最多等 20ms
  if (duration == 0) return -1; // 超时没测到
  return duration * 0.034 / 2;
}

void loop() {
  long distance = measureDistance();
  unsigned long now = millis();

  // 打印距离
  if (distance > 0) {
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");
  } else {
    Serial.println("Distance: Out of range");
  }

  // 判断是否有人靠近
  if (distance > 0 && distance < thresholdDistance) {
    if (!personDetected || now - lastDetectionTime > 5000) {
      Serial.println("DETECTED");
      lastDetectionTime = now;
      personDetected = true;
    }
    delay(5000); // 有人 → 延迟检测
  } else {
    personDetected = false;
    delay(300); // 没人 → 加快检测频率
  }
}
