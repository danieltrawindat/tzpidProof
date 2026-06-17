# TZPID Edge-Case Strengthening Batch

Generated UTC: 2026-06-11T10:54:26.524228+00:00

This is a curated rescue batch. It does not mutate the master registry. It identifies compact equations that strengthen the proof package by testing boundary behavior, conservation, topology, spectral roots, exact ratios, and closure equations.

| ID | Lane | HOL contract | Wolfram check | Equation | Proof value |
|---|---|---|---|---|---|
| ID0400 | Hubble/Friedmann breathing | `cosmological_density_contract` | `positive_cosmological_density` | \rho_\Lambda = (\hbar c/R^4)(\Phi_0/\Phi_{\mathrm{total}}) | Boundary scale check: finite positive radius and nonzero total flux make the density expression well-defined. |
| ID0024 | Vacuum cutoff / matter creation | `vacuum_cutoff_admissible` | `positive_vacuum_cutoff_integrand` | \rho_{\mathrm{vac}}^T=u_T^{-4}\int_0^{\omega_{\mathrm{cut}}}\eta(\omega)\hbar\omega\,d\omega | Cutoff guard: explicitly separates the finite cutoff assumption from the integral carrier. |
| ID0200 | Gyromagnetic movement / spectral modes | `alfven_mode_contract` | `alfven_speed_positive_domain` | v_A=B/\sqrt{\mu_0\rho},\quad k_n=n/R | High-impact supernode: ties MHD speed, radial quantization, and gyro dispersion into one reusable carrier. |
| ID0020 | Holonomy / winding | `half_integer_winding_contract` | `half_integer_winding_examples` | w=(2\pi)^{-1}\oint_\Gamma\nabla\theta\cdot d\ell,\quad w\in\tfrac12\mathbb Z | Topological edge case: makes half-integer winding an explicit carrier instead of loose prose. |
| ID0212 | Bessel bridge / gyromagnetic coupling | `bessel_gyro_product_contract` | `half_order_bessel_zero` | B(r,\theta)=\sum_{n=0}^{\infty}J_{n+1/2}(kr)e^{in\theta} | Connects the Bessel spectrum directly to the gyromagnetic field carrier. |
| ID0335 | Einstein recovery | `einstein_recovery_residual_zero` | `einstein_residual_zero` | G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi Gc^{-4}T_{\mu\nu}+\Phi^{TZP}_{\mu\nu},\quad \Phi^{TZP}_{\mu\nu}\to0 | Recovery guardrail: the correction term vanishes in the far-field limit. |
| ID0388 | Hubble/Friedmann breathing | `friedmann_component_contract` | `friedmann_positive_components` | H^2(a)=H_0^2(\Omega_m a^{-3}+\Omega_r a^{-4}+\Omega_k a^{-2}+\Omega_\Lambda) | Parameter scaffold for Hubble breathing, CMB/BAO/SN distance checks, and w0-wa extensions. |
| ID1816 | Poisson closure | `poisson_residual_zero` | `poisson_residual_zero` | \nabla^2\Phi=4\pi G_{\mathrm{eff}}\rho(x) | Shared terminal node for gravity and matter-creation papers. |
| ID9513 | Phase locking resonance | `kuramoto_threshold_contract` | `kuramoto_threshold_exact` | K=\|\omega_1-\omega_2\| | Sharp capture threshold for resonance locking and orbital synchronization. |
| ID2988 | Gyromagnetic movement / topology | `helicity_integral_contract` | `helicity_dot_product_sample` | \mathcal H_M=\int_V A\cdot B\,d^3x | MHD/topological invariant carrier for movement and helicity conservation. |
| ID3290 | Boundary spectral stress test | `helmholtz_residual_zero` | `helmholtz_residual_zero` | \nabla^2p+k^2p=0,\quad p\|_{\partial V}=f(\theta,\phi,t) | Boundary-condition stress test for spectral enclosure claims. |
| ID3330 | Hyperspherical projection | `spherical_mode_factor_contract` | `spherical_harmonic_normalization_sample` | Y_\ell^m(\theta,\phi)=N_{\ell m}P_\ell^m(\cos\theta)e^{im\phi} | Angular eigenmode carrier for projection from S3/S2 into radial spectra. |
| ID0040 | Gyromagnetic movement / MHD | `elsasser_contract` | `elsasser_critical_sample` | \Lambda=B^2/(\rho\mu\Omega^2),\quad \Lambda_{\mathrm{crit}}\approx1 | Criticality edge case for magnetic--rotational equipartition. |
| ID0188 | Matter creation threshold | `pressure_threshold_contract` | `pressure_threshold_boolean` | P_{\mathrm{vac}}\ge P_{\mathrm{crit}}\Rightarrow \rho_{\mathrm{matter}}\uparrow | Threshold carrier for matter-creation claims. |
| ID3435 | Exact ratio / threshold | `ratio_gate_contract` | `ratio_gate_gt_one` | B(\chi)=\Delta\phi(\chi)/\phi_c=33.34^\circ/30^\circ\approx10/9>1 | Rescued cleanup row: a compact exact-ratio gate that is easy to certify. |
| ID6515 | Spherical modes | `finite_mode_sum_contract` | `finite_mode_count_sample` | \Psi_{\rm wave}=\sum_{\ell\ge2}\sum_{m=-\ell}^{\ell}A_{\ell m}Y_\ell^m(\theta,\lambda)e^{i\omega_{\ell m}t} | Rescued mode-sum carrier for the enclosure projection lane. |
| ID1285 | Vacuum cutoff | `finite_cutoff_guard` | `finite_cutoff_integral_sample` | \langle\phi^2\rangle=\int_0^{\omega_{\mathrm{cut}}}\frac{\hbar}{2\omega}\eta(\omega)d\omega,\quad \omega_{\mathrm{cut}}<\infty | Rescued cutoff equation that turns divergence risk into an explicit assumption. |
| ID1507 | Conservation law | `helicity_sum_conservation_contract` | `constant_sum_derivative_zero` | \frac{d}{dt}(H_{\mathrm{field}}+H_{\mathrm{mech}})=0 | Rescued conservation guardrail for gyromagnetic motion. |
| ID1954 | Kaluza-Klein spectral edge case | `kk_massive_residual_zero` | `kk_residual_zero` | (\Box_{(4)}+n^2/R_{KK}^2)\phi_n=0 | Rescued KK spectral residual for higher-dimensional mode tests. |
| ID5228 | Poisson closure rescue | `density_poisson_contract` | `density_poisson_sample` | \rho=m_0n,\quad \nabla^2\Phi=4\pi G_{\rm eff}\rho | Rescued density-to-Poisson closure bridge. |
