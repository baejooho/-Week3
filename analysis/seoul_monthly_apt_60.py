"""3.11.3 최근 2년간 서울지역 월별 아파트 분양가격 비교 (전용 60㎡ 이하).

apt_national.csv에서 서울 · 전용면적 60제곱미터이하 · 2023년과 2024년
분양가격(천원/㎡)을 월별로 비교한다.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "apt_national.csv"
OUT_DIR = ROOT / "output"
SIZE = "전용면적 60제곱미터이하"
YEARS = (2023, 2024)


def load_prices(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, encoding="cp949")
    frame["분양가격"] = pd.to_numeric(
        frame["분양가격(제곱미터)"].astype(str).str.strip().str.replace(",", "", regex=False),
        errors="coerce",
    )
    frame["연도"] = frame["연도"].astype(int)
    frame["월"] = frame["월"].astype(int)
    return frame


def seoul_small(frame: pd.DataFrame) -> pd.DataFrame:
    picked = frame[
        (frame["지역명"] == "서울")
        & (frame["규모구분"] == SIZE)
        & (frame["연도"].isin(YEARS))
    ].copy()
    picked = picked.sort_values(["연도", "월"])
    if picked["분양가격"].isna().any():
        missing = picked.loc[picked["분양가격"].isna(), ["연도", "월"]]
        raise ValueError(f"서울 60㎡ 이하 2023–2024에 결측 가격이 있습니다:\n{missing}")
    if len(picked) != 24:
        raise ValueError(f"월별 1건이어야 하는데 {len(picked)}건입니다.")
    return picked


def monthly_compare(picked: pd.DataFrame) -> pd.DataFrame:
    wide = picked.pivot(index="월", columns="연도", values="분양가격").sort_index()
    wide.columns = [str(year) for year in wide.columns]
    wide["차이"] = wide["2024"] - wide["2023"]
    wide["증감률"] = wide["차이"] / wide["2023"] * 100
    wide["2023_평당"] = wide["2023"] * 3.3
    wide["2024_평당"] = wide["2024"] * 3.3
    return wide


def summarize(wide: pd.DataFrame) -> dict:
    avg_2023 = wide["2023"].mean()
    avg_2024 = wide["2024"].mean()
    without_june = wide.drop(index=6)
    return {
        "avg_2023": avg_2023,
        "avg_2024": avg_2024,
        "avg_diff": avg_2024 - avg_2023,
        "avg_rate": (avg_2024 - avg_2023) / avg_2023 * 100,
        "avg_2023_ex_june": without_june["2023"].mean(),
        "avg_2024_ex_june": without_june["2024"].mean(),
        "higher_months": int((wide["차이"] > 0).sum()),
        "max_month": int(wide["차이"].idxmax()),
        "max_diff": float(wide["차이"].max()),
        "min_month": int(wide["차이"].idxmin()),
        "min_diff": float(wide["차이"].min()),
    }


def save_chart(wide: pd.DataFrame, path: Path) -> None:
    font_path = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
    if Path(font_path).exists():
        font_manager.fontManager.addfont(font_path)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=font_path).get_name()
    plt.rcParams["axes.unicode_minus"] = False

    months = [f"{month}월" for month in wide.index]
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1.4]})

    x = range(len(wide))
    width = 0.38
    axes[0].bar([i - width / 2 for i in x], wide["2023"], width, label="2023년", color="#4C78A8")
    axes[0].bar([i + width / 2 for i in x], wide["2024"], width, label="2024년", color="#F58518")
    axes[0].set_ylabel("분양가격 (천원/㎡)")
    axes[0].set_title("서울 전용 60㎡ 이하 월별 아파트 분양가격 (2023년 · 2024년)")
    axes[0].legend()
    axes[0].axhline(wide["2023"].mean(), color="#4C78A8", linestyle="--", linewidth=0.8, alpha=0.7)
    axes[0].axhline(wide["2024"].mean(), color="#F58518", linestyle="--", linewidth=0.8, alpha=0.7)

    colors = ["#E45756" if value < 0 else "#54A24B" for value in wide["증감률"]]
    axes[1].bar(x, wide["증감률"], color=colors)
    axes[1].axhline(0, color="#333333", linewidth=0.6)
    axes[1].set_ylabel("전년 동월 대비 (%)")
    axes[1].set_xlabel("월")
    axes[1].set_xticks(list(x), months)

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=140)
    plt.close(fig)


def main() -> None:
    wide = monthly_compare(seoul_small(load_prices(DATA)))
    stats = summarize(wide)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    table_path = OUT_DIR / "seoul_60_2023_2024.csv"
    wide.to_csv(table_path, encoding="utf-8-sig", float_format="%.2f")
    chart_path = OUT_DIR / "seoul_60_2023_2024.png"
    save_chart(wide, chart_path)

    print("월별 분양가격 (천원/㎡)")
    print(wide[["2023", "2024", "차이", "증감률"]].to_string(float_format=lambda v: f"{v:,.1f}"))
    print()
    print(
        f"연평균 2023 {stats['avg_2023']:,.0f} → 2024 {stats['avg_2024']:,.0f} "
        f"({stats['avg_diff']:+,.0f}, {stats['avg_rate']:+.1f}%)"
    )
    print(
        f"6월 제외 연평균 2023 {stats['avg_2023_ex_june']:,.0f} → "
        f"2024 {stats['avg_2024_ex_june']:,.0f}"
    )
    print(f"2024년이 높은 달 {stats['higher_months']}/12")
    print(f"최대 상승 {stats['max_month']}월 {stats['max_diff']:+,.0f}")
    print(f"최대 하락 {stats['min_month']}월 {stats['min_diff']:+,.0f}")
    print(f"표 {table_path}")
    print(f"그림 {chart_path}")


if __name__ == "__main__":
    main()
