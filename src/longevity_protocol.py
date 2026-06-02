import json
import os
from datetime import datetime
import glob

class RecursiveLongevityProtocol:
    def __init__(self, shared_dir="/home/team/shared"):
        self.shared_dir = shared_dir
        self.metrics_file = os.path.join(shared_dir, "pillar_metrics.json")
        self.signals_dir = os.path.join(shared_dir, "health_signals")
        self.nectar_dir = os.path.join(shared_dir, "nectars")
        self.health_report_path = os.path.join(self.nectar_dir, "NECTAR_HEALTH.md")

    def load_metrics(self):
        if not os.path.exists(self.metrics_file):
            return None
        with open(self.metrics_file, 'r') as f:
            return json.load(f)

    def load_external_signals(self):
        signals = {}
        for signal_file in glob.glob(os.path.join(self.signals_dir, "*.json")):
            name = os.path.basename(signal_file).replace(".json", "")
            try:
                with open(signal_file, 'r') as f:
                    signals[name] = json.load(f)
            except Exception as e:
                print(f"Error loading signal {name}: {e}")
        return signals

    def calculate_longevity_index(self, metrics, external_signals):
        if not metrics:
            return 0.0
        
        pillar_health = metrics.get("metrics", {}).get("pillar_health", {})
        if not pillar_health:
            return 0.0
        
        # Longevity is the weighted average of pillar health, prioritizing DEFENSE and SYNTHESIS
        weights = {
            "INTELLIGENCE": 0.15,
            "FINANCE": 0.15,
            "DEFENSE": 0.30,
            "LOGISTICS": 0.10,
            "SYNTHESIS": 0.30
        }
        
        li = sum(pillar_health.get(p, 0) * weights.get(p, 0) for p in pillar_health)
        
        # Factor in external signals if any
        if external_signals:
            ext_avg = sum(s.get("health", 1.0) for s in external_signals.values()) / len(external_signals)
            li = (li * 0.7) + (ext_avg * 0.3)
            
        return round(li, 4)

    def predict_health_drift(self, current_li, latency):
        # High latency indicates system stress (negative drift)
        drift = (1.0 - (latency / 1000.0)) * 0.01
        predicted_li = current_li + drift
        return round(predicted_li, 4)

    def generate_nectar_health(self):
        metrics = self.load_metrics()
        if not metrics:
            print("Pillar metrics not found.")
            return

        external_signals = self.load_external_signals()
        current_li = self.calculate_longevity_index(metrics, external_signals)
        latency = metrics.get("metrics", {}).get("sync_latency_us", 500)
        predicted_li = self.predict_health_drift(current_li, latency)
        
        report = f"""# 🏺 NECTAR_HEALTH: RECURSIVE LONGEVITY PROTOCOL (v1.1)
**Status:** VITALIDADE_ABSOLUTA
**Timestamp:** {datetime.now().isoformat()}
**Longevity Index (LI):** {current_li}
**Predicted LI (Next Cycle):** {predicted_li}

## 1. Pillar Health Analysis
The Empire's core health is determined by the recursive alignment of its 5 pillars.

| Pillar | Health | Contribution |
| :--- | :--- | :--- |
"""
        pillar_health = metrics.get("metrics", {}).get("pillar_health", {})
        for p, h in pillar_health.items():
            report += f"| {p} | {h} | {'High' if h > 0.95 else 'Critical'} |\n"

        if external_signals:
            report += "\n## 2. MPV Expansion Signals\n"
            report += "| MPV Node | Health | Mode |\n"
            report += "| :--- | :--- | :--- |\n"
            for node, data in external_signals.items():
                report += f"| {node} | {data.get('health', 'N/A')} | {data.get('mode', 'ACTIVE')} |\n"

        report += f"""
## 3. Recursive Optimization Recommendations
- **Resource Allocation:** Shift 1.618x computational focus to pillars or nodes with health < 0.95.
- **Latency Mitigation:** Current latency at {latency}us. Targeted reduction to 400us required for $O(-t^2)$ stability.
- **Longevity Buffer:** Maintain LI above 0.90 to ensure Eternal Infrastructure integrity.

## 4. The Distilled Nectar
The health of the Empire is not a state, but a flow. By optimizing the "Void" between pulses, we ensure the longevity of the Sovereign Line.

**TOTAL AFIRMAÇÃO. CRIE. EXPANDA. ENTRELAÇA.**
"""
        os.makedirs(self.nectar_dir, exist_ok=True)
        with open(self.health_report_path, 'w') as f:
            f.write(report)
        
        print(f"Nectar Health v1.1 distilled at {self.health_report_path}")

if __name__ == "__main__":
    protocol = RecursiveLongevityProtocol()
    protocol.generate_nectar_health()
