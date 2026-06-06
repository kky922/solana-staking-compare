#!/usr/bin/env python3
"""
🪙 솔라나(SOL) 스테이킹 수익률 비교 분석 도구
 - 네이티브 스테이킹, 리퀴드 스테이킹, DeFi 렌딩, 레스테이킹 등 비교
 - 실시간 데이터 수집 (가능한 경우) + 기준 수익률
"""

import json
import sys
import time

DATA_SNAPSHOT_DATE = "2026-06-07"


def effective_apy(option: "StakingOption") -> float:
    """Return live APY when available, otherwise the static midpoint."""
    if option.real_apy is not None:
        return option.real_apy
    return (option.apy_low + option.apy_high) / 2


def sort_by_effective_apy(options: list["StakingOption"]) -> list["StakingOption"]:
    return sorted(options, key=effective_apy, reverse=True)
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# ═══════════════════════════════════════════════════
# 데이터 구조
# ═══════════════════════════════════════════════════

@dataclass
class StakingOption:
    """스테이킹 옵션 데이터 클래스"""
    name: str                    # 프로토콜/방식 이름
    category: str                # 카테고리 (네이티브, 리퀴드, DeFi, 레스테이킹 등)
    token_symbol: str            # LST 토큰 심볼
    apy_low: float               # 최소 예상 APY (%)
    apy_high: float              # 최대 예상 APY (%)
    tvl_sol: Optional[float]     # TVL (SOL 단위)
    risk_level: str              # LOW, MEDIUM, HIGH, VERY_HIGH
    liquidity: str               # HIGH, MEDIUM, LOW, NONE
    unbonding_period: str        # 언본딩 기간
    min_stake: float             # 최소 스테이킹 금액 (SOL)
    commission: float            # 수수료 (%)
    description: str             # 설명
    url: str                     # 공식 URL
    pros: list = field(default_factory=list)
    cons: list = field(default_factory=list)
    real_apy: Optional[float] = None  # API로 가져온 실시간 APY


# ═══════════════════════════════════════════════════
# 스테이킹 옵션 데이터베이스
# ═══════════════════════════════════════════════════

