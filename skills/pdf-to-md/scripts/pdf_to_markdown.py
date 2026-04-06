#!/usr/bin/env python3
"""
PDF to Markdown Converter

이 스크립트는 PDF 파일을 Markdown 형식으로 변환합니다.
텍스트 기반 PDF의 텍스트, 표, 리스트 등의 구조를 유지하며 변환합니다.
"""

import sys
import os
from pathlib import Path
import re

def clean_markdown_text(text):
    """마크다운 텍스트에서 불필요한 OCR 아티팩트를 제거합니다."""
    lines = text.split('\n')
    cleaned_lines = []
    skip_until_marker = False

    for line in lines:
        # Start/End 마커 제거
        if '----- Start of picture text -----' in line or '----- End of picture text -----' in line:
            continue

        # 다른 불필요한 패턴들도 제거 (필요시 추가)
        # 예: 이미지 설명 텍스트, 페이지 번호 등
        if re.match(r'^\s*-+\s*(Start|End)\s+of\s+\w+\s*-+\s*$', line):
            continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

def check_dependencies():
    """필요한 라이브러리가 있는지 확인하고 적절한 것을 반환합니다."""
    try:
        import pymupdf4llm
        return "pymupdf4llm"
    except ImportError:
        pass

    try:
        import pdfplumber
        return "pdfplumber"
    except ImportError:
        pass

    try:
        import fitz  # PyMuPDF
        return "pymupdf"
    except ImportError:
        pass

    return None

def convert_with_pymupdf4llm(pdf_path, md_path, extract_images=False):
    """pymupdf4llm을 사용하여 PDF를 Markdown으로 변환 (가장 추천)"""
    try:
        import pymupdf4llm
        import pymupdf  # fitz
        import os

        # 이미지 추출 옵션 설정
        if extract_images:
            # PDF 파일이 있는 디렉토리로 이동
            pdf_dir = Path(pdf_path).parent.resolve()
            original_cwd = os.getcwd()

            try:
                os.chdir(pdf_dir)

                # 이미지를 저장할 디렉토리 생성 (현재 작업 디렉토리 기준)
                images_dir = Path("images").resolve()

                # 이미지 디렉토리가 없으면 생성
                if not images_dir.exists():
                    images_dir.mkdir(parents=True, exist_ok=True)
                    print(f"이미지 디렉토리 생성: {images_dir}")

                # 이미지 추출 enabled로 변환
                md_text = pymupdf4llm.to_markdown(
                    pdf_path,
                    write_images=True,
                    image_path=str(images_dir),  # 현재 디렉토리 기준 경로
                    image_format="png",
                    dpi=300
                )
            finally:
                # 원래 디렉토리로 복귀
                os.chdir(original_cwd)
        else:
            # 텍스트만 추출
            md_text = pymupdf4llm.to_markdown(pdf_path)
            images_dir = None

        # 불필요한 텍스트 제거 (OCR 아티팩트 등)
        md_text = clean_markdown_text(md_text)

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_text)

        if extract_images and images_dir:
            # 생성된 이미지 파일 개수 확인
            image_files = list(images_dir.glob("*.png")) + list(images_dir.glob("*.jpg"))
            print(f"✓ {len(image_files)}개의 이미지가 {images_dir} 디렉토리에 저장되었습니다")

        return True
    except Exception as e:
        print(f"pymupdf4llm 변환 오류: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

def convert_with_pdfplumber(pdf_path, md_path):
    """pdfplumber를 사용하여 PDF를 Markdown으로 변환 (표 추출에 강점)"""
    try:
        import pdfplumber

        markdown_lines = []

        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # 페이지 구분자
                if page_num > 1:
                    markdown_lines.append("")
                    markdown_lines.append("---")
                    markdown_lines.append("")

                # 표 추출
                tables = page.find_tables()
                table_bboxes = [table.bbox for table in tables]

                # 텍스트와 표 처리
                if not tables:
                    # 표가 없으면 전체 텍스트 추출
                    text = page.extract_text()
                    if text:
                        lines = text.split('\n')
                        markdown_lines.extend(lines)
                else:
                    # 표가 있으면 텍스트와 표를 혼합 처리
                    # (간단한 구현: 표 위주로 처리)
                    for i, table in enumerate(tables):
                        # 표 데이터 추출
                        df = table.extract()
                        if df:
                            # Markdown 테이블 생성
                            if len(df) > 0:
                                # 헤더
                                header = "| " + " | ".join(str(cell) if cell else "" for cell in df[0]) + " |"
                                separator = "|" + "|".join(["---"] * len(df[0])) + "|"
                                markdown_lines.append(header)
                                markdown_lines.append(separator)

                                # 데이터 행
                                for row in df[1:]:
                                    row_text = "| " + " | ".join(str(cell) if cell else "" for cell in row) + " |"
                                    markdown_lines.append(row_text)

                        markdown_lines.append("")

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_lines))

        return True
    except Exception as e:
        print(f"pdfplumber 변환 오류: {e}", file=sys.stderr)
        return False

