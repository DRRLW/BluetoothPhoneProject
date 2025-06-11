const int trigPin = 9;
const int echoPin = 10;

long duration;
float distance;

const float detectionThreshold = 30.0; // cm

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

float measureDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.0343 / 2;
  return distance;
}

void loop() {
  float dist = measureDistance();

  if (dist > 0 && dist < detectionThreshold) {
    Serial.println("DETECTED");
    delay(300);  // 减少串口刷屏频率
  }
}
