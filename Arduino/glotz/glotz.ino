#include <Servo.h>

// Adjust these for your servos
const int hMin = 1600;
const int hMax = 700;

const int vMin = 1100;
const int vMax = 1600;

// Do not change anything after this if you don't know what you're doing
Servo horizontal;
Servo vertical;

// if override is set to -1, the control box takes over
int override_h = -1;
int override_v = -1;

void setup() {
    // horizontal swiveling servo is on pin 10
    horizontal.attach(10);

    // vertical servo on 9
    vertical.attach(9);

    // start the serial processing
    Serial.begin(9600);
}

void loop() {
    // Horizontal potientiometer is on A1
    int h = analogRead(A1);

    // Vertival potentiometer is on A0
    int v = analogRead(A0);

    // if the override is active replace measurement
    if (override_h >= 0){
        h = override_h;
    }
    if (override_v >= 0){
        v = override_v;
    }

    // map ADC converted value into safe range
    h = map(h, 0, 1023, hMin, hMax);
    v = map(v, 0, 1023, vMin, vMax);

    // set servos
    horizontal.writeMicroseconds(h);
    vertical.writeMicroseconds(v);

    // wait some time to allow the PWM to settle
    delay(5);
}


void serialEvent() {
    // While there are bytes in the serial queue process them
    while (Serial.available()) {

        // read two comma separated values
        int h = Serial.parseInt();
        int v = Serial.parseInt();

        // if the next char is a newline the format was correct
        if (Serial.read() == '\n') {
            // set overrides
            override_h = constrain(h, -1, 1023);
            override_v = constrain(v, -1, 1023);

            // echo back what has been set
            Serial.print("Setting values: h = ");
            Serial.print(override_h);
            Serial.print(", v = ");
            Serial.println(override_v);
        }
    }
}