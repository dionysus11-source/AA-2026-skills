# GitHub 배포 가이드

이 스킬은 Claude Code Plugin Marketplace 시스템을 지원합니다. 사용자가 쉽게 설치할 수 있도록 `.claude-plugin/marketplace.json` 파일이 포함되어 있습니다.

## 1. GitHub 리포지토리 생성

1. https://github.com 접속
2. 우측 상단 `+` → `New repository`
3. 다음 정보 입력:
   - **Repository name**: `pdf-to-md-skill`
   - **Description**: `Claude Code용 PDF를 Markdown으로 변환하는 스킬`
   - **Visibility**: `Public` (추천)
   - **Initialize**: 체크하지 않기
4. `Create repository` 클릭

## 2. 로컬에서 Remote 설정 및 Push

GitHub에서 리포지토리를 만든 후, 아래 명령어를 터미널에서 실행하세요:

```bash
cd ~/Desktop/pdf-to-md-skill

# YOUR_USERNAME을 본인의 GitHub 사용자명으로 변경
git remote add origin https://github.com/YOUR_USERNAME/pdf-to-md-skill.git

# 브랜치 이름 설정 (main)
git branch -M main

# GitHub에 push
git push -u origin main
```

## 3. README.md 수정

리포지토리에 push한 후, GitHub 웹사이트에서 README.md를 열고 `YOUR_USERNAME`을 본인의 사용자명으로 변경하세요:

```markdown
git clone https://github.com/YOUR_USERNAME/pdf-to-md-skill.git
```

## 4. 배포 완료 후

사용자들은 두 가지 방법으로 설치할 수 있습니다:

### 방법 1: Marketplace (추천)
Claude Code에서 다음 명령어를 실행:
```
/plugin marketplace add dionysus11-source/AA-2026-skills
/plugin install pdf-to-md@pdf-tools
```

### 방법 2: Git Clone
```bash
git clone https://github.com/dionysus11-source/AA-2026-skills.git
```

상세 사용법은 README.md에 설명되어 있습니다.

## 주의사항

- 첫 push 시 GitHub 로그인이 필요할 수 있습니다
- 2단계 인증을 사용하는 경우 Personal Access Token이 필요할 수 있습니다
