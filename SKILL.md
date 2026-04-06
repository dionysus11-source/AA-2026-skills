---
name: pdf-to-md
description: PDF를 Markdown으로 변환합니다. PDF 문서를 텍스트 기반의 Markdown 파일로 변환할 때 사용합니다. 텍스트와 이미지를 모두 추출합니다. PDF 파일을 Markdown으로 바꾸기, PDF에서 텍스트 추출, PDF를 마크다운으로 변환, PDF 문서를 텍스트 파일로 변환, PDF 내용을 추출, 보고서를 문서화 등의 요청에 자동으로 활성화됩니다.
---

# PDF to Markdown 변환기

이 스킬은 PDF 문서를 Markdown 형식으로 변환합니다. 텍스트, 이미지, 표, 리스트 등의 구조를 유지하면서 변환합니다.

## 주요 기능

- ✅ 텍스트 추출 (한글, 영문 지원)
- ✅ 이미지 추출 및 자동 참조
- ✅ 표, 리스트, 헤딩 구조 유지
- ✅ OCR 지원 (스캔한 PDF)
- ✅ 고해상도 이미지 추출 (300 DPI)

## 변환 방법

이 스킬은 Python 스크립트를 사용하여 PDF를 변환합니다. `scripts/pdf_to_markdown.py` 스크립트를 사용하세요.

### 스크립트 사용법

```bash
python scripts/pdf_to_markdown.py <input.pdf> [output.md] [--no-images]
```

- `input.pdf`: 변환할 PDF 파일 경로 (필수)
- `output.md`: 출력 Markdown 파일 경로 (선택, 기본값: input 파일명.md)
- `--no-images`: 이미지 추출 비활성화 (선택, 기본값: 이미지 추출)

### 의존성 설치

다음 Python 라이브러리 중 하나가 필요합니다:

```bash
# 추천 (이미지 추출 지원)
pip install pymupdf4llm

# 또는 다른 라이브러리
pip install pdfplumber
pip install PyMuPDF
```

### 출력 구조

변환 후 다음 파일들이 생성됩니다:

```
input.md           # 변환된 Markdown 파일
images/            # 추출된 이미지 폴더
  ├── input.pdf-0001-01.png
  ├── input.pdf-0002-03.png
  └── ...
```

Markdown 파일에서 이미지는 다음과 같이 참조됩니다:

```markdown
![](images/input.pdf-0001-01.png)
```

### 예제 스크립트

스크립트는 다음 기능을 구현해야 합니다:

1. **텍스트 추출**: PDF의 각 페이지에서 텍스트를 추출
2. **이미지 추출**: PDF 내 이미지를 PNG 파일로 저장
3. **구조 유지**:
   - 제목/헤더를 Markdown 헤딩(#, ##, ###)으로 변환
   - 표를 Markdown 테이블 문법으로 변환
   - 리스트(ul/ol)를 Markdown 리스트로 변환
   - 문단 구조를 유지
4. **자동 참조**: Markdown에서 이미지를 자동으로 참조

## 사용자 요청 처리

사용자가 PDF 변환을 요청하면:

1. **입력 파일 확인**: 사용자가 PDF 파일 경로를 제공했는지 확인
2. **출력 파일 결정**:
   - 사용자가 출력 경로를 지정했으면 그 경로 사용
   - 아니면 입력 파일명과 같은 이름의 .md 파일 생성
3. **스크립트 실행**: `scripts/pdf_to_markdown.py` 실행
4. **결과 보고**: 변환이 완료되면 출력 파일 경로와 이미지 개수를 알림

## 일반적인 사용 시나리오

- "이 PDF를 Markdown으로 변환해줘"
- "보고서.pdf를 텍스트 파일로 변환해줘"
- "PDF 내용을 추출해서 .md 파일로 만들어줘"
- "문서.pdf를 마크다운 형식으로 변환하고 싶어"
- "이 PDF의 내용을 정리해줘"
- "보고서를 문서화해서 공유 가능하게 만들어줘"

## 주의사항

- pymupdf4llm을 사용하면 최상의 결과를 얻을 수 있습니다
- 이미지는 PNG 형식으로 추출됩니다 (300 DPI)
- 스캔한 PDF는 OCR을 사용하여 텍스트를 추출합니다
- 한글 및 다국어 텍스트를 완벽하게 지원합니다
- 복잡한 레이아웃의 경우 구조가 완벽하게 유지되지 않을 수 있습니다
