import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file into DataFrame
results_df = pd.read_csv('/Users/tortolla/Downloads/RNN.csv')

metrics = ['Loss', 'MAE', 'MSE', 'RMSE', 'MAPE', 'R²']
colors = ['blue', 'green']
fig, axes = plt.subplots(len(metrics), 1, figsize=(10, 36))
fig.suptitle('RNN')

for i, (metric, ax) in enumerate(zip(metrics, axes)):
    regular_mean_col = f'Regular {metric} Mean'
    regular_ci_col = f'Regular {metric} CI'
    neuro_mean_col = f'Neuro {metric} Mean'
    neuro_ci_col = f'Neuro {metric} CI'
    
    ax.errorbar(results_df['FLOPS'], results_df[regular_mean_col], yerr=results_df[regular_ci_col], fmt='o', label='Regular Sensor', color=colors[0])
    ax.errorbar(results_df['FLOPS'], results_df[neuro_mean_col], yerr=results_df[neuro_ci_col], fmt='x', label='Neuro Sensor', color=colors[1])
    
    if metric == 'R²':
        regular_max = results_df[regular_mean_col].max()
        neuro_max = results_df[neuro_mean_col].max()
        ax.axhline(regular_max, color='red', linestyle='--', label=f'Regular Max {metric}: {regular_max:.4f}')
        ax.axhline(neuro_max, color='orange', linestyle='--', label=f'Neuro Max {metric}: {neuro_max:.4f}')
    else:
        regular_min = results_df[regular_mean_col].min()
        neuro_min = results_df[neuro_mean_col].min()
        ax.axhline(regular_min, color='red', linestyle='--', label=f'Regular Min {metric}: {regular_min:.4f}')
        ax.axhline(neuro_min, color='orange', linestyle='--', label=f'Neuro Min {metric}: {neuro_min:.4f}')
    
    ax.set_xlabel('FLOPS')
    ax.set_ylabel(metric)
    ax.set_title(f'{metric} vs FLOPS')
    ax.legend()
    ax.grid(True)

# Save the combined figure
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('RNN_300.png')
plt.show()

print("Processing complete.")
