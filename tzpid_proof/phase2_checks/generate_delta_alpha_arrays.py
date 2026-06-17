from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


def gaussian(x_grid: np.ndarray, y_grid: np.ndarray, x0: float, y0: float, sigma: float) -> np.ndarray:
    return np.exp(-((x_grid - x0) ** 2 + (y_grid - y0) ** 2) / (2.0 * sigma**2))


def generate_delta_alpha_arrays(
    *,
    grid_size: int,
    domain_half_width: float,
    oscillation_scale: float,
    log_epsilon: float,
    phase_amplitude: float,
    source_sigma: float,
    source_offset: float,
) -> dict[str, np.ndarray | float | int]:
    axis = np.linspace(-domain_half_width, domain_half_width, grid_size)
    x_grid, y_grid = np.meshgrid(axis, axis)
    r_grid = np.sqrt(x_grid**2 + y_grid**2)
    domain_radius = float(np.max(r_grid))

    j11 = 3.83170597
    delta = (j11 - np.pi) / j11

    delta_alpha = j11 * delta * (r_grid / domain_radius)
    delta_alpha_shell_cos = np.cos(oscillation_scale * delta_alpha)
    delta_alpha_osc = np.sin(2.0 * np.pi * delta_alpha)
    delta_alpha_log = np.sin(np.pi * np.log(1.0 / (r_grid + log_epsilon)))
    delta_phi = phase_amplitude * np.pi * delta_alpha_osc

    source_0 = gaussian(x_grid, y_grid, 0.0, 0.0, source_sigma)
    source_1 = gaussian(x_grid, y_grid, source_offset, source_offset, source_sigma)
    j_total = source_0 + np.exp(1j * delta_phi) * source_1

    return {
        "x": axis,
        "y": axis,
        "r_grid": r_grid,
        "domain_radius": domain_radius,
        "j11": j11,
        "delta": delta,
        "delta_alpha": delta_alpha,
        "delta_alpha_shell_cos": delta_alpha_shell_cos,
        "delta_alpha_osc": delta_alpha_osc,
        "delta_alpha_log": delta_alpha_log,
        "delta_phi": delta_phi,
        "source_0": source_0,
        "source_1": source_1,
        "j_total_real": np.real(j_total),
        "j_total_imag": np.imag(j_total),
        "j_total_abs": np.abs(j_total),
        "j_total_phase": np.angle(j_total),
    }


def save_arrays(output_dir: Path, arrays: dict[str, np.ndarray | float | int], params: dict[str, float | int]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, value in arrays.items():
        if isinstance(value, np.ndarray):
            np.save(output_dir / f"{name}.npy", value)

    np.savez_compressed(
        output_dir / "delta_alpha_array_bundle.npz",
        **{name: value for name, value in arrays.items() if isinstance(value, np.ndarray)},
    )

    summary = {
        **params,
        "domain_radius": float(arrays["domain_radius"]),
        "j11": float(arrays["j11"]),
        "delta": float(arrays["delta"]),
        "array_files": sorted(path.name for path in output_dir.glob("*.npy")),
    }
    (output_dir / "delta_alpha_array_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Delta Alpha Array Bundle",
        "",
        "Generated arrays:",
        "",
        "- `delta_alpha.npy`: linear Bessel-derived radial phase.",
        "- `delta_alpha_shell_cos.npy`: theorem-aligned shell field, `cos(scale * delta_alpha)`.",
        "- `delta_alpha_osc.npy`: shell-generating sine field, `sin(2*pi*delta_alpha)`.",
        "- `delta_alpha_log.npy`: log-periodic scale field.",
        "- `delta_phi.npy`: EM/Lz phase driver, `A*pi*delta_alpha_osc`.",
        "- `j_total_abs.npy`, `j_total_phase.npy`: coupled source-field observables.",
        "",
        "## Constants",
        "",
        f"- `j11`: `{summary['j11']}`",
        f"- `delta`: `{summary['delta']}`",
        f"- `domain_radius`: `{summary['domain_radius']}`",
        f"- `oscillation_scale`: `{params['oscillation_scale']}`",
        "",
    ]
    (output_dir / "delta_alpha_array_summary.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    plot_names = [
        "delta_alpha",
        "delta_alpha_shell_cos",
        "delta_alpha_osc",
        "delta_alpha_log",
        "delta_phi",
        "j_total_abs",
    ]
    for ax, name in zip(axes.flat, plot_names):
        image = ax.imshow(arrays[name], origin="lower", cmap="viridis")
        ax.set_title(name)
        ax.set_xticks([])
        ax.set_yticks([])
        fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(output_dir / "delta_alpha_array_bundle.png", dpi=180)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Delta-alpha simulation arrays.")
    parser.add_argument("--grid-size", type=int, default=400)
    parser.add_argument("--domain-half-width", type=float, default=1.0)
    parser.add_argument("--oscillation-scale", type=float, default=10.0)
    parser.add_argument("--log-epsilon", type=float, default=1e-6)
    parser.add_argument("--phase-amplitude", type=float, default=1.0)
    parser.add_argument("--source-sigma", type=float, default=0.02)
    parser.add_argument("--source-offset", type=float, default=0.015)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("phase2_checks") / "delta_alpha_arrays",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    params = {
        "grid_size": args.grid_size,
        "domain_half_width": args.domain_half_width,
        "oscillation_scale": args.oscillation_scale,
        "log_epsilon": args.log_epsilon,
        "phase_amplitude": args.phase_amplitude,
        "source_sigma": args.source_sigma,
        "source_offset": args.source_offset,
    }
    arrays = generate_delta_alpha_arrays(**params)
    save_arrays(args.output_dir, arrays, params)
    print(json.dumps({k: v for k, v in params.items()}, indent=2))
    print(f"wrote {args.output_dir}")


if __name__ == "__main__":
    main()