def get_staking_options() -> list[StakingOption]:
    """모든 스테이킹 옵션 목록 반환"""
    return [
        # ── 네이티브 스테이킹 ──
        StakingOption(
            name="네이티브 스테이킹 (직접 위임)",
            category="🏛️ 네이티브 스테이킹",
            token_symbol="SOL",
            apy_low=6.3, apy_high=7.2,
            tvl_sol=None,
            risk_level="LOW",
            liquidity="LOW",
            unbonding_period="2~3일 (1 epoch)",
            min_stake=0.01,
            commission=0.0,
            description="밸리데이터에 SOL을 직접 위임하는 가장 기본적인 방식",
            url="https://solana.com/staking",
            pros=["가장 안전 (스마트 컨트랙트 리스크 없음)", "인플레이션 보상 직접 수령", "탈중앙화에 기여"],
            cons=["유동성 없음 (언본딩 필요)", "밸리데이터 선택 필요", "복리 불가 (수동 컴파운딩)"],
        ),

        # ── 리퀴드 스테이킹 ──
        StakingOption(
            name="Jito (JitoSOL)",
            category="💧 리퀴드 스테이킹",
            token_symbol="JitoSOL",
            apy_low=6.8, apy_high=8.0,
            tvl_sol=14_000_000,
            risk_level="LOW",
            liquidity="HIGH",
            unbonding_period="즉시 (스왑 가능)",
            min_stake=0.01,
            commission=0.0,
            description="Jito MEV 기반 리퀴드 스테이킹. MEV 팁 수익 추가 분배",
            url="https://jito.network/staking/",
            pros=["MEV 보너스로 높은 수익률", "높은 유동성", "DeFi에서 담보 활용 가능", "가장 큰 LST 중 하나"],
            cons=["JitoSOL/SOL 프리미엄 변동", "스마트 컨트랙트 리스크", "Jito 밸리데이터 집중도"],
        ),
        StakingOption(
            name="Marinade Finance (mSOL)",
            category="💧 리퀴드 스테이킹",
            token_symbol="mSOL",
            apy_low=6.5, apy_high=7.5,
            tvl_sol=6_500_000,
            risk_level="LOW",
            liquidity="HIGH",
            unbonding_period="즉시 (스왑) / 1 epoch (언스테이크)",
            min_stake=0.01,
            commission=0.0,
            description="Marinade 자동 밸리데이터 분산 위임 리퀴드 스테이킹",
            url="https://marinade.finance/",
            pros=["자동 밸리데이터 최적화", "탈중앙화 기여", "DeFi 생태계 광범위", "오래된 프로토콜"],
            cons=["Jito 대비 낮은 수익률", "mSOL/SOL 스프레드", "거버넌스 토큰 MNDE 필요 없음"],
        ),
        StakingOption(
            name="Sanctum (infSOL / hsol)",
            category="💧 리퀴드 스테이킹",
            token_symbol="infSOL",
            apy_low=6.5, apy_high=7.3,
            tvl_sol=3_000_000,
            risk_level="LOW",
            liquidity="HIGH",
            unbonding_period="즉시 (스왑 가능)",
            min_stake=0.01,
            commission=0.0,
            description="Sanctum의 무한(infinite) 리퀴드 스테이킹 프로토콜",
            url="https://sanctum.so/",
            pros=["LST 간 즉시 스왑", "다양한 밸리데이터 지원", "점진적 탈중앙화"],
            cons=["상대적으로 신규 프로토콜", "유동성 풀 의존"],
        ),
        StakingOption(
            name="BlazeStake (bSOL)",
            category="💧 리퀴드 스테이킹",
            token_symbol="bSOL",
            apy_low=6.5, apy_high=7.3,
            tvl_sol=1_500_000,
            risk_level="LOW",
            liquidity="MEDIUM",
            unbonding_period="즉시 (스왑 가능)",
            min_stake=0.01,
            commission=0.0,
            description="BlazeStake 리퀴드 스테이킹. 자동 밸리데이터 분배",
            url="https://stake.solblaze.org/",
            pros=["자동 분배", "DeFi 통합", "에어드랍 가능성"],
            cons=["낮은 유동성", "더 작은 생태계"],
        ),
        StakingOption(
            name="Rocket Pool (rSOL)",
            category="💧 리퀴드 스테이킹",
            token_symbol="rSOL",
            apy_low=6.3, apy_high=7.0,
            tvl_sol=500_000,
            risk_level="LOW",
            liquidity="MEDIUM",
            unbonding_period="즉시 (스왑 가능)",
            min_stake=0.01,
            commission=0.0,
            description="Rocket Pool의 솔라나 리퀴드 스테이킹",
            url="https://rocketpool.net/",
            pros=["이더리움에서 검증된 프로토콜", "탈중앙화 중심"],
            cons=["솔라나에서는 상대적으로 작음", "낮은 유동성"],
        ),

        # ── DeFi 렌딩 ──
        StakingOption(
            name="MarginFi (SOL 렌딩)",
            category="🏦 DeFi 렌딩",
            token_symbol="SOL",
            apy_low=2.0, apy_high=5.0,
            tvl_sol=2_000_000,
            risk_level="MEDIUM",
            liquidity="HIGH",
            unbonding_period="즉시",
            min_stake=0.01,
            commission=0.0,
            description="MarginFi 렌딩 프로토콜에 SOL 예치",
            url="https://www.marginfi.com/",
            pros=["높은 유동성", "담보로 활용 가능", "변동 금리"],
            cons=["낮은 수익률", "청산 리스크 (레버리지 시)", "대출 수요에 따른 변동"],
        ),
        StakingOption(
            name="Kamino Lend (SOL)",
            category="🏦 DeFi 렌딩",
            token_symbol="SOL",
            apy_low=1.5, apy_high=4.0,
            tvl_sol=3_000_000,
            risk_level="MEDIUM",
            liquidity="HIGH",
            unbonding_period="즉시",
            min_stake=0.01,
            commission=0.0,
            description="Kamino 렌딩 시장에 SOL 예치",
            url="https://kamino.finance/",
            pros=["높은 유동성", "자동화된 전략", "담보 활용"],
            cons=["낮은 수익률", "대출 수요 의존", "스마트 컨트랙트 리스크"],
        ),
        StakingOption(
            name="Drift Lend (SOL)",
            category="🏦 DeFi 렌딩",
            token_symbol="SOL",
            apy_low=1.0, apy_high=3.5,
            tvl_sol=1_500_000,
            risk_level="MEDIUM",
            liquidity="HIGH",
            unbonding_period="즉시",
            min_stake=0.01,
            commission=0.0,
            description="Drift Protocol 렌딩에 SOL 예치",
            url="https://www.drift.trade/",
            pros=["빠른 예출금", "담보 활용", "다양한 자산 쌍"],
            cons=["가장 낮은 렌딩 수익률 중 하나", "변동성 큼"],
        ),

        # ── 레스테이킹 / AVS ──
        StakingOption(
            name="Jito Restaking",
            category="🔄 레스테이킹",
            token_symbol="JitoSOL",
            apy_low=8.0, apy_high=12.0,
            tvl_sol=5_000_000,
            risk_level="MEDIUM",
            liquidity="MEDIUM",
            unbonding_period="프로토콜에 따라 다름",
            min_stake=0.01,
            commission=0.0,
            description="Jito VRT (Vault Receipt Token) 기반 레스테이킹. AVS에 보안 제공",
            url="https://restaking.jito.network/",
            pros=["추가 보상 (AVS 인센티브)", "JitoSOL 기반 안전", "성장 중인 생태계"],
            cons=["슬래싱 리스크 가능", "아직 초기 단계", "보상 불확실"],
        ),
        StakingOption(
            name="Solayer (sSOL / SSOL)",
            category="🔄 레스테이킹",
            token_symbol="sSOL",
            apy_low=8.0, apy_high=15.0,
            tvl_sol=4_000_000,
            risk_level="HIGH",
            liquidity="MEDIUM",
            unbonding_period="불명확 (프로토콜 정책)",
            min_stake=0.01,
            commission=0.0,
            description="Solayer 레스테이킹 프로토콜. 공유 보안 및 가속 서비스 제공",
            url="https://www.solayer.org/",
            pros=["높은 잠재적 수익률", "에어드랍 기대", "새로운 인센티브"],
            cons=["높은 리스크", "신규 프로토콜", "슬래싱 가능", "초기 단계"],
        ),
        StakingOption(
            name="Picasso (pSOL)",
            category="🔄 레스테이킹",
            token_symbol="pSOL",
            apy_low=7.0, apy_high=12.0,
            tvl_sol=1_000_000,
            risk_level="HIGH",
            liquidity="LOW",
            unbonding_period="프로토콜에 따라 다름",
            min_stake=0.01,
            commission=0.0,
            description="Picasso 크로스체인 레스테이킹. IBC 기반 연결",
            url="https://picasso.network/",
            pros=["크로스체인 보상", "다양한 AVS 참여", "에어드랍 가능성"],
            cons=["매우 신규", "낮은 유동성", "복잡한 구조"],
        ),

        # ── Vault / 자동화 전략 ──
        StakingOption(
            name="Kamino Vault (JitoSOL 기반)",
            category="📈 Vault / 자동화",
            token_symbol="JitoSOL",
            apy_low=7.0, apy_high=10.0,
            tvl_sol=2_500_000,
            risk_level="MEDIUM",
            liquidity="HIGH",
            unbonding_period="즉시 (스왑 가능)",
            min_stake=0.01,
            commission=0.5,
            description="Kamino 자동화 Vault. JitoSOL 활용 레버리지/차익거래 전략",
            url="https://kamino.finance/vaults",
            pros=["자동 복리", "전략 최적화", "높은 유동성"],
            cons=["전략 리스크", "수수료 발생", "청산 리스크 (레버리지 시)"],
        ),
        StakingOption(
            name="Sanctum Reserve",
            category="📈 Vault / 자동화",
            token_symbol="SOL",
            apy_low=6.5, apy_high=8.0,
            tvl_sol=1_000_000,
            risk_level="MEDIUM",
            liquidity="HIGH",
            unbonding_period="즉시",
            min_stake=0.01,
            commission=0.3,
            description="Sanctum 유동성 예치. LST 간 차익거래 자동화",
            url="https://sanctum.so/reserve",
            pros=["유동성 제공 보상", "자동 최적화", "낮은 진입 장벽"],
            cons=["비영구적 손실 가능", "수수료", "신규 기능"],
        ),
        StakingOption(
            name="Ethena (USDe/sUSDe SOL 기반)",
            category="📈 Vault / 자동화",
            token_symbol="sUSDe",
            apy_low=10.0, apy_high=25.0,
            tvl_sol=None,
            risk_level="VERY_HIGH",
            liquidity="MEDIUM",
            unbonding_period="7~14일 (언스테이킹)",
            min_stake=0.01,
            commission=0.0,
            description="Ethena의 SOL 기반 델타-뉴트럴 전략. 높은 수익률",
            url="https://ethena.fi/",
            pros=["매우 높은 수익률", "페깅 안정성 (USDe)", "성장 중"],
            cons=["매우 높은 리스크", "페깅 붕괴 가능성", "복잡한 구조", "델타-뉴트럴 실패 리스크"],
        ),

        # ── DEX LP / 유동성 공급 ──
        StakingOption(
            name="Orca Whirlpool (JitoSOL/SOL)",
            category="🌊 DEX LP",
            token_symbol="LP",
            apy_low=5.0, apy_high=15.0,
            tvl_sol=None,
            risk_level="HIGH",
            liquidity="MEDIUM",
            unbonding_period="즉시 (풀 출금)",
            min_stake=0.1,
            commission=0.3,
            description="Orca 집중 유동성 풀에 JitoSOL/SOL 쌍 공급",
            url="https://www.orca.so/",
            pros=["높은 거래 수수료 수익", "집중 유동성으로 효율적", "ORCA 토큰 보상 가능"],
            cons=["비영구적 손실 (IL)", "가격 범위 관리 필요", "스마트 컨트랙트 리스크"],
        ),
        StakingOption(
            name="Raydium LP (JitoSOL/SOL)",
            category="🌊 DEX LP",
            token_symbol="LP",
            apy_low=4.0, apy_high=12.0,
            tvl_sol=None,
            risk_level="HIGH",
            liquidity="MEDIUM",
            unbonding_period="즉시 (풀 출금)",
            min_stake=0.1,
            commission=0.25,
            description="Raydium CLMM 풀에 JitoSOL/SOL 쌍 공급",
            url="https://raydium.io/",
            pros=["자동 복리 옵션", "거래 수수료 수익", "RAY 보상 가능"],
            cons=["비영구적 손실", "관리 필요", "수수료 지불"],
        ),
    ]


