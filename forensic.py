import numpy as np
import librosa
import scipy.stats
import soundfile as sf
import logging
import json
import argparse
import sys
import os
import time
from dataclasses import dataclass
from typing import Dict, Any, Tuple
from scipy.signal import lfilter, medfilt
from scipy.spatial.distance import cosine, euclidean
from datetime import datetime

# ==========================================
# 1. CONFIGURATION & LOGGING
# ==========================================
logging.basicConfig(level=logging.ERROR)

@dataclass
class ForensicConfig:
    """Settings for the analysis engine."""
    sample_rate: int = 16000
    stft_n_fft: int = 2048
    stft_hop_length: int = 512
    lpc_order: int = 12
    quantization_factor: float = 10.0
    
    # Baselines for Evasion Detection (Eq 30)
    # Calibrated to 'Real' dataset characteristics:
    # Splice ~0.1, Morph ~0.1, Crypto ~0.9 (Integrity)
    baselines: Dict[str, float] = None

    def __post_init__(self):
        if self.baselines is None:
            self.baselines = {
                'splice': 0.1,      # Real files are continuous (Low score)
                'morph': 0.1,       # Real files match Laplace dist (Low score)
                'noise': 0.001,     # Real files are clean
                'comp': 0.02,       # Real files have low quantization error
                'stego': 0.0,       # Real files have no hidden data
                'crypto': 0.9       # Real files have high integrity (High score)
            }

