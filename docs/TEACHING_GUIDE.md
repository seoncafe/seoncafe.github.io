# Teaching 페이지 관리 방법

이 저장소의 최상위 폴더에서 아래 명령을 실행합니다. Python 3.9 이상만 필요하며, 추가 패키지를 설치할 필요는 없습니다.

```sh
cd /Users/kiseon/GitHub/seoncafe.github.io
```

현재 **Exoplanetary Atmospheres (Fall, 2026)**와 앞으로 추가하는 과목은 이 방식으로 관리합니다. 기존의 지난 학기 자료는 `Teaching.html`에 그대로 보존되어 있습니다.

## 관리 파일

```text
Teaching_files/
  2026b_ExoAtm/
    course.json          # 과목명·학기·시간·장소·참고문헌
    lectures.csv         # 강의별 날짜·시간·제목·PDF·업데이트 날짜
    .pdf-hashes.json     # PDF 링크 버전 관리용; 자동 생성, 직접 수정하지 않음
    ExoAtm_lecture01.pdf
scripts/
  update_teaching.py     # CSV와 과목 정보를 Teaching.html에 반영
```

`Teaching.html`의 `BEGIN MANAGED COURSES`와 `END MANAGED COURSES` 사이 내용은 자동 생성됩니다. 이 부분을 직접 편집하면 다음 갱신 때 덮어써집니다.

## 1. 기존 PDF 수정하기

1. 수정한 PDF로 기존 파일을 덮어씁니다. 예: `Teaching_files/2026b_ExoAtm/ExoAtm_lecture06.pdf`.
2. 아래 명령을 실행합니다.

```sh
python3 scripts/update_teaching.py
```

각 PDF의 **파일시스템 최종 수정 시각(mtime)**을 한국 시간으로 변환한 날짜가 `updated`와 HTML에 자동 반영됩니다. 실행일이나 PDF 내부 메타데이터 날짜를 사용하지 않습니다. 내용이 같아도 파일 수정 날짜가 달라지면 표시 날짜도 바뀝니다. 같은 PDF를 여러 강의가 공유하면 해당 강의들의 날짜가 함께 바뀝니다.

파일 복사나 Git 재다운로드(checkout/clone)로 수정 시각이 달라질 수 있습니다. 원래 수정 날짜를 유지하려면 파일을 복사할 때 수정 시각도 보존해야 합니다. 매 실행 시 실제 PDF의 수정 날짜가 기준이 됩니다.

PDF 링크에는 내용 기반 버전 값이 붙습니다. 같은 날 PDF를 여러 번 수정해도 새 링크로 연결되어 이전 PDF가 브라우저 캐시에 남는 문제를 줄입니다.

중요: 파일을 덮어쓴 것만으로 HTML은 갱신되지 않습니다. 위 명령을 실행한 뒤 변경분을 함께 commit/push해야 합니다.

## 2. 강의 날짜·시간·제목 변경하기

해당 과목의 `lectures.csv`를 텍스트 편집기 또는 Excel에서 엽니다. Excel을 사용하면 저장 형식은 **CSV UTF-8**로 선택하고, 날짜는 `YYYY-MM-DD`, 시간은 `HH:MM` 형식을 유지합니다. 필요한 경우 셀 형식을 텍스트로 지정합니다.

```csv
lecture,date,time,title,pdf,updated
6,2026-10-19,13:00,Solutions of the Radiative Transfer Equation 2,ExoAtm_lecture06.pdf,2026-10-18
7,,09:00,Vertical Thermal Structure of Atmospheres,ExoAtm_lecture07.pdf,2026-10-17
```

| 열 | 입력 방법 |
|---|---|
| `lecture` | 강의 번호. 과목 안에서 중복되지 않는 양의 정수 |
| `date` | 강의 날짜, 예: `2026-10-19`. 미정이면 빈칸 → 페이지에 `TBA` 표시 |
| `time` | 24시간 표기, 예: `09:00`, `13:00`. 미정이면 빈칸 |
| `title` | 강의 제목. 쉼표가 있으면 CSV 규칙에 따라 전체를 큰따옴표로 감쌈 |
| `pdf` | `lectures.csv`가 있는 폴더 기준 PDF 경로. 파일명이 바뀌면 이 값도 변경 |
| `updated` | `YYYY-MM-DD`. PDF가 있으면 파일의 최종 수정 날짜로 자동 덮어씀; 직접 입력 불필요 |

수정 후 다시 실행합니다.

```sh
python3 scripts/update_teaching.py
```

일정이나 제목만 수정하고 PDF 수정 시각이 그대로라면 업데이트 날짜도 유지됩니다. PDF가 있는 행의 `updated`를 수동으로 바꿔도 다음 실행 시 파일의 실제 수정 날짜로 맞춰집니다. PDF가 없는 행의 기존 `updated` 값은 유지됩니다.

## 3. 같은 과목에 새 강의 추가하기

1. 해당 과목 폴더에 PDF를 넣습니다.
2. `lectures.csv` 마지막에 한 줄을 추가합니다. 예:

```csv
17,2026-12-28,09:00,Additional Topics,ExoAtm_lecture17.pdf,
```

3. `python3 scripts/update_teaching.py`를 실행합니다.

강의는 번호순으로 정렬됩니다. 새 PDF의 `updated`는 파일의 최종 수정 날짜로 자동 기록됩니다. PDF가 아직 없으면 미리 행을 만들어 두어도 됩니다. 이 경우 강의는 표시되지만 PDF 링크는 생기지 않습니다. 나중에 파일을 넣고 갱신하면 링크가 활성화되고 날짜도 기록됩니다.

두 회차가 같은 파일을 사용하는 경우 각 행의 `pdf`에 같은 경로를 입력하면 됩니다.

## 4. 새 학기·새 과목 추가하기

다음 명령에서 폴더명과 과목 정보를 바꿔 실행합니다. 폴더명에는 영문·숫자·밑줄·하이픈을 사용할 수 있습니다.

```sh
python3 scripts/update_teaching.py \
  --new-course 2027a_RadiativeTransfer \
  --title "Radiative Transfer" \
  --term "Spring, 2027" \
  --schedule "Tuesday, 1PM - 4PM / LWC UST room" \
  --sort-date 2027-03-02
```

이 명령은 새 폴더에 `course.json`과 `lectures.csv`를 만들고 Teaching 페이지를 갱신합니다. 기존 과목 파일이 있으면 덮어쓰지 않고 오류를 표시합니다.

- `sort_date`는 과목 정렬 기준 날짜입니다. 값이 최신인 과목이 페이지 위에 나옵니다.
- 생성된 `lectures.csv`의 첫 행을 실제 강의 정보로 수정하고, PDF 파일을 넣습니다.
- 참고문헌은 `course.json`의 `references`에 추가합니다.

```json
{
  "title": "Radiative Transfer",
  "term": "Spring, 2027",
  "schedule": "Tuesday, 1PM - 4PM / LWC UST room",
  "sort_date": "2027-03-02",
  "references": [
    {"title": "Radiative Processes in Astrophysics (Rybicki & Lightman)"},
    {"title": "Online reference", "url": "https://example.com/reference"}
  ]
}
```

수정 후 `python3 scripts/update_teaching.py`를 실행하면 완성된 과목 정보가 반영됩니다. `course.json`이 없는 기존 폴더는 자동 목록에 포함되지 않습니다.

## 5. 로컬 확인과 업로드

```sh
python3 scripts/update_teaching.py
python3 -m http.server 8765 --bind 127.0.0.1
```

브라우저에서 [Teaching 로컬 미리보기](http://127.0.0.1:8765/Teaching.html)를 열고 날짜·제목·PDF 링크를 확인합니다. 이미 서버가 실행 중이면 새 서버를 띄우지 말고 페이지를 새로고침합니다. `PDF pending` 메시지는 아직 없는 PDF를 뜻하며 오류가 아닙니다.

확인이 끝나면 아래 명령 하나로 갱신·commit·push를 진행합니다.

```sh
python3 scripts/update_teaching.py --publish
```

기본 명령(`--publish` 없음)은 로컬 파일만 갱신합니다. `--publish`를 붙이면 관리 중인 과목의 PDF·CSV·`course.json`·`.pdf-hashes.json`과 `Teaching.html`을 commit한 뒤 현재 브랜치를 `origin`에 push합니다. 별도로 stage해 둔 다른 파일은 이 commit에 포함하지 않습니다. CSV에서 참조하지 않는 보조 파일이나 지난 강의의 자료를 수정했다면 별도로 commit해야 합니다.

원하는 commit 메시지를 지정할 수도 있습니다.

```sh
python3 scripts/update_teaching.py --publish --message "Update Exoplanetary Atmospheres lecture notes"
```

GitHub에 push할 수 있도록 기존 Git 인증이 설정되어 있어야 합니다. Push가 실패하면 오류를 표시하고 로컬 commit은 보존합니다. 원격 변경 등 오류 원인을 해결한 뒤 같은 명령을 다시 실행하면 기존 commit을 push합니다. 원격 변경을 강제로 덮어쓰거나 자동 병합하지 않습니다.

변경 사항이 없으면 새 commit을 만들지 않습니다. Push 후 실제 사이트 반영에는 GitHub Pages 배포 시간이 걸릴 수 있습니다. 새 과목 생성 명령에도 `--publish`를 추가할 수 있습니다.

## 주의할 점

- CSV 열 이름과 순서는 유지합니다. 날짜 오류나 중복 강의 번호가 있으면 스크립트가 오류를 출력하며 페이지와 상태 파일은 갱신하지 않습니다.
- 강의의 파일명을 바꾸면 CSV의 `pdf` 경로도 바꿉니다. 새 경로의 PDF도 해당 파일의 최종 수정 날짜를 사용합니다.
- 기존 Exoplanetary Atmospheres의 Lecture 12는 다른 과목 RT PDF를 가리키고 있어, Lecture 11과 같은 `ExoAtm_lecture11_12.pdf`를 사용하도록 정리했습니다. 실제 PDF를 만들 때 필요하면 각 회차의 경로를 변경합니다.
- Sitely로 다시 내보내면 HTML의 생성 영역 표시와 반응형 클래스가 덮어써질 수 있습니다. 현재 저장소의 표시·클래스·CSS 링크를 보존해야 합니다.
- 이 스크립트는 로컬에서 실행합니다. `--publish`를 사용하면 GitHub까지 업로드합니다. 브라우저에서 직접 입력하는 관리자 화면은 아닙니다.
