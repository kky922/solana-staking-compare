#!/usr/bin/env python3
"""
🪙 솔라나(SOL) 스테이킹 수익률 비교 - 웹 대시보드
Streamlit + Plotly 기반 인터랙티브 대시보드
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 기존 데이터 모듈 임포트
from sol_staking_compare import get_staking_options, get_sol_price, get_marinade_apy

# ═══════════════════════════════════════════════════
# 페이지 설정
# ═══════════════════════════════════════════════════
st.set_page_config(
    page_title="SOL 스테이킹 비교 대시보드",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 800; }
    .kpi-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #333;
    }
    .kpi-value { font-size: 2rem; font-weight: 700; }
    .kpi-label { font-size: 0.9rem; color: #aaa; }
    .risk-low { color: #00e676; }
    .risk-medium { color: #ffeb3b; }
    .risk-high { color: #ff5252; }
    .risk-very-high { color: #ff1744; font-weight: bold; }
    div[data-testid="stSidebar"] { background-color: #0f0f23; }
    .stMetric { background-color: #1a1a2e; border-radius: 10px; padding: 10px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# 데이터 로드 (캐시)
# ═══════════════════════════════════════════════════
@st.cache_data(ttl=300)
def load_data():
    options = get_staking_options()
    sol_price = get_sol_price()
    marinade_apy = get_marinade_apy()
    if marinade_apy and isinstance(marinade_apy, (int, float)):
        for opt in options:
            if "Marinade" in opt.name:
                opt.real_apy = float(marinade_apy)
    return options, sol_price


def to_dataframe(options):
    rows = []
    for o in options:
        avg_apy = (o.apy_low + o.apy_high) / 2
        rows.append({
            "프로토콜": o.name,
            "카테고리": o.category,
            "토큰": o.token_symbol,
            "APY 최소": o.apy_low,
            "APY 최대": o.apy_high,
            "APY 평균": avg_apy,
            "TVL (SOL)": o.tvl_sol if o.tvl_sol else 0,
            "리스크": o.risk_level,
            "유동성": o.liquidity,
            "언본딩": o.unbonding_period,
            "최소금액": o.min_stake,
            "수수료": o.commission,
            "설명": o.description,
            "URL": o.url,
            "장점": ", ".join(o.pros),
            "단점": ", ".join(o.cons),
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════
# 메인 앱
# ═══════════════════════════════════════════════════
def main():
    # 데이터 로드
    options, sol_price = load_data()
    df = to_dataframe(options)

    # ── 사이드바 ──
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png",
                 width=80) if False else st.markdown("## 🪙 SOL Staking")

        st.markdown("### ⚙️ 필터 설정")

        # 카테고리 필터
        categories = df["카테고리"].unique().tolist()
        selected_cats = st.multiselect(
            "카테고리 선택",
            categories,
            default=categories,
        )

        # 리스크 필터
        risk_levels = ["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
        selected_risks = st.multiselect(
            "리스크 수준",
            risk_levels,
            default=risk_levels,
        )

        # 유동성 필터
        liquidity_levels = ["HIGH", "MEDIUM", "LOW"]
        selected_liquidity = st.multiselect(
            "유동성",
            liquidity_levels,
            default=liquidity_levels,
        )

        st.markdown("---")
        st.markdown("### 💰 수익 시뮬레이션")

        sim_sol = st.slider("SOL 수량", 1, 1000, 100, step=1)
        sim_years = st.slider("투자 기간 (년)", 0.5, 5.0, 1.0, step=0.5)
        compound = st.checkbox("복리 적용", value=True)

        st.markdown("---")
        if st.button("🔄 데이터 새로고침", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        st.markdown("---")
        st.caption(f"업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # 필터 적용
    mask = (
        df["카테고리"].isin(selected_cats)
        & df["리스크"].isin(selected_risks)
        & df["유동성"].isin(selected_liquidity)
    )
    filtered = df[mask]

    # ── 헤더 ──
    st.markdown("# 🪙 솔라나(SOL) 스테이킹 수익률 비교 대시보드")
    st.caption("Solana Staking Yield Comparison Dashboard | 18개 프로토콜 비교 분석")

    # ── KPI 카드 ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        price_str = f"${sol_price:,.2f}" if sol_price else "N/A"
        st.metric("💰 SOL 가격", price_str)
    with col2:
        st.metric("📊 프로토콜 수", f"{len(filtered)}개")
    with col3:
        max_apy = filtered["APY 평균"].max() if len(filtered) > 0 else 0
        st.metric("🚀 최고 APY", f"{max_apy:.1f}%")
    with col4:
        avg_apy = filtered["APY 평균"].mean() if len(filtered) > 0 else 0
        st.metric("📈 평균 APY", f"{avg_apy:.1f}%")

    st.markdown("---")

    # ── 탭 구성 ──
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 비교 테이블",
        "📈 시각화 차트",
        "🔍 프로토콜 상세",
        "🎯 추천 전략",
        "💰 수익 시뮬레이터",
    ])

    # ═══════════════ TAB 1: 비교 테이블 ═══════════════
    with tab1:
        st.subheader("📊 스테이킹 옵션 비교 테이블")

        # 정렬 옵션
        sort_col = st.selectbox("정렬 기준", ["APY 평균", "APY 최대", "TVL (SOL)", "수수료", "프로토콜"], index=0)
        sort_asc = st.checkbox("오름차순", value=False)

        display_df = filtered.sort_values(sort_col, ascending=sort_asc).reset_index(drop=True)

        # 스타일링된 데이터프레임
        styled = display_df[["프로토콜", "카테고리", "APY 평균", "APY 최소", "APY 최대", "TVL (SOL)", "리스크", "유동성", "수수료"]].copy()
        styled.index = range(1, len(styled) + 1)

        # 색상 적용
        def risk_color(val):
            colors = {"LOW": "#00e676", "MEDIUM": "#ffeb3b", "HIGH": "#ff5252", "VERY_HIGH": "#ff1744"}
            return f"color: {colors.get(val, 'white')}"

        def apy_bar(val):
            return f"background: linear-gradient(90deg, #1a6b3c {min(val/25*100, 100):.0f}%, transparent {min(val/25*100, 100):.0f}%)"

        styled_styled = styled.style.format({
            "APY 평균": "{:.1f}%",
            "APY 최소": "{:.1f}%",
            "APY 최대": "{:.1f}%",
            "TVL (SOL)": "{:,.0f}",
            "수수료": "{:.1f}%",
        }).applymap(risk_color, subset=["리스크"]).applymap(risk_color, subset=["유동성"])

        st.dataframe(styled_styled, use_container_width=True, height=500)

        # 카테고리 요약
        st.markdown("### 📋 카테고리 요약")
        cat_summary = filtered.groupby("카테고리").agg(
            프로토콜수=("프로토콜", "count"),
            평균APY=("APY 평균", "mean"),
            최고APY=("APY 최대", "max"),
            총TVL=("TVL (SOL)", "sum"),
        ).round(1)
        cat_summary.columns = ["프로토콜 수", "평균 APY(%)", "최고 APY(%)", "총 TVL(SOL)"]
        st.dataframe(cat_summary, use_container_width=True)

    # ═══════════════ TAB 2: 시각화 차트 ═══════════════
    with tab2:
        st.subheader("📈 수익률 & 리스크 시각화")

        chart1, chart2 = st.columns(2)

        with chart1:
            st.markdown("#### 📊 프로토콜별 APY 비교")
            fig_apy = px.bar(
                filtered.sort_values("APY 평균", ascending=True),
                y="프로토콜",
                x=["APY 최소", "APY 평균", "APY 최대"],
                orientation="h",
                color="카테고리",
                title="APY 범위 비교",
                height=600,
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig_apy.update_layout(
                font=dict(size=11),
                xaxis_title="APY (%)",
                yaxis_title="",
                legend_title="카테고리",
            )
            st.plotly_chart(fig_apy, use_container_width=True)

        with chart2:
            st.markdown("#### ⚖️ 리스크 vs 수익률 스캐터")
            risk_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "VERY_HIGH": 4}
            scatter_df = filtered.copy()
            scatter_df["리스크값"] = scatter_df["리스크"].map(risk_map)

            fig_scatter = px.scatter(
                scatter_df,
                x="리스크값",
                y="APY 평균",
                size="TVL (SOL)",
                color="카테고리",
                hover_name="프로토콜",
                hover_data=["APY 최소", "APY 최대", "유동성"],
                title="리스크 vs 수익률 (버블 = TVL)",
                height=600,
            )
            fig_scatter.update_layout(
                xaxis=dict(
                    title="리스크",
                    tickvals=[1, 2, 3, 4],
                    ticktext=["LOW", "MEDIUM", "HIGH", "VERY_HIGH"],
                ),
                yaxis_title="평균 APY (%)",
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        chart3, chart4 = st.columns(2)

        with chart3:
            st.markdown("#### 🥧 카테고리별 TVL 분포")
            tvl_df = filtered[filtered["TVL (SOL)"] > 0]
            if len(tvl_df) > 0:
                fig_pie = px.pie(
                    tvl_df,
                    values="TVL (SOL)",
                    names="카테고리",
                    title="TVL 분포 (SOL)",
                    hole=0.4,
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        with chart4:
            st.markdown("#### 🏊 유동성 vs 리스크 분포")
            heat_df = filtered.copy()
            heat_df["count"] = 1
            heat_data = heat_df.groupby(["리스크", "유동성"])["count"].sum().reset_index()
            risk_order = ["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
            liq_order = ["HIGH", "MEDIUM", "LOW"]

            fig_heat = go.Figure(data=go.Heatmap(
                z=[[len(heat_data[(heat_data["리스크"]==r) & (heat_data["유동성"]==l)]) or 0 for l in liq_order] for r in risk_order],
                x=liq_order,
                y=risk_order,
                colorscale="Viridis",
                showscale=True,
            ))
            fig_heat.update_layout(title="프로토콜 분포", xaxis_title="유동성", yaxis_title="리스크")
            st.plotly_chart(fig_heat, use_container_width=True)

    # ═══════════════ TAB 3: 프로토콜 상세 ═══════════════
    with tab3:
        st.subheader("🔍 프로토콜 상세 정보")

        for cat in filtered["카테고리"].unique():
            cat_df = filtered[filtered["카테고리"] == cat]
            st.markdown(f"### {cat}")

            cols = st.columns(min(len(cat_df), 3))
            for i, (_, row) in enumerate(cat_df.iterrows()):
                with cols[i % 3]:
                    risk_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴", "VERY_HIGH": "💀"}
                    liq_emoji = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}

                    with st.container(border=True):
                        st.markdown(f"**{row['프로토콜']}** `{row['토큰']}`")
                        st.markdown(f"📊 APY: **{row['APY 최소']:.1f}% ~ {row['APY 최대']:.1f}%**")
                        st.markdown(f"{risk_emoji.get(row['리스크'], '')} 리스크: **{row['리스크']}**")
                        st.markdown(f"{liq_emoji.get(row['유동성'], '')} 유동성: **{row['유동성']}**")

                        tvl_str = f"{row['TVL (SOL)']:,.0f} SOL" if row['TVL (SOL)'] > 0 else "N/A"
                        st.caption(f"TVL: {tvl_str} | 수수료: {row['수수료']:.1f}%")
                        st.caption(f"⏰ 언본딩: {row['언본딩']}")

                        with st.expander("상세 보기"):
                            st.markdown(f"📝 {row['설명']}")
                            st.markdown(f"✅ **장점:** {row['장점']}")
                            st.markdown(f"❌ **단점:** {row['단점']}")
                            st.markdown(f"🔗 [공식 사이트]({row['URL']})")
            st.markdown("---")

    # ═══════════════ TAB 4: 추천 전략 ═══════════════
    with tab4:
        st.subheader("🎯 투자 성향별 추천 전략")

        rec1, rec2, rec3, rec4 = st.columns(4)

        with rec1:
            st.markdown("### 🟢 보수형")
            st.markdown("**안전 최우선**")
            st.markdown("""
            1. 🏛️ **네이티브 스테이킹** - 리스크 제로
            2. 💧 **JitoSOL** - MEV 보너스
            3. 💧 **Marinade (mSOL)** - 검증됨

            💡 **70% 네이티브 + 30% JitoSOL**
            """)
            # 포트폴리오 파이차트
            fig_rec1 = px.pie(
                values=[70, 30],
                names=["네이티브 스테이킹", "JitoSOL"],
                hole=0.5,
                color_discrete_sequence=["#00e676", "#4caf50"],
            )
            fig_rec1.update_layout(height=250, showlegend=True)
            st.plotly_chart(fig_rec1, use_container_width=True)

        with rec2:
            st.markdown("### 🟡 중립형")
            st.markdown("**수익/안정 균형**")
            st.markdown("""
            1. 💧 **JitoSOL** - 최고의 균형
            2. 📈 **Kamino Vault** - 자동 복리
            3. 📈 **Sanctum Reserve** - 유동성

            💡 **50% JitoSOL + 30% Kamino + 20% Sanctum**
            """)
            fig_rec2 = px.pie(
                values=[50, 30, 20],
                names=["JitoSOL", "Kamino Vault", "Sanctum"],
                hole=0.5,
                color_discrete_sequence=["#ffeb3b", "#ffc107", "#ff9800"],
            )
            fig_rec2.update_layout(height=250, showlegend=True)
            st.plotly_chart(fig_rec2, use_container_width=True)

        with rec3:
            st.markdown("### 🔴 공격형")
            st.markdown("**최대 수익 추구**")
            st.markdown("""
            1. 💀 **Ethena (sUSDe)** - 10~25% APY
            2. 🔄 **Solayer** - 에어드랍 기대
            3. 🌊 **Orca/Raydium LP** - 수수료 수익

            💡 **40% JitoSOL + 30% Solayer + 20% Restaking + 10% LP**
            """)
            fig_rec3 = px.pie(
                values=[40, 30, 20, 10],
                names=["JitoSOL", "Solayer", "Jito Restaking", "DEX LP"],
                hole=0.5,
                color_discrete_sequence=["#ff5252", "#f44336", "#e53935", "#c62828"],
            )
            fig_rec3.update_layout(height=250, showlegend=True)
            st.plotly_chart(fig_rec3, use_container_width=True)

        with rec4:
            st.markdown("### 🟣 DeFi 파워유저")
            st.markdown("**레버리지 전략**")
            st.markdown("""
            1. 📈 **JitoSOL→Kamino Vault** - 레버리지 복리
            2. 🌊 **JitoSOL→Orca LP** - 집중 유동성
            3. 🏦 **mSOL→MarginFi** - 대출+레버리지

            💡 **LST 담보 레버리지 루핑**
            ⚠️ 청산 리스크 주의!
            """)

        st.markdown("---")
        st.markdown("### ⚠️ 세금 & 주의사항 (한국 기준)")
        tax_col1, tax_col2 = st.columns(2)
        with tax_col1:
            st.info("""
            **📌 세금 안내**
            - 스테이킹 보상 → 기타소득 가능
            - 2025년~ 가상자산소득세 (연 250만원↑)
            - LST 스왑 → 양도소득세 가능
            - 실현 수익만 과세
            """)
        with tax_col2:
            st.warning("""
            **📌 리스크 체크리스트**
            - □ 밸리데이터 평판/성과 확인
            - □ 프로토콜 감사(audit) 여부
            - □ TVL 규모와 유동성
            - □ 스마트 컨트랙트 버그 리스크
            - □ 슬래싱 가능 여부
            - □ 언본딩 기간 숙지
            """)

    # ═══════════════ TAB 5: 수익 시뮬레이터 ═══════════════
    with tab5:
        st.subheader("💰 수익 시뮬레이터")
        st.markdown(f"**투자 금액:** {sim_sol} SOL = **${sim_sol * sol_price:,.2f}**" if sol_price else f"**투자 금액:** {sim_sol} SOL")

        # 대표 프로토콜 선택
        sim_protocols = {
            "🏛️ 네이티브 스테이킹": 6.8,
            "💧 JitoSOL": 7.4,
            "💧 mSOL": 7.0,
            "💧 Sanctum": 6.9,
            "🏦 DeFi 렌딩 (평균)": 3.5,
            "🔄 Jito Restaking": 10.0,
            "🔄 Solayer": 11.5,
            "📈 Kamino Vault": 8.5,
            "📈 Ethena": 17.5,
            "🌊 DEX LP (평균)": 9.5,
        }

        # 수익 계산
        results = []
        for name, apy in sim_protocols.items():
            if compound:
                final = sim_sol * (1 + apy / 100) ** sim_years
            else:
                final = sim_sol * (1 + apy / 100 * sim_years)
            gain = final - sim_sol
            gain_usd = gain * sol_price if sol_price else 0
            results.append({
                "프로토콜": name,
                "APY": f"{apy:.1f}%",
                f"{sim_years}년 후 SOL": f"{final:.2f}",
                "SOL 수익": f"+{gain:.2f}",
                "USD 수익": f"+${gain_usd:,.2f}" if sol_price else "N/A",
                "수익_SOL": gain,
                "수익_USD": gain_usd,
            })

        sim_df = pd.DataFrame(results)

        # 수익 바차트
        fig_sim = px.bar(
            sim_df.sort_values("수익_SOL", ascending=True),
            y="프로토콜",
            x="수익_SOL",
            orientation="h",
            title=f"예상 수익 ({sim_sol} SOL, {sim_years}년, {'복리' if compound else '단리'})",
            color="수익_SOL",
            color_continuous_scale="Greens",
        )
        fig_sim.update_layout(
            xaxis_title=f"수익 (SOL)",
            yaxis_title="",
            height=500,
        )
        st.plotly_chart(fig_sim, use_container_width=True)

        # 상세 테이블
        display_sim = sim_df[["프로토콜", "APY", f"{sim_years}년 후 SOL", "SOL 수익", "USD 수익"]].copy()
        st.dataframe(display_sim, use_container_width=True, hide_index=True)

        st.info(f"💡 {'복리' if compound else '단리'} 기준 | USD 수익은 현재 SOL 가격(${sol_price:,.2f}) 기준" if sol_price else "💡 SOL 가격을 불러올 수 없어 USD 수익은 N/A로 표시됩니다")

    # ── 푸터 ──
    st.markdown("---")
    st.caption(f"🪙 SOL 스테이킹 비교 대시보드 | 데이터: CoinGecko, 프로토콜 공식 자료 | 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.caption("⚠️ 수익률은 예상치이며 실제와 다를 수 있습니다. 투자 전 DYOR!")


if __name__ == "__main__":
    main()