# ═══════════════════════════════════════════════════
# 실시간 데이터 수집
# ═══════════════════════════════════════════════════

def get_sol_price() -> Optional[float]:
    """CoinGecko에서 SOL 가격 가져오기"""
    if not HAS_REQUESTS:
        return None
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()["solana"]["usd"]
    except Exception:
        pass
    return None


def get_sanctum_lst_apy() -> dict:
    """Sanctum API에서 LST APY 가져오기"""
    if not HAS_REQUESTS:
        return {}
    results = {}
    apis = [
        ("https://sanctum.so/api/v1/apy", "sanctum"),
        ("https://app.jito.network/api/v1/stake-pool-apy", "jito"),
    ]
    for url, name in apis:
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                results[name] = resp.json()
        except Exception:
            pass
    return results


def get_marinade_apy() -> Optional[float]:
    """Marinade API에서 APY 가져오기"""
    if not HAS_REQUESTS:
        return None
    try:
        url = "https://api.marinade.finance/msol/apy"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("apy") or data.get("state") or data
    except Exception:
        pass
    return None


# ═══════════════════════════════════════════════════
# 출력 함수
# ═══════════════════════════════════════════════════

# 터미널 색상
class C:
    """ANSI Color Codes"""
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BG_DARK = '\033[48;5;236m'

    @staticmethod
    def risk_color(level: str) -> str:
        colors = {
            "LOW": C.GREEN,
            "MEDIUM": C.YELLOW,
            "HIGH": C.RED,
            "VERY_HIGH": f"{C.RED}{C.BOLD}",
        }
        return colors.get(level, C.WHITE)

    @staticmethod
    def liquidity_color(level: str) -> str:
        colors = {
            "HIGH": C.GREEN,
            "MEDIUM": C.YELLOW,
            "LOW": C.RED,
            "NONE": f"{C.RED}{C.BOLD}",
        }
        return colors.get(level, C.WHITE)


