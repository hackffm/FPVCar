/*
 Servo on 9, 10
 Button Sense: 0..1 not pressed, ~549..562 pressed
 */
#include <PWMServo.h>
#include <Wire.h>

PWMServo myservo1, myservo2;
 
#define POWERHOLD 2
#define MOTOR_SLEEP 7

#define EN_3V3         2
#define EN_5V1         4
#define EN_5V5         7
#define CHARGER_CE     8
#define DRV_AENBL     11
#define DRV_BENBL      3
#define DRV_APHASE     6
#define DRV_BPHASE     5
#define BUTTON_SENSE  A7

#define CHARGER_ADR   0x6B

int speed0 = 100;  // forward/backward
int speed1 = 200;  // turn on same position
int speed2 = 120;
int speed3 = 60;

long ll, rr;
long act_x = 0;
long act_y = 0;
long act_rotate = 0;

int millivolt;

int loopCnt = 0;

#define DTIMEOUT 2000
uint16_t driveTimeout = 0;

void txEn() {
  pinMode(1, OUTPUT);
  delayMicroseconds(10);
}

void txDis() {
  Serial.flush();
  pinMode(1, INPUT_PULLUP);
} 

int chgRegWrite(uint8_t reg, uint8_t data) {
  int ret = 0;
  
  Wire.beginTransmission(CHARGER_ADR);
  Wire.write(reg);
  Wire.write(data);
  ret = Wire.endTransmission(true);   
  return(ret);
}

int chgRegRead(uint8_t reg) {
  int ret = 0;
  
  Wire.beginTransmission(CHARGER_ADR);
  Wire.write(reg);
  ret = Wire.endTransmission(false);  
  if(ret == 0) {
    Wire.requestFrom(CHARGER_ADR, 1, true);
    ret = Wire.read();
  } else {
    ret = -ret;
  }
  return(ret);
}  

int chgVbat() {
  chgRegWrite(0x02, 0x8d); // enable ADC in charger
  delay(100);
  int v = chgRegRead(0x0e);
  if(v<0) return(v);
  int volt = 2304;
  if(v & 1) volt += 20;
  if(v & 2) volt += 40;
  if(v & 4) volt += 80;
  if(v & 8) volt += 160;
  if(v & 16) volt += 320;
  if(v & 32) volt += 640;
  if(v & 64) volt += 1280;
  return(volt);
}

int chgVbus() {
  chgRegWrite(0x02, 0x8d);
  delay(100);
  int v = chgRegRead(0x11);

  int volt = 2600;
  if(v & 1) volt += 100;
  if(v & 2) volt += 200;
  if(v & 4) volt += 400;
  if(v & 8) volt += 800;
  if(v & 16) volt += 1600;
  if(v & 32) volt += 3200;
  if(v & 64) volt += 6400;
  return(volt);
}

int chgIbat() {
  chgRegWrite(0x02, 0x8d);
  delay(100);
  int v = chgRegRead(0x11);

  int value = 2600;
  if(v & 1) value += 50;
  if(v & 2) value += 100;
  if(v & 4) value += 200;
  if(v & 8) value += 400;
  if(v & 16) value += 800;
  if(v & 32) value += 1600;
  if(v & 64) value += 3200;
  return(value);
}

// the setup routine runs once when you press reset:
void setup() {     
  Serial.begin(38400);
  Wire.begin();
  
  pinMode(EN_3V3, OUTPUT);
  digitalWrite(EN_3V3, HIGH); 
  
  pinMode(EN_5V1, OUTPUT);
  digitalWrite(EN_5V1, HIGH);  
  
  pinMode(DRV_AENBL, OUTPUT); 
  pinMode(DRV_BENBL, OUTPUT); 
  pinMode(DRV_APHASE, OUTPUT); 
  pinMode(DRV_BPHASE, OUTPUT); 
  
  myservo1.attach(SERVO_PIN_A);  
  myservo2.attach(SERVO_PIN_B); 
  myservo1.write(90);           
  myservo2.write(90);  
  delay(100);
  
  pinMode(EN_5V5, OUTPUT);
  digitalWrite(EN_5V5, HIGH);

  
  delay(100);
}


void loop() {
  checkButton();
  serialParser();
  if(((uint16_t)millis() - driveTimeout) > DTIMEOUT) {
    driveTimeout = millis();
    drive(0,0,0);    
  }

}

void drive(short x, short y, short rotate) {  
  // later: add acceleration here
  act_x = constrain(x,-255,255);
  act_y = constrain(y,-255,255);
  act_rotate = constrain((rotate*3),-255,255);
  
  // calculate wheel speed
  //if(act_y < 0) act_x = -act_x;
  ll = -(act_x/2) - act_y - act_rotate;
  rr = +(act_x/2) - act_y + act_rotate;
  
  fahr(ll, rr); 
}

