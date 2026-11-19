"""
3.10.5 Unemployment Rate (LUR) 실업률 경제 지표 분석

- IMF WEO indicator code: LUR
- 2022년 국가별 실업률을 오름차순으로 80개국 표시
- 관심 국가 3~4개 강조
- 2023 - 2022 차이값을 같은 그래프에 표시
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

# VS Code / 서버 환경 모두에서 저장 가능하도록 non-GUI 백엔드 사용
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import requests
from matplotlib import font_manager
from matplotlib.patches import Patch


# 관심 국가 (ISO3 코드)
FOCUS_COUNTRIES = {
    "KOR": "Korea",
    "USA": "United States",
    "JPN": "Japan",
    "DEU": "Germany",
}

N_COUNTRIES = 80
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
FIGURE_PATH = OUTPUT_DIR / "lur_2022_and_diff.png"
DATA_PATH = OUTPUT_DIR / "lur_2022_2023.csv"


def setup_korean_font() -> None:
    """한글 깨짐 방지용 폰트 설정."""
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


def fetch_lur(start_year: int = 2022, end_year: int = 2023) -> pd.DataFrame:
    """IMF SDMX API에서 LUR(실업률) 연간 데이터를 가져온다."""
    url = (
        "https://api.imf.org/external/sdmx/2.1/data/WEO/.LUR.A"
        f"?startPeriod={start_year}&endPeriod={end_year}"
    )
    response = requests.get(url, timeout=120, headers={"Accept": "application/json"})
    response.raise_for_status()
    payload = response.json()

    series_dims = payload["structure"]["dimensions"]["series"]
    observation_dims = payload["structure"]["dimensions"]["observation"]
    years = {i: int(v["id"]) for i, v in enumerate(observation_dims[0]["values"])}

    rows: list[dict] = []
    for key, obj in payload["dataSets"][0]["series"].items():
        indexes = list(map(int, key.split(":")))
        meta: dict = {}
        for dim, idx in zip(series_dims, indexes):
            value = dim["values"][idx]
            meta[dim["id"]] = value.get("id")
            meta[f"{dim['id']}_name"] = value.get("name")

        for obs_index, values in obj.get("observations", {}).items():
            raw = values[0]
            if raw is None:
                continue
            rows.append(
                {
                    "country_code": meta["COUNTRY"],
                    "country": meta["COUNTRY_name"],
                    "year": years[int(obs_index)],
                    "lur": float(raw),
                }
            )

    df = pd.DataFrame(rows)
    # ISO3 국가만 사용 (지역 합계 코드 제외)
    df = df[df["country_code"].str.fullmatch(r"[A-Z]{3}")].copy()
    return df


def shorten_country_name(name: str) -> str:
    mapping = {
        "Korea, Republic of": "Korea",
        "United States": "United States",
        "United Kingdom": "United Kingdom",
        "China, People's Republic of": "China",
        "Russian Federation": "Russia",
        "Turkiye": "Turkiye",
        "Czech Republic": "Czechia",
        "Slovak Republic": "Slovakia",
        "Netherlands, The Kingdom of the": "Netherlands",
        "Andorra, Principality of": "Andorra",
        "Liechtenstein, Principality of": "Liechtenstein",
        "Aruba, Kingdom of the Netherlands": "Aruba",
    }
    return mapping.get(name, name)


def prepare_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """2022 실업률 오름차순 80개국 + 2023-2022 차이."""
    wide = (
        df.pivot_table(index=["country_code", "country"], columns="year", values="lur")
        .dropna(subset=[2022, 2023])
        .reset_index()
    )
    wide["country_short"] = wide["country"].map(shorten_country_name)
    wide["diff_2023_2022"] = wide[2023] - wide[2022]
    wide = wide.sort_values(2022, ascending=True).head(N_COUNTRIES).reset_index(drop=True)
    wide["focus"] = wide["country_code"].isin(FOCUS_COUNTRIES)
    return wide


def plot_lur(analysis: pd.DataFrame, save_path: Path) -> None:
    """
    하나의 그래프에 표시:
    - 막대: 2022년 실업률 (오름차순 80개국)
    - 선: 2023 - 2022 차이값
    - 관심 국가는 색/마커로 강조
    """
    setup_korean_font()

    x = range(len(analysis))
    colors = ["#D62728" if flag else "#4C78A8" for flag in analysis["focus"]]

    fig, ax1 = plt.subplots(figsize=(18, 8))

    ax1.bar(x, analysis[2022], color=colors, alpha=0.85, label="2022 LUR (%)")
    ax1.set_ylabel("2022 Unemployment Rate (LUR, %)", fontsize=12)
    ax1.set_xlabel("Countries (ascending by 2022 LUR)", fontsize=12)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(analysis["country_short"], rotation=90, fontsize=7)
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

    # 관심 국가 라벨
    for i, row in analysis[analysis["focus"]].iterrows():
        ax1.annotate(
            row["country_short"],
            xy=(i, row[2022]),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            color="#D62728",
        )
        ax2.scatter([i], [row["diff_2023_2022"]], color="#D62728", s=55, zorder=5)

    ax1.set_title(
        "IMF WEO LUR | 2022 Unemployment Rate (Ascending, Top 80)\n"
        "with 2023-2022 Difference on the Same Chart",
        fontsize=14,
        pad=12,
    )

    # 범례 합치기
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    focus_patch = Patch(color="#D62728", label="Focus countries")
    ax1.legend(handles1 + handles2 + [focus_patch], labels1 + labels2 + ["Focus countries"], loc="upper left")

    fig.tight_layout()
    save_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"그래프 저장: {save_path}")


def print_focus_summary(analysis: pd.DataFrame) -> None:
    print("\n[관심 국가 요약]")
    focus = analysis[analysis["focus"]][
        ["country_code", "country_short", 2022, 2023, "diff_2023_2022"]
    ].copy()
    focus = focus.rename(columns={2022: "LUR_2022", 2023: "LUR_2023"})
    print(focus.to_string(index=False))

    print("\n[해석 포인트]")
    print("- 막대가 낮을수록 2022년 실업률이 낮은 국가입니다.")
    print("- 초록 선이 0보다 크면 2023년에 실업률이 상승, 작으면 하락입니다.")
    print("- 빨간 막대/라벨은 관심 국가(KOR, USA, JPN, DEU)입니다.")


def main() -> None:
    print("IMF WEO LUR 데이터 다운로드 중...")
    raw = fetch_lur(2022, 2023)
    analysis = prepare_analysis(raw)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    analysis.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
    print(f"데이터 저장: {DATA_PATH}")
    print(f"분석 국가 수: {len(analysis)} (2022 실업률 오름차순)")

    print_focus_summary(analysis)
    plot_lur(analysis, FIGURE_PATH)


if __name__ == "__main__":
    main()
