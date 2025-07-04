def calc_max_drawdown(balance_df):
    max_drawdown = 0
    peak = balance_df["value"].iloc[0]

    for current_value in balance_df["value"]:
        if current_value > peak:
            peak = current_value
        drawdown = (peak - current_value) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return round(max_drawdown * 100, 2)
