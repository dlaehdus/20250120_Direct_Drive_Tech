import serial
#외부 장치(예: Arduino, 마이크로컨트롤러)와 **시리얼 포트(USB, UART)**를 통해 통신할 수 있도록 도와주는 라이브러리입니다.
import struct
#데이터를 바이트(bytes) 형식으로 **패킹(packing)**하거나 **언패킹(unpacking)**할 때 사용합니다.
#예를 들어, 정수(int), 실수(float) 같은 데이터를 바이트 형태로 변환하여 시리얼 포트로 전송할 수 있습니다.
import time
from threading import Thread, Event
#**threading**은 프로그램을 여러 스레드로 나누어 병렬 처리를 구현할 때 사용됩니다.

class MotorController:
#메서드 정의: MotorController 클래스의 **생성자(constructor)**
    def __init__(self, port, baudrate=115200, timeout=1):
    #객체를 만들 때 호출되는 함수
        try:
        #예외 처리 블록의 시작입니다.
            self.ser = serial.Serial(  
                #시리얼 포트 객체(serial.Serial)를 생성합니다.
                port=port,
                #포트 연결 설정: 주어진 포트에 대해 시리얼 연결을 설정합니다 예: '/dev/ttyACM0', 'COM3'
                baudrate=baudrate,
                #통신 속도 (기본값: 115200 bps). 일반적인 시리얼 통신 속도입니다.
                parity=serial.PARITY_NONE,
                #패리티 비트는 데이터 전송 중 에러 검출을 위한 추가 비트입니다.
                # **PARITY_NONE**은 패리티 비트를 사용하지 않겠다는 의미입니다.
                stopbits=serial.STOPBITS_ONE,
                #**STOPBITS_ONE**은 1개의 정지 비트를 사용하겠다는 설정입니다.
                bytesize=serial.EIGHTBITS,
                #**EIGHTBITS**는 8비트(1바이트) 데이터를 전송한다는 의미입니다.
                timeout=timeout
                #시리얼 포트에서 데이터를 읽을 때 **최대 대기 시간(초)**입니다. 기본값은 1초입니다.
            )
            print(f"[INFO] Connected to {port}")
            #시리얼 포트에 성공적으로 연결되면 포트 이름과 함께 메시지를 출력합니다.
        except serial.SerialException as e:
        #이 블록 안의 코드가 오류를 발생시키면 except 블록이 실행됩니다./dev/ttyACM2
            print(f"[ERROR] Failed to connect to {port}: {e}")
            #예외 처리: 연결 실패 시 오류 메시지를 출력하고 예외를 발생시킵니다.
            raise


        self.running = Event()
        #Event 객체를 생성하여 self.running에 저장합니다.스레드의 실행 상태를 제어하는 객체.
        #스레드는 프로그램 내에서 동시에 실행되는 작은 작업 단위
        #멀티스레드는 여러 스레드를 사용하여 동시에 작업 수행
        self.running.set()
        #Event 객체의 상태 합니다. 즉, 이 구문은 해당 스크립트가 다른 파일에서 import되지 않고, 독립적으로 실행될 를 "설정됨(켜짐)" 상태로 변경합니다.


    def decimal_to_hex_bytes(self, decimal): #decimal_to_hex_bytes라는 메서드를 정의합니다. 이 메서드는 decimal이라는 매개변수를 받습니다
        hex_string = format(struct.unpack('>H', struct.pack('>h', decimal))[0], 'x').zfill(4)
        #struct 라이브러리는 숫자를 바이트 데이터로 변환할 때 사용합니다
        #'>h' 포맷:
        #>: 빅엔디안 방식 (바이트 순서를 왼쪽부터 저장)
        #h: 16비트 부호 있는 정수 (2바이트) 이 부분은 decimal 값을 2바이트 부호 있는 정수로 변환합니다.
        #'>H' 포맷:
        #>: 빅엔디안 방식
        #H: 16비트 부호 없는 정수 (2바이트)
        #format() 함수는 숫자를 16진수 문자열로 변환합니다.
        #'x': 소문자 16진수로 변환 (예: 0x1234 → '1234'
        #format() 함수는 숫자를 16진수 문자열로 변환합니다.
        #'x': 소문자 16진수로 변환 (예: 0x1234 → '1234'
        #이 부분은 부호 있는 정수를 부호 없는 정수로 해석합니다.
        return int(hex_string[:2], 16), int(hex_string[2:], 16)
        #hex_string[:2]: 앞의 2자리 16진수를 가져옵니다.
        #hex_string[2:]: 뒤의 2자리 16진수를 가져옵니다
        #int(..., 16): 문자열을 정수형 16진수로 변환합니다.




        #motor.decimal_to_hex_bytes(258)
        #258 → 2바이트 빅엔디안으로 변환
        #16진수 문자열 → '0102'
        #앞 2자리: '01' → 1
        #뒤 2자리: '02' → 2
        #최종 반환 값: (1, 2)
    def calculate_crc(self, data):
    #calculate_crc라는 메서드를 정의합니다. 이 메서드는 data라는 매개변수를 받습니다.
    #바이트 시퀀스 데이터를 오류 검출을 위해 CRC-8 MAXIM 알고리즘을 사용해서 계산하는 거죠.
    #**CRC (Cyclic Redundancy Check)**는 데이터 전송 중 오류 검출을 위해 사용되는 체크섬 알고리즘이에요.
    #네트워크 통신, 파일 전송, 센서 데이터 처리 등에서 데이터가 손상됐는지 확인할 때 사용되죠.
    #CRC는 XOR 연산을 기반으로 오류를 검출해요.
    #XOR 연산은 두 비트가 다르면 1, 같으면 0을 반환합니다.
    #데이터가 조금만 변해도 XOR 결과가 크게 바뀌기 때문에, 오류 검출에 강력합니다.
        CRC8_MAXIM_table = (
        #CRC8_MAXIM_table은 CRC-8 알고리즘을 수행하는데 사용되는 고정된 테이블입니다.
        #이 테이블은 미리 계산된 CRC 값들로 구성돼 있어요.
        #테이블을 사용하면 계산 속도가 훨씬 빨라지기 때문이에요.
        #데이터 바이트마다 테이블을 참조해서 빠르게 CRC 값을 계산할 수 있습니다.
        0x00, 0x5e, 0xbc, 0xe2, 0x61, 0x3f, 0xdd, 0x83,
        0xc2, 0x9c, 0x7e, 0x20, 0xa3, 0xfd, 0x1f, 0x41,
        0x9d, 0xc3, 0x21, 0x7f, 0xfc, 0xa2, 0x40, 0x1e,
        0x5f, 0x01, 0xe3, 0xbd, 0x3e, 0x60, 0x82, 0xdc,
        0x23, 0x7d, 0x9f, 0xc1, 0x42, 0x1c, 0xfe, 0xa0,
        0xe1, 0xbf, 0x5d, 0x03, 0x80, 0xde, 0x3c, 0x62,
        0xbe, 0xe0, 0x02, 0x5c, 0xdf, 0x81, 0x63, 0x3d,
        0x7c, 0x22, 0xc0, 0x9e, 0x1d, 0x43, 0xa1, 0xff,
        0x46, 0x18, 0xfa, 0xa4, 0x27, 0x79, 0x9b, 0xc5,
        0x84, 0xda, 0x38, 0x66, 0xe5, 0xbb, 0x59, 0x07,
        0xdb, 0x85, 0x67, 0x39, 0xba, 0xe4, 0x06, 0x58,
        0x19, 0x47, 0xa5, 0xfb, 0x78, 0x26, 0xc4, 0x9a,
        0x65, 0x3b, 0xd9, 0x87, 0x04, 0x5a, 0xb8, 0xe6,
        0xa7, 0xf9, 0x1b, 0x45, 0xc6, 0x98, 0x7a, 0x24,
        0xf8, 0xa6, 0x44, 0x1a, 0x99, 0xc7, 0x25, 0x7b,
        0x3a, 0x64, 0x86, 0xd8, 0x5b, 0x05, 0xe7, 0xb9,
        0x8c, 0xd2, 0x30, 0x6e, 0xed, 0xb3, 0x51, 0x0f,
        0x4e, 0x10, 0xf2, 0xac, 0x2f, 0x71, 0x93, 0xcd,
        0x11, 0x4f, 0xad, 0xf3, 0x70, 0x2e, 0xcc, 0x92,
        0xd3, 0x8d, 0x6f, 0x31, 0xb2, 0xec, 0x0e, 0x50,
        0xaf, 0xf1, 0x13, 0x4d, 0xce, 0x90, 0x72, 0x2c,
        0x6d, 0x33, 0xd1, 0x8f, 0x0c, 0x52, 0xb0, 0xee,
        0x32, 0x6c, 0x8e, 0xd0, 0x53, 0x0d, 0xef, 0xb1,
        0xf0, 0xae, 0x4c, 0x12, 0x91, 0xcf, 0x2d, 0x73,
        0xca, 0x94, 0x76, 0x28, 0xab, 0xf5, 0x17, 0x49,
        0x08, 0x56, 0xb4, 0xea, 0x69, 0x37, 0xd5, 0x8b,
        0x57, 0x09, 0xeb, 0xb5, 0x36, 0x68, 0x8a, 0xd4,
        0x95, 0xcb, 0x29, 0x77, 0xf4, 0xaa, 0x48, 0x16,
        0xe9, 0xb7, 0x55, 0x0b, 0x88, 0xd6, 0x34, 0x6a,
        0x2b, 0x75, 0x97, 0xc9, 0x4a, 0x14, 0xf6, 0xa8,
        0x74, 0x2a, 0xc8, 0x96, 0x15, 0x4b, 0xa9, 0xf7,
        0xb6, 0xe8, 0x0a, 0x54, 0xd7, 0x89, 0x6b, 0x35
        )
        crc = 0x00
        #처음에는 CRC 값을 0으로 초기화합니다.
        for byte in data:
        #data에서 각 byte를 하나씩 처리하는 반복문입니다. data는 바이트 시퀀스
            crc = CRC8_MAXIM_table[crc ^ byte]
            #crc ^ byte는 현재 crc 값과 byte 값을 XOR 연산합니다.
            #그 결과를 CRC 테이블에서 찾은 값으로 갱신합니다
        return crc
        #이 값은 CRC-8 체크섬으로, 데이터 전송이나 저장 중에 발생할 수 있는 오류를 검출하는 데 사용됩니다.
        #최종적으로 계산된 CRC 값을 반환합니다.
        #이 값이 데이터의 무결성을 검증하는 데 사용됩니다.


    def send_data(self, data):
        try:
            self.ser.write(data)
            #self.ser는 직렬 포트(Serial port)를 나타내는 객체로 추정됩니다.
            #보통 pyserial 라이브러리를 사용하여 직렬 통신을 처리합니다.
            print(f"[INFO] Sent: {data.hex()}")
            #data.hex()는 전송한 데이터를 16진수 문자열 형식으로 출력하는 방법입니다.
            #예를 들어, data가 b'\x01\x02'라면 data.hex()는 '0102'를 반환합니다.
        except serial.SerialException as e:
            print(f"[ERROR] Failed to send data: {e}")


    def id_set(self, ID):
        data = bytes([0xAA, 0x55, 0x53, ID, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        #bytes([...])는 바이트 객체를 생성하는 방법으로, 이 리스트의 값들은 각각 16진수로 나타낸 바이트 값을 나타냅니다.
        #data는 전송할 데이터를 정의한 바이트 시퀀스입니다.
        #0xAA, 0x55, 0x53: 특정 시작 시퀀스나 고정된 헤더일 수 있습니다.
        #ID: 함수의 매개변수로 받은 ID 값이 들어갑니다.
        for _ in range(5):
            #이 반복문은 5번 반복합니다. _는 반복 변수를 사용할 필요가 없을 때 주로 쓰는 변수입니다.
            self.send_data(data)
            #send_data 메서드를 호출하여 data를 직렬 포트를 통해 전송합니다.
            #이 데이터는 위에서 정의된 바이트 시퀀스입니다.


    def id_query(self):
        data = bytes([0xC8, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xDE])
        self.send_data(data)
        try:
            if self.ser.readable():
                response = self.ser.read(1)
                #직렬 포트(self.ser)에서 응답을 읽어옵니다.
                #응답은 1바이트이며, self.ser.read(1)을 통해 읽습니다.
                print(f"[INFO] ID: 0x{ord(response):02X}")
        except serial.SerialException as e:
            print(f"[ERROR] Failed to read ID: {e}")


    def switch_velocity_mode(self, ID):
        data = bytes([ID, 0xA0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02])
        #0xA0: 명령 코드 또는 기능을 나타내는 값일 가능controller.stop()성이 있습니다.
        #이 값은 속도 모드 전환을 의미하는 명령을 나타냅니다.
        #나머지 바이트들 (0x00): 추가적인 파라미터들이나 여유 공간일 수 있습니다
        self.send_data(data)


    def set_velocity(self, ID, speed):
        speed_H, speed_L = self.decimal_to_hex_bytes(speed)
        data_temp = bytes([ID, 0x64, speed_H, speed_L, 0x00, 0x00, 0x00, 0x00, 0x00])
        #data_temp는 속도를 설정하기 위한 명령을 담고 있는 바이트 시퀀스입니다.
        #speed_H와 speed_L: 앞서 변환한 속도의 고위 바이트와 저위 바이트입니다.
        #0x64: 명령 코드로, 이 값은 속도 설정을 의미하는 명령일 수 있습니다.
        crc = self.calculate_crc(data_temp)
        #CRC 체크섬을 계산하는 함수입니다. CRC는 전송된 데이터의 무결성을 확인하는 데 사용됩니다
        data = data_temp + bytes([crc])
        self.send_data(data)


    def brake(self, ID):
        data_temp = bytes([ID, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00])
        #0xFF: 브레이크 명령에 해당하는 특수한 값일 수 있습니다. 브레이크를 활성화하는 역할을 할 것입니다.
        crc = self.calculate_crc(data_temp)
        data = data_temp + bytes([crc])
        self.send_data(data)


    def periodic_query(self, interval=1):
        while self.running.is_set():
        #self.running은 보통 스레드나 프로세스가 실행 중인지 아닌지를 나타내는 Event 객체입니다
            self.id_query()
            time.sleep(interval)


    def start_query_thread(self, interval=1):
    #이 스레드는 1초마다 id_query()를 호출하고, self.running이 True인 동안 계속 반복됩니다.
    #self.running.set()이 호출되면, periodic_query는 1초마다 id_query를 실행하고
    #self.running.clear()가 호출되면 루프가 종료됩니다.
        self.query_thread = Thread(target=self.periodic_query, args=(interval,))
        self.query_thread.daemon = True
        self.query_thread.start()


    def stop(self, ID):
        print("[INFO] Stopping controller...")
        self.running.clear()
        ##self.running.clear()가 호출되면 루프가 종료됩니다.
        if self.query_thread.is_alive():
        #is_alive() 메서드는 query_thread가 현재 실행 중인지 확인합니다.
        # 스레드가 실행 중이면 True를 반환합니다
            self.query_thread.join()
            #join()은 query_thread가 종료될 때까지 메인 스레드가 기다리도록 만듭니다.
            #즉, query_thread가 완료될 때까지 stop 메서드는 실행을 멈추고 대기합니다.
        self.ser.close()
        print("[INFO] Controller stopped.")


if __name__ == "__main__":
    controller = MotorController(port='/dev/ttyACM0')
    controller.start_query_thread(interval=5)
    #interval=5는 5초 간격으로 주기적인 쿼리 작업이 실행되도록 설정합니다.
    #id_query() 메서드를 호출하여 모터의 ID를 주기적으로 쿼리합니다.
    try:
        controller.set_velocity(0x01, 10)
        #set_velocity 메서드를 호출하여 모터의 속도를 설정합니다.
        #첫 번째 인수 0x01은 모터의 ID이고, 두 번째 인수 100은 설정할 속도 값입니다.
        time.sleep(10)
        #10초 동안 프로그램을 일시 중지시킵니다. 이 시간 동안 모터는 설정된 속도로 동작합니다.
        controller.brake(0x01)
        #brake 메서드를 호출하여 모터를 정지시킵니다.
    except KeyboardInterrupt:
        print("[INFO] Interrupted by user.")
    finally:
        controller.stop()
