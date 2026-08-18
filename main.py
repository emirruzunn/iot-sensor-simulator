import argparse
import csv
import sys
from sensors.simulator import SensorSimulator
from storage.logger import save_to_csv, save_to_json
from reporting.stats import calculate_metrics

def main():
    parser = argparse.ArgumentParser(description="IoT Sensör Veri Simülatörü ve CLI Raporlama Aracı")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. GENERATE Komutu
    gen_parser = subparsers.add_parser("generate", help="Sanal sensör verisi üretir ve kaydeder")
    gen_parser.add_argument("--count", type=int, default=10, help="Üretilecek veri sayısı (varsayılan: 10)")
    gen_parser.add_argument("--sensor-id", type=str, default="SENSOR-01", help="Sensör kimliği")
    gen_parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Kayıt formatı (csv veya json)")
    gen_parser.add_argument("--output", type=str, default="data/readings", help="Dosya yolu (uzantı olmadan)")

    # 2. REPORT Komutu
    rep_parser = subparsers.add_parser("report", help="Kayıtlı dosyalardan istatistiksel rapor üretir")
    rep_parser.add_argument("--file", type=str, required=True, help="Okunacak veri dosyası (CSV)")
    rep_parser.add_argument("--metric", choices=["temperature", "humidity", "battery"], help="Filtrelenecek metrik")

    args = parser.parse_args()

    # --- Generate İşlemleri ---
    if args.command == "generate":
        sim = SensorSimulator(args.sensor_id)
        data = [sim.read_all() for _ in range(args.count)]
        
        filepath = f"{args.output}.{args.format}"
        if args.format == "csv":
            save_to_csv(data, filepath)
        else:
            save_to_json(data, filepath)
            
        print(f"Başarılı: {args.count} adet veri '{filepath}' dosyasına yazıldı.")

    # --- Report İşlemleri ---
    elif args.command == "report":
        records = []
        try:
            with open(args.file, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                records = list(reader)
        except FileNotFoundError:
            print(f"Hata: '{args.file}' dosyasi bulunamadi.")
            sys.exit(1)

        if not records:
            print(f"Uyarı: '{args.file}' dosyasinda okunacak veri bulunamadi.")
            sys.exit(0)

        stats = calculate_metrics(records, args.metric)
        
        print(f"\nIoT Sensör Raporu — {args.file}")
        print("─" * 50)
        print(f"Kayıt sayısı   : {len(records)}")
        print(f"Tarih aralığı  : {records[0]['timestamp']} → {records[-1]['timestamp']}\n")
        
        print(f"{'Metrik':<18} {'Min':<8} {'Max':<8} {'Ortalama':<8}")
        print("─" * 50)
        for m, vals in stats.items():
            isim = "Sıcaklık (°C)" if m == "temperature" else "Nem (%)" if m == "humidity" else "Batarya (%)"
            print(f"{isim:<18} {vals['min']:<8} {vals['max']:<8} {vals['avg']:<8}")

if __name__ == "__main__":
    main()