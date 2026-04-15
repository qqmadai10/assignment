# Alpha Factors Analysis for MFE5210

**Course:** MFE5210 Algorithmic Trading  
**Author:** Qiao Lanying 225040361

---

## 📁 Project Structure
```bash
alpha_factors/
├── btc_data.csv # BTC daily data (source: Binance API)
├── final_factors.py # 15 alpha factor calculations
├── select_best_factors.py # Select 5 low-correlation factors
├── analysis.py # Correlation matrix & Sharpe ratio
├── selected_5_factors.csv # Final 5 selected factors data
├── alpha_factors.csv # All 15 factors data
├── sharp_ratios.csv # Sharpe ratios for all factors
├── correlation_matrix.png # Correlation heatmap
├── download_binance_data.py # Data download script
└── main.py # Main runner script
```

---

## 📊 Factor List (15 candidates → 5 selected)
| Factor | Description |
|--------|-------------|
| Volatility | 20-day historical volatility |
| VPT | Volume Price Trend |
| VolRatio | Current volume / 5-day average volume |
| ClosePos | Closing price position in 10-day range |
| OBV | On-Balance Volume |

---

## 📈 Correlation Matrix (5 selected factors)
|           | ClosePos | VPT | VolRatio | OBV | Volatility |
|-----------|----------|-----|----------|-----|------------|
| ClosePos  | 1.0000   | 0.1019 | 0.0296 | 0.0517 | 0.0164 |
| VPT       | 0.1019   | 1.0000 | 0.0684 | 0.0306 | -0.0003 |
| VolRatio  | 0.0296   | 0.0684 | 1.0000 | -0.0097 | -0.0477 |
| OBV       | 0.0517   | 0.0306 | -0.0097 | 1.0000 | 0.0329 |
| Volatility| 0.0164   | -0.0003 | -0.0477 | 0.0329 | 1.0000 |

**Maximum correlation: 0.1019 ✅ (≤ 0.5, requirement satisfied)**

---

## 📉 Sharpe Ratios (Annualized)
| Factor | Sharpe Ratio |
|--------|--------------|
| Volatility | **0.4193** |
| VPT | 0.1848 |
| VolRatio | -0.2839 |
| ClosePos | -0.3492 |
| OBV | -1.0190 |


**Average Sharpe Ratio: -0.2096**
**Best Factor:** Volatility (0.4193)  
**Worst Factor:** OBV (-1.0190)

---


### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Analysis
```bash
python select_best_factors.py
```

### 3. View Results
```bash
selected_5_factors.csv - Factor values
sharp_ratios.csv - Sharpe ratios
correlation_matrix.png - Heatmap
```

### Data Source
BTC daily data downloaded from Binance public API:
```bash
python download_binance_data.py
```

