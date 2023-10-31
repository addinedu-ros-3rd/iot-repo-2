# 물류 자동화 시스템
<p align="center">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/1ff34acc-31dc-4b7b-8f39-6a2308d35edd" height="400" width="600">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/86283716/f307b3a5-0992-4a52-91ca-687a7f884c1c" height="400" width="600">
</p>

## 프로젝트 기간
2023.10.23 ~ 2023.10.27 (5일)

## 기술 스택
### 개발 환경
<img src="https://img.shields.io/badge/arduino-00878F?style=for-the-badge&logo=arduino&logoColor=#00878F">

### 언어

## 프로젝트 소개
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
- 

### RC카

## 시스템 구성
<p align="center">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/b917c461-7ad4-43a7-91b3-2db9daa03f0e" >
</p>

- 컨베이어 벨트
- RC 주행 로봇
- 데이터베이스
- 서버
- CCTV
- 통합 관리 GUI
- 로봇 제어 모바일 어플리케이션

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
