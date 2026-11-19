# 3.10.5 Unemployment Rate (LUR) 분석

IMF WEO `WEOApr2024.xlsx`의 지표 코드 `LUR`(실업률)을 사용합니다.

## 분석 내용

- 2022년 실업률 오름차순 정렬 후 80개국 표시
- 관심 국가 강조: Korea, United States, Japan, Germany
- 같은 그래프에 `2023 - 2022` 차이값 표시

## VS Code에서 실행

1. `lur_analysis/WEOApr2024.xlsx` 파일이 같은 폴더에 있는지 확인
2. 터미널에서:

```bash
cd lur_analysis
python -m pip install -r requirements.txt
python lur_unemployment_analysis.py
```

## 결과

- `output/lur_2022_and_diff.png`
- `output/lur_2022_2023.csv`

관심 국가는 `lur_unemployment_analysis.py`의 `FOCUS_COUNTRIES`에서 바꿀 수 있습니다.