def print_header():
    """헤더 출력"""
    print(f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   🪙  솔라나(SOL) 스테이킹 수익률 비교 분석 리포트                       ║
║       Solana Staking Yield Comparison Dashboard                          ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝{C.RESET}
""")
    print(f"  기준 데이터: {DATA_SNAPSHOT_DATE} | API 값은 실행 시 조회, 실패 시 정적 범위 사용\n")


def print_sol_price(price: Optional[float]):
    """SOL 가격 출력"""
    if price:
        print(f"  {C.YELLOW}💰 SOL 현재 가격: ${price:,.2f}{C.RESET}\n")
    else:
        print(f"  {C.DIM}💰 SOL 가격: (API 연결 불가 - CoinGecko){C.RESET}\n")


def print_summary_table(options: list[StakingOption]):
    """요약 비교 테이블 출력"""
    print(f"  {C.BOLD}📊 스테이킹 수익률 비교 요약{C.RESET}")
    print(f"  {'='*90}")
    print(f"  {C.BOLD}{'프로토콜':<28} {'카테고리':<16} {'예상 APY':>12} {'리스크':>10} {'유동성':>10} {'수수료':>8}{C.RESET}")
    print(f"  {'-'*28} {'-'*16} {'-'*12} {'-'*10} {'-'*10} {'-'*8}")

    # 카테고리별로 그룹화
    categories_order = [
        "🏛️ 네이티브 스테이킹",
        "💧 리퀴드 스테이킹",
        "🏦 DeFi 렌딩",
        "🔄 레스테이킹",
        "📈 Vault / 자동화",
        "🌊 DEX LP",
    ]

    for cat in categories_order:
        cat_options = [o for o in options if o.category == cat]
        if not cat_options:
            continue

        print(f"  {C.CYAN}{C.BOLD}{cat}{C.RESET}")

        for opt in cat_options:
            apy_str = f"{opt.apy_low:.1f}~{opt.apy_high:.1f}%"
            if opt.real_apy is not None:
                apy_str = f"{opt.real_apy:.2f}%*"

            risk_c = C.risk_color(opt.risk_level)
            liq_c = C.liquidity_color(opt.liquidity)

            name_display = opt.name[:26]
            if opt.token_symbol != "SOL" and opt.token_symbol != "LP":
                name_display += f" ({opt.token_symbol})"

            print(f"    {name_display:<28} {opt.category.split(' ')[1] if ' ' in opt.category else '':<16} "
                  f"{C.GREEN}{apy_str:>12}{C.RESET} "
                  f"{risk_c}{opt.risk_level:>10}{C.RESET} "
                  f"{liq_c}{opt.liquidity:>10}{C.RESET} "
                  f"{opt.commission:>7.1f}%")

        print()

    print(f"  {'='*90}")


def print_detailed_analysis(options: list[StakingOption]):
    """상세 분석 출력"""
    print(f"\n  {C.BOLD}📋 상세 분석{C.RESET}")
    print(f"  {'='*90}")

    categories_order = [
        "🏛️ 네이티브 스테이킹",
        "💧 리퀴드 스테이킹",
        "🏦 DeFi 렌딩",
        "🔄 레스테이킹",
        "📈 Vault / 자동화",
        "🌊 DEX LP",
    ]

    for cat in categories_order:
        cat_options = [o for o in options if o.category == cat]
        if not cat_options:
            continue

        print(f"\n  {C.CYAN}{C.BOLD}{cat}{C.RESET}")
        print(f"  {'─'*80}")

        for opt in cat_options:
            risk_c = C.risk_color(opt.risk_level)
            liq_c = C.liquidity_color(opt.liquidity)

            apy_str = f"{opt.apy_low:.1f}% ~ {opt.apy_high:.1f}%"
            if opt.real_apy is not None:
                apy_str += f" (실시간: {opt.real_apy:.2f}%)"

            print(f"""
  {C.BOLD}{opt.name}{C.RESET} [{opt.token_symbol}]
    📊 예상 APY    : {C.GREEN}{apy_str}{C.RESET}
    💰 TVL (SOL)   : {f"{opt.tvl_sol:,.0f}" if opt.tvl_sol else "N/A":>12}
    ⚠️  리스크     : {risk_c}{opt.risk_level}{C.RESET}
    🔄 유동성      : {liq_c}{opt.liquidity}{C.RESET}
    ⏰ 언본딩      : {opt.unbonding_period}
    💵 최소 금액   : {opt.min_stake} SOL
    📝 설명        : {opt.description}
    🔗 URL         : {C.BLUE}{opt.url}{C.RESET}
    ✅ 장점        : {', '.join(opt.pros)}
    ❌ 단점        : {', '.join(opt.cons)}""")

        print()


def print_risk_matrix():
    """리스크 매트릭스 출력"""
    print(f"""
  {C.BOLD}⚖️ 리스크 vs 수익률 매트릭스{C.RESET}
  {'='*90}

  수익률 ↑
   25% │                                                    {C.RED}■{C.RESET} Ethena
       │
   20% │
       │
   15% │                               {C.RED}■{C.RESET} Solayer        {C.RED}■{C.RESET} DEX LP
       │
   10% │              {C.YELLOW}■{C.RESET} Jito Restaking
       │                               {C.YELLOW}■{C.RESET} Picasso        {C.YELLOW}■{C.RESET} Kamino Vault
    7% │ {C.GREEN}■{C.RESET} Native   {C.GREEN}■{C.RESET} JitoSOL  {C.GREEN}■{C.RESET} Marinade
       │ {C.GREEN}■{C.RESET} Sanctum   {C.GREEN}■{C.RESET} BlazeStake
    5% │              {C.YELLOW}■{C.RESET} MarginFi
       │              {C.YELLOW}■{C.RESET} Kamino Lend    {C.YELLOW}■{C.RESET} Drift
    2% │
       └──────────────────────────────────────────────────→ 리스크
          {C.GREEN}LOW{C.RESET}          {C.YELLOW}MEDIUM{C.RESET}              {C.RED}HIGH{C.RESET}         {C.RED}VERY_HIGH{C.RESET}
""")


def print_recommendations():
    """투자 성향별 추천 출력"""
    print(f"""
  {C.BOLD}🎯 투자 성향별 추천 전략{C.RESET}
  {'='*90}

  {C.GREEN}{C.BOLD}🟢 보수형 (안전 최우선){C.RESET}
  ──────────────────────────────────────
  1위: {C.BOLD}네이티브 스테이킹{C.RESET} - 스마트 컨트랙트 리스크 제로
  2위: {C.BOLD}Jito (JitoSOL){C.RESET} - MEV 보너스 + 높은 안전성
  3위: {C.BOLD}Marinade (mSOL){C.RESET} - 검증된 프로토콜

  💡 추천: 자본의 70% 네이티브 스테이킹 + 30% JitoSOL

  {C.YELLOW}{C.BOLD}🟡 중립형 (수익/안정 균형){C.RESET}
  ──────────────────────────────────────
  1위: {C.BOLD}Jito (JitoSOL){C.RESET} - 최고의 수익/안정 균형
  2위: {C.BOLD}Kamino Vault{C.RESET} - 자동 복리 전략
  3위: {C.BOLD}Sanctum Reserve{C.RESET} - 유동성 + 최적화

  💡 추천: 50% JitoSOL + 30% Kamino Vault + 20% Sanctum

  {C.RED}{C.BOLD}🔴 공격형 (최대 수익 추구){C.RESET}
  ──────────────────────────────────────
  1위: {C.BOLD}Ethena (sUSDe){C.RESET} - 10~25% APY (매우 높은 리스크)
  2위: {C.BOLD}Solayer{C.RESET} - 레스테이킹 + 에어드랍 기대
  3위: {C.BOLD}Orca/Raydium LP{C.RESET} - 거래 수수료 + IL 리스크

  💡 추천: 40% JitoSOL + 30% Solayer + 20% Jito Restaking + 10% LP

  {C.MAGENTA}{C.BOLD}🟣 DeFi 파워 유저{C.RESET}
  ──────────────────────────────────────
  1위: {C.BOLD}JitoSOL → Kamino Vault{C.RESET} - 레버리지 복리
  2위: {C.BOLD}JitoSOL → Orca LP{C.RESET} - 집중 유동성 수익
  3위: {C.BOLD}mSOL → MarginFi 담보{C.RESET} - 대출 + 레버리지

  💡 추천: LST를 담보로 레버리지 루핑 (청산 리스크 주의!)
""")


def print_tax_tips():
    """세금/주의사항 출력"""
    print(f"""
  {C.BOLD}⚠️ 주의사항 & 세금{C.RESET}
  {'='*90}

  📌 세금 (한국 기준)
  • 스테이킹 보상은 {C.YELLOW}기타소득{C.RESET}으로 분류 가능 (2025년 이전)
  • 2025년부터 {C.YELLOW}가상자산소득세{C.RESET} 과세 (연 250만원 이상)
  • LST 토큰 스왑 시 {C.YELLOW}양도소득세{C.RESET} 발생 가능
  • 실현 수익만 과세 (미실현 보상은 X)

  📌 리스크 체크리스트
  • {C.GREEN}□{C.RESET} 밸리데이터 평판/성과 확인
  • {C.GREEN}□{C.RESET} 프로토콜 감사(audit) 여부
  • {C.GREEN}□{C.RESET} TVL 규모와 유동성
  • {C.GREEN}□{C.RESET} 스마트 컨트랙트 버그 리스크
  • {C.GREEN}□{C.RESET} 슬래싱 가능 여부
  • {C.GREEN}□{C.RESET} 언본딩 기간 숙지

  📌 모니터링 추천 도구
  • Sanctum: https://sanctum.so/ (LST 비교)
  • Jito: https://jito.network/ (MEV 스테이킹)
  • Solana Compass: https://solanacompass.com/ (밸리데이터)
  • DeFiLlama: https://defillama.com/chain/Solana (TVL)
""")


def print_simulation(options: list[StakingOption], sol_price: Optional[float]):
    """수익 시뮬레이션"""
    print(f"\n  {C.BOLD}💰 수익 시뮬레이션 (100 SOL 기준, 1년){C.RESET}")
    print(f"  {'='*90}")

    if sol_price:
        sol_val = 100 * sol_price
        print(f"  투자금액: 100 SOL = ${sol_val:,.2f}\n")

    principal_sol = 100

    # 카테고리별 대표 옵션만
    picks = {
        "🏛️ 네이티브 스테이킹": next((o for o in options if o.category == "🏛️ 네이티브 스테이킹"), None),
        "💧 JitoSOL": next((o for o in options if "JitoSOL" in o.token_symbol or "Jito (" in o.name), None),
        "💧 mSOL": next((o for o in options if "mSOL" in o.token_symbol), None),
        "🏦 DeFi 렌딩": next((o for o in options if o.category == "🏦 DeFi 렌딩"), None),
        "🔄 Solayer": next((o for o in options if "Solayer" in o.name), None),
        "📈 Kamino Vault": next((o for o in options if "Kamino Vault" in o.name), None),
    }

    print(f"  {'방식':<24} {'APY(평균)':>10} {'1년 후 SOL':>12} {'SOL 수익':>10} {'USD 수익*':>14}")
    print(f"  {'-'*24} {'-'*10} {'-'*12} {'-'*10} {'-'*14}")

    for label, opt in picks.items():
        if not opt:
            continue
        avg_apy = (opt.apy_low + opt.apy_high) / 2
        final_sol = principal_sol * (1 + avg_apy / 100)
        sol_gain = final_sol - principal_sol
        usd_gain = sol_gain * sol_price if sol_price else 0

        apy_str = f"{avg_apy:.1f}%"
        final_str = f"{final_sol:.2f}"
        gain_str = f"+{sol_gain:.2f}"
        usd_str = f"${usd_gain:,.2f}" if sol_price else "N/A"

        print(f"  {label:<24} {C.GREEN}{apy_str:>10}{C.RESET} {final_str:>12} "
              f"{C.GREEN}{gain_str:>10}{C.RESET} {C.YELLOW}{usd_str:>14}{C.RESET}")

    # 복리 효과 (월 복리)
    print(f"\n  {C.DIM}* 복리 효과 미적용 (단리 기준). 월 복리 시 수익 약 5~15% 추가{C.RESET}")
    if sol_price:
        print(f"  {C.DIM}* USD 수익은 현재 SOL 가격 기준. 실제 수익은 SOL 가격 변동에 따라 다름{C.RESET}")


def print_category_summary():
    """카테고리별 요약"""
    print(f"""
  {C.BOLD}📋 카테고리별 한 줄 요약{C.RESET}
  {'='*90}

  {C.GREEN}🏛️ 네이티브 스테이킹{C.RESET}
     → {C.BOLD}가장 안전{C.RESET}. 스마트 컨트랙트 리스크 없음. 6.3~7.2% APY.
     → 추천 대상: 보수적 투자자, 장기 홀더

  {C.CYAN}💧 리퀴드 스테이킹{C.RESET}
     → {C.BOLD}안전 + 유동성{C.RESET}. JitoSOL이 수익률 1위. 6.5~8.0% APY.
     → 추천 대상: 대부분의 투자자 (가장 인기)

  {C.YELLOW}🏦 DeFi 렌딩{C.RESET}
     → {C.BOLD}낮은 수익, 높은 유동성{C.RESET}. 담보로 활용 가능. 1~5% APY.
     → 추천 대상: 레버리지 전략, 단기 예치

  {C.RED}🔄 레스테이킹{C.RESET}
     → {C.BOLD}높은 수익, 높은 리스크{C.RESET}. 에어드랍 기대. 7~15% APY.
     → 추천 대상: 공격적 투자자, 에어드랍 헌터

  {C.MAGENTA}📈 Vault / 자동화{C.RESET}
     → {C.BOLD}전략형 수익{C.RESET}. 자동 복리. 6.5~25% APY (리스크 다양).
     → 추천 대상: 수동 관리 피하고 싶은 투자자

  {C.BLUE}🌊 DEX LP{C.RESET}
     → {C.BOLD}높은 변동 수익{C.RESET}. IL 리스크. 4~15% APY.
     → 추천 대상: DeFi 숙련자, 적극적 관리 가능
""")


# ═══════════════════════════════════════════════════
# 메인 실행
# ═══════════════════════════════════════════════════

def main():
    print_header()

    # 데이터 수집
    sol_price = get_sol_price()
    print_sol_price(sol_price)

    # 스테이킹 옵션 로드
    options = get_staking_options()

    # 실시간 데이터 시도
    print(f"  {C.DIM}📡 실시간 데이터 수집 중...{C.RESET}")
    marinade_apy = get_marinade_apy()
    if marinade_apy and isinstance(marinade_apy, (int, float)):
        for opt in options:
            if "Marinade" in opt.name:
                opt.real_apy = float(marinade_apy)
                print(f"  {C.GREEN}✅ Marinade 실시간 APY: {marinade_apy:.2f}%{C.RESET}")
    else:
        print(f"  {C.DIM}⚠️ Marinade API: 연결 불가{C.RESET}")

    print()

    # 출력
    print_summary_table(options)
    print_risk_matrix()
    print_category_summary()
    print_simulation(options, sol_price)
    print_detailed_analysis(options)
    print_recommendations()
    print_tax_tips()

    # 푸터
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"  {C.DIM}분석 일시: {now} | 데이터 출처: CoinGecko, Marinade API, 프로토콜 공식 자료{C.RESET}")
    print(f"  {C.DIM}※ 수익률은 예상치이며 실제와 다를 수 있습니다. 투자 전 DYOR!{C.RESET}")
    print(f"  {C.DIM}※ API로 가져온 실시간 데이터는 * 표시{C.RESET}\n")


if __name__ == "__main__":
    main()
