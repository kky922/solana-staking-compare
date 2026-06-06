# 🪙 솔라나(SOL) 스테이킹 수익률 비교 대시보드

> Solana Staking Yield Comparison Dashboard  
> 네이티브 스테이킹, 리퀴드 스테이킹, DeFi 렌딩, 레스테이킹 등 **18개 프로토콜** 비교 분석

---

## 📊 빠른 실행

```bash
# 터미널 리포트 (CLI)
cd ~/solana
python3 sol_staking_compare.py

# 웹 대시보드 (Streamlit)
cd ~/solana
streamlit run sol_dashboard.py --server.port 8555

# 또는 실행 스크립트
bash start_sol_dashboard.sh
```

접속: **http://localhost:8555**

---

## 🔄 데이터 최신화 (리프레시) 안내

| 방법 | 데이터 갱신 여부 | 설명 |
|---|---|---|
| **F5 / 브라우저 새로고침** | ⚡ 캐시 5분 경과 시 자동 | `@st.cache_data(ttl=300)` 설정 |
| **사이드바 "🔄 데이터 새로고침" 버튼** | ✅ **즉시 갱신** | 캐시 삭제 → API 재호출 |
| **SOL 가격** | ✅ 실시간 | CoinGecko API (`api.coingecko.com`) |
| **Marinade APY** | ✅ 실시간 (연결 시) | Marinade API (`api.marinade.finance`) |
| **프로토콜 기본 APY** | ⚠️ 하드코딩 | 코드 수정으로 업데이트 필요 |

> 💡 **권장:** 대시보드 열 때마다 사이드바 **"🔄 데이터 새로고침"** 버튼 클릭 → 확실한 최신화

---

## 📋 전체 프로토콜 비교 테이블

### 🏛️ 네이티브 스테이킹

| 프로토콜 | APY | 리스크 | 유동성 | 언본딩 | 수수료 | 최소금액 |
|---|---|---|---|---|---|---|
| **네이티브 스테이킹 (직접 위임)** | 6.3~7.2% | 🟢 LOW | 🔴 LOW | 2~3일 (1 epoch) | 0% | 0.01 SOL |

- **설명:** 밸리데이터에 SOL을 직접 위임하는 가장 기본적인 방식
- ✅ **장점:** 가장 안전 (스마트 컨트랙트 리스크 없음), 인플레이션 보상 직접 수령, 탈중앙화에 기여
- ❌ **단점:** 유동성 없음 (언본딩 필요), 밸리데이터 선택 필요, 복리 불가 (수동 컴파운딩)
- 🔗 https://solana.com/staking

---

### 💧 리퀴드 스테이킹 (Liquid Staking)

| 프로토콜 | 토큰 | APY | TVL (SOL) | 리스크 | 유동성 | 언본딩 | 수수료 |
|---|---|---|---|---|---|---|---|
| **Jito (JitoSOL)** | JitoSOL | 6.8~8.0% | 14,000,000 | 🟢 LOW | 🟢 HIGH | 즉시 (스왑) | 0% |
| **Marinade Finance (mSOL)** | mSOL | 6.5~7.5% | 6,500,000 | 🟢 LOW | 🟢 HIGH | 즉시/1 epoch | 0% |
| **Sanctum (infSOL)** | infSOL | 6.5~7.3% | 3,000,000 | 🟢 LOW | 🟢 HIGH | 즉시 (스왑) | 0% |
| **BlazeStake (bSOL)** | bSOL | 6.5~7.3% | 1,500,000 | 🟢 LOW | 🟡 MEDIUM | 즉시 (스왑) | 0% |
| **Rocket Pool (rSOL)** | rSOL | 6.3~7.0% | 500,000 | 🟢 LOW | 🟡 MEDIUM | 즉시 (스왑) | 0% |

#### 상세 정보

