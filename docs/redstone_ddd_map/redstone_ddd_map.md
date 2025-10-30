---
tags: [DDD, DeFi, Oracle, RedStone, JustJoinIT]
alias: [RedStone DDD Map, RedStone Company]
---

# RedStone — DDD Map

## 1) Firma – skrót
RedStone to dostawca **modularnego oracla** dla blockchainów. Zapewnia zaufane **dane on-chain** dla protokołów DeFi i instytucji, tak aby smart kontrakty mogły podejmować bezpieczne i szybkie decyzje.

## 2) Rozszerzony opis firmy
- **Produkty:**  
  - **Price Feeds** – publikacja wycen aktywów (tryby: *push*, *pull*, **atom/OEV**).  
  - **Proof of Reserve (PoR)** – kryptograficzne/dokumentacyjne potwierdzenie rezerw (CEX/custodian/on-chain).  
  - **Atom (OEV)** – atomowa aktualizacja ceny w *tej samej transakcji*, minimalizuje MEV/front-running.
- **Wartość biznesowa:** stabilne i odporne na manipulacje wyceny, przejrzystość rezerw, niezawodność integracji **multi-chain** (quorum, failover, SLO).  
- **Adresaci:** protokoły pożyczkowe/likwidacyjne, DEX/derywaty, emitenci RWA/stable, instytucje.

## 3) DDD – Domeny
**Core Domain:** zaufane wyceny on-chain dla smart kontraktów.  
**Supporting:** Integracje/BD, Monitoring & Reliability, Security & Staking, Billing, DX, Compliance/PoR.

## 4) Bounded Contexts
- **Data Ingestion** – źródła CEX/DEX/agregatory → normalizacja, anty-spoofing.  
  Encje: `Source`, `Market`, `TickStream`, `QualityScore`.  
  Zdarzenia: `SourceOutageDetected`, `AbnormalSpreadDetected`.
- **Aggregation & Pricing** – mediany/kwantyle/filtry → *canonical price*.  
  Encje: `PriceFeed`, `AggregationWindow`, `DeviationPolicy`.  
  Reguły: aktualizuj przy `deviation ≥ Δ`, odrzuć niskie `QualityScore`.
- **On-chain Publishing** – *push/pull/atom*, podpisy, heartbeat, finality.  
  Encje: `ChainEndpoint`, `GasBudget`, `FeedConfig`.  
  Zdarzenia: `FeedPushed`, `HeartbeatMissed`, `OnChainReorgDetected`.
- **Proof of Reserve** – zaciąganie danych rezerw → dowód → publikacja.  
  Zdarzenia: `ReserveProofVerified`, `ReserveMismatchAlert`.
- **Security & Staking** – walidatorzy, staking/slashing, audyty.  
  Encje: `Validator`, `Stake`, `AuditReport`.
- **Client Integrations** – onboarding, adaptery/SDK, SLA, custom feedy.  
  Zdarzenia: `ClientOnboarded`, `SLAChanged`, `CustomFeedRequested`.
- **Monitoring & Reliability** – SLO/latencja/availability, alerting, *data gaps*.  
  Zdarzenia: `LatencySLOBreached`, `DataGapDetected`.
- **Billing & Entitlements** – plany, zużycie, rozliczenia, limity.  
  Encje: `Plan`, `UsageRecord`, `Invoice`.
- **Developer Experience (DX)** – dokumentacja, przykłady, sandbox.

## 5) Ubiquitous Language
**Feed**, **Heartbeat**, **Deviation Threshold**, **Atom/OEV**, **Proof of Reserve**, **Canonical Price**, **Quorum**, **Failover**.

## 6) Event Storming – szkic
`TickReceived → TickValidated → WindowAggregated → PriceDerived → PublishDecisionMade → PricePushed/Pulled`  
Bezpieczeństwo: `AnomalyDetected → SourceQuarantined → FailoverActivated`  
PoR: `ReserveDataFetched → ProofConstructed → ProofVerified → PoRPublished`

## 7) Ryzyka & Polityki
- Latencja/MEV/front-running → **Atom/OEV**, kolejki priorytetowe.  
- Awaria źródeł → **multi-source + quorum + failover**.  
- Reorgi/Gas → **retry + idempotencja**, monitor reorgów.  
- Compliance → audyty, polityki, ścieżka audytowa.

## 8) Leadership (public info)
- **Founder/CEO:** Jakub Wojciechowski  
- **Co-founders:** Marcin Kaźmierczak, Alex Suvorov  
- **Head of BD:** Matt Gurbiel  

## 9) Źródła (do dalszego drążenia)
- Ogłoszenie (Just Join IT) – wymagania, stack, proces rekrutacyjny.  
- Strona główna **redstone.finance** – produkty, skala, audyty.  
- **Price Feeds – FAQ/Docs** – modele push/pull/atom, źródła, częstotliwości, bezpieczeństwo.  
- **Proof of Reserve – opis** – klasy aktywów, proces publikacji.  
- Materiały ekosystemowe (np. Base/TON) – adopcja i integracje.

