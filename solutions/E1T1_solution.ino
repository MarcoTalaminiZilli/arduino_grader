// COLE AQUI O CÓDIGO A SER USADO COMO GABARITO

#include <Servo.h>

int pinoLed = 10;
int pinoServo = 9;
Servo meuServo;

void setup(){

    pinMode(pinoLed, OUTPUT);
    meuServo.attach(pinoServo);
}

void loop(){

    digitalWrite(pinoLed, HIGH);

    for (int i=0; i<180; i++){
        meuServo.write(i);
        delay(10);
    }

    digitalWrite(pinoLed, LOW);

    meuServo.write(0);
}