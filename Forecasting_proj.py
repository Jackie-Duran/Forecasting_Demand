
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



df = pd.read_csv(r'/Users/jackieduran/Desktop/MGT 155/Rice_Demand.csv')


# Compute forecast and forecast errors
# Forecast starts at index 10 (11th row), which is the average of the first 10 demands
forecasts = [None] * 10  
for i in range(10, len(df)):
    avg_prev_10 = df.loc[i-10:i-1, 'Demand'].mean()
    forecasts.append(avg_prev_10)

df['forecast'] = forecasts
df['forecast_error'] = df['Demand'] - df['forecast']

# Looking at data
df.head(11)

df.loc[500]


forecast_week_501 = df.loc[500, 'forecast']

# Dropping Na
forecast_errors = df['forecast_error'].dropna().values

simulated_demands = forecast_week_501 + forecast_errors


# Calculating average profit
buy_range = range(19191, 22191)
results = []

for buy in buy_range:
    units_sold = np.minimum(buy, simulated_demands)
    profit = 22 * units_sold - 6 * buy
    avg_profit = profit.mean()
    results.append((buy, avg_profit))

# Convert results to DataFrame for easier analysis
df_profit = pd.DataFrame(results, columns=['buy_quantity', 'average_profit'])

# Find the buy quantity that gives the highest average profit
optimal_row = df_profit.loc[df_profit['average_profit'].idxmax()]
optimal_row


# Plot to visualize 
plt.figure(figsize=(10, 6))
plt.plot(df_profit['buy_quantity'], df_profit['average_profit'], 'g-', linewidth=2)
plt.axvline(optimal_row['buy_quantity'], color='red', linestyle='--', 
            label=f'Optimal: {optimal_row["buy_quantity"]:.0f} units')

plt.xlabel('Buy Quantity (units)')
plt.ylabel('Average Profit ($)')
plt.title('Rice Demand: Profit vs Buy Quantity')
plt.legend()
plt.grid(True, alpha=0.3)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

plt.tight_layout()
plt.show()

print(f"\nOptimal buy quantity: {optimal_row['buy_quantity']:.0f} units")
print(f"Expected profit: ${optimal_row['average_profit']:,.2f}")



