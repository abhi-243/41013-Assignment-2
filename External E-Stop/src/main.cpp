#include <Arduino.h>

const int buttonPin = 2;
bool lastButtonState = HIGH;     // Because of INPUT_PULLUP
bool currentButtonState = HIGH;
unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 10;  // 10 ms debounce

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);
  while (!Serial) {} // wait for Serial
}

void loop() {
  int reading = digitalRead(buttonPin);

  // if the button state has changed
  if (reading != lastButtonState) {
    lastDebounceTime = millis();  // reset debounce timer
  }

  // if enough time has passed, consider it a valid state change
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != currentButtonState) {
      currentButtonState = reading;

      if (currentButtonState == LOW) {
        Serial.println("RELEASED");
      } else {
        Serial.println("PRESSED");
      }
    }
  }

  lastButtonState = reading;
}