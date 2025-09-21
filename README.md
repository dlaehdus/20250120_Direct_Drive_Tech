2025.01.20

인휠모터의 모드설정, 속도설정등 기본적인 설정을 수행할수 있게 만든 코드
기본적인 모터의 실행방법만 프로그래밍함.

ggggg
  gear1 - 한 모터의 설정을 세팅하기 위한 코드
  gear2 - 한 모터의 설정을 세팅하기 위한 코드
  wheelgear1 - gear1, gear2에서 사용하는 코드
  wheelgear2 - wheelgear1 업그레이드 버전 

src
  carlim_drive - 인휠모터를 이용해서 키 입력에 따른 속도값이 모터에 적용되게끔 하는 코드 다이나믹셀도 사용하여 조향각 조정 아크만 계산
  carlim_key - 키 입력을 감지하고 지속적인 키 입력에 반응하는 코드


필요한 부품
https://www.notion.so/2025-01-20-Direct-Drive-Tech-19792e9f586980e99adecb1413b5fd88
https://en.directdrive.com/
https://www.waveshare.com/product/usb-to-4ch-rs485.htm

Direct Drive Tech 인휠모터의 여러 모드를 정리해
추후 인휠모터 사용시 인휠모터의 점검에 사용

src파일을 전방조향 4wheel에 사용되는 아커만조향, 각속도등을 적용시켜 키 입력으로 바퀴에 마찰을 최소화하여 움직이도록 하는 코드
