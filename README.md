<div align="center">

<!-- HEADER BLOCK -->
<br/>

```
 █████╗ ██╗   ██╗██████╗ ██╗ ██████╗     ███████╗ ██████╗ ██████╗ ███████╗███╗   ██╗███████╗██╗ ██████╗
██╔══██╗██║   ██║██╔══██╗██║██╔═══██╗    ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██║██╔════╝
███████║██║   ██║██║  ██║██║██║   ██║    █████╗  ██║   ██║██████╔╝█████╗  ██╔██╗ ██║███████╗██║██║     
██╔══██║██║   ██║██║  ██║██║██║   ██║    ██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██║╚██╗██║╚════██║██║██║     
██║  ██║╚██████╔╝██████╔╝██║╚██████╔╝    ██║     ╚██████╔╝██║  ██║███████╗██║ ╚████║███████║██║╚██████╗
╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═════╝
```

**Advanced Audio Forensic Analyzer**

*Detect splicing · Voice morphing · Noise injection · Steganography · Evasion attacks*

<br/>

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](https://opensource.org/licenses/MIT)
[![Librosa](https://img.shields.io/badge/Librosa-0.10%2B-f97316?style=for-the-badge)](https://librosa.org/)
[![SciPy](https://img.shields.io/badge/SciPy-1.7%2B-8b5cf6?style=for-the-badge&logo=scipy&logoColor=white)](https://scipy.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.20%2B-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5%2B-11557c?style=for-the-badge&logo=plotly&logoColor=white)](https://matplotlib.org/)
[![Tests](https://img.shields.io/badge/Tests-Passing-2ea44f?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/RootSecX/audio-forensic-analyzer/actions)
[![Status](https://img.shields.io/badge/Status-Active-10b981?style=for-the-badge)](https://github.com/YOUR_USERNAME/audio-forensic-analyzer)

<br/>

> A **multi-indicator forensic engine** that unmasks audio manipulation — from crude splices to sophisticated evasion attacks — and renders its findings as a detailed terminal report alongside an interactive HTML intelligence dashboard.

<br/>

---

</div>

<br/>

## ◈ Table of Contents

- [Overview](#-overview)
- [Detection Capabilities](#-detection-capabilities)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Methodology](#-methodology-deep-dive)
- [Output Examples](#-output-examples)
- [Architecture](#-architecture)
- [Limitations](#-limitations--disclaimer)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

<br/>

---

## ◈ Overview

Audio Forensic Analyzer is a **research-grade toolkit** built to detect a wide spectrum of audio manipulation techniques. It combines classical signal processing with information-theoretic divergence measures and adaptive evasion detection — all packaged into a single Python script with zero complicated setup.

```
                                                                 Input Audio (WAV)
                                                                       │
                                                                       ▼
                                               ┌──────────────────────────────────────────────────────┐
                                               │               FORENSIC ENGINE v2.0                   │
                                               │                                                      │
                                               │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
                                               │  │ Splicing │  │ Morphing │  │  Noise   │            │
                                               │  │  (GLR)   │  │  (KLD)   │  │ Injection│            │
                                               │  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
                                               │       │             │             │                  │
                                               │  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐            │
                                               │  │ Compress │  │  Stegano │  │Watermark │            │
                                               │  │  (STFT)  │  │  (LSB)   │  │ Integrity│            │
                                               │  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
                                               │       └─────────────┴─────────────┘                  │
                                               │                       │                              │
                                               │              ┌────────┴────────┐                     │
                                               │              │  Evasion Attack │                     │
                                               │              │    Detector     │                     │
                                               │              └────────┬────────┘                     │
                                               │                       │                              │
                                               │              ┌────────┴────────┐                     │
                                               │              │  VERDICT ENGINE │                     │
                                               │              └─────────────────┘                     │
                                               └──────────────────────────────────────────────────────┘
                                                      │                                       │
                                                      ▼                                       ▼
                                                Terminal Report                        HTML Dashboard 

```

<br/>

---

## ◈ Detection Capabilities

Seven independent indicators feed a weighted verdict system calibrated against real speech corpora.

<br/>

| # | Indicator | Method | Authentic Threshold | What It Catches |
|---|-----------|--------|:-------------------:|-----------------|
| 1 | **Splicing** | Generalized Likelihood Ratio (GLR) | `< 6.0` | Cut-and-paste edits, abrupt signal discontinuities |
| 2 | **Voice Morphing** | KL Divergence — residual vs. Laplace | `< 0.25` | Voice conversion, neural voice cloning |
| 3 | **Noise Injection** | Median-filter residual variance | `< 0.01` | Artificially added ambient noise layers |
| 4 | **Compression Artifacts** | STFT quantization error | `< 0.10` | Re-encoding, multi-generational compression |
| 5 | **Steganography** | LSB distribution KL divergence | `< 0.50` | Hidden data payloads in least-significant bits |
| 6 | **Watermark Integrity** | High-frequency energy analysis | `> 0.50` | Watermark stripping or destruction |
| 7 | **Evasion Attack** | Weighted baseline deviation | `< 15.0` | Adversarial perturbations masking forgery |

<br/>

> **Verdict logic** — indicators are combined adaptively. A single high-risk score can trigger `DETECTED AS FORGERY` when it exceeds its threshold by a significant margin; borderline cases are evaluated holistically across all seven dimensions.

<br/>

---

## ◈ Quick Start

### Prerequisites

```
Python  ≥ 3.8
pip     (any recent version)
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/RootSecX/audio-forensic-analyzer.git
cd audio-forensic-analyzer

# 2. Install dependencies
pip install -r requirements.txt
```

### requirements.txt

```
librosa>=0.10.0
numpy>=1.21.0
scipy>=1.7.0
soundfile>=0.10.0
```

<br/>

---

## ◈ Usage

### Analyze a file

```bash
python forensic.py --input path/to/audio.wav
```

### Run demo mode *(no audio file needed)*

```bash
python forensic.py --demo
```

Generates a synthetic `demo_audio.wav` — 4 seconds of noise with an artificial splice — and runs the full pipeline. Ideal for first-time testing.

### Interactive prompt fallback

```bash
python forensic.py
# → Script prompts: "Enter audio file path:"
```

<br/>

---

## ◈ Configuration

All parameters live in the `ForensicConfig` dataclass at the top of `forensic.py`. No external config files needed.

```python
@dataclass
class ForensicConfig:
    # ── Audio ────────────────────────────────────────────
    sample_rate: int = 16000          # Resample to this rate before analysis

    # ── STFT ─────────────────────────────────────────────
    stft_n_fft: int = 2048            # FFT window size
    stft_hop_length: int = 512        # Hop length (frames overlap)

    # ── LPC ──────────────────────────────────────────────
    lpc_order: int = 12               # LPC model order for excitation analysis

    # ── Compression Detection ─────────────────────────────
    quantization_factor: float = 10.0 # STFT magnitude quantization step

    # ── Evasion Detection ─────────────────────────────────
    baselines: Dict[str, float] = {   # Calibrated reference values (real speech)
        "splicing":      3.5,
        "morphing":      0.12,
        "noise":         0.003,
        "compression":   0.05,
        "steganography": 0.18,
        "watermark":     0.82,
    }
```

> **Tip:** Increase the `limit` parameter inside `detect_splicing_glr()` from `4000` to the full sample count for exhaustive splice detection on longer recordings.

<br/>

---

## ◈ Methodology Deep Dive

<details>
<summary><strong>1 · Splicing Detection (GLR)</strong></summary>

<br/>

Scans the signal for the single most abrupt change point by computing the **Generalized Likelihood Ratio** — the log-ratio between a single-Gaussian model fitted to the entire window and a two-segment model fitted on either side of a candidate cut point.

A high GLR score indicates the signal statistics shift dramatically at one location, consistent with a splice joining two independent recordings.

</details>

<details>
<summary><strong>2 · Voice Morphing Detection (KL Divergence)</strong></summary>

<br/>

Fits an **LPC (Linear Predictive Coding)** model to the signal and extracts the residual excitation — the component that carries the speaker's unique glottal signature. Natural speech excitation closely follows a **Laplace distribution**.

Voice conversion algorithms alter this residual in characteristic ways. KL divergence between the observed residual distribution and the theoretical Laplace baseline quantifies how far the signal departs from natural speech statistics.

</details>

<details>
<summary><strong>3 · Noise Injection Detection</strong></summary>

<br/>

Applies a median filter (kernel size 3) to the signal and computes the **variance of the difference** between the original and the smoothed version. Authentic recordings have a low, stable residual. Injected noise layers create high or irregular residual variance.

</details>

<details>
<summary><strong>4 · Compression Artifact Detection</strong></summary>

<br/>

Computes the **STFT magnitude spectrum**, quantizes it using `quantization_factor`, then measures the mean absolute error between original and quantized magnitudes. Authentic uncompressed audio exhibits minimal quantization error; files that have been re-encoded (e.g., MP3 → WAV) or passed through multiple compression cycles show elevated error.

</details>

<details>
<summary><strong>5 · Steganography Detection (LSB Analysis)</strong></summary>

<br/>

Extracts the **least-significant bits** from the 16-bit PCM samples and measures their distribution using KL divergence against a uniform (0.5, 0.5) distribution. Authentic audio LSBs are near-random. Steganographic payloads introduce statistical bias detectable via this divergence metric.

</details>

<details>
<summary><strong>6 · Watermark Integrity</strong></summary>

<br/>

Assumes watermarks are typically embedded in the **high-frequency band** of the spectrum. Low high-frequency energy relative to the overall signal suggests that watermark content has been stripped, overwritten, or destroyed — often a deliberate step in laundering manipulated content.

</details>

<details>
<summary><strong>7 · Evasion Attack Detection</strong></summary>

<br/>

Computes a **weighted sum of absolute deviations** from pre-calibrated baselines derived from real speech statistics. Sophisticated forgeries that pass individual detectors may still exhibit collectively anomalous deviation patterns across all seven indicators — a signature this module is specifically designed to expose.

</details>

<br/>

---

## ◈ Output Examples

### Terminal Report

```
================================================================
                      FINAL FORENSIC REPORT
================================================================
File   : suspicious.wav
Status : ██ DETECTED AS FORGERY

DETAILED SCORES:
────────────────────────────────────────────────────────────────
 NO.  INDICATOR              SCORE      NORMAL     RISK
────────────────────────────────────────────────────────────────
  1   SPLICING (GLR)         8.21345    < 6.0      [HIGH RISK] → Indicates cut/paste editing
  2   MORPHING (KLD)         0.32140    < 0.25     [HIGH RISK] → Indicates voice conversion
  3   NOISE INJECTION        0.00821    < 0.01     [OK]        → Within normal variance
  4   COMPRESSION            0.14233    < 0.10     [HIGH RISK] → Multi-generation encoding
  5   STEGANOGRAPHY (KLD)    0.23110    < 0.50     [OK]        → LSB appears random
  6   WATERMARK INTEGRITY    0.41200    > 0.50     [HIGH RISK] → High-freq energy loss
  7   EVASION ATTACK         19.8500    < 15.0     [HIGH RISK] → Adversarial perturbation
────────────────────────────────────────────────────────────────
VERDICT: 4 of 7 indicators flagged as HIGH RISK
================================================================
```

### HTML Dashboard

The interactive dashboard renders three panels side-by-side:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| **Radar Chart** | 7-axis polygon | Visual forgery signature across all indicators |
| **Bar Chart** | Log-scale comparison | Each score vs. its threshold at a glance |
| **Score Table** | Color-coded rows | Full numeric breakdown with risk annotation |

> Run the tool to generate `forensic_report.html` and open it in any modern browser. No server required.

<br/>

---

## ◈ Architecture

```
audio-forensic-analyzer/
│
├── forensic.py              ← Entire engine: detection + reporting + dashboard
├── requirements.txt         ← Four dependencies only
├── LICENSE                  ← MIT
├── README.md                ← Info
│
└── docs/
    └── Sample_Dashboard_Preview.html   
```

The project is intentionally **single-file** — `forensic.py` contains the detector classes, verdict engine, terminal reporter, and HTML dashboard generator. This maximizes portability: copy one file, install four packages, run.

<br/>

---

## ◈ Limitations & Disclaimer

> ⚠️ **This tool is for educational and research purposes only. Output is not certified for use as court evidence.**

| Limitation | Detail |
|------------|--------|
| **Splicing scan depth** | Analyses first 4 000 samples by default for speed. Increase `limit` in `detect_splicing_glr()` for full-file coverage. |
| **Steganography coverage** | Detects LSB-plane uniformity only. Advanced hiding techniques (DCT-domain, spread-spectrum) are out of scope. |
| **Watermark scheme** | Assumes high-frequency embedding. Real-world watermarks vary significantly in implementation. |
| **Input quality** | Performance degrades on heavily compressed sources (< 64 kbps) or very short clips (< 1 second). |
| **False positives** | Highly processed but legitimate audio (e.g., mastered music) may trigger some indicators. Interpret scores holistically. |

<br/>

---

## ◈ Roadmap

Planned improvements — contributions welcome:

- [ ] **ENF (Electric Network Frequency) analysis** — timestamp verification via power-grid hum
- [ ] **CUSUM / Bayesian change-point** — finer-grained splice localisation with temporal maps
- [ ] **DCT-domain steganography** — detect spread-spectrum and JPEG-style hiding
- [ ] **Batch processing CLI** — analyse entire directories with aggregated reporting
- [ ] **Confidence intervals** — Monte Carlo uncertainty estimation on each score
- [ ] **GAN artifact detection** — spectral signatures left by neural voice synthesis models

<br/>

---

## ◈ Contributing

Pull requests and issues are warmly welcomed.

```bash
# Fork → clone → branch
git checkout -b feature/enf-analysis

# Make changes, then verify with demo mode
python forensic.py --demo

# Open a PR with a clear description of what changed and why
```

Please follow existing code style: type hints, dataclass config, docstrings on all public methods.

<br/>

---

## ◈ License

Distributed under the **MIT License** — see [`LICENSE`](LICENSE) for full terms.

<br/>

---

## ◈ Citation

If you use this tool in published research, please cite:

```bibtex
@misc{audioforensic2026,
  author    = {Muhammad Ahmaad},
  title     = {Advanced Audio Forensic Analyzer},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/RootSecX/audio-forensic-analyzer}
}
```

<br/>

---

<div align="center">

Built with precision using `librosa` · `NumPy` · `SciPy` · `Chart.js`

<br/>

*If this project helped you, consider leaving a ⭐ — it keeps the work going.*

</div>
