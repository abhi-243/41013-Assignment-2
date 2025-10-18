#include <Arduino.h>
#include <Bounce>

const int buttonPin = 2;  
Bounce button(buttonPin, 10);

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);
  while (!Serial) {} // wait for Serial
}

void loop() {
  button.update();

  if (button.fallingEdge()) {
    Serial.println("PRESSED");
  }
  if (button.risingEdge()) {
    Serial.println("RELEASED");
  }
}