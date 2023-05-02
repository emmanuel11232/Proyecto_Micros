#include <FastLED.h>
#define LED_PIN     16
#define LED_PIN2    17
#define NUM_LEDS    139

String board[8][8];
CRGB leds[NUM_LEDS];
//CRGB leds2[NUM_LEDS];


void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
}
void loop() {
  if (Serial.available() > 0) {
    String datos = Serial.readStringUntil('\n');
    Serial.print("Recibido:");
    for(int i=0;i<=7;i++){
      for(int j=0;j<=7;j++){
        board[i][j]=datos.substring((16*i+2*j),(16*i+2*j)+2);
        Serial.println(board[i][j]);
      }
    }  
  }
  int cont = 0;
  for (int n = 0; n<8; n++)
  {
    for (int i = 0; i <8; i++)
  {
    if ((board[n][i]) =="wP") //PAWN = ROJO
    {
      leds[cont]= CRGB(255, 0, 0);
      leds[(cont+1)]= CRGB(255, 255, 255);
      FastLED.show();
      Serial.print("wP");
      Serial.print(" ");
    }
    else if ((board[n][i]) =="wN") // KNIGHT=VERDE
    {
      leds[cont]= CRGB(0, 255, 0);
      leds[(cont+1)]= CRGB(255, 255, 255);
      FastLED.show();
      Serial.print("wN");
      Serial.print(" ");
    }
    else if ((board[n][i]) =="wB") //BISHOP= AZUL
    {
      leds[cont]= CRGB(0, 0, 255);
      leds[(cont+1)]= CRGB(255, 255, 255);
      FastLED.show();
      Serial.print("wB");
      Serial.print(" ");     
    }
    else if ((board[n][i]) =="wQ") //QUEEN= ROSADO
    {
      leds[cont]= CRGB(255, 0, 127);
      leds[(cont+1)]= CRGB(255, 255, 255);
      FastLED.show();
      Serial.print("wQ");
      Serial.print(" ");
    }
    else if ((board[n][i]) =="wK") //KING= AMARILLO
    {
      leds[cont]= CRGB(255, 255, 0);
      leds[(cont+1)]= CRGB(255, 255, 255);
      FastLED.show();
      Serial.print("wK");
      Serial.print(" ");
    }
    else if ((board[n][i]) =="wR") { // ROOK = CIAN
      leds[cont]= CRGB(0, 255, 130);
      leds[(cont+1)]= CRGB(255, 255, 255);
      FastLED.show();
      Serial.print("wR");
      Serial.print(" ");
    }

    if ((board[n][i]) =="bP") //PAWN = ROJO
    {
      leds[cont]= CRGB(255, 0, 0);
      leds[(cont+1)]= CRGB(0, 0, 0);
      FastLED.show();
      Serial.print("bP");
      Serial.print(" ");
    }
    else if ((board[n][i]) =="bN") // KNIGHT=VERDE
    {
      leds[cont]= CRGB(0, 255, 0);
      leds[(cont+1)]= CRGB(0, 0, 0);
      FastLED.show();
      Serial.print("bN");
      Serial.print(" ");
    }
    else if ((board[n][i]) =="bB") //BISHOP= AZUL
    {
      leds[cont]= CRGB(0, 0, 255);
      leds[(cont+1)]= CRGB(0, 0, 0);
      FastLED.show();
      Serial.print("bB");
      Serial.print(" ");     
    }
    else if ((board[n][i]) =="bQ") //QUEEN= ROSADO
    {
      leds[cont]= CRGB(255, 0, 127);
      leds[(cont+1)]= CRGB(0, 0, 0);
      FastLED.show();
      Serial.print("bQ");
      Serial.print(" ");
    }
    else if ((board[n][i]) =="bK") //KING= AMARILLO
    {
      leds[cont]= CRGB(255, 255, 0);
      leds[(cont+1)]= CRGB(0, 0, 0);
      FastLED.show();
      Serial.print("bK");
      Serial.print(" ");
    }
    else if ((board[n][i]) =="bR") { // ROOK = CIAN
      leds[cont]= CRGB(0, 255, 255);
      leds[(cont+1)]= CRGB(0, 0, 0);
      FastLED.show();
      Serial.print("bR");
      Serial.print(" ");
    }


    else if((board[n][i]) =="--"){ // -- = 0
      leds[cont]= CRGB(0, 0, 0);
      leds[(cont+1)]= CRGB(0, 0, 0);
      FastLED.show();
      Serial.print("--");
      Serial.print(" ");
    }
    cont = cont +2;
    }
  
    }

  
}
