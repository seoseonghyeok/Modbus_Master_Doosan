# Modbus_Master_Doosan
Modbus_Master_Doosan_Robot

# Modbus_Master (Doosan Robot)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📘 프로그램 소개
**Modbus_Master**는 **Modbus TCP 프로토콜**을 사용하여  
두산로봇(Doosan Robot)과 같은 원격 장비의 상태를 실시간으로 모니터링하고  
데이터를 읽고 쓰기할 수 있는 GUI 기반 툴입니다.

---

## ⚙️ 개발 환경
- **언어:** Python  
- **GUI:** PyQt5  
- **빌드:** PyInstaller (exe 변환)  
- **폴더 구조:**
  ```
  Modbus_Master(Doosan).py       # 메인 실행 파일
  qt/                            # UI (.ui) 파일 폴더
  dist/                          # exe 빌드 결과 폴더
  ```

---

## 🚀 실행 방법
### 1️⃣ Python 환경에서 실행
```bash
python Modbus_Master(Doosan).py
```

### 2️⃣ exe 파일로 실행
`dist` 폴더 안의 실행 파일(`Modbus_Master.exe`)을 직접 실행합니다.

---

## 🖥️ UI 구성

<img width="834" height="748" alt="image" src="https://github.com/user-attachments/assets/e9fa075f-593f-4c19-8caa-d61214dc8672" />

| 항목 | 설명 |
|------|------|
| **IP 입력란** | 접속할 Modbus 서버(장비)의 IP 주소 입력 |
| **PORT 입력란** | 접속할 Modbus 서버의 포트 번호 입력 |
| **Connect 버튼** | 서버 접속 시도 |
| **Disconnect 버튼** | 서버 연결 해제 |
| **Close 버튼** | 프로그램 종료 |
| **Read 버튼** | 지정한 주소 범위 데이터를 한 번 읽기 |
| **Write 버튼** | Write 테이블의 데이터를 서버에 쓰기 |
| **Read_Auto 버튼** | 자동 읽기(0.5초 간격) 토글 |
| **Read Table** | 읽어온 데이터 표시 |
| **Write Table** | 쓰기할 데이터 입력 |
| **로봇 상태 표시** | 로봇 상태를 숫자와 텍스트로 표시 |
---

## 📋 사용 방법

### 🔹 1. 서버 접속
1. IP 입력란에 서버 IP 주소 입력 (예: `192.168.0.10`)  
2. PORT 입력란에 포트 번호 입력 (예: `502`)  
3. **Connect** 클릭 → “Connecting” 로그 표시 (녹색)  
4. 로봇 상태가 0.5초 간격으로 자동 업데이트  

### 🔹 2. 서버 연결 해제
- **Disconnect** 클릭 → “Disconnecting” 로그 표시 (빨간색)  
- 버튼 및 테이블 비활성화  

### 🔹 3. 데이터 읽기
- 주소 범위 선택 → **Read 버튼** 클릭 → 테이블에 데이터 표시  

### 🔹 4. 자동 읽기
- **Auto 토글** ON → 0.5초마다 데이터 자동 갱신  
- 다시 클릭 시 OFF  

### 🔹 5. 데이터 쓰기
- Write 주소 범위 설정 → 테이블 자동 생성  
- 값 입력 후 **Write 버튼** 클릭 → 서버에 전송  

### 🔹 6. 프로그램 종료
- **Close 버튼** 클릭 시 연결 해제 후 프로그램 종료  

---

## 🧠 참고 사항
- IP/Port 미입력 시 **경고 메시지** 표시  
- 서버 미연결 상태에서 읽기/쓰기 시 **오류 메시지** 발생  
- 자동 읽기 중에는 연결이 유지되어야 함  
- 종료 전 **반드시 Disconnect 버튼으로 연결 해제**  

---

## 🧩 문제 해결 (Troubleshooting)
| 문제 상황 | 해결 방법 |
|------------|------------|
| 서버 연결 불가 | IP와 Port 번호를 확인 |
| 읽기/쓰기 오류 | 서버 상태 및 네트워크 점검 |
| UI 멈춤/비정상 작동 | 프로그램 재실행 |

---

## 🏷️ 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다.  
자유롭게 수정 및 배포할 수 있습니다.

---

## 👨‍💻 제작자
**Developer:** [SeongHyeok]  
**Email:** [https://github.com/seoseonghyeok]