**Jito (JitoSOL)**
- 📝 Jito MEV 기반 리퀴드 스테이킹. MEV 팁 수익 추가 분배
- ✅ MEV 보너스로 높은 수익률, 높은 유동성, DeFi에서 담보 활용 가능, 가장 큰 LST 중 하나
- ❌ JitoSOL/SOL 프리미엄 변동, 스마트 컨트랙트 리스크, Jito 밸리데이터 집중도
- 🔗 https://jito.network/staking/

**Marinade Finance (mSOL)**
- 📝 Marinade 자동 밸리데이터 분산 위임 리퀴드 스테이킹
- ✅ 자동 밸리데이터 최적화, 탈중앙화 기여, DeFi 생태계 광범위, 오래된 프로토콜
- ❌ Jito 대비 낮은 수익률, mSOL/SOL 스프레드
- 🔗 https://marinade.finance/

**Sanctum (infSOL)**
- 📝 Sanctum의 무한(infinite) 리퀴드 스테이킹 프로토콜
- ✅ LST 간 즉시 스왑, 다양한 밸리데이터 지원, 점진적 탈중앙화
- ❌ 상대적으로 신규 프로토콜, 유동성 풀 의존
- 🔗 https://sanctum.so/

**BlazeStake (bSOL)**
- 📝 BlazeStake 리퀴드 스테이킹. 자동 밸리데이터 분배
- ✅ 자동 분배, DeFi 통합, 에어드랍 가능성
- ❌ 낮은 유동성, 더 작은 생태계
- 🔗 https://stake.solblaze.org/

**Rocket Pool (rSOL)**
- 📝 Rocket Pool의 솔라나 리퀴드 스테이킹
- ✅ 이더리움에서 검증된 프로토콜, 탈중앙화 중심
- ❌ 솔라나에서는 상대적으로 작음, 낮은 유동성
- 🔗 https://rocketpool.net/

---

### 🏦 DeFi 렌딩

| 프로토콜 | APY | TVL (SOL) | 리스크 | 유동성 | 언본딩 | 수수료 |
|---|---|---|---|---|---|---|
| **MarginFi (SOL 렌딩)** | 2.0~5.0% | 2,000,000 | 🟡 MEDIUM | 🟢 HIGH | 즉시 | 0% |
| **Kamino Lend (SOL)** | 1.5~4.0% | 3,000,000 | 🟡 MEDIUM | 🟢 HIGH | 즉시 | 0% |
| **Drift Lend (SOL)** | 1.0~3.5% | 1,500,000 | 🟡 MEDIUM | 🟢 HIGH | 즉시 | 0% |

#### 상세 정보

**MarginFi**
- 📝 MarginFi 렌딩 프로토콜에 SOL 예치
- ✅ 높은 유동성, 담보로 활용 가능, 변동 금리
- ❌ 낮은 수익률, 청산 리스크 (레버리지 시), 대출 수요에 따른 변동
- 🔗 https://www.marginfi.com/

**Kamino Lend**
- 📝 Kamino 렌딩 시장에 SOL 예치
- ✅ 높은 유동성, 자동화된 전략, 담보 활용
- ❌ 낮은 수익률, 대출 수요 의존, 스마트 컨트랙트 리스크
- 🔗 https://kamino.finance/

**Drift Lend**
- 📝 Drift Protocol 렌딩에 SOL 예치
- ✅ 빠른 예출금, 담보 활용, 다양한 자산 쌍
- ❌ 가장 낮은 렌딩 수익률 중 하나, 변동성 큼
- 🔗 https://www.drift.trade/

---

### 🔄 레스테이킹 (Restaking)

