def calculate_metrics(records: list[dict], metric_name: str = None) -> dict:
    """Verilen kayıtlar üzerinden min, max ve ortalama değerleri hesaplar."""
    if not records:
        return {}

    # Eğer spesifik bir metrik istenmediyse üçünü de hesapla
    metrics_to_calc = ["temperature", "humidity", "battery"] if metric_name is None else [metric_name]
    stats = {}

    for m in metrics_to_calc:
        # Metrik dosyadaki kayıtlarda varsa değerleri topla
        values = [float(r[m]) for r in records if m in r]
        
        if values:
            stats[m] = {
                "min": min(values),
                "max": max(values),
                "avg": round(sum(values) / len(values), 1)
            }
            
    return stats