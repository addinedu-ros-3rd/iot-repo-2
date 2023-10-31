# 물류 자동화 시스템
<p align=center width="100%">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/1ff34acc-31dc-4b7b-8f39-6a2308d35edd" height="400" width="45%" style="float:left">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/86283716/f307b3a5-0992-4a52-91ca-687a7f884c1c" height="400" width="45%" style="float:left">
</p>

<p align=center>
  <a href="https://youtu.be/QK5B_ghezHc?feature=shared">
    <img src="http://img.youtube.com/vi/QK5B_ghezHc/0.jpg">
  </a>
  <br>
  <a href="https://youtu.be/QK5B_ghezHc?feature=shared">영상 보러 가기</a>
</p>

## 프로젝트 기간
2023.10.23 ~ 2023.10.27 (5일)

## 기술 스택
### 개발 환경
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white)
![Arduino](https://img.shields.io/badge/arduino-00878F?style=for-the-badge&logo=arduino&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)   
</div>

### 언어
![C++](https://img.shields.io/badge/c++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)

### 커뮤니케이션
![Slack](https://img.shields.io/badge/slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)


## 프로젝트 소개
### 자동 분류 컨베이어 벨트와 라인 유도 주행을 활용한 물류 자동화 시스템
- 물류 프로세스 중 인력과 시간이 많이 소모되는 상품 분류 및 배송 단계의 자동화
- RFID와 데이터베이스를 활용 재고 추적
- 라인 유도 주행, 장애물 인식 기술을 사용한 자율 주행

## 팀원 소개 및 역할
|구분|이름|역할|
|---|---|---|
|팀장|강한얼|회로 설계, 하드웨어 제작, DC 모터 제어, 다중 RFID 인식, 다중 분류기 서보 모터 제어, CCTV|
|팀원|강소희|회로 설계, 하드웨어 제작, 서보 모터 제어|
|팀원|오윤|DB 설계, PyQt, 시리얼 통신, RFID 인식|
|팀원|조태상|회로 설계, IR 및 초음파 센서 튜닝|
|팀원|한승준|하드웨어 제작, 블루투스 시리얼 통신, 모바일 앱 제작, QA|

## 기능리스트
### 컨베이어 벨트
- 컨베이어 벨트 제어
  - 벨트 원격 제어(On/Off)
- 상품 인식 및 분류
  - RFID 모듈을 통한 상품 ID 인식
  - ID별 상품의 카테고리를 DB에서 조회하여 상품의 이동 위치를 결정
  - 결정된 위치의 서보 모터 분류기를 실행하여 이동 하는 상품을 분류 및 출고
- 재고 추적 및 관리
  - DB를 통해 각 상품의 ID 및 목적지 데이터 관리
  - 각 상품이 입고된 시점을 DB에 업데이트
  - 분류 및 출고된 시점의 시간을 DB에 업데이트
  - CCTV를 통해 상황 녹화
- 통신
  - 통신으로 서버와 데이터를 주고 받음

### RC카
- 로봇 제어
  - 관리자 앱을 통해 로봇을 ON/ OFF 및 움직임을 제어
- 라인 인식
  - 로봇 앞쪽에 위치한 IR(Infrared ray)센서를 통해 라인을 인식
  - IR 센서는 좌, 우에 위치하며 직선, 곡선, 정지 라인을 인식
  - 인식한 라인의 형태에 따라 4개 모터에 알맞은 시나리오 (직진, 좌회전, 우회전, 정지)
- 장애물 인식
  - Ultrasonic 센서를 통해 차의 진행방향에 장애물이 있는지 없는지 판단
  - 차의 진행방향과 동일한 선상에서 장애물을 인식한 경우 일단 정지
  - 서보모터를 회천하여 왼쪽과 오른쪽의 장애물 여부를 판단하고, 턴하거나 계속 정지
- 통신
  - 실시간으로 IR 센서 및 거리 값을 받음

## 시스템 구성
<p align="center">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/b917c461-7ad4-43a7-91b3-2db9daa03f0e" >
</p>

- 컨베이어 벨트 : 상품 인식, 자동 분류
- RC 주행 로봇 : 라인 주행, 장애물 인식
- 데이터베이스 : 재고 추적, 관리
- 서버 : 통신 및 통합 제어
- CCTV : 화면 촬영 및 녹화
- 통합 관리 GUI & 로봇 제어 모바일 어플리케이션

## 순서도
### 컨베이어 벨트
<p align="center">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/b2e89e98-b77a-4357-9f82-3edf6458d2b5" >
</p>

### RC 주행 로봇
<p align="center">
  <img src="https://github.com/YunOh21/edu/assets/86283716/c67541fe-5e51-4ef5-ae8b-76062660170e">
</p>

<p align="center">
  <img src="https://github.com/YunOh21/edu/assets/86283716/b9ad98dc-5b48-4f02-925b-522748cd4d19">
</p>
