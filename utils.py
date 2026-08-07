def format_rupiah(nominal: float) -> str:
    try: return f"Rp{int(nominal):,}".replace(',', '.')
    except (ValueError, TypeError): return "Rp0"

def format_qty(value, asset_type):
    try:
        if not value: return "-"
        val = float(value)
        val_str = f"{int(val)}" if val.is_integer() else f"{val:.4f}".rstrip('0').rstrip('.')
        unit = "Lot" if asset_type == 'Saham' else "Gram" if asset_type == 'Emas' else "Koin" if asset_type == 'Kripto' else "Unit"
        return f"{val_str} {unit}"
    except: return f"{value}"

def clean_string_input(raw_input: str) -> str:
    return raw_input.strip().title() if raw_input else ""
