1. 시리얼 통신 (Serial Communication)
pyserial 라이브러리를 사용해 모터와 시리얼 통신을 한다.
serial.Serial()을 통해 포트를 열고, 데이터를 송수신한다.
self.ser.write(data)를 사용하여 데이터를 전송하고, self.ser.read(10)을 사용하여 응답을 받는다.
2. 바이트 변환 (Byte Conversion)
모터가 이해할 수 있도록 숫자를 바이트로 변환하는 과정이 필요하다.
decimal_to_hex_bytes(decimal): 부호 있는 16비트 정수를 2바이트로 변환한다.
decimal_to_hex_bytes_angle(decimal): 부호 없는 16비트 정수를 2바이트로 변환한다.
3. CRC (오류 검출)
calculate_crc(data): CRC-8 MAXIM 체크섬을 계산하여 데이터의 무결성을 확인한다.
CRC는 통신 오류를 감지하는 역할을 한다.
4. 모터 제어 명령어
모터의 ID 설정, 모드 변경, 속도 및 각도 설정 등의 명령을 만든다.
id_set(ID): 모터 ID를 설정하는 명령어를 전송한다.
switch_current_mode(ID), switch_velocity_mode(ID), switch_angle_mode(ID): 모터를 각각 전류, 속도, 각도 모드로 변경한다.
set_velocity(ID, speed): 특정 속도로 모터를 회전시킨다.
set_angle(ID, target_angle): 지정된 각도로 모터를 회전시킨다.
brake(ID): 모터를 정지시키는 브레이크 명령을 보낸다.
5. 상대 각도 설정 (Relative Angle Calculation)
set_relative_angle(ID, target_angle): 현재 모터의 각도를 조회한 후, 목표 각도를 더한 후 다시 설정한다.
query_velocity_and_angle(ID): 현재 속도와 각도를 조회하여 출력한다.
6. 예외 처리 (Exception Handling)
try-except 블록을 사용해 시리얼 통신 오류(serial.SerialException)를 처리한다.
KeyboardInterrupt 예외를 잡아서 프로그램이 강제 종료될 때 메시지를 출력한다.