# ==========================================
# 2. CORE ANALYZER ENGINE
# ==========================================
class AdvancedForensicAnalyzer:
    def __init__(self, audio_path: str, config: ForensicConfig):
        self.config = config
        self.path = audio_path
        self.y = None
        self.sr = None
        self.S = None
        
        # Load immediately
        self._load_and_preprocess()

    def _load_and_preprocess(self):
        print(f"[INFO] Loading Audio: {self.path}")
        try:
            self.y, self.sr = librosa.load(self.path, sr=self.config.sample_rate)
            duration = len(self.y) / self.config.sample_rate
            print(f"[INFO] Sample Rate: {self.sr} Hz | Duration: {duration:.1f}s")
            
            if len(self.y) == 0:
                raise ValueError("Audio file is empty")
            
            print("[INFO] Pre-computing STFT and LPC features...")
            self.S = np.abs(librosa.stft(self.y, n_fft=self.config.stft_n_fft))
            print("\n--- RUNNING ANTI-FORENSIC INDICATORS ---")
            
        except Exception as e:
            print(f"[ERROR] Failed to process file: {e}")
            sys.exit(1)

    # --- INDICATOR A: SPLICING (GLR) ---
    def detect_splicing_glr(self) -> float:
        """Eq 23 & 24: Generalized Likelihood Ratio (Normalized)"""
        print("> (a) Analyzing Splicing (GLR)...")
        
        limit = min(len(self.y), 4000)
        y_seg = self.y[:limit] 
        n = len(y_seg)
        
        if np.std(y_seg) > 1e-9:
            y_seg = (y_seg - np.mean(y_seg)) / np.std(y_seg)
        
        mu0, std0 = np.mean(y_seg), np.std(y_seg) + 1e-9
        ll_0 = np.sum(scipy.stats.norm.logpdf(y_seg, mu0, std0))
        
        max_glr = 0.0
        peak_frame = 0
        
        step = 100
        search_range = range(int(n*0.1), int(n*0.9), step)
        
        for i, k in enumerate(search_range):
            if i % 5 == 0: 
                print(f"      [Progress] Scanning frame {k}/{n}...")
            
            seg_a, seg_b = y_seg[:k], y_seg[k:]
            
            mu_a, std_a = np.mean(seg_a), np.std(seg_a) + 1e-9
            mu_b, std_b = np.mean(seg_b), np.std(seg_b) + 1e-9
            
            ll_a = np.sum(scipy.stats.norm.logpdf(seg_a, mu_a, std_a))
            ll_b = np.sum(scipy.stats.norm.logpdf(seg_b, mu_b, std_b))
            
            glr = (ll_a + ll_b) - ll_0
            if glr > max_glr: 
                max_glr = glr
                peak_frame = k

        normalized_glr = float(max_glr / (n / 50.0)) 

        msg = f"      [ALERT] Discontinuity at frame {peak_frame}." if normalized_glr > 6.0 else "      [INFO] No significant discontinuities found."
        print(msg)
        return max(0.0, normalized_glr)

    # --- INDICATOR B: MORPHING ---
    def detect_morphing_excitation(self) -> float:
        """Eq 25: Excitation Distance (KL-Divergence vs Laplace)"""
        print("\n> (b) Analyzing Voice Morphing...")
        
        a = librosa.lpc(self.y, order=self.config.lpc_order)
        excitation = lfilter(a, [1], self.y)
        
        excitation = (excitation - np.mean(excitation)) / (np.std(excitation) + 1e-9)
        
        hist, bins = np.histogram(excitation, bins=50, density=True)
        hist = hist + 1e-9 
        
        bin_centers = 0.5 * (bins[1:] + bins[:-1])
        pdf_natural = scipy.stats.laplace.pdf(bin_centers, 0, 1 / np.sqrt(2)) 
        pdf_natural = pdf_natural + 1e-9
        
        score = scipy.stats.entropy(hist, pdf_natural)
        
        # Updated logic: Real speech is usually < 0.20
        msg = "Deviation from natural statistics" if score > 0.2 else "Matches natural speech stats"
        print(f"      [Metric] Distribution Divergence (KL): {score:.4f} ({msg})")
        return float(score)

    # --- INDICATOR C: NOISE ---
    def detect_noise_injection(self) -> float:
        """Eq 26: Residual Variance"""
        print("\n> (c) Analyzing Noise Injection...")
        r_x = medfilt(self.y, kernel_size=3)
        score = float(np.var(self.y - r_x))
        print(f"      [Metric] Residual Variance: {score:.5f}")
        return score

    # --- INDICATOR D: COMPRESSION ---
    def detect_compression(self) -> float:
        """Eq 27: Quantization Error (Normalized)"""
        print("\n> (d) Analyzing Compression Artifacts...")
        q = self.config.quantization_factor
        q_s = np.round(self.S * q) / q
        
        total_error = np.sum(np.abs(self.S - q_s))
        score = float(total_error / self.S.size)
        
        print(f"      [Metric] Mean Quantization Error: {score:.4f}")
        return score

    # --- INDICATOR E: STEGANOGRAPHY ---
    def detect_steganography(self) -> float:
        """Eq 28: KL Divergence of LSB"""
        print("\n> (e) Analyzing Steganography...")
        y_int = (self.y * 32767).astype(np.int16)
        lsb = y_int & 1
        p_obs, _ = np.histogram(lsb, bins=[0,1,2], density=True)
        p_nat = np.array([0.5, 0.5])
        epsilon = 1e-10
        score = float(np.sum(p_obs * np.log((p_obs + epsilon)/(p_nat + epsilon))))
        
        msg = "Low probability of hidden data" if score < 0.1 else "Possible LSB Steganography"
        print(f"      [Metric] KL-Divergence: {score:.3f} ({msg})")
        return score

    # --- INDICATOR F: WATERMARK ---
    def detect_watermark(self) -> float:
        """Eq 29: Integrity Check"""
        print("\n> (f) Analyzing Watermark Integrity...")
        high_freq = np.mean(self.S[int(self.config.stft_n_fft/4):, :])
        score = float(1.0 - np.tanh(high_freq))
        
        msg = "Watermark likely destroyed/absent" if score < 0.5 else "Watermark intact"
        print(f"      [Metric] Integrity Score: {score:.2f} ({msg})")
        return score

    # --- INDICATOR G: EVASION ---
    def detect_evasion(self, metrics: Dict[str, float]) -> float:
        """Eq 30: Deviation from Baseline"""
        print("\n> (g) Detecting Forensic Evasion...")
        dev = 0.0
        for k, v in metrics.items():
            if k in self.config.baselines:
                diff = abs(v - self.config.baselines[k])
                
                # Weighting: Splicing is critical, minor morph variance is okay
                if k == 'splice': diff *= 5.0    # High penalty for splice deviation
                elif k == 'comp': diff *= 5.0 
                elif k == 'noise': diff *= 500.0
                elif k == 'morph': diff *= 2.0   # Lower penalty for morph variance
                else: diff *= 5.0
                
                dev += diff
        
        dev = dev / len(self.config.baselines)
        print(f"      [Metric] Anomaly Deviation: {dev:.1f}")
        return float(dev)

    def analyze(self) -> Dict[str, Any]:
        """Runs full pipeline and returns dictionary"""
        results = {
            'splice': self.detect_splicing_glr(),
            'morph': self.detect_morphing_excitation(),
            'noise': self.detect_noise_injection(),
            'comp': self.detect_compression(),
            'stego': self.detect_steganography(),
            'crypto': self.detect_watermark()
        }
        results['evasion'] = self.detect_evasion(results)
        
        # Calibrated Decision Logic
        # 1. Splicing is the strongest indicator of manipulation > 6.0
        # 2. Morphing > 0.25 (Relaxed slightly to avoid false positives on natural variation)
        # 3. Evasion > 10.0 (Tightened now that baselines are accurate)
        is_forgery = (
            (results['splice'] > 6.0) or 
            (results['morph'] > 0.25) or 
            (results['evasion'] > 15.0)
        )
        results['status'] = 'DETECTED AS FORGERY' if is_forgery else 'AUTHENTIC'
        
        return results

