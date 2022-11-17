//####################################################
//#   apple_tester_1.0
//#   programmed by: Tomas Picha
//####################################################


// DESCRTIPTION: - Same pulse detection as on the spider

// HW: Aruino nano

/*----------------------- DEPENDENCES ----------------------------------*/


/*----------------------- DEFINITION -----------------------------------*/
const byte counter1_channelA = 2;
const byte counter1_channelB = 3;

int enc_counter_1 = 0; // value of first encoder
int enc_counter_1_prev = -1; //previous value of first encoder

byte encoder1_status = 0;

const int encoder_status_tabel [] = {0,-1,1,10,1,0,10,-1,-1,10,0,1,10,1,-1,0};

void setup() {
  
  serial_initial();
  pins_initial();
  encoder_init();
  
}

void loop() {

  meassure ();
}