def convert_with_pymupdf(pdf_path, md_path):
    """PyMuPDF(fitz)를 사용하여 PDF를 Markdown으로 변환 (기본)"""
    try:
        import fitz

        doc = fitz.open(pdf_path)
        markdown_lines = []

        for page_num, page in enumerate(doc, 1):
            # 페이지 구분자
            if page_num > 1:
                markdown_lines.append("")
                markdown_lines.append(f"## 페이지 {page_num}")
                markdown_lines.append("")

            # 텍스트 블록 추출
            blocks = page.get_text("dict")["blocks"]

            for block in blocks:
                if block["type"] == 0:  # 텍스트 블록
                    # 폰트 정보를 확인하여 헤딩 감지
                    for line in block["lines"]:
                        if not line["spans"]:
                            continue

                        # 라인의 텍스트 추출
                        line_text = " ".join(span["text"] for span in line["spans"])

                        if not line_text.strip():
                            continue

                        # 첫 번째 span의 폰트 크기로 헤딩 레벨 결정
                        font_size = line["spans"][0]["size"]
                        font_flags = line["spans"][0]["flags"]

                        # 폰트 굵기에 따른 헤딩 결정
                        if font_flags & 2**4:  # bold
                            if font_size >= 20:
                                line_text = f"# {line_text}"
                            elif font_size >= 16:
                                line_text = f"## {line_text}"
                            elif font_size >= 14:
                                line_text = f"### {line_text}"

                        markdown_lines.append(line_text)
                    markdown_lines.append("")  # 문단 사이 빈 줄

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_lines))

        doc.close()
        return True

    except Exception as e:
        print(f"PyMuPDF 변환 오류: {e}", file=sys.stderr)
        return False

def pdf_to_markdown(pdf_path, md_path=None, extract_images=True):
    """PDF를 Markdown으로 변환하는 메인 함수"""

    # 입력 파일 확인
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"오류: PDF 파일을 찾을 수 없습니다: {pdf_path}", file=sys.stderr)
        return False

    if not pdf_path.suffix.lower() == '.pdf':
        print(f"오류: PDF 파일이 아닙니다: {pdf_path}", file=sys.stderr)
        return False

    # 출력 경로 결정
    if md_path is None:
        md_path = pdf_path.with_suffix('.md')
    else:
        md_path = Path(md_path)

    # 사용 가능한 라이브러리 확인 및 변환
    library = check_dependencies()

    if library == "pymupdf4llm":
        print("pymupdf4llm을 사용하여 변환합니다...")
        if extract_images:
            print("이미지 추출 모드: 활성화")
        success = convert_with_pymupdf4llm(str(pdf_path), str(md_path), extract_images)
    elif library == "pdfplumber":
        print("pdfplumber를 사용하여 변환합니다...")
        success = convert_with_pdfplumber(str(pdf_path), str(md_path))
    elif library == "pymupdf":
        print("PyMuPDF를 사용하여 변환합니다...")
        success = convert_with_pymupdf(str(pdf_path), str(md_path))
    else:
        print("오류: PDF 변환을 위한 라이브러리를 찾을 수 없습니다.", file=sys.stderr)
        print("다음 중 하나를 설치해주세요:", file=sys.stderr)
        print("  pip install pymupdf4llm      (추천)", file=sys.stderr)
        print("  pip install pdfplumber", file=sys.stderr)
        print("  pip install PyMuPDF", file=sys.stderr)
        return False

    if success:
        print(f"✓ 변환 완료: {md_path}")
        return True
    else:
        print(f"✗ 변환 실패", file=sys.stderr)
        return False

def main():
    if len(sys.argv) < 2:
        print("사용법: python pdf_to_markdown.py <input.pdf> [output.md] [--no-images]")
        print("")
        print("옵션:")
        print("  --no-images    이미지를 추출하지 않고 텍스트만 변환 (기본: 이미지 추출)")
        print("")
        print("예시:")
        print("  python pdf_to_markdown.py document.pdf")
        print("  python pdf_to_markdown.py document.md (document.pdf로 변환)")
        print("  python pdf_to_markdown.py input.pdf output.md")
        print("  python pdf_to_markdown.py input.pdf output.md --no-images")
        sys.exit(1)

    pdf_path = sys.argv[1]
    md_path = None
    extract_images = True  # 기본적으로 이미지 추출

    # 인자 파싱
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--no-images":
            extract_images = False
        elif not sys.argv[i].startswith("--"):
            md_path = sys.argv[i]
        i += 1

    if pdf_to_markdown(pdf_path, md_path, extract_images):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
