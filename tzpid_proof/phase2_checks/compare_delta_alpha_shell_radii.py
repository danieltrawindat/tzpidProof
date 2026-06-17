from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks


@dataclass(frozen=True)
class ShellComparison:
    n: int
    predicted_radius: float
    observed_radius: float
    absolute_error: float
    relative_error: float


def radial_profile(
    r_grid: np.ndarray,
    field: np.ndarray,
    domain_radius: float,
    bins: int,
) -> tuple[np.ndarray, np.ndarray]:
    r_bins = np.linspace(0.0, domain_radius, bins)
    r_centers = 0.5 * (r_bins[:-1] + r_bins[1:])
    profile = np.zeros_like(r_centers)

    for index in range(len(r_centers)):
        mask = (r_grid >= r_bins[index]) & (r_grid < r_bins[index + 1])
        if np.any(mask):
            profile[index] = float(np.mean(np.abs(field[mask])))

    return r_centers, profile


def compare_shells(
    *,
    grid_size: int,
    domain_half_width: float,
    radial_bins: int,
    oscillation_scale: float,
    peak_height_fraction: float,
    damping: float,
    profile_mode: str,
    field: np.ndarray | None = None,
    domain_radius_override: float | None = None,
) -> tuple[dict[str, float | int], list[ShellComparison], np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    external_input = field is not None
    if field is None:
        axis = np.linspace(-domain_half_width, domain_half_width, grid_size)
        x_grid, y_grid = np.meshgrid(axis, axis)
        r_grid = np.sqrt(x_grid**2 + y_grid**2)
        domain_radius = float(np.max(r_grid))
    else:
        field = np.asarray(field, dtype=float)
        if field.ndim != 2:
            raise ValueError(f"field must be 2D, got shape {field.shape}")
        y_size, x_size = field.shape
        x_axis = np.linspace(-domain_half_width, domain_half_width, x_size)
        y_axis = np.linspace(-domain_half_width, domain_half_width, y_size)
        x_grid, y_grid = np.meshgrid(x_axis, y_axis)
        r_grid = np.sqrt(x_grid**2 + y_grid**2)
        domain_radius = (
            float(domain_radius_override)
            if domain_radius_override is not None
            else float(np.max(r_grid))
        )

    j11 = 3.83170597
    j_half = float(np.pi)
    delta = (j11 - j_half) / j11

    # Theorem-consistent scaled phase:
    # Delta alpha_s(r) = scale * j11 * delta * r / R.
    phase = oscillation_scale * j11 * delta * (r_grid / domain_radius)
    if field is None:
        field = np.cos(phase) * np.exp(-(r_grid**2) * damping)

    if profile_mode == "raw_abs":
        profile_field = np.abs(field)
    elif profile_mode == "envelope_corrected_abs":
        envelope = np.exp(-(r_grid**2) * damping)
        profile_field = np.abs(field) / np.maximum(envelope, np.finfo(float).eps)
    elif profile_mode == "oscillatory_abs":
        profile_field = np.abs(np.cos(phase))
    elif profile_mode == "field":
        profile_field = field
    else:
        raise ValueError(
            "profile_mode must be one of: raw_abs, envelope_corrected_abs, oscillatory_abs, field"
        )

    r_centers, profile = radial_profile(r_grid, profile_field, domain_radius, radial_bins)
    peaks, peak_info = find_peaks(
        profile,
        height=float(np.max(profile) * peak_height_fraction),
    )
    observed = r_centers[peaks]

    predicted_all: list[tuple[int, float]] = []
    n = 1
    while True:
        predicted_radius = n * np.pi * domain_radius / (j11 * delta * oscillation_scale)
        if predicted_radius > domain_radius:
            break
        predicted_all.append((n, float(predicted_radius)))
        n += 1

    comparisons: list[ShellComparison] = []
    for n_value, predicted_radius in predicted_all:
        if len(observed) == 0:
            break
        nearest_index = int(np.argmin(np.abs(observed - predicted_radius)))
        observed_radius = float(observed[nearest_index])
        absolute_error = float(abs(predicted_radius - observed_radius))
        relative_error = float(absolute_error / predicted_radius) if predicted_radius else 0.0
        comparisons.append(
            ShellComparison(
                n=int(n_value),
                predicted_radius=float(predicted_radius),
                observed_radius=observed_radius,
                absolute_error=absolute_error,
                relative_error=relative_error,
            )
        )

    summary: dict[str, float | int] = {
        "grid_size": grid_size,
        "domain_half_width": domain_half_width,
        "domain_radius": domain_radius,
        "radial_bins": radial_bins,
        "oscillation_scale": oscillation_scale,
        "peak_height_fraction": peak_height_fraction,
        "damping": damping,
        "profile_mode": profile_mode,
        "field_source": "external" if external_input else "synthetic",
        "j11": j11,
        "j_half": j_half,
        "delta": delta,
        "detected_peaks": int(len(observed)),
        "predicted_shells_in_domain": int(len(predicted_all)),
        "mean_absolute_error": float(np.mean([row.absolute_error for row in comparisons]))
        if comparisons
        else 0.0,
        "max_absolute_error": float(np.max([row.absolute_error for row in comparisons]))
        if comparisons
        else 0.0,
        "mean_relative_error": float(np.mean([row.relative_error for row in comparisons]))
        if comparisons
        else 0.0,
    }
    return summary, comparisons, r_centers, profile, observed, field


def first_numeric_array_from_npz(path: Path) -> np.ndarray:
    with np.load(path) as archive:
        for name in archive.files:
            value = np.asarray(archive[name])
            if np.issubdtype(value.dtype, np.number) and value.ndim == 2:
                return value
        raise ValueError(f"No 2D numeric array found in {path}")


def coerce_to_2d(array: np.ndarray, slice_index: int) -> np.ndarray:
    array = np.asarray(array)
    if array.ndim == 2:
        return array
    if array.ndim == 3:
        if not 0 <= slice_index < array.shape[0]:
            raise IndexError(
                f"slice index {slice_index} is outside first axis with length {array.shape[0]}"
            )
        return np.asarray(array[slice_index])
    raise ValueError(f"Expected a 2D field or 3D time stack, got shape {array.shape}")


def first_numeric_array_from_hdf5(path: Path, dataset: str | None, slice_index: int) -> np.ndarray:
    try:
        import h5py  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError(
            "HDF5 input requires h5py. Install it with `python -m pip install h5py`."
        ) from exc

    def visit_group(group: Any) -> np.ndarray | None:
        for key in group:
            value = group[key]
            if hasattr(value, "shape") and hasattr(value, "dtype"):
                array = np.asarray(value)
                if np.issubdtype(array.dtype, np.number) and array.ndim in {2, 3}:
                    return coerce_to_2d(array, slice_index)
            elif hasattr(value, "keys"):
                nested = visit_group(value)
                if nested is not None:
                    return nested
        return None

    with h5py.File(path, "r") as handle:
        if dataset:
            return coerce_to_2d(np.asarray(handle[dataset]), slice_index)
        array = visit_group(handle)
        if array is None:
            raise ValueError(f"No 2D numeric dataset or 3D numeric time stack found in {path}")
        return array


def load_external_field(path: Path, dataset: str | None, slice_index: int) -> np.ndarray:
    suffix = path.suffix.lower()
    if suffix == ".npy":
        return np.asarray(np.load(path))
    if suffix == ".npz":
        return first_numeric_array_from_npz(path)
    if suffix in {".csv", ".txt"}:
        return np.loadtxt(path, delimiter="," if suffix == ".csv" else None)
    if suffix in {".h5", ".hdf5"}:
        return first_numeric_array_from_hdf5(path, dataset, slice_index)
    raise ValueError(f"Unsupported field input extension: {suffix}")


def write_outputs(
    *,
    output_dir: Path,
    summary: dict[str, float | int],
    comparisons: list[ShellComparison],
    r_centers: np.ndarray,
    profile: np.ndarray,
    observed: np.ndarray,
    field: np.ndarray,
    domain_half_width: float,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = [asdict(row) for row in comparisons]
    (output_dir / "delta_alpha_shell_comparison.json").write_text(
        json.dumps({"summary": summary, "comparisons": rows}, indent=2),
        encoding="utf-8",
    )

    with (output_dir / "delta_alpha_shell_comparison.csv").open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "n",
                "predicted_radius",
                "observed_radius",
                "absolute_error",
                "relative_error",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Delta Alpha Shell Radius Comparison",
        "",
        (
            "External-field shell comparison:"
            if summary.get("field_source") == "external"
            else "Synthetic theorem-consistent check:"
        ),
        "",
        "`Delta alpha_s(r) = scale * j11 * delta * r / R`",
        "",
        "`r_n = n*pi*R/(scale*j11*delta)`",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Shells",
            "",
            "| n | predicted radius | observed radius | absolute error | relative error |",
            "|---:|---:|---:|---:|---:|",
        ]
    )
    for row in comparisons:
        lines.append(
            f"| {row.n} | {row.predicted_radius:.6f} | {row.observed_radius:.6f} | "
            f"{row.absolute_error:.6f} | {row.relative_error:.6%} |"
        )
    (output_dir / "delta_alpha_shell_comparison.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].plot(r_centers, profile, label="Radial profile")
    if len(observed):
        peak_indices = [int(np.argmin(np.abs(r_centers - radius))) for radius in observed]
        axes[0].scatter(
            observed,
            profile[peak_indices],
            color="red",
            label="Detected peaks",
            zorder=3,
        )
    axes[0].set_title("Radial Profile with Peaks")
    axes[0].set_xlabel("r")
    axes[0].set_ylabel("Mean absolute field")
    axes[0].legend()

    image = axes[1].imshow(
        field,
        extent=[
            -domain_half_width,
            domain_half_width,
            -domain_half_width,
            domain_half_width,
        ],
        origin="lower",
        cmap="viridis",
    )
    axes[1].set_title(
        "External Delta Alpha Field"
        if summary.get("field_source") == "external"
        else "Synthetic Delta Alpha Field"
    )
    fig.colorbar(image, ax=axes[1], fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(output_dir / "delta_alpha_shell_comparison.png", dpi=180)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare Delta-alpha Bessel shell predictions with detected synthetic radial peaks.",
    )
    parser.add_argument("--grid-size", type=int, default=500)
    parser.add_argument("--domain-half-width", type=float, default=1.0)
    parser.add_argument("--radial-bins", type=int, default=300)
    parser.add_argument("--oscillation-scale", type=float, default=10.0)
    parser.add_argument("--peak-height-fraction", type=float, default=0.1)
    parser.add_argument("--damping", type=float, default=2.0)
    parser.add_argument(
        "--profile-mode",
        choices=["raw_abs", "envelope_corrected_abs", "oscillatory_abs", "field"],
        default=None,
        help="Profile used for peak detection. raw_abs includes damping; the other modes isolate phase shells.",
    )
    parser.add_argument("--field-file", type=Path, default=None)
    parser.add_argument("--hdf5-dataset", type=str, default=None)
    parser.add_argument("--slice-index", type=int, default=0)
    parser.add_argument("--domain-radius", type=float, default=None)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("phase2_checks") / "delta_alpha_shell_run",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    external_field = (
        load_external_field(args.field_file, args.hdf5_dataset, args.slice_index)
        if args.field_file is not None
        else None
    )
    profile_mode = args.profile_mode
    if profile_mode is None:
        profile_mode = "raw_abs" if external_field is not None else "oscillatory_abs"
    summary, comparisons, r_centers, profile, observed, field = compare_shells(
        grid_size=args.grid_size,
        domain_half_width=args.domain_half_width,
        radial_bins=args.radial_bins,
        oscillation_scale=args.oscillation_scale,
        peak_height_fraction=args.peak_height_fraction,
        damping=args.damping,
        profile_mode=profile_mode,
        field=external_field,
        domain_radius_override=args.domain_radius,
    )
    if args.field_file is not None:
        summary["field_file"] = str(args.field_file)
        if args.hdf5_dataset is not None:
            summary["hdf5_dataset"] = args.hdf5_dataset
        summary["slice_index"] = args.slice_index
    write_outputs(
        output_dir=args.output_dir,
        summary=summary,
        comparisons=comparisons,
        r_centers=r_centers,
        profile=profile,
        observed=observed,
        field=field,
        domain_half_width=args.domain_half_width,
    )

    print("Delta alpha shell comparison")
    print(json.dumps(summary, indent=2))
    for row in comparisons:
        print(
            f"n={row.n}: pred={row.predicted_radius:.6f}, "
            f"obs={row.observed_radius:.6f}, error={row.absolute_error:.6f}, "
            f"rel={row.relative_error:.4%}"
        )


if __name__ == "__main__":
    main()