| 프로토콜 | 토큰 | APY | TVL (SOL) | 리스크 | 유동성 | 언본딩 | 수수료 |
|---|---|---|---|---|---|---|---|
| **Jito Restaking** | JitoSOL | 8.0~12.0% | 5,000,000 | 🟡 MEDIUM | 🟡 MEDIUM | 프로토콜별 | 0% |
| **Solayer (sSOL)** | sSOL | 8.0~15.0% | 4,000,000 | 🔴 HIGH | 🟡 MEDIUM | 불명확 | 0% |
| **Picasso (pSOL)** | pSOL | 7.0~12.0% | 1,000,000 | 🔴 HIGH | 🔴 LOW | 프로토콜별 | 0% |

#### 상세 정보

**Jito Restaking**
- 📝 Jito VRT (Vault Receipt Token) 기반 레스테이킹. AVS에 보안 제공
- ✅ 추가 보상 (AVS 인센티브), JitoSOL 기반 안전, 성장 중인 생태계
- ❌ 슬래싱 리스크 가능, 아직 초기 단계, 보상 불확실
- 🔗 https://restaking.jito.network/

**Solayer (sSOL)**
- 📝 Solayer 레스테이킹 프로토콜. 공유 보안 및 가속 서비스 제공
- ✅ 높은 잠재적 수익률, 에어드랍 기대, 새로운 인센티브
- ❌ 높은 리스크, 신규 프로토콜, 슬래싱 가능, 초기 단계
- 🔗 https://www.solayer.org/

**Picasso (pSOL)**
- 📝 Picasso 크로스체인 레스테이킹. IBC 기반 연결
- ✅ 크로스체인 보상, 다양한 AVS 참여, 에어드랍 가능성
- ❌ 매우 신규, 낮은 유동성, 복잡한 구조
- 🔗 https://picasso.network/

---

### 📈 Vault / 자동화

| 프로토콜 | 토큰 | APY | TVL (SOL) | 리스크 | 유동성 | 언본딩 | 수수료 |
|---|---|---|---|---|---|---|---|
| **Kamino Vault** | JitoSOL | 7.0~10.0% | 2,500,000 | 🟡 MEDIUM | 🟢 HIGH | 즉시 (스왑) | 0.5% |
| **Sanctum Reserve** | SOL | 6.5~8.0% | 1,000,000 | 🟡 MEDIUM | 🟢 HIGH | 즉시 | 0.3% |
| **Ethena (sUSDe)** | sUSDe | 10.0~25.0% | N/A | 💀 VERY_HIGH | 🟡 MEDIUM | 7~14일 | 0% |

#### 상세 정보

**Kamino Vault (JitoSOL 기반)**
- 📝 Kamino 자동화 Vault. JitoSOL 활용 레버리지/차익거래 전략
- ✅ 자동 복리, 전략 최적화, 높은 유동성
- ❌ 전략 리스크, 수수료 발생, 청산 리스크 (레버리지 시)
- 🔗 https://kamino.finance/vaults

**Sanctum Reserve**
- 📝 Sanctum 유동성 예치. LST 간 차익거래 자동화
- ✅ 유동성 제공 보상, 자동 최적화, 낮은 진입 장벽
- ❌ 비영구적 손실 가능, 수수료, 신규 기능
- 🔗 https://sanctum.so/reserve

**Ethena (USDe/sUSDe)**
- 📝 Ethena의 SOL 기반 델타-뉴트럴 전략. 높은 수익률
- ✅ 매우 높은 수익률, 페깅 안정성 (USDe), 성장 중
- ❌ 매우 높은 리스크, 페깅 붕괴 가능성, 복잡한 구조, 델타-뉴트럴 실패 리스크
- 🔗 https://ethena.fi/

---

### 🌊 DEX LP (유동성 공급)

| 프로토콜 | APY | 리스크 | 유동성 | 언본딩 | 수수료 | 최소금액 |
|---|---|---|---|---|---|---|
| **Orca Whirlpool (JitoSOL/SOL)** | 5.0~15.0% | 🔴 HIGH | 🟡 MEDIUM | 즉시 (풀 출금) | 0.3% | 0.1 SOL |
| **Raydium LP (JitoSOL/SOL)** | 4.0~12.0% | 🔴 HIGH | 🟡 MEDIUM | 즉시 (풀 출금) | 0.25% | 0.1 SOL |

