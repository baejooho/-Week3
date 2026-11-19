# 3.10.5 Unemployment Rate (LUR) 분석

IMF WEO 지표 코드 `LUR`(실업률)로 2022·2023년 국가별 실업률을 분석합니다.

## 분석 내용

- 2022년 실업률 오름차순 정렬 후 80개국 표시
- 관심 국가 강조: Korea, United States, Japan, Germany
- 같은 그래프에 `2023 - 2022` 차이값 표시

## VS Code에서 실행

```bash
cd lur_analysis
python -m pip install -r requirements.txt
python lur_unemployment_analysis.py
```

## 결과 파일

- `output/lur_2022_and_diff.png` : 그래프
- `output/lur_2022_2023.csv` : 분석 데이터

## 관심 국가 바꾸기

`lur_unemployment_analysis.py`의 `FOCUS_COUNTRIES` 딕셔너리를 수정하세요.
