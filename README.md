# PIRO Q&A 시스템

> 세션 질문이 묻히지 않는 구조화된 Q&A 플랫폼

## 📋 프로젝트 개요

피로그래밍 세션 중 질문이 몰릴 때 질문이 묻히는 문제를 해결하기 위한 Q&A 시스템입니다.
- 질문 카드 형식으로 관리
- 세션/과제별 카테고리 분류
- 해결/미해결 체크리스트 기능
- 운영진 대시보드로 미답변 질문 관리

## 🚀 시작하기

### 환경 설정

1. **가상환경 생성 및 활성화**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

2. **의존성 설치**
```bash
pip install django
```

3. **데이터베이스 마이그레이션**
```bash
python manage.py migrate
```

4. **관리자 계정 생성**
```bash
python manage.py createsuperuser
```

5. **서버 실행**
```bash
python manage.py runserver
```

6. **초기 데이터 설정**
- `http://127.0.0.1:8000/admin` 접속
- Category(카테고리) 추가: 세션명, 과제명 등

## 📁 프로젝트 구조

```
hackathon_pirostack/
├── hackathon/          # 메인 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── questions/          # Q&A 앱
│   ├── models.py      # Category, Question, Answer 모델
│   ├── views.py       # 뷰 로직
│   ├── forms.py       # Django Forms
│   ├── urls.py        # URL 라우팅
│   ├── admin.py       # 관리자 페이지 설정
│   └── templates/     # HTML 템플릿
├── templates/          # 공통 템플릿
│   └── base.html      # 기본 레이아웃
├── manage.py
└── README.md
```

## 🎨 디자인 시스템

### 컬러 팔레트
- **Primary Green**: `#059212` (네비게이션)
- **Bright Green**: `#06D001` (버튼 기본)
- **Lime**: `#9BEC00` (버튼 호버)
- **Black**: `#000000` (텍스트)
- **White**: `#ffffff` (배경)

### 타이포그래피
- **폰트**: Pretendard Variable
- **Line height**: 140%
- **Letter spacing**: -2.5%

## 📊 데이터베이스 모델

### Category (카테고리)
- 세션명 또는 과제명
- `name`: 카테고리 이름
- `category_type`: 'session' 또는 'assignment'

### Question (질문)
- `category`: 카테고리 (FK)
- `title`: 질문 제목
- `content`: 질문 내용
- `is_resolved`: 해결 여부 (체크박스 기능)
- `is_anonymous`: 익명 여부 (기본: True)
- `created_at`: 작성 시간

### Answer (답변)
- `question`: 질문 (FK)
- `content`: 답변 내용
- `is_staff`: 운영진 답변 여부
- `is_anonymous`: 익명 여부
- `created_at`: 작성 시간

## 🔗 주요 URL

| URL | 설명 |
|-----|------|
| `/` | 메인 페이지 (질문 목록으로 리다이렉트) |
| `/questions/` | 전체 질문 목록 |
| `/questions/create/` | 질문 작성 |
| `/questions/<id>/` | 질문 상세 |
| `/questions/category/<id>/` | 카테고리별 질문 목록 |
| `/questions/staff/` | 미답변 질문 목록 (운영진) |
| `/admin/` | 관리자 페이지 |

## 👥 팀 역할 분담

### 1. [이영주] 질문 및 답변 코어 (Questions & Interaction)

가장 핵심이 되는 CRUD와 질문 상태 관리를 담당합니다.

**담당 API:**
- ✅ **질문 관리 API**: 질문 생성(업로드), 수정, 삭제, 상세 조회
- ✅ **답변 및 꼬리질문 API**: 답변 등록 및 답변에 대한 대댓글(꼬리질문) 기능
- ✅ **해결 상태 체크**: `is_resolved` 필드를 활용해 질문의 완료 유무 토글 API
- 🔲 **찜하기(Scrap) API**: 특정 질문을 내 보관함에 추가/삭제하는 기능

**현재 구현된 기능:**
- `question_list()`: 전체 질문 목록 조회
- `question_detail()`: 질문 상세 및 답변 조회
- `question_create()`: QuestionForm을 사용한 질문 작성
- `answer_create()`: AnswerForm을 사용한 답변 작성
- `question_resolve()`: 해결/미해결 토글

**TODO:**
- [ ] 질문 수정/삭제 API 구현
- [ ] 꼬리질문(대댓글) 기능 구현
- [ ] 찜하기 모델 및 API 구현

---

### 2. [이서현] 정렬 및 사용자 홈 (User Home & Filtering)

데이터를 필터링하고 사용자가 보기 편하게 가공하는 역할을 담당합니다.

**담당 API:**
- 🔲 **커스텀 정렬 API**: 세션별, 과제별, 시간순 정렬 필터링
- 🔲 **사용자 마이페이지 API**:
    - 내가 찜한 질문 리스트
    - 내가 작성한 질문 리스트
- 🔲 **FAQ API**: 자주 묻는 질문 고정 리스트 제공
- 🔲 **검색 API**: 키워드 기반 질문 검색

**TODO:**
- [ ] 정렬/필터링 쿼리셋 구현
- [ ] 마이페이지 뷰 및 URL 추가
- [ ] FAQ 모델 및 API 구현
- [ ] 검색 기능 구현 (Q 객체 활용)

---

### 3. [김서윤] 운영진 대시보드 (Admin)

운영진 전용 기능과 관리자 도구를 담당합니다.

**담당 API:**
- 🔲 **운영진 홈 API**:
    - `is_answered=False`인 질문만 필터링해서 보여주는 미응답 질문 리스트
    - 전체 질문 통계 (오늘 올라온 질문 수 등)
- 🔲 **권한 필터**: 일반 유저가 운영진 API에 접근하지 못하도록 하는 Permission 클래스 구현
- 🔲 **카테고리 관리 API**: 세션명이나 과제 카테고리 생성/수정/삭제 (운영진 전용)

**현재 구현된 기능:**
- `staff_unanswered()`: 미답변 질문 목록 뷰 (기본 구현)

**TODO:**
- [ ] 운영진 대시보드 통계 기능
- [ ] Permission 클래스 구현
- [ ] 카테고리 CRUD API 구현
- [ ] 운영진 전용 템플릿 개선

---

## 🛠 개발 가이드

### 새로운 기능 추가하기

1. **모델 수정 시**
```bash
python manage.py makemigrations
python manage.py migrate
```

2. **뷰 추가 시**
- `questions/views.py`에 함수 추가
- `questions/urls.py`에 URL 패턴 추가
- `questions/templates/questions/`에 템플릿 추가

3. **관리자 페이지 설정**
- `questions/admin.py`에서 모델 등록

### 코드 스타일
- Django 컨벤션 준수
- Docstring 작성 (함수 설명)
- 의미 있는 변수명 사용

## 📝 Git 커밋 컨벤션

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 코드
chore: 빌드 업무, 패키지 관리
```

## 🤝 기여하기

1. 본인 브랜치 생성: `git checkout -b feature/기능명`
2. 변경사항 커밋: `git commit -m 'feat: 기능 추가'`
3. 브랜치에 푸시: `git push origin feature/기능명`
4. Pull Request 생성

## 📞 문의

프로젝트 관련 문의사항은 팀 채널로 연락주세요!

---

**Built with Django 6.0 & Pretendard Font** 💚
