import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class FactorAnalysis:
    def __init__(self, factors: pd.DataFrame, prices: pd.Series):
        """
        factors: 因子数据（每列是一个因子）
        prices: 价格数据（用于计算未来收益率）
        """
        self.factors = factors
        self.prices = prices

    def compute_correlation_matrix(self) -> pd.DataFrame:
        """计算因子之间的相关性矩阵"""
        return self.factors.corr()

    def compute_sharpe_ratio(self, returns: pd.Series, periods_per_year: int = 252) -> float:
        """计算年化夏普比率"""
        if len(returns) < 2 or returns.std() == 0:
            return 0.0
        return np.sqrt(periods_per_year) * returns.mean() / returns.std()

    def compute_factor_sharpe(self, lookahead_days: int = 1) -> pd.DataFrame:
        """
        计算每个因子的夏普比率
        lookahead_days: 未来多少天的收益率
        """
        # 计算未来收益率
        future_returns = self.prices.pct_change(lookahead_days).shift(-lookahead_days)

        results = []
        for col in self.factors.columns:
            # 使用因子值预测未来收益
            factor = self.factors[col].dropna()
            returns_aligned = future_returns.reindex(factor.index)

            # 策略：做多高因子值，做空低因子值
            long_signal = factor > factor.quantile(0.7)
            short_signal = factor < factor.quantile(0.3)

            strategy_returns = pd.Series(0, index=returns_aligned.index)
            strategy_returns[long_signal] = returns_aligned[long_signal]
            strategy_returns[short_signal] = -returns_aligned[short_signal]

            sharpe = self.compute_sharpe_ratio(strategy_returns.dropna())

            results.append({
                'Factor': col,
                'Sharpe_Ratio': sharpe,
                'Signal_Count': long_signal.sum() + short_signal.sum()
            })

        return pd.DataFrame(results)

    def print_report(self):
        """打印完整分析报告"""
        print("\n" + "=" * 70)
        print("ALPHA FACTOR ANALYSIS REPORT")
        print("=" * 70)

        # 相关性矩阵
        corr_matrix = self.compute_correlation_matrix()
        print("\n" + "-" * 70)
        print("FACTOR CORRELATION MATRIX")
        print("-" * 70)
        print(corr_matrix.round(4))

        # 检查最大相关性
        corr_values = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        max_corr = corr_values.max().max() if not corr_values.isnull().all().all() else 0
        print(f"\nMaximum correlation: {max_corr:.4f}")

        if max_corr > 0.5:
            print("⚠️  WARNING: Maximum correlation exceeds 0.5!")
        else:
            print("✅ Maximum correlation is ≤ 0.5 - Good!")

        # 夏普比率
        sharpe_df = self.compute_factor_sharpe()
        print("\n" + "-" * 70)
        print("FACTOR SHARPE RATIOS (Annualized)")
        print("-" * 70)
        print(sharpe_df.to_string(index=False))

        avg_sharpe = sharpe_df['Sharpe_Ratio'].mean()
        print(f"\nAverage Sharpe Ratio: {avg_sharpe:.4f}")

        # 最佳和最差因子
        best = sharpe_df.loc[sharpe_df['Sharpe_Ratio'].idxmax()]
        worst = sharpe_df.loc[sharpe_df['Sharpe_Ratio'].idxmin()]
        print(f"\nBest Factor: {best['Factor']} (Sharpe: {best['Sharpe_Ratio']:.4f})")
        print(f"Worst Factor: {worst['Factor']} (Sharpe: {worst['Sharpe_Ratio']:.4f})")

        print("\n" + "=" * 70)

        return sharpe_df

    def plot_correlation_heatmap(self, save_path='correlation_matrix.png'):
        """绘制相关性热力图"""
        plt.figure(figsize=(12, 10))
        corr = self.compute_correlation_matrix()
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0,
                    fmt='.3f', square=True, linewidths=0.5)
        plt.title('Alpha Factor Correlation Matrix', fontsize=14)
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
        print(f"\nCorrelation heatmap saved to {save_path}")