# kkt_test — AI 버크셔 투자 리서치 세팅

`.claude/skills/`에 [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire)(MIT) 스킬 21개가 들어 있다.
버핏·멍거·돤융핑(段永平)·리루(李录) 4대가 관점의 가치투자 리서치 워크플로다.

## 사용

- 자연어: `버크셔 스킬 사용해서 하이닉스 종목 분석해줘` → 맞는 스킬을 골라 실행
- 직접 호출: `/investment-research SK하이닉스`, `/investment-checklist 삼성전자, 애플`, `/news-pulse 테슬라` 등
- 빠른 1차 거르기는 `/quality-screen`·`/investment-checklist`, 깊게 볼 때만 `/investment-research`·`/investment-team` (토큰 많이 씀)

## 규칙

- 사용자가 한국어로 물으면 보고서와 답변도 **한국어**로 쓴다 (스킬 원문이 중국어여도 마찬가지).
- 보고서는 `reports/`에 저장한다. 회사별 보고서는 `reports/{회사명}/` 폴더에 둔다.
- 객관성 원칙(스킬들이 말하는 "CLAUDE.md 客观性原则"):
  - 사실은 데이터와 출처로 뒷받침하고, 의견·추정은 "의견"/"추정"으로 표시한다.
  - 강세/약세 입장을 미리 정하지 않는다. 데이터 → 논리 → 결론 순서.
  - 핵심 판단마다 반대 근거를 함께 적는다.
  - 모르면 "불확실" 또는 "데이터 부족"이라고 쓴다.
- 핵심 재무 수치는 독립 출처 2곳으로 교차검증하고, 차이가 1%를 넘으면 표시한다.
- 시가총액·PER·ROE 등 계산은 `python3 tools/financial_rigor.py`로 한다 (암산 금지). 통화 단위를 항상 명시한다.
- 연구 시작 전 `date`로 오늘 날짜를 확인하고, 보고서 머리에 데이터 기준일을 적는다.
- 대가별 코멘트는 실제 발언이 아니라 AI가 그 관점으로 쓴 모의 코멘트임을 밝힌다.
- 모든 결과 끝에: **교육·참고용이며 매수·매도 추천이 아님. 투자 판단은 본인 책임.**

## 업데이트

`python3 scripts/sync_ai_berkshire.py` — 원본 최신본을 받아 `.claude/skills/`, `tools/`를 다시 만든다.
생성된 `SKILL.md`는 직접 고치지 말고 스크립트에서 고친다.
