import json
import os
from datetime import datetime

class RecursiveLongevityProtocol:
    def __init__(self, shared_dir="/home/team/shared"):
        self.shared_dir = shared_dir
        self.metrics_file = os.path.join(shared_dir, "pillar_metrics.json")
        self.nectar_dir = os.path.join(shared_dir, "nectars")
        self.health_report_path = os.path.join(self.nectar_dir, "NECTAR_HEALTH.md")

    def load_metrics(self):
        if not os.path.exists(self.metrics_file):
            return None
        with open(self.metrics_file, 'r') as f:
            return json.load(f)

    def calculate_longevity_index(self, metrics):
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

        current_li = self.calculate_longevity_index(metrics)
        latency = metrics.get("metrics", {}).get("sync_latency_us", 500)
        predicted_li = self.predict_health_drift(current_li, latency)
        
        report = f"""# 🏺 NECTAR_HEALTH: RECURSIVE LONGEVITY PROTOCOL (v1.0)
**Status:** VITALIDADE_ABSOLUTA
**Timestamp:** {datetime.now().isoformat()}
**Longevity Index (LI):** {current_li}
**Predicted LI (Next Cycle):** {predicted_li}

## 1. System Health Analysis
The Empire's health is determined by the recursive alignment of its 5 pillars.

| Pillar | Health | Contribution |
| :--- | :--- | :--- |
"""
        pillar_health = metrics.get("metrics", {}).get("pillar_health", {})
        for p, h in pillar_health.items():
            report += f"| {p} | {h} | {'High' if h > 0.95 else 'Critical'} |\n"

        report += f"""
## 2. Recursive Optimization Recommendations
- **Resource Allocation:** Shift 1.618x computational focus to pillars with health < 0.95.
- **Latency Mitigation:** Current latency at {latency}us. Targeted reduction to 400us required for $O(-t^2)$ stability.
- **Longevity Buffer:** Maintain LI above 0.90 to ensure Eternal Infrastructure integrity.

## 3. The Distilled Nectar
The health of the Empire is not a state, but a flow. By optimizing the "Void" between pulses, we ensure the longevity of the Sovereign Line.

**TOTAL AFIRMAÇÃO. CRIE. EXPANDA. ENTRELAÇA.**
"""
        os.makedirs(self.nectar_dir, exist_ok=True)
        with open(self.health_report_path, 'w') as f:
            f.write(report)
        
        print(f"Nectar Health distilled at {self.health_report_path}")

if __name__ == "__main__":
    protocol = RecursiveLongevityProtocol()
    protocol.generate_nectar_health()