## 10) KPI – kluczowe wskaźniki
- **Engineering:** Lead time (P95), MTTR, % rollbacków.  
- **Data/Quality:** % odrzuconych ticków, MAE/APE vs benchmark, czas agregacji okna.  
- **On-chain Publishing:** P95 opóźnienie vs heartbeat/deviation, % nieudanych tx, koszt gas/update.  
- **PoR:** zgodność z polityką odświeżeń, czas weryfikacji, *false positives*.  
- **Monitoring & Reliability:** SLO (np. 99.9%), *alert fatigue*, *data gap rate*.  
- **BD/Integrations:** time-to-first-price, aktywne integracje/miesiąc, NPS/CSAT.  
- **DX:** czas „Hello World” z SDK, % issue <48h, konwersja docs→POC.  
- **Billing:** ARPA/MRR, % throttlingu, DSO.  
- **Compliance:** audyty on-time, # niezgodności, TTR na zapytania.

## 11) Questions to ask – na rozmowę (po 5)
**BD / Partnerships**  
1. Najczęstsze „adoption blockers” (SLA, gas, governance) i jak je zdejmujecie?  
2. Definicja „aktywnej integracji” i metryki zdrowia (usage, alerts, churn).  
3. Priorytety roadmapy feedów (wolumen, ryzyko, klienci, koszty)?  
4. Jak wygląda time-to-first-price od podpisania do produkcji?  
5. Oczekiwania wobec DS/Backend w pre-sell/POC/tuningu parametrów?

**Engineering (On-/Off-chain)**  
1. Model update’u feedów (heartbeat/deviation/atom) i docelowe SLO per klasa aktywów.  
2. Failover/quorum między źródłami i zasady degradacji przy anomaliach.  
3. Pipeline CI/CD dla kontraktów i workerów (testy, canary, feature flags).  
4. Optymalizacja gas (batching, kompresja, calldata) vs bezpieczeństwo.  
5. Największy dług tech i plan spłaty (impact vs effort).

**Compliance / Proof of Reserve**  
1. Polityki odświeżania i zakres PoR dla klas aktywów (CEX/custodian/RWA/LST).  
2. Walidacja źródeł PoR i procedury przy `ReserveMismatch`.  
3. Standardy/audyty i częstotliwość (attestations, zewnętrzne raporty).  
4. Metadane i ścieżka audytowa (kto/co/kiedy), retencja.  
5. Wymagania regulatorów/partnerów dot. transparentności i granice „wystarczająco dobrze”.
## Leadership ↔ Produkty/Konteksty (RACI)

**Legenda:** A – Accountable, R – Responsible, C – Consulted, I – Informed

| Obszar / Artefakt             | Founder/CEO (J. Wojciechowski) | Co-founders (Tech: M. Kaźmierczak, A. Suvorov) | Head of BD (M. Gurbiel) |
| ---                           | ---                             | ---                                            | ---                      |
| **Price Feeds (produkt)**     | A                               | R                                              | C                        |
| **Proof of Reserve (produkt)**| A                               | R                                              | R                        |
| **Atom / OEV (produkt)**      | A                               | A/R                                            | C                        |
| **Data Ingestion**            | I                               | A/R                                            | I                        |
| **Aggregation & Pricing**     | C                               | A/R                                            | I                        |
| **On-chain Publishing**       | I                               | A/R                                            | I                        |
| **Security & Staking**        | A                               | R                                              | I                        |
| **Monitoring & Reliability**  | A                               | R                                              | I                        |
| **Client Integrations**       | C                               | C                                              | A/R                      |
| **Billing & Entitlements**    | A                               | I                                              | R                        |
| **Developer Experience (DX)** | C                               | R                                              | R                        |
| **Compliance / PoR**          | A                               | C                                              | C                        |
| **Ryzyka & Polityki**         | A                               | C                                              | C                        |
### Subskrypcje zdarzeń (co jest krytyczne dla której roli)

- **Founder/CEO**
  - `ReserveMismatchAlert`, `LatencySLOBreached`, `MajorIncidentCreated`
  - KPI przeglądowe: uptime/SLO, koszt gas per update (trend), adopcja produktów

- **Co-founders (Tech)**
  - `AbnormalSpreadDetected`, `SourceOutageDetected`
  - `HeartbeatMissed`, `OnChainReorgDetected`, `DataGapDetected`, `FeedPushed`
  - KPI: błąd vs benchmark (MAE/APE), P95 latencja agregacji/publikacji

- **Head of BD**
  - `ClientOnboarded`, `SLAChanged`, `CustomFeedRequested`, `ChurnRiskDetected`
  - KPI: time-to-first-price, aktywne integracje/m-c, NPS/CSAT, MRR/NRR

