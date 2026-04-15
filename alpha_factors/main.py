import pandas as pd
import numpy as np
from factors import AlphaFactors
from analysis import FactorAnalysis


def main():
    print("=" * 70)
    print("ALPHA FACTOR GENERATION SYSTEM")
    print("=" * 70)

    # 1. 加载数据
    print("\n[1] Loading BTC data...")
    df = pd.read_csv('btc_data.csv', index_col=0, parse_dates=True)
    print(f"Loaded {len(df)} records from {df.index[0]} to {df.index[-1]}")

    # 确保有必要的列（币安数据列名是小写）
    if 'open' not in df.columns:
        # 如果列名是 Open, High 等（首字母大写），转换一下
        df.columns = [col.lower() for col in df.columns]

    print(f"Data columns: {list(df.columns)}")

    # 2. 计算 Alpha 因子
    print("\n[2] Calculating Alpha factors...")
    calculator = AlphaFactors(df)
    factors = calculator.calculate_all_factors()
    print(f"Generated {len(factors.columns)} factors: {list(factors.columns)}")

    # 显示因子统计
    print("\n[3] Factor Statistics:")
    print(factors.describe().round(4))

    # 3. 分析因子
    print("\n[4] Analyzing factors...")
    prices = df['close']
    analyzer = FactorAnalysis(factors, prices)

    # 4. 生成报告
    sharpe_df = analyzer.print_report()

    # 5. 保存结果
    print("\n[5] Saving results...")
    factors.to_csv('alpha_factors.csv')
    sharpe_df.to_csv('sharpe_ratios.csv')
    analyzer.plot_correlation_heatmap()

    print("\n" + "=" * 70)
    print("✅ Analysis complete!")
    print("=" * 70)
    print("Files saved:")
    print("   - alpha_factors.csv: All factor values")
    print("   - sharpe_ratios.csv: Sharpe ratios per factor")
    print("   - correlation_matrix.png: Correlation heatmap")


if __name__ == "__main__":
    main()