/**
 * Motor driver is DRV8835, Mode-Pin is hard-wired to H (= PH/EN-Mode)
 * APHASE = Set direction
 * AENBL  = H enable H-bridge
 *
 * left positive = left motors forward
 * right positive = right motors forward
 */
void fahr(int left, int right) {
  left = constrain(left, -255, 255);
  right = constrain(right, -255, 255);
  //Serial.print("Fahr ");
  //Serial.print(left);
  //Serial.print(", ");
  //Serial.println(right);
  
  if((right == 0) && (left == 0)) {
    // digitalWrite(EN_5V5, LOW); // Motors off
  } else {
    // digitalWrite(EN_5V5, HIGH); // Motors on
  }
  
  if(right == 0) {
    digitalWrite(DRV_AENBL, LOW);
  } else if(right < 0) {
    digitalWrite(DRV_APHASE, HIGH);
    analogWrite(DRV_AENBL, (-right));
  } else {
    digitalWrite(DRV_APHASE, LOW);
    analogWrite(DRV_AENBL, right);
  }
  
  if(left == 0) {
    digitalWrite(DRV_BENBL, LOW);
  } else if(left < 0) {
    digitalWrite(DRV_BPHASE, HIGH);
    analogWrite(DRV_BENBL, (-left));
  } else {
    digitalWrite(DRV_BPHASE, LOW);
    analogWrite(DRV_BENBL, left);
  }  

  //TCCR2B |= 3;
  //TCCR2B &= 0xf9;
}

void checkButton() {
  static uint8_t old_buttonstate = 0;
  uint8_t new_buttonstate;  
  static uint32_t button_ts = 0;
  
  
  if(analogRead(BUTTON_SENSE) > 200) {
    new_buttonstate = 1;  
  } else {
    new_buttonstate = 0;
  }    
  
  if(old_buttonstate != new_buttonstate) {
    if(new_buttonstate == 1) {
      // now pressed
      button_ts = millis(); 
    }
  } else {
      if(new_buttonstate == 1) {
          if((millis() - button_ts) > 5000) {
              Serial.println("LongPressed5s");
              button_ts = millis();
          }
      }   
  }
  old_buttonstate = new_buttonstate;
}

