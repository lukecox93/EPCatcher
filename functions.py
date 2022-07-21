def convert_to_decimal(num, den):
    return round(float(num) / float(den) + 1, 2)


def add_names_and_prices(current_price, name, number, odds):
    current_price.append([name, number, odds])
    return current_price
