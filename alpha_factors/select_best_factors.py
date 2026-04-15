import pandas as pd
import numpy as np
from final_factors import FinalAlphaFactors


def select_low_correlation_factors(factors, max_corr=0.5, target_count=5):
    """筛选低相关性的因子"""
    corr_matrix = factors.corr()

    # 计算每个因子与其他因子的最大相关性
    max_correlations = {}
    for col in factors.columns:
        other_cols = [c for c in factors.columns if c != col]
        max_corr_val = max([abs(corr_matrix.loc[col, c]) for c in other_cols])
        max_correlations[col] = max_corr_val

    # 按最大相关性排序
    sorted_factors = sorted(max_correlations.items(), key=lambda x: x[1])

    # 贪心选择
    selected = []
    for factor, corr in sorted_factors:
        if len(selected) >= target_count:
            break

        # 检查与已选因子的相关性
        if selected:
            max_with_selected = max([abs(corr_matrix.loc[factor, s]) for s in selected])
            if max_with_selected <= max_corr:
                selected.append(factor)
        else:
            selected.append(factor)

    return selected, max_correlations


def main():
    print("=" * 70)
    print("SELECTING BEST 5 LOW-CORRELATION ALPHA FACTORS")
    print("=" * 70)

    # 加载数据
    df = pd.read_csv('btc_data.csv', index_col=0, parse_dates=True)
    if 'open' not in df.columns:
        df.columns = [col.lower() for col in df.columns]

    print(f"\nLoaded {len(df)} records")

    # 计算所有 15 个因子
    calculator = FinalAlphaFactors(df)
    factors = calculator.calculate_all_factors()

    print(f"\nCalculated {len(factors.columns)} factors:")
    print(list(factors.columns))

    # 筛选低相关因子
    selected, max_corrs = select_low_correlation_factors(factors, max_corr=0.5, target_count=5)

    print("\n" + "=" * 70)
    print("SELECTED FACTORS (Correlation <= 0.5)")
    print("=" * 70)

    for factor in selected:
        print(f"  {factor}: max correlation = {max_corrs[factor]:.4f}")

    # 计算夏普比率
    from analysis import FactorAnalysis
    analyzer = FactorAnalysis(factors[selected], df['close'])
    sharpe_df = analyzer.print_report()

    # 保存结果
    factors[selected].to_csv('selected_5_factors.csv')
    print("\nSaved to selected_5_factors.csv")


if __name__ == "__main__":
    main()