# airklassmissions
Quriously AIR KLASS Python/Django 백엔드 개발자 - 과제 전형

### 배포 주소 ~~[GoTo]~~ ▶ 현재 비용 문제로 인해 내려둔 상태입니다.

### 진행사항 확인 ~~[GoTo]~~
- 요구사항 분석, 관련 정보 및 프로젝트 상세 진행사항 기록을 위해 사용

## 과제 해석
서비스를 사용할 수 있는 권한이 있는 client에게 강의를 등록하고 해당 강의에 대한 질문 및 답변을 등록할 수 있는 기능을 제공하는 서비스라고 해석하였습니다.

## 목차
- [요구사항 구현 범위](#요구사항)
- [기술 스택](#기술-스택)
- [ERD](#erd)
- [API 명세서](#api-명세서)
- [구현 과정](#구현-과정)
- [구현 주요 부분](#구현-주요-부분)
- [프로그램 설치 및 실행 방법](#step-to-run)

## 요구사항
> **:pushpin: 체크한 내역으로 구현된 범위를 확인할 수 있습니다.**
- Database
    - [x]  SQLite 사용
    - [x]  REST API 요구사항에 맞는 DB 구성
        - 수강생, 강사, 강의, 질문, 답변 모델 간 관계 구현
- REST API
    - 사용자 API
        - [x]  회원가입, 로그인, 로그아웃
        - [x]  로그인 하지 않은 사용자에 대한 접근 제한
            - 강의 상세내역(질문과 답변 포함) 조회 등 제외
    - 강의 API
        - [x]  강의 생성
            - 강사만 생성 가능
        - [x]  해당 강의에 작성된 질문과 답변 조회
    - 질문 API
        - [x]  강의에 대한 질문 등록
        - [x]  작성한 질문 내역 삭제
            - 답변이 달린 질문일 경우 삭제 불가
    - 답변 API
        - [x]  질문에 대한 답변 등록
            - 해당 강의를 생성한 강사만 등록 가능
        - [x]  작성한 답변 내역 삭제
        - [x]  작성된 질문 내역 삭제
- Implementation
    - 과제 종료일: 2022년 9월 25일 23:59
    - [x]  Python3 + Django + Django REST Framework 사용
    - [x]  정상적인 서버 실행 가능하도록 구현
    - [x]  원격 서버 배포
    - [x]  README.md 작성
        - 서버 실행방법, 구현 스펙, 구현 범위, 과제 구현 과정 등

## 구현

### 기술 스택
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/> <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=SQLite&logoColor=white"/> <img src="https://img.shields.io/badge/PyCharm-000000?style=flat-square&logo=PyCharm&logoColor=white"/> <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=Docker&logoColor=white"/> <img src="https://img.shields.io/badge/AWS EC2-232F3E?style=flat-square&logo=Amazon AWS&logoColor=white"/>

### 개발 기간
* 2022.09.21. - 2022.09.25

> ### ERD
<img src="./source/erd.png" alt="erd">

> ### API 명세서
### ~~[GoTo]~~

> ### 구현 과정
- ViewSet을 이용한 RESTful API 구현
    - 사용자 회원가입, 로그인, 로그아웃 구현
        - simplejwt를 이용해 token을 발행하고 permission customizing을 통한 사용자 접근 권한을 부여하도록 구현했습니다.
    - 사용자 정보 수정 및 삭제 구현
        - 로그인 시 발행된 access_token으로 인증하지 않을 경우 401 error를 리턴합니다.
    - 강사 등록, 조회, 수정, 삭제 구현
        - 로그인 시 발행된 access_token으로 인증하지 않을 경우 401 error를 리턴합니다.
        - 강사 조회 시 사용자 본인이 작성한 내역만 조회할 수 있도록 구현했습니다.
    - 강의 등록, 조회, 수정, 삭제 구현
        - 강의 리스트, 상세 조회 시 인증 여부에 상관없이 조회할 수 있도록 구현했습니다.
        - 강의 상세 조회 시 해당 강의의 수강생 질문, 강사 답변을 함께 조회할 수 있도록 구현했습니다.
        - 강의 등록, 수정, 삭제 시 로그인 시 발행된 access_token으로 인증하지 않고, 사용자가 강사로 등록되지 않은 경우 401 error를 리턴합니다.
    - 질문 등록, 조회, 수정, 삭제 구현
        - 로그인 시 발행된 access_token으로 인증하지 않을 경우 401 error를 리턴합니다.
        - 질문 조회 시 사용자 본인이 작성한 내역만 조회할 수 있도록 구현했습니다.
        - 질문 삭제 시 답변이 등록된 질문일 경우 삭제가 불가하도록 구현했습니다.
        - 질문 삭제 시 인증받은 사용자가 질문이 작성된 강의의 강사일 경우 삭제가 가능하도록 구현했습니다.
    - 답변 등록, 조회, 삭제 구현
        - 로그인 시 발행된 access_token으로 인증하지 않고, 사용자 본인이 등록한 강의의 질문이 아닐 경우 401 error를 리턴합니다.
- Gunigorn, Nginx 적용 및 AWS EC2, Docker 이용한 배포
- Postman을 이용한 API 명세서 작성

> ### 구현 주요 부분
- RESTful API 구현을 위한 uri 및 API Response 구성
    - 리소스 간 관계를 이해하기 쉽게 표현하기 위해 uri를 구성했습니다.
    - API 요청 수행 시 예외가 발생할 수 있는 부분을 예외 처리하여 해당 의미를 담아 API 응답 메세지를 구현했습니다.
    - API 응답으로 처리 상태를 잘 확인할 수 있도록 200, 201, 400, 401, 404 등의 상태 코드를 구분해 API 상태 코드를 구현했습니다.
- permission customizing을 통한 사용자 접근 권한 부여
    - DRF에서 기본적으로 제공하는 permission과 커스텀 permission으로 일반 사용자, 수강생, 강사가 각각 접근할 수 있는 API를 구분해 접근 권한을 부여했습니다.
- Master 객체 생성, 삭제 시 User 객체 강사 여부 업데이트
    - 모델링 초기, User 객체에 `is_master` 필드 값으로 수강생과 강사를 구분하도록 구성했지만, 추후 강사에 대한 데이터나 강사와 관련된 API를 관리하는 확장성을 고려하여 Master 객체를 User 객체와 1:1 관계로 구성했습니다.
    - Master 객체 생성, 삭제 시 User 객체의 `is_master` 필드를 `True`, `False`로 업데이트하여 로그인한 사용자의 정보만으로 강사 여부를 확인할 수 있도록 구현했습니다.
- serializer를 통한 참조 모델 필드 조회
    - serializer relational field를 작성해 참조 모델의 필드를 조회할 수 있도록 구현했습니다.

### Step to run
> window 환경에서 구현 및 실행되었습니다.

#### Local server
1. github에서 해당 프로젝트의 repository를 clone합니다.
```shell
$ git clone https://github.com/Jjenny-K/airklassmissions.git
```

2. 해당 프로젝트의 웹 서버가 실행되는 directory로 이동합니다.
```shell
$ cd airklassmissions
$ cd djangomission
```

3. .env 파일을 root directory에 생성 후, 프로젝트와 연동을 위한 정보를 저장합니다.
```
SECRET_KEY='[SECRET_KEY]'
```

4. 가상환경을 설정한 후 필요한 라이브러리를 설치합니다.
```shell
$ python -m venv venv
$ venv/Scripts/activate
$ python install -r requirements.txt
```

5. model migration을 진행합니다.
```shell
$ python manage.py migrate --settings=djangomission.settings.develop
```

6. local server를 실행합니다.
```shell
$ python manage.py runserver --settings=djangomission.settings.develop
```

#### Docker server
1. github에서 해당 프로젝트의 repository를 clone합니다.
```shell
$ git clone https://github.com/Jjenny-K/airklassmissions.git
```

2. 해당 프로젝트의 웹 서버가 실행되는 directory로 이동합니다.
```shell
$ cd airklassmissions
$ cd djangomission
```

3. .env 파일을 root directory에 생성 후, 프로젝트와 연동을 위한 정보를 저장합니다.
```
SECRET_KEY='[SECRET_KEY]'
```

4. nginx/conf.d/default/conf 파일 내 server_name을 배포용 ip로 변경합니다.

5. docker에 이미지를 만들고 배포를 진행합니다.
```shell
$ sudo docker-compose up -d --build
```

## 작성자
All of development : :monkey_face: **Kang Jeonghui**
