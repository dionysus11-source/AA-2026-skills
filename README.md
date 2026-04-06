# PDF to Markdown Converter Skill

Claude Code용 PDF를 Markdown으로 변환하는 스킬입니다. PDF 문서의 텍스트와 이미지를 추출하여 Markdown 파일로 변환합니다.

## 주요 기능

- ✅ **텍스트 추출**: 한글, 영문 텍스트 추출
- ✅ **구조 유지**: 표, 리스트, 헤딩 구조 보존
- ✅ **이미지 추출**: PDF 내 이미지를 PNG 파일로 저장
- ✅ **자동 참조**: Markdown에서 이미지를 자동으로 참조
- ✅ **OCR 지원**: 스캔한 PDF도 처리 가능

## 설치 방법

### 방법 1: Claude Code Plugin Marketplace (추천)

```bash
# 1. Marketplace 추가
claude plugin marketplace add YOUR_USERNAME/pdf-to-md-skill

# 2. 스킬 설치
claude plugin install pdf-to-md@pdf-tools

# 3. 의존성 설치
python3 -m venv ~/.claude/venv
source ~/.claude/venv/bin/activate  # Windows: ~/.claude/venv\\Scripts\\activate
pip install pymupdf4llm
```

### 방법 2: 수동 설치

```bash
# 1. 리포지토리 클론
git clone https://github.com/YOUR_USERNAME/pdf-to-md-skill.git
cd pdf-to-md-skill

# 2. Claude Code 스킬 디렉토리로 복사
# macOS/Linux
cp -r . ~/.claude/skills/pdf-to-md

# Windows
xcopy /E /I . %USERPROFILE%\.claude\skills\pdf-to-md

# 3. 의존성 설치

```bash
# 가상 환경 생성 (권장)
python3 -m venv ~/.claude/venv
source ~/.claude/venv/bin/activate  # Windows: ~/.claude/venv\\Scripts\\activate

# PyMuPDF4LLM 설치
pip install pymupdf4llm

# 또는 다른 라이브러리
# pip install pdfplumber
# pip install PyMuPDF
```

## 사용 방법

Claude Code에서 다음과 같이 요청하면 자동으로 스킬이 실행됩니다:

```
"이 PDF를 Markdown으로 변환해줘"
"PDF 파일을 마크다운으로 바꿔줘"
"문서.pdf를 텍스트 파일로 변환해줘"
```

### 수동 사용

```bash
python scripts/pdf_to_markdown.py input.pdf [output.md]
```

## 옵션

- `--no-images`: 이미지를 추출하지 않고 텍스트만 변환
- 기본적으로 이미지를 추출하고 `images/` 폴더에 저장

## 예시

```bash
# 기본 사용 (이미지 추출 포함)
python scripts/pdf_to_markdown.py document.pdf

# 출력 파일 지정
python scripts/pdf_to_markdown.py input.pdf output.md

# 텍스트만 추출
python scripts/pdf_to_markdown.py document.pdf --no-images
```

## 지원되는 PDF 형식

- 텍스트 기반 PDF (일반 문서, 보고서, 논문 등)
- 스캔한 PDF (OCR 사용)
- 한글/영문 혼합 문서

## 결과물

변환 후 다음 파일들이 생성됩니다:

```
input.md           # 변환된 Markdown 파일
images/            # 추출된 이미지 폴더
  ├── input.pdf-0001-01.png
  ├── input.pdf-0002-03.png
  └── ...
```

## 요구사항

- Python 3.8+
- PyMuPDF4LLM (또는 pdfplumber, PyMuPDF)
- Claude Code

## 라이선스

MIT License

## 기여

이 프로젝트에 기여하고 싶으시다면 Pull Request를 제출해주세요!

## 문제 보고

버그나 기능 요청은 [Issues](https://github.com/YOUR_USERNAME/pdf-to-md-skill/issues)에 등록해주세요.

## 참고

이 스킬은 Claude Code의 스킬 시스템을 사용하여 자동으로 트리거됩니다. PDF 변환이 필요한 작업을 요청하면 Claude가 자동으로 이 스킬을 사용합니다.