#### 상세 정보

**Orca Whirlpool (JitoSOL/SOL)**
- 📝 Orca 집중 유동성 풀에 JitoSOL/SOL 쌍 공급
- ✅ 높은 거래 수수료 수익, 집중 유동성으로 효율적, ORCA 토큰 보상 가능
- ❌ 비영구적 손실 (IL), 가격 범위 관리 필요, 스마트 컨트랙트 리스크
- 🔗 https://www.orca.so/

**Raydium LP (JitoSOL/SOL)**
- 📝 Raydium CLMM 풀에 JitoSOL/SOL 쌍 공급
- ✅ 자동 복리 옵션, 거래 수수료 수익, RAY 보상 가능
- ❌ 비영구적 손실, 관리 필요, 수수료 지불
- 🔗 https://raydium.io/

---

## 📋 카테고리별 한 줄 요약

| 카테고리 | 특징 | APY 범위 | 추천 대상 |
|---|---|---|---|
| 🏛️ **네이티브 스테이킹** | 가장 안전. 스마트 컨트랙트 리스크 없음 | 6.3~7.2% | 보수적 투자자, 장기 홀더 |
| 💧 **리퀴드 스테이킹** | 안전 + 유동성. JitoSOL이 수익률 1위 | 6.5~8.0% | 대부분의 투자자 (가장 인기) |
| 🏦 **DeFi 렌딩** | 낮은 수익, 높은 유동성. 담보 활용 | 1~5% | 레버리지 전략, 단기 예치 |
| 🔄 **레스테이킹** | 높은 수익, 높은 리스크. 에어드랍 기대 | 7~15% | 공격적 투자자, 에어드랍 헌터 |
| 📈 **Vault / 자동화** | 전략형 수익. 자동 복리 | 6.5~25% | 수동 관리 피하고 싶은 투자자 |
| 🌊 **DEX LP** | 높은 변동 수익. IL 리스크 | 4~15% | DeFi 숙련자, 적극적 관리 가능 |

---

## 🎯 투자 성향별 추천 전략

### 🟢 보수형 (안전 최우선)

| 순위 | 프로토콜 | 이유 |
|---|---|---|
| 1위 | **네이티브 스테이킹** | 스마트 컨트랙트 리스크 제로 |
| 2위 | **Jito (JitoSOL)** | MEV 보너스 + 높은 안정성 |
| 3위 | **Marinade (mSOL)** | 검증된 프로토콜 |

> 💡 **추천 포트폴리오:** 70% 네이티브 스테이킹 + 30% JitoSOL

### 🟡 중립형 (수익/안정 균형)

| 순위 | 프로토콜 | 이유 |
|---|---|---|
| 1위 | **Jito (JitoSOL)** | 최고의 수익/안정 균형 |
| 2위 | **Kamino Vault** | 자동 복리 전략 |
| 3위 | **Sanctum Reserve** | 유동성 + 최적화 |

> 💡 **추천 포트폴리오:** 50% JitoSOL + 30% Kamino Vault + 20% Sanctum

### 🔴 공격형 (최대 수익 추구)

| 순위 | 프로토콜 | 이유 |
|---|---|---|
| 1위 | **Ethena (sUSDe)** | 10~25% APY (매우 높은 리스크) |
| 2위 | **Solayer** | 레스테이킹 + 에어드랍 기대 |
| 3위 | **Orca/Raydium LP** | 거래 수수료 + IL 리스크 |

> 💡 **추천 포트폴리오:** 40% JitoSOL + 30% Solayer + 20% Jito Restaking + 10% LP

### 🟣 DeFi 파워 유저