void serialParser() {
  static char cmd[64];
  static byte charCount = 0;

  int r,x,y,phi;

  while(Serial.available()) {
    // if any char in serial buffer available then do the parsing

    char c;
    c = Serial.read(); // read one char from serial buffer

    if((c==8) && (charCount>0)) charCount--; // backspace

    if(c>=32) { // char in num char range then add char to cmd array
      cmd[charCount] = c;
      charCount++;
    }

    if((c==0x0D) || (c==0x0A) || (charCount>60) || 
     ((charCount == 1) && ((c=='a') || (c=='s') || (c=='d') || 
     (c=='w') || (c==' ') || (c=='q') || (c=='e')))
    ) {
      // if the char is NL(New Line 0x0A) 
      // or CR (carriage return 0x0D) 
      // or cmd array buffer limit reached
      // parse the cmd buffer

      cmd[charCount]=0; // clear the last char in cmd buffer
      
      if(charCount>=1) { // prevent empty cmd buffer parsing
      
        if(cmd[0] == 'T') {
            txDis();
        } else {
            txEn();
        }

        switch(cmd[0]) {
          case '?':
            // show command listup
            Serial.println(F("Direct: adswqe space, Indirect: vMmNnP\a"));
            break;

          case ' ': // stop
            fahr(0,0);
            Serial.print("ADC: ");
            Serial.println(analogRead(BUTTON_SENSE));
            break;
            
          case 'a': // left
            fahr(speed3,speed2);
            driveTimeout = millis();
            break;
            
          case 'd': // right
            fahr(speed2,speed3);
            driveTimeout = millis();
            break; 
    
          case 's': // backward
            fahr(-speed0,-speed0);
            driveTimeout = millis();
            break;  
   
          case 'w': // forward 
            fahr(speed0,speed0);
            driveTimeout = millis();
            break;  

          case 'q': // rotate left
            fahr(-speed1,speed1);
            driveTimeout = millis();
            break;
   
          case 'e': // rotate right
            fahr(speed1,-speed1);
            driveTimeout = millis();
            break;      
      
          case 'v':
            {
              Serial.print("v:");
              Serial.println(chgVbat());
            }
            break;  
          case 'V':
            {
              Serial.print("V:");
              Serial.println(chgVbus());
            }
            break;
          case 'o':
          {
            Serial.print("o:");
            Serial.println(chgIbat()); 
            break; 
          }
          
          case 'i':
            if(charCount>=2) {
              short reg;
              short dat;
              r = sscanf_P(&cmd[1],PSTR("%x %x"),&reg,&dat);
              if(r == 1) {
                Serial.print("R ");
                Serial.print(reg, HEX);
                Serial.print(":0x");
                Serial.println(chgRegRead(reg), HEX);
              } else if(r == 2) {
                Serial.print("W ");
                Serial.print(reg, HEX);
                Serial.print(":0x");
                Serial.print(dat, HEX);
                Serial.print(" Res:");
                Serial.println(chgRegWrite(reg, dat)); 
              }
            } else {
              for(int i=0; i<0x14; i++) {
                Serial.print(i, HEX);
                Serial.print(":0x");
                Serial.println(chgRegRead(i), HEX);
              }
            }
            break;

          case 'm':
          case 'M':
            if(charCount>=2) {
              short xx; 
              short yy;
              short rr;
              r = sscanf_P(&cmd[1],PSTR("%d %d %d"),&xx,&yy,&rr);
              if(r>=2) {
                if(cmd[0] == 'm') { 
                  drive(xx,yy,rr);
                  //fahr(-left,-right);
                  //Serial.print(act_x);
                  //Serial.print(',');
                  //Serial.print(act_y);
                  //Serial.print(',');
                  //Serial.println(act_rotate); 
                  driveTimeout = millis();                  
                }
              }
            }
            break;          

          case 'f':
          case 'F':
            if(charCount>=2) {
              short ll; 
              short rr;
              r = sscanf_P(&cmd[1],PSTR("%d %d"),&ll,&rr);
              if(r>=2) {
                if(cmd[0] == 'f') { 
                  fahr(ll,rr); 
                  driveTimeout = millis();                  
                }
              }
            }
            break; 

          case 'n':
          case 'N':
            if(charCount>=2) {
              int rl; 
              int ou;
              r = sscanf_P(&cmd[1],PSTR("%i %i"),&rl,&ou);
              if(r==2) {
                if(cmd[0] == 'N') {
                  myservo2.write(rl);
                  myservo1.write(ou);
                  driveTimeout = millis(); 
                } else {
                  Serial.print("N ");
                  Serial.print(rl);
                  Serial.print(", ");
                  Serial.println(ou);                
                }
              }
            }
            break;             
            
          case 'p':
            if(charCount>=2) {
              int posi = 900;
              switch(cmd[1]) {
                case '0':
                  // relative goto parser
                  
                  r = sscanf_P(&cmd[2],PSTR("%i"),&speed0);
                  if(r==1) {
                    Serial.println(speed0); 
                  } else {
                    Serial.println("?");
                  }
                  break;
                  
                case '1':
                  // relative goto parser
                  
                  r = sscanf_P(&cmd[2],PSTR("%i"),&speed1);
                  if(r==1) {
                    Serial.println(speed1); 
                  } else {
                    Serial.println("?");
                  }
                  break;
                  
                case '2':
                  // relative goto parser
                  
                  r = sscanf_P(&cmd[2],PSTR("%i"),&speed2);
                  if(r==1) {
                    Serial.println(speed2); 
                  } else {
                    Serial.println("?");
                  }
                  break;
                  break;
                  
                case '3':
                  // relative goto parser
                  
                  r = sscanf_P(&cmd[2],PSTR("%i"),&speed3);
                  if(r==1) {
                    Serial.println(speed3); 
                  } else {
                    Serial.println("?");
                  }
                  break;
                  
                  
                case 'v':
                  r = sscanf_P(&cmd[2],PSTR("%i"),&posi);
                  if(r==1) {
                    Serial.println(posi);
                    myservo1.write(posi); 
                  } else {
                    Serial.println("?");
                  }
                  break;

                  
                case 'h':
                  r = sscanf_P(&cmd[2],PSTR("%i"),&posi);
                  if(r==1) {
                    Serial.println(posi);
                    myservo2.write(posi); 
                  } else {
                    Serial.println("?");
                  }
                  break;                                    

                  
                case '!': // off after 1 minute
                  r = sscanf_P(&cmd[2],PSTR("%i"),&posi);
                  if((r==1) && (posi == 999)) 
                  {
                    Serial.println("Off after 60s!");
                    digitalWrite(EN_5V5, LOW); // Motors off
                    delay(60000);
                    digitalWrite(EN_5V1, LOW);
                    delay(5000);
                    digitalWrite(EN_3V3, LOW);
                    delay(5000);
                  }
                  break;
                                    
                case 'a':

                  break;

                default:
                  Serial.println("valid commands pp");
                  break;
              }
            }
            
            break; // case 'p'


            
          default:
            Serial.println("hae?\a");
            break;

        }
      }
      charCount = 0;
      //Serial.print(">");
    }
  }
}
