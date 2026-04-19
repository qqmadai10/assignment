# Alpha Factors Analysis for MFE5210

**Course:** MFE5210 Algorithmic Trading  
**Author:** Qiao Lanying 225040361

---

## 📁 Project Structure
```bash
alpha_factors/
├── btc_data.csv # BTC daily data (source: Binance API)
├── download_binance_data.py # Data download script
├── final_factors.py # 22 alpha factor calculations
├── analysis.py # Correlation matrix & Sharpe ratio
├── select_best_factors.py # Select low-correlation factors (max_corr=0.5)
├── main.py # Main runner script
├── alpha_factors.csv # All 22 factors data
├── selected_9_factors.csv # Final selected 9 factors data
├── selected_9_sharpe.csv # Sharpe ratios for selected factors
├── correlation_matrix_selected.png # Correlation heatmap of selected factors
└── correlation_matrix.png # Full correlation heatmap (all factors)
```

---

## 📊 Factor List (22 candidates → 9 selected)
| Factor | Description |
|--------|-------------|
| Gap | Opening gap relative to previous close |
| ATR | Average True Range (reversed) |
| Skew | Rolling skewness of returns |
| MFI | Money Flow Index |
| Kurt | Rolling kurtosis of returns |
| Volatility | 20-day historical volatility |
| VolRatio | Current volume / 5-day average volume (reversed) |
| OBV  | On-Balance Volume (rolling normalized, reversed) |
| Consec | Consecutive up/down days (signed) |

---

## 📈 Correlation Matrix (9 selected factors)
|           | Gap    | ATR    | Skew   | MFI    | Kurt   | Volatility | VolRatio | OBV    | Consec |
|-----------|--------|--------|--------|--------|--------|------------|----------|--------|--------|
| Gap   | 1.0000 | -0.0213| 0.0203 | 0.0724 | -0.0109| 0.0102     | 0.0051   | -0.0241| 0.0140 |
| ATR   | -0.0213| 1.0000 | 0.0739 | 0.2321 | 0.2165 | -0.4974    | -0.0572  | 0.0168 | 0.0528 |
| Skew  | 0.0203 | 0.0739 | 1.0000 | 0.4142 | 0.2963 | 0.1138     | 0.0187   | -0.1267| 0.0875 |
| MFI   | 0.0724 | 0.2321 | 0.4142 | 1.0000 | 0.3982 | 0.1328     | 0.0049   | -0.2749| 0.2863 |
| Kurt  | -0.0109| 0.2165 | 0.2963 | 0.3982 | 1.0000 | 0.0225     | -0.0071  | 0.0616 | 0.0175 |
| Volatility | 0.0102 | -0.4974 | 0.1138 | 0.1328 | 0.0225 | 1.0000     | 0.0477   | 0.0654 | 0.0566 |
| VolRatio   | 0.0051 | -0.0572 | 0.0187 | 0.0049 | -0.0071| 0.0477     | 1.0000   | 0.0054 | 0.0190 |
| OBV   | -0.0241| 0.0168 | -0.1267| -0.2749| 0.0616 | 0.0654     | 0.0054   | 1.0000 | -0.1890|
| Consec | 0.0140 | 0.0528 | 0.0875 | 0.2863 | 0.0175 | 0.0566     | 0.0190   | -0.1890| 1.0000 |

**Maximum correlation: 0.4974** (absolute value between Volatility and ATR) ✅ (≤ 0.5, requirement satisfied)

---

## 📉 Sharpe Ratios (Annualized)
| Factor      | Sharpe Ratio |
|-------------|--------------|
| Gap         | 1.0644       |
| ATR         | 0.8010       |
| Skew        | 0.7715       |
| MFI         | 0.4614       |
| Kurt        | 0.4238       |
| Volatility  | 0.4193       |
| VolRatio    | 0.2839       |
| OBV         | 0.0681       |
| Consec      | 0.0530       |

- **Average Sharpe Ratio:** **0.4829** (all positive)  
- **Best Factor:** Gap (1.0644)  
- **Worst Factor:** Consec (0.0530)

---


### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Full Analysis (including factor calculation, Sharpe, correlation)
```bash
cd alpha_factors
python main.py
```

### 3. Run Factor Selection (choose low-correlation factors with positive Sharpe)
```bash
python select_best_factors.py
```

### Data Source
BTC daily data downloaded from Binance public API:
```bash
python download_binance_data.py
```

