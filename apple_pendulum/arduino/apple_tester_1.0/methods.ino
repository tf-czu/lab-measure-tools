/*----------------------Serial-initialization------------------------------------*/
void serial_initial(){
  Serial.begin(2000000); 
  while (!Serial) {
      ; 
  }
}

/*----------------------pins-initialization------------------------------------*/
void pins_initial(){

  pinMode(counter1_channelA, INPUT);
  pinMode(counter1_channelB, INPUT);
}

/*----------------------encoder_initialization------------------------------------*/
void encoder_init() {
  encoder_read();
}


/*-------------------------- meassure  -------------------------*/

void meassure () {
    
  encoder_read();
  encoders_counting();
  serial_prnt_encoders_check();
}

/*----------------------serial-print_encoders_check------------------------------------*/
void serial_prnt_encoders_check() {
  if (enc_counter_1 != enc_counter_1_prev) {
    Serial.println(enc_counter_1);
    enc_counter_1_prev = enc_counter_1;
  }
}

/*----------------------encoder_read------------------------------------*/
void encoder_read() {
  byte temp_A = 0;
  byte temp_B = 0;

  encoder1_status = encoder1_status & B0011;
  encoder1_status = encoder1_status << 2;

  temp_A = digitalRead(counter1_channelA);
  temp_A = temp_A & B0001;
  temp_A = temp_A << 1;
  encoder1_status = encoder1_status | temp_A;
  temp_B = digitalRead(counter1_channelB);
  temp_B = temp_B & B0001;
  encoder1_status = encoder1_status | temp_B;
}

/*----------------------encoders_counting------------------------------------*/
void encoders_counting() {
  if(abs(encoder_status_tabel[encoder1_status]) != 10) {
    enc_counter_1 = enc_counter_1 + encoder_status_tabel[encoder1_status];
  } else {
    //Serial.println("skip_error");
  }
}