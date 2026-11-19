"""
3.10.5 Unemployment Rate (LUR) 실업률 경제 지표 분석

데이터: WEOApr2024.xlsx (IMF WEO)
- code: LUR
- 2022년 국가별 실업률 오름차순 80개국
- 관심 국가 3~4개 강조
- 같은 그래프에 2023 - 2022 차이값 표시
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager
from matplotlib.patches import Patch


FOCUS_COUNTRIES = {
    "KOR": "Korea",
    "USA": "United States",
    "JPN": "Japan",
    "DEU": "Germany",
}

N_COUNTRIES = 80
BASE_DIR = Path(__file__).resolve().parent
WEO_PATH = BASE_DIR / "WEOApr2024.xlsx"
OUTPUT_DIR = BASE_DIR / "output"
FIGURE_PATH = OUTPUT_DIR / "lur_2022_and_diff.png"
DATA_PATH = OUTPUT_DIR / "lur_2022_2023.csv"


def setup_korean_font() -> None:
    candidates = [
        "Malgun Gothic",
        "AppleGothic",
        "NanumGothic",
        "WenQuanYi Micro Hei",
        "Noto Sans CJK KR",
    ]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False


def load_lur_from_weo(path: Path) -> pd.DataFrame:
    """WEO Excel에서 LUR(실업률) 행만 읽어 2022·2023 값을 정리한다."""
    if not path.exists():
        raise FileNotFoundError(
            f"WEO 파일이 없습니다: {path}\n"
            "VS Code에서 lur_analysis 폴더에 WEOApr2024.xlsx 를 넣어 주세요."
        )

    raw = pd.read_excel(path)
    lur = raw[raw["WEO Subject Code"] == "LUR"].copy()

    # 연도 컬럼이 문자열일 수도 있어서 안전하게 맞춤
    year_cols = {}
    for y in (2022, 2023):
        if y in lur.columns:
            year_cols[y] = y
        elif str(y) in lur.columns:
            year_cols[y] = str(y)
        else:
            raise KeyError(f"WEO 파일에 {y}년 컬럼이 없습니다.")

    out = pd.DataFrame(
        {
            "country_code": lur["ISO"].astype(str),
            "country": lur["Country"].astype(str),
            "LUR_2022": pd.to_numeric(lur[year_cols[2022]], errors="coerce"),
            "LUR_2023": pd.to_numeric(lur[year_cols[2023]], errors="coerce"),
        }
    )
    out = out.dropna(subset=["LUR_2022", "LUR_2023"])
    out = out[out["country_code"].str.fullmatch(r"[A-Z]{3}")].copy()
    return out.reset_index(drop=True)


def prepare_analysis(df: pd.DataFrame) -> pd.DataFrame:
    wide = df.copy()
    wide["diff_2023_2022"] = wide["LUR_2023"] - wide["LUR_2022"]
    wide = wide.sort_values("LUR_2022", ascending=True).head(N_COUNTRIES).reset_index(drop=True)
    wide["focus"] = wide["country_code"].isin(FOCUS_COUNTRIES)
    return wide


def plot_lur(analysis: pd.DataFrame, save_path: Path) -> None:
    setup_korean_font()

    x = range(len(analysis))
    colors = ["#D62728" if flag else "#4C78A8" for flag in analysis["focus"]]

    fig, ax1 = plt.subplots(figsize=(18, 8))
    ax1.bar(x, analysis["LUR_2022"], color=colors, alpha=0.85, label="2022 LUR (%)")
    ax1.set_ylabel("2022 Unemployment Rate (LUR, %)", fontsize=12)
    ax1.set_xlabel("Countries (ascending by 2022 LUR)", fontsize=12)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(analysis["country"], rotation=90, fontsize=7)
    ax1.grid(axis="y", linestyle="--", alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(
        list(x),
        analysis["diff_2023_2022"],
        color="#2CA02C",
        marker="o",
        linewidth=1.5,
        markersize=3.5,
        label="2023 - 2022 (pp)",
    )
    ax2.axhline(0, color="gray", linewidth=1, linestyle=":")
    ax2.set_ylabel("Difference 2023 - 2022 (percentage points)", fontsize=12)

    for i, row in analysis[analysis["focus"]].iterrows():
        ax1.annotate(
            row["country"],
            xy=(i, row["LUR_2022"]),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            color="#D62728",
        )
        ax2.scatter([i], [row["diff_2023_2022"]], color="#D62728", s=55, zorder=5)

    ax1.set_title(
        "IMF WEO LUR | 2022 Unemployment Rate (Ascending, 80 countries)\n"
        "with 2023 - 2022 Difference  |  source: WEOApr2024.xlsx",
        fontsize=14,
        pad=12,
    )

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    focus_patch = Patch(color="#D62728", label="Focus countries")
    ax1.legend(
        handles1 + handles2 + [focus_patch],
        labels1 + labels2 + ["Focus countries"],
        loc="upper left",
    )

    fig.tight_layout()
    save_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"그래프 저장: {save_path}")


def print_focus_summary(analysis: pd.DataFrame) -> None:
    print("\n[관심 국가 요약]")
    focus = analysis[analysis["focus"]][
        ["country_code", "country", "LUR_2022", "LUR_2023", "diff_2023_2022"]
    ]
    print(focus.to_string(index=False))
    print("\n[해석]")
    print("- 파란/빨간 막대: 2022년 실업률 (왼쪽 축)")
    print("- 초록 선: 2023 - 2022 차이 (오른쪽 축, 단위: %p)")
    print("- 빨간 강조: Korea, United States, Japan, Germany")


def main() -> None:
    print(f"WEO 파일 읽기: {WEO_PATH}")
    raw = load_lur_from_weo(WEO_PATH)
    analysis = prepare_analysis(raw)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    analysis.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
    print(f"데이터 저장: {DATA_PATH}")
    print(f"분석 국가 수: {len(analysis)} (2022 실업률 오름차순)")

    print_focus_summary(analysis)
    plot_lur(analysis, FIGURE_PATH)


if __name__ == "__main__":
    main()
