# 물류 자동화 시스템
<p align=center width="100%">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/1db8d4a6-1a5e-4e2f-a21d-fcc9dca9c9e8" height="300" width="20%" style="float:left">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/7cecec09-93a3-41dd-89e9-d0f1c56d90fe" height="300" width="35%" style="float:left">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/a692ad11-e3d7-41f0-9d14-d83217968a53" height="300" width="35%" style="float:left">
</p>

## 발표 자료
https://docs.google.com/presentation/d/1v5rwfUhqAP4vXjpZGAlny1NlASyI4Voo/edit?usp=sharing&ouid=118365173441214220116&rtpof=true&sd=true

## 시스템 구성
<p align="center">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/5707552a-9e11-4089-819d-b437377eab6d" width="90%" style="float:left">
</p>

- Automatic Sorter (자동 화물 분류기) : 화물 인식, 자동 분류
- Autonomous Driving Robot (자율 주행 로봇) : 라인 주행, 장애물 인식
- Central Management System (중앙 관리 시스템) : 통신 및 통합 제어
- DB : 재고 추적, 관리
- CCTV : 현장 녹화



## 팀원 소개 및 역할
|구분|이름|역할|
|---|---|---|
|팀장|강한얼|전체 시스템 구성도 제작, 컨베이어 벨트 제어 전반(RFID, 서보 모터, DC 모터), CCTV 기능|
|팀원|강소희|분류기 서보 모터 제어, 회로 설계, 하드웨어 제작|
|팀원|오윤|DB 설계, Query 작성, PyQt, 시리얼 통신, RFID 인식|
|팀원|조태상|IR 및 초음파 센서 튜닝, 자율 주행 로봇 제작|
|팀원|한승준|자율 주행 로봇 시스템 구성도 제작, 회로 설계, 블루투스 시리얼 통신, 모바일 앱 제작|

## 프로젝트 기간
2023.10.23 ~ 2023.10.27 (5일)

