"""Initial single-instructor course catalog and idempotent database seeding."""

import json
import sqlite3


INSTRUCTOR = "AI Academy"

SEED_COURSES = (
    {
        "id": 1,
        "title": "파이썬으로 시작하는 데이터 분석",
        "subtitle": "기초 문법부터 실전 데이터 리포트까지",
        "description": "파이썬과 pandas를 활용해 데이터를 정리하고 시각화하는 과정을 배웁니다.",
        "category": "데이터 분석",
        "level": "입문",
        "price": 39000,
        "thumbnail_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
        "instructor": INSTRUCTOR,
        "rating": 4.8,
        "student_count": 1820,
        "total_lectures": 6,
        "total_duration_minutes": 116,
        "curriculum": [
            {"section": "분석 환경과 파이썬 기초", "lectures": [
                {"title": "분석 환경 준비하기", "duration_minutes": 12},
                {"title": "변수와 자료형 익히기", "duration_minutes": 18},
            ]},
            {"section": "pandas로 데이터 다루기", "lectures": [
                {"title": "DataFrame 읽고 살펴보기", "duration_minutes": 20},
                {"title": "결측치와 데이터 정리", "duration_minutes": 22},
            ]},
            {"section": "시각화와 미니 프로젝트", "lectures": [
                {"title": "차트로 인사이트 표현하기", "duration_minutes": 19},
                {"title": "리포트 완성하기", "duration_minutes": 25},
            ]},
        ],
    },
    {
        "id": 2,
        "title": "실무자를 위한 생성형 AI와 프롬프트",
        "subtitle": "생성형 AI의 원리와 업무 자동화 활용법",
        "description": "생성형 AI의 핵심 개념을 익히고 명확한 프롬프트를 설계해 반복 업무에 적용합니다.",
        "category": "AI·머신러닝",
        "level": "입문",
        "price": 45000,
        "thumbnail_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80",
        "instructor": INSTRUCTOR,
        "rating": 4.9,
        "student_count": 2450,
        "total_lectures": 4,
        "total_duration_minutes": 81,
        "curriculum": [
            {"section": "생성형 AI 이해하기", "lectures": [
                {"title": "생성형 AI와 언어 모델", "duration_minutes": 16},
                {"title": "좋은 프롬프트의 구조", "duration_minutes": 21},
            ]},
            {"section": "업무에 적용하기", "lectures": [
                {"title": "문서와 아이디어 작업 자동화", "duration_minutes": 20},
                {"title": "나만의 업무 프롬프트 만들기", "duration_minutes": 24},
            ]},
        ],
    },
    {
        "id": 3,
        "title": "FastAPI로 만드는 파이썬 백엔드",
        "subtitle": "REST API 설계부터 SQLite 연동까지",
        "description": "FastAPI와 SQLite로 검증, 데이터 저장, 오류 응답을 갖춘 백엔드 서비스를 완성합니다.",
        "category": "백엔드 개발",
        "level": "중급",
        "price": 59000,
        "thumbnail_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=900&q=80",
        "instructor": INSTRUCTOR,
        "rating": 4.7,
        "student_count": 960,
        "total_lectures": 6,
        "total_duration_minutes": 133,
        "curriculum": [
            {"section": "FastAPI 핵심", "lectures": [
                {"title": "프로젝트와 첫 번째 엔드포인트", "duration_minutes": 18},
                {"title": "요청 검증과 응답 모델", "duration_minutes": 23},
            ]},
            {"section": "데이터베이스와 API", "lectures": [
                {"title": "SQLite 연결과 CRUD", "duration_minutes": 26},
                {"title": "페이지네이션과 필터링", "duration_minutes": 20},
            ]},
            {"section": "서비스 마무리", "lectures": [
                {"title": "예외 처리와 설정 관리", "duration_minutes": 22},
                {"title": "API 문서와 배포 준비", "duration_minutes": 24},
            ]},
        ],
    },
    {
        "id": 4,
        "title": "머신러닝 첫걸음: 예측 모델 만들기",
        "subtitle": "scikit-learn으로 배우는 모델링의 전 과정",
        "description": "데이터 전처리와 모델 평가를 익히고 실제 예측 문제를 단계별로 해결합니다.",
        "category": "AI·머신러닝",
        "level": "중급",
        "price": 55000,
        "thumbnail_url": "https://images.unsplash.com/photo-1527474305487-b87b222841cc?auto=format&fit=crop&w=900&q=80",
        "instructor": INSTRUCTOR,
        "rating": 4.8,
        "student_count": 1340,
        "total_lectures": 4,
        "total_duration_minutes": 84,
        "curriculum": [
            {"section": "머신러닝 워크플로", "lectures": [
                {"title": "문제 정의와 데이터 분리", "duration_minutes": 18},
                {"title": "전처리 파이프라인 구성", "duration_minutes": 24},
            ]},
            {"section": "학습과 평가", "lectures": [
                {"title": "분류 모델 학습하기", "duration_minutes": 22},
                {"title": "지표로 모델 비교하기", "duration_minutes": 20},
            ]},
        ],
    },
    {
        "id": 5,
        "title": "HTML·CSS·JavaScript 웹 개발 입문",
        "subtitle": "브라우저에서 동작하는 첫 웹 프로젝트",
        "description": "웹의 기본 구조부터 반응형 레이아웃과 인터랙션까지 직접 구현해 봅니다.",
        "category": "프론트엔드 개발",
        "level": "입문",
        "price": 35000,
        "thumbnail_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80",
        "instructor": INSTRUCTOR,
        "rating": 4.6,
        "student_count": 2110,
        "total_lectures": 4,
        "total_duration_minutes": 83,
        "curriculum": [
            {"section": "웹 페이지의 뼈대", "lectures": [
                {"title": "HTML 문서 구조 만들기", "duration_minutes": 17},
                {"title": "의미 있는 요소와 접근성", "duration_minutes": 20},
            ]},
            {"section": "스타일과 인터랙션", "lectures": [
                {"title": "Flexbox와 반응형 레이아웃", "duration_minutes": 24},
                {"title": "JavaScript로 메뉴 만들기", "duration_minutes": 22},
            ]},
        ],
    },
    {
        "id": 6,
        "title": "SQL로 배우는 데이터베이스 실전",
        "subtitle": "조회부터 조인과 집계까지 한 번에",
        "description": "실무에서 자주 쓰는 SQL을 익히고 데이터를 정확하게 조회하고 요약하는 법을 배웁니다.",
        "category": "데이터 분석",
        "level": "입문",
        "price": 32000,
        "thumbnail_url": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?auto=format&fit=crop&w=900&q=80",
        "instructor": INSTRUCTOR,
        "rating": 4.7,
        "student_count": 1560,
        "total_lectures": 4,
        "total_duration_minutes": 78,
        "curriculum": [
            {"section": "SQL 조회 기초", "lectures": [
                {"title": "테이블과 SELECT 문", "duration_minutes": 15},
                {"title": "조건과 정렬 활용하기", "duration_minutes": 18},
            ]},
            {"section": "실무 쿼리 작성", "lectures": [
                {"title": "JOIN으로 테이블 연결하기", "duration_minutes": 24},
                {"title": "GROUP BY와 집계 함수", "duration_minutes": 21},
            ]},
        ],
    },
)


def seed_courses(connection: sqlite3.Connection) -> None:
    """Insert starter courses once, preserving edits to existing catalog rows."""
    connection.executemany(
        """INSERT OR IGNORE INTO courses (
            id, title, subtitle, description, category, level, price, thumbnail_url,
            instructor, rating, student_count, total_lectures,
            total_duration_minutes, curriculum
        ) VALUES (
            :id, :title, :subtitle, :description, :category, :level, :price, :thumbnail_url,
            :instructor, :rating, :student_count, :total_lectures,
            :total_duration_minutes, :curriculum
        )""",
        [
            {
                **{key: value for key, value in course.items() if key != "curriculum"},
                "curriculum": json.dumps(course["curriculum"], ensure_ascii=False),
            }
            for course in SEED_COURSES
        ],
    )