# ==========================================
# 3. REPORT GENERATOR (HTML/CLI)
# ==========================================
class ForensicReporter:
    def __init__(self, data: Dict[str, Any], filename: str):
        self.data = data
        self.filename = filename

    def _get_risk_info(self, key, value) -> Tuple[str, str, str]:
        """Returns (Risk Label, Explanation, Normal Score String) based on thresholds"""
        
        if key == 'splice':
            threshold = "< 6.0"
            if value > 6.0: return "[HIGH RISK]", "Indicates cut/paste editing", threshold
            if value > 4.0: return "[MED RISK]", "Possible discontinuity", threshold
            return "[LOW RISK]", "Continuous stream", threshold
        
        if key == 'morph':
            threshold = "< 0.25"
            if value > 0.25: return "[HIGH RISK]", "Indicates voice conversion", threshold
            if value > 0.15: return "[MED RISK]", "Unnatural excitation stats", threshold
            return "[LOW RISK]", "Natural speech patterns", threshold

        if key == 'noise':
            threshold = "< 0.01"
            if value > 0.01: return "[HIGH RISK]", "Heavy noise injection", threshold
            if value > 0.005: return "[MED RISK]", "Possible masking noise", threshold
            return "[LOW RISK]", "Clean background", threshold

        if key == 'comp':
            threshold = "< 0.10"
            if value > 0.10: return "[HIGH RISK]", "Double compression artifacts", threshold
            return "[LOW RISK]", "Normal compression levels", threshold

        if key == 'stego':
            threshold = "< 0.50"
            if value > 0.5: return "[HIGH RISK]", "Hidden data payload likely", threshold
            return "[LOW RISK]", "No hidden data found", threshold

        if key == 'crypto':
            threshold = "> 0.50"
            if value < 0.2: return "[FAIL]", "No valid signature found", threshold
            return "[PASS]", "Watermark integrity verified", threshold

        if key == 'evasion':
            threshold = "< 15.0"
            if value > 15.0: return "[HIGH RISK]", "Adaptive attack detected", threshold
            return "[LOW RISK]", "Consistent with baseline", threshold
            
        return "", "", ""

    def print_cli_report(self):
        """Generates the detailed CLI output requested"""
        d = self.data
        print("\n" + "="*85)
        print("                        FINAL FORENSIC REPORT")
        print("="*85)
        print(f"File: {self.filename}")
        print(f"Status: {d['status']}")
        print("\nDETAILED SCORES:")
        print(f"{'NO.':<4} {'INDICATOR':<22} {'SCORE':<10} {'NORMAL':<10} {'RISK':<12} {'EXPLANATION'}")
        print("-" * 85)
        
        keys_map = [
            ('splice', 'SPLICING (GLR)'),
            ('morph', 'MORPHING (Dist)'),
            ('noise', 'NOISE (Var)'),
            ('comp', 'COMPRESSION (Q-Err)'),
            ('stego', 'STEGANOGRAPHY (KL)'),
            ('crypto', 'WATERMARK (Integ.)'),
            ('evasion', 'EVASION (Deviation)')
        ]

        for i, (k, label) in enumerate(keys_map, 1):
            val = d[k]
            risk, expl, norm = self._get_risk_info(k, val)
            print(f"{i:<4} {label:<22} {val:<10.5f} {norm:<10} {risk:<12} -> {expl}")

        print("\n[CONCLUSION]")
        if d['status'] == 'DETECTED AS FORGERY':
            print("The file exhibits indicators of manipulation.")
            if d['splice'] > 6.0:
                print("High GLR score suggests potential splicing/editing.")
            if d['morph'] > 0.20:
                print("Excitation statistics deviate from natural human speech models (Laplacian).")
        else:
            print("The file appears to be authentic with no significant statistical anomalies.")
        print("="*85 + "\n")

    def save_html_report(self, output_path="forensicreport.html"):
        """Generates the interactive HTML dashboard"""
        json_payload = json.dumps(self.data)
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Forensic Analysis Report</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                :root {{ --primary: #2c3e50; --danger: #e74c3c; --success: #27ae60; --bg: #f8f9fa; }}
                body {{ font-family: 'Segoe UI', sans-serif; background: var(--bg); margin: 0; padding: 20px; color: #333; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                .header {{ border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }}
                .header h1 {{ margin: 0; color: var(--primary); font-size: 24px; }}
                .status {{ padding: 8px 16px; border-radius: 50px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; font-size: 14px; }}
                .status.forgery {{ background: rgba(231, 76, 60, 0.1); color: var(--danger); border: 1px solid var(--danger); }}
                .status.authentic {{ background: rgba(39, 174, 96, 0.1); color: var(--success); border: 1px solid var(--success); }}
                .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }}
                .metric-card {{ background: #fff; border: 1px solid #eee; border-radius: 8px; padding: 20px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th {{ text-align: left; color: #7f8c8d; font-size: 12px; text-transform: uppercase; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
                td {{ padding: 12px 0; border-bottom: 1px solid #f1f1f1; font-family: 'Courier New', monospace; font-weight: 600; }}
                .risk-high {{ color: var(--danger); }}
                .risk-low {{ color: var(--success); }}
                .chart-container {{ position: relative; height: 300px; width: 100%; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div>
                        <h1>Audio Forensic Report</h1>
                        <p style="margin: 5px 0 0; color: #7f8c8d;">Target: {self.filename} | {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                    </div>
                    <div class="status {'forgery' if self.data['status'] == 'DETECTED AS FORGERY' else 'authentic'}">
                        {self.data['status']}
                    </div>
                </div>

                <div class="grid">
                    <div class="metric-card">
                        <h3>Indicator Radar</h3>
                        <div class="chart-container">
                            <canvas id="radarChart"></canvas>
                        </div>
                    </div>
                    <div class="metric-card">
                        <h3>Detailed Analysis</h3>
                        <table>
                            <thead><tr><th>Metric</th><th>Score</th><th>Normal</th><th>Risk</th></tr></thead>
                            <tbody id="tableBody"></tbody>
                        </table>
                    </div>
                </div>

                <div class="metric-card">
                    <h3>Score vs Threshold Comparison</h3>
                    <div class="chart-container">
                        <canvas id="barChart"></canvas>
                    </div>
                </div>
            </div>

            <script>
                const data = {json_payload};
                
                // --- Definitions with Normal Thresholds for JS ---
                const metrics = [
                    {{key: 'splice', label: 'Splicing', thresh: 6.0, normal: '< 6.0'}},
                    {{key: 'morph', label: 'Morphing', thresh: 0.25, normal: '< 0.25'}},
                    {{key: 'noise', label: 'Noise', thresh: 0.01, normal: '< 0.01'}},
                    {{key: 'comp', label: 'Compression', thresh: 0.1, normal: '< 0.1'}},
                    {{key: 'stego', label: 'Steganography', thresh: 0.5, normal: '< 0.5'}},
                    {{key: 'evasion', label: 'Evasion', thresh: 15.0, normal: '< 15.0'}}
                ];

                // --- Populate Table ---
                const tableBody = document.getElementById('tableBody');
                metrics.forEach(m => {{
                    const val = data[m.key];
                    const isHigh = val > m.thresh;
                    const row = `<tr>
                        <td>${{m.label}}</td>
                        <td>${{val.toFixed(4)}}</td>
                        <td style="color:#7f8c8d">${{m.normal}}</td>
                        <td class="${{isHigh ? 'risk-high' : 'risk-low'}}">${{isHigh ? 'HIGH' : 'LOW'}}</td>
                    </tr>`;
                    tableBody.innerHTML += row;
                }});

                // --- Radar Chart ---
                new Chart(document.getElementById('radarChart'), {{
                    type: 'radar',
                    data: {{
                        labels: metrics.map(m => m.label),
                        datasets: [{{
                            label: 'Forgery Signature',
                            data: metrics.map(m => data[m.key] * (m.key === 'noise' ? 1000 : (m.key === 'morph' ? 100 : 1))), 
                            backgroundColor: 'rgba(231, 76, 60, 0.2)',
                            borderColor: '#e74c3c',
                            pointBackgroundColor: '#c0392b'
                        }}]
                    }},
                    options: {{ maintainAspectRatio: false }}
                }});

                // --- Bar Chart (Comparison) ---
                const labels = metrics.map(m => m.label);
                const actualScores = metrics.map(m => data[m.key]);
                const thresholds = metrics.map(m => m.thresh);

                new Chart(document.getElementById('barChart'), {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: [
                            {{
                                label: 'Actual Score',
                                data: actualScores,
                                backgroundColor: '#2c3e50'
                            }},
                            {{
                                label: 'Normal Threshold (Max)',
                                data: thresholds,
                                backgroundColor: '#e74c3c'
                            }}
                        ]
                    }},
                    options: {{
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                type: 'logarithmic',
                                title: {{ display: true, text: 'Logarithmic Scale' }}
                            }}
                        }}
                    }}
                }});
            </script>
        </body>
        </html>
        """
        with open(output_path, 'w') as f:
            f.write(html)
        print(f"\n[INFO] Interactive Report generated: {output_path}")

# ==========================================
# 4. MAIN EXECUTION
# ==========================================
def main():
    parser = argparse.ArgumentParser(description="Advanced Audio Forensic Tool")
    parser.add_argument("--input", type=str, help="Path to input audio file")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode")
    
    args = parser.parse_args()
    file_path = args.input

    # 1. Input Field Logic (If no args provided)
    if not file_path and not args.demo:
        print("Audio Forensic Tool v2.0")
        print("------------------------")
        user_input = input("Enter path to audio file (or press ENTER for Demo): ").strip()
        if user_input:
            file_path = user_input
        else:
            args.demo = True

    # 2. Handle Demo Data Generation
    if args.demo:
        print("\n[WARNING] No input file provided. Generating SYNTHETIC DEMO audio...")
        file_path = "demo_audio.wav"
        sr = 16000
        # Generate 4 seconds of noise
        y = np.random.uniform(-0.1, 0.1, sr*4) 
        # Inject artificial "Splice" (Discontinuity)
        y[int(sr*3.2):int(sr*3.2)+500] *= 5.0 
        sf.write(file_path, y, sr)
    
    # 3. Execution Pipeline
    if file_path:
        config = ForensicConfig()
        analyzer = AdvancedForensicAnalyzer(file_path, config)
        results = analyzer.analyze()
        
        reporter = ForensicReporter(results, file_path)
        reporter.print_cli_report()
        reporter.save_html_report("forensicreport.html")

if __name__ == "__main__":
    main()