## 기술 스택
### 개발 환경
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white)
![Arduino](https://img.shields.io/badge/arduino-00878F?style=for-the-badge&logo=arduino&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)
![RDS](https://img.shields.io/badge/AWS%20RDS-527FFF?style=for-the-badge&logo=Amazon%20RDS&logoColor=white)
![Qt](https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=Qt&logoColor=white)
![mitapp](https://github.com/addinedu-ros-3rd/iot-repo-2/assets/81555330/11db2c8f-f4ae-46c0-ae71-d83b6e9e1d5c)
</div>

### 언어
![C++](https://img.shields.io/badge/c++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)

### DBMS
![Mysql](https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

### 커뮤니케이션
![Slack](https://img.shields.io/badge/slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)


## 프로젝트 소개
### 자동 화물 분류기와 자율 주행 로봇을 활용한 물류 자동화 시스템
- 물류 프로세스 중 인력과 시간이 많이 소모되는 화물 분류 및 배송 단계의 자동화
- RFID와 DB를 활용 재고 추적
- 라인 유도 주행, 장애물 인식 기술을 사용한 자율 주행

## 1. Automatic Sorter (자동 화물 분류기)
### 1) 화물 입고, 분류 시나리오
<p align=center width="100%">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/86283716/e06fb21a-12e2-4509-a289-6712d118fb66"  width="70%" style="float:left">
</p>

### 2) 하드웨어 구성
<p align=center width="100%">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/95ad5f7f-eeac-4258-aadc-dce893411d87"  width="90%" style="float:left">
</p>

### 3) 기능 리스트
- 분류기 제어
  - 컨베이어 벨트 원격 제어(On/Off)
    
- 화물 인식 및 분류
  - RFID 모듈을 통한 화물 ID 인식
  - ID별 화물의 분류 위치를 DB에서 조회하여 화물의 이동 위치를 결정
  - 결정된 위치의 서보 모터 분류기를 실행하여 이동 하는 화물을 분류 및 출고

- 재고 추적 및 관리
  - DB를 통해 각 화물의 ID 및 분류 위치 데이터 관리
  - 각 화물이 입고된 시점을 DB에 업데이트
  - 분류 및 출고된 시점의 시간을 DB에 업데이트
  - CCTV를 통해 상황 녹화

- 통신
  - 통신으로 PC와 데이터를 주고 받음

## 2. Autonomous Driving Robot (자율 주행 로봇)
### 1) 주행 시나리오 
<p align=center width="100%">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/86283716/71eef0f0-99ae-4f48-89e1-74cf73e2dc82"  width="90%" style="float:left">
</p>

### 2) 하드웨어 구성 
<p align=center width="100%">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/46445b2c-462b-4fed-b6d5-0dc7a5d866c8"  width="90%" style="float:left">
</p>

### 3) 기능 리스트
- 로봇 제어
  - 관리자 앱을 통해 로봇을 ON / OFF 및 움직임을 제어

- 라인 인식
  - 로봇 앞쪽에 위치한 IR (Infrared ray) 센서를 통해 라인을 인식
  - IR 센서는 좌, 우에 위치하며 직선, 곡선, 정지 라인을 인식
  - 인식한 라인의 형태에 따라 4개 모터에 알맞은 시나리오 (직진, 좌회전, 우회전, 정지)

- 장애물 인식
  - Ultrasonic 센서를 통해 차의 진행방향에 장애물 여부 판단
  - 로봇의 진행방향과 동일한 선상에서 장애물을 인식한 경우 일단 정지
  - 서보 모터를 회전하여 왼쪽과 오른쪽의 장애물 여부를 판단하고 정지 상태 유지

- 통신
  - 실시간으로 IR 센서 및 거리 값을 받음

## 3. PC
<p align=center width="100%">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/143172717/b64cfec8-6e68-4a55-8b92-c6d6072ecca3"  width="70%" style="float:left">
</p>

### 1) 중앙 관제 시스템 GUI
<p align=center width="100%">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/61872888/55a9a938-947d-474f-8270-0e2fe1ee35c0"  width="90%" style="float:left">
</p>

① 입고/처리/출고 시점 선택 (달력으로 년월일 선택, 시분초는 입력) <br>
② 분류 콤보박스 선택 (서울_창고 / 부산_창고 / 출고) <br>
③ 상태 콤보박스 선택 (미입고 / 입고 / 출고) <br>
④ 특정 RFID 검색 (입력 형태가 틀린 경우 아래에 형태 안내 띄움) <br>
⑤ 검색 필터(시점, 분류, 상태, RFID) 초기화 <br>
⑥ 검색: 현재 설정된 조건으로 DB 조회 <br>
⑦ 벨트제어: Start/Stop <br>
⑧ DB 조회결과 표시 <br>
⑨ CCTV 화면표시 On/Off <br>
⑩ CCTV 영상 녹화 On/Off <br>
⑪ CCTV 사진 촬영 <br>
⑫ CCTV 현재 화면

### 2) Database : 분류기 및 로그 데이터 구조
<p align=center width="100%">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/86283716/f3068ab0-60aa-4da3-94c8-6bbcbf976f7f"  width="90%" style="float:left">
  <img src="https://github.com/addinedu-ros-3rd/iot-repo-2/assets/86283716/677f1675-5f62-4c38-a1f1-825987cf0ae8"  width="90%" style="float:left">
</p>

## 4. 설계에 있었지만 구현하지 못한 내용
- GUI를 통한 belt on/off/속도 제어 기능
  - 모터 제어 가능한 하드웨어 고장
  - belt 테이블 활용 x

- RFID 리더기로 재고 관리 및 오분류/분실 방지 기능
  - RFID-RC522 모듈 사용, 회로 또는 전원 문제로 리더기가 인식하지 못하는 케이스 다수 발생
  - warning_log 테이블 활용 x

- 차량 출발/도착/현재 위치 DB에 update하여 벨트와 상호 통신
  - 개발 기간 단축을 위해 블루투스 통신으로만 차량 제어, 와이파이 연계하지 못함
  - car 테이블, car_log 테이블 활용 x

## 5. 실행
- 라이브러리 설치
```
pip install -r requirements.txt
```
  - Conveyer_Belt/requirements.txt 파일을 사용합니다.
  - db property 파일 설정: DB 접속은 config.ini 파일로 설정했습니다. git에 연동하지 않았으므로, 다음과 같은 형태로 생성이 필요합니다.
```
[dev]
host = 
port = 
user = 
password = 
database = 
```
- ini 파일이 가리키는 데이터베이스에 접속 후, Conveyer_Belt/create_and_init.sql 파일을 사용합니다.
```
source create_and_init.sql
```
- 파일명이나 경로, 형식을 수정한다면 Conveyer_Belt/src/DB.py 파일도 수정이 필요합니다.

## 6. 시연 영상
<p align=center>
  <a href="https://youtu.be/QK5B_ghezHc?feature=shared">
    <img src="https://i.ytimg.com/vi/QK5B_ghezHc/maxresdefault.jpg" width="40%">
  </a>
  <br>
  <a href="https://youtu.be/QK5B_ghezHc?feature=shared">데모 영상 보러 가기</a>
</p>

## 7. 참고자료
- 기술문서
  - PyQt5: https://lastminuteengineers.com/how-rfid-works-rc522-arduino-tutorial/
  - Arduino: https://www.arduino.cc/reference/en/
  - pySerial: https://pyserial.readthedocs.io/en/latest/

- 그외
  - 분류기: https://youtu.be/lV08Ol6wmts?feature=shared
  - 주행 로봇: https://youtu.be/Y7B1dHH443A?feature=shared
  - RFID: https://lastminuteengineers.com/how-rfid-works-rc522-arduino-tutorial/

## License
 
Copyright (c) 2023 Haneol Kang, Sohee Kang, Yun Oh, Taesang Cho, Seungjun Han

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