| 순위 | 전략 | 이유 |
|---|---|---|
| 1위 | **JitoSOL → Kamino Vault** | 레버리지 복리 |
| 2위 | **JitoSOL → Orca LP** | 집중 유동성 수익 |
| 3위 | **mSOL → MarginFi 담보** | 대출 + 레버리지 |

> 💡 **추천:** LST를 담보로 레버리지 루핑 (⚠️ 청산 리스크 주의!)

---

## ⚖️ 리스크 vs 수익률 매트릭스

```
수익률 ↑
 25% │                                                    ■ Ethena
     │
 20% │
     │
 15% │                               ■ Solayer        ■ DEX LP
     │
 10% │              ■ Jito Restaking
     │                               ■ Picasso        ■ Kamino Vault
  7% │ ■ Native   ■ JitoSOL  ■ Marinade
     │ ■ Sanctum   ■ BlazeStake
  5% │              ■ MarginFi
     │              ■ Kamino Lend    ■ Drift
  2% │
     └──────────────────────────────────────────────────→ 리스크
        LOW          MEDIUM              HIGH         VERY_HIGH
```

---

## ⚠️ 세금 & 주의사항 (한국 기준)

### 📌 세금 안내
- 스테이킹 보상은 **기타소득**으로 분류 가능 (2025년 이전)
- 2025년부터 **가상자산소득세** 과세 (연 250만원 이상)
- LST 토큰 스왑 시 **양도소득세** 발생 가능
- 실현 수익만 과세 (미실현 보상은 X)

### 📌 리스크 체크리스트
- ☑ 밸리데이터 평판/성과 확인
- ☑ 프로토콜 감사(audit) 여부
- ☑ TVL 규모와 유동성
- ☑ 스마트 컨트랙트 버그 리스크
- ☑ 슬래싱 가능 여부
- ☑ 언본딩 기간 숙지

### 📌 모니터링 추천 도구
- **Sanctum:** https://sanctum.so/ (LST 비교)
- **Jito:** https://jito.network/ (MEV 스테이킹)
- **Solana Compass:** https://solanacompass.com/ (밸리데이터)
- **DeFiLlama:** https://defillama.com/chain/Solana (TVL)

---

## 🗂️ 파일 구조

```
solana/
├── sol_staking_compare.py   # 데이터 모델 + CLI 리포트 (터미널용)
├── sol_dashboard.py         # Streamlit 웹 대시보드
├── start_sol_dashboard.sh   # 대시보드 실행 스크립트
└── README.md                # 이 파일
```

### `sol_staking_compare.py` — 데이터 엔진
- `StakingOption` 데이터클래스 (18개 프로토콜 정의)
- `get_sol_price()` — CoinGecko 실시간 SOL 가격
- `get_marinade_apy()` — Marinade 실시간 APY
- `get_sanctum_lst_apy()` — Sanctum/Jito LST APY
- CLI 컬러 리포트 출력

### `sol_dashboard.py` — 웹 대시보드
- **탭 1:** 📊 비교 테이블 (정렬/필터 가능)
- **탭 2:** 📈 시각화 차트 (APY 바, 리스크 스캐터, TVL 파이, 히트맵)
- **탭 3:** 🔍 프로토콜 상세 카드
- **탭 4:** 🎯 투자 성향별 추천 전략
- **탭 5:** 💰 수익 시뮬레이터 (SOL 수량/기간/복리 설정)

---

## 📦 의존성

```
streamlit
plotly
pandas
requests
```

설치: `pip install streamlit plotly pandas requests`

---

## 📊 데이터 출처

- **SOL 가격:** [CoinGecko API](https://api.coingecko.com)
- **Marinade APY:** [Marinade API](https://api.marinade.finance)
- **프로토콜 정보:** 각 프로토콜 공식 문서 및 웹사이트
- **TVL 데이터:** DeFiLlama, 프로토콜 공식 대시보드

---

> ⚠️ 수익률은 예상치이며 실제와 다를 수 있습니다. 투자 전 DYOR!