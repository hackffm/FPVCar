/*
 Servo on 9, 10
 */
#include <PWMServo.h>

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

int speed0 = 60;  // forward/backward
int speed1 = 75;  // turn on same position
int speed2 = 80;
int speed3 = 20;

long ll, rr;
long act_x = 0;
long act_y = 0;
long act_rotate = 0;

int millivolt;

int loopCnt = 0;

#define DTIMEOUT 2000
uint16_t driveTimeout = 0;



// the setup routine runs once when you press reset:
void setup() {     
  Serial.begin(38400);
  
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

  serialParser();
  if(((uint16_t)millis() - driveTimeout) > DTIMEOUT) {
    driveTimeout = millis();
    //drive(0,0,0);    
  }

}

void updateWheels() {
  // calculate wheel speed
  //if(act_y < 0) act_x = -act_x;
  ll = -(act_x/2) - act_y - act_rotate;
  rr = +(act_x/2) - act_y + act_rotate;
  
  fahr(constrain(ll,-255,255), constrain(rr,-255,255));  
}

void drive(short x, short y, short rotate) {  
  // later: add acceleration here
  act_x = constrain(x,-255,255);
  act_y = constrain(y,-255,255);
  act_rotate = constrain((rotate*3),-255,255);
  
  updateWheels();
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

void serialParser() {
  static char cmd[64];
  static byte charCount = 0;

  int r,x,y,phi;

  if(Serial.available()) {
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
              Serial.println(millivolt);
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
      Serial.print(">");
    }
  }
}
