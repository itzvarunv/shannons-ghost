# Fencer run

Topics kept: 200 · extracted: 128 · pairs: 19

Accepted by judge + checker: 2

## F001 · rejected
- **A:** [Bloch oscillation](https://en.wikipedia.org/wiki/Bloch_oscillation) (mechanics): `D(p, t, 1) = -e * E`
- **B:** [Heat bath](https://en.wikipedia.org/wiki/Heat_bath) (thermal): `D(S_Res, t, 1) = D(Q, t, 1) / T`
- judge: related=False, score=0.0, reason: Different physical domains and unrelated mathematical equations.
- mapping: `{}` → judge said not related

## F002 · rejected
- **A:** [Dissipation factor](https://en.wikipedia.org/wiki/Dissipation_factor) (electrical): `DF = omega * C * ESR`
- **B:** [Hydraulic engineering](https://en.wikipedia.org/wiki/Hydraulic_engineering) (fluids): `p = rho * g * y`
- judge: related=False, score=0.0, reason: One is an electrical circuit relation, the other is hydrostatic pressure.
- mapping: `{}` → judge said not related

## F003 · rejected
- **A:** [Optimal rotation age](https://en.wikipedia.org/wiki/Optimal_rotation_age) (economics): `D(V, t, 1) = a / (1 + b * t) * V * (1 - V / K)`
- **B:** [Carrying capacity](https://en.wikipedia.org/wiki/Carrying_capacity) (population biology): `D(N, t, 1) = r * N * (1 - N / K)`
- judge: related=False, score=2.0, reason: Different ODE structures; timber growth has time-dependent coefficients unlike standard logistic growth.
- mapping: `{}` → judge said not related

## F004 · rejected
- **A:** [Cross section (physics)](https://en.wikipedia.org/wiki/Cross_section_(physics)) (nuclear): `D(Phi, z, 1) = -n * sigma * Phi`
- **B:** [Diffusion-controlled reaction](https://en.wikipedia.org/wiki/Diffusion-controlled_reaction) (chemistry): `D(B, r, 1) + B / (k_B * T) * D(U, r, 1) = 0`
- judge: related=False, score=0.0, reason: Different differential equations describing distinct physical processes.
- mapping: `{}` → judge said not related

## F005 · rejected
- **A:** [Lotka–Volterra equations](https://en.wikipedia.org/wiki/Lotka–Volterra_equations) (population biology): `D(x, t, 1) = alpha * x - beta * x * y`
- **B:** [Compartmental models (epidemiology)](https://en.wikipedia.org/wiki/Compartmental_models_(epidemiology)) (epidemiology): `D(I, t, 1) = (beta / N) * I * S - gamma * I`
- judge: related=False, score=3.0, reason: Both are population models, but specific equations and variables do not match.
- mapping: `{}` → judge said not related

## F006 · rejected
- **A:** [Aghion–Howitt model](https://en.wikipedia.org/wiki/Aghion–Howitt_model) (economics): `y = A * x**alpha`
- **B:** [Exact solutions of classical central-force problems](https://en.wikipedia.org/wiki/Exact_solutions_of_classical_central-force_problems) (mechanics): `F = a * r**n`
- judge: related=False, score=0.0, reason: Economic production function and central-force potential have different meanings and variables.
- mapping: `{}` → judge said not related

## F007 · rejected
- **A:** [Mark and recapture](https://en.wikipedia.org/wiki/Mark_and_recapture) (population biology): `N_hat = n * K / k`
- **B:** [Acid dissociation constant](https://en.wikipedia.org/wiki/Acid_dissociation_constant) (chemistry): `K_a = (A_minus * H_plus) / HA`
- judge: related=False, score=0.0, reason: Statistical mark-recapture estimator formula differs fundamentally from chemical equilibrium constant expression.
- mapping: `{}` → judge said not related

## F008 · rejected
- **A:** [Analytical regularization](https://en.wikipedia.org/wiki/Analytical_regularization) (electrical): `X + A * X = B`
- **B:** [Chemisorption](https://en.wikipedia.org/wiki/Chemisorption) (chemistry): `delta_G = delta_H - T * delta_S`
- judge: related=False, score=0.0, reason: Linear operator equation and thermodynamic Gibbs free energy relation are unrelated.
- mapping: `{}` → judge said not related

## F009 · rejected
- **A:** [Detailed balance](https://en.wikipedia.org/wiki/Detailed_balance) (chemistry): `pi_i * P_ij = pi_j * P_ji`
- **B:** [Cross Gramian](https://en.wikipedia.org/wiki/Cross_Gramian) (control): `A * W_X + W_X * A = -B * C`
- judge: related=False, score=0.0, reason: Detailed balance product relation is not structurally identical to the matrix Sylvester equation.
- mapping: `{}` → judge said not related

## F010 · ACCEPTED
- **A:** [Classical mechanics](https://en.wikipedia.org/wiki/Classical_mechanics) (mechanics): `v = D(r, t, 1)`
- **B:** [Group delay and phase delay](https://en.wikipedia.org/wiki/Group_delay_and_phase_delay) (optics): `tau_g = -D(phi, omega, 1)`
- judge: related=True, score=9.0, reason: Both define velocity/delay as the negative derivative of position/phase with respect to time/frequency.
- mapping: `{"v": "tau_g", "r": "-phi", "t": "omega"}` → A becomes B (A/B = 1)

## F011 · rejected
- **A:** [Input–output model](https://en.wikipedia.org/wiki/Input–output_model) (economics): `x = A * x + y`
- **B:** [Cointegration](https://en.wikipedia.org/wiki/Cointegration) (finance): `y_t - beta * x_t = u_t`
- judge: related=False, score=0.0, reason: Input-output model and cointegration represent different economic concepts with completely different equations.
- mapping: `{}` → judge said not related

## F012 · rejected
- **A:** [Group-velocity dispersion](https://en.wikipedia.org/wiki/Group-velocity_dispersion) (optics): `GVD = D(k, omega, 2)`
- **B:** [Control volume](https://en.wikipedia.org/wiki/Control_volume) (thermal): `d_dt = D(p, t, 1) + v * nabla`
- judge: related=False, score=0.0, reason: Optics dispersion and control volume thermodynamic balance are fundamentally unrelated physical processes.
- mapping: `{}` → judge said not related

## F013 · rejected · trivial form
- **A:** [Lipophilic efficiency](https://en.wikipedia.org/wiki/Lipophilic_efficiency) (pharmacology): `LiPE = pIC50 - LogP`
- **B:** [Beat (acoustics)](https://en.wikipedia.org/wiki/Beat_(acoustics)) (mechanics): `f_beat = f_1 - f_2`
- judge: related=False, score=0.0, reason: Lipophilic efficiency and acoustic beats share a subtraction form but describe completely unrelated domains.
- mapping: `{}` → judge said not related

## F014 · rejected · trivial form
- **A:** [Kinetic chain length](https://en.wikipedia.org/wiki/Kinetic_chain_length) (chemistry): `nu = R_p / R_i`
- **B:** [Huygens principle of double refraction](https://en.wikipedia.org/wiki/Huygens_principle_of_double_refraction) (optics): `k = omega / c`
- judge: related=False, score=0.0, reason: Polymer kinetic chain length and optical wave number formulas represent different physical phenomena.
- mapping: `{}` → judge said not related

## F015 · ACCEPTED · trivial form
- **A:** [Karlovitz number](https://en.wikipedia.org/wiki/Karlovitz_number) (chemistry): `Ka = t_F / t_eta`
- **B:** [Binding potential](https://en.wikipedia.org/wiki/Binding_potential) (pharmacology): `BP = R / K_i`
- judge: related=True, score=10.0, reason: Both equations represent a simple ratio of two quantities, mapping directly to each other.
- mapping: `{"Ka": "BP", "t_F": "R", "t_eta": "K_i"}` → A becomes B (A/B = 1)

## F016 · rejected · trivial form
- **A:** [Accumulation function](https://en.wikipedia.org/wiki/Accumulation_function) (finance): `A = A_0 * a`
- **B:** [AK model](https://en.wikipedia.org/wiki/AK_model) (economics): `Y = A*K`
- judge: related=False, score=2.0, reason: Actuarial accumulation and macroeconomics AK model use multiplication but represent distinct concepts.
- mapping: `{}` → judge said not related

## F017 · rejected · trivial form
- **A:** [Atomic ratio](https://en.wikipedia.org/wiki/Atomic_ratio) (chemistry): `atomic_ratio = atomic_percent_i / atomic_percent_j`
- **B:** [Case fatality rate](https://en.wikipedia.org/wiki/Case_fatality_rate) (epidemiology): `CFR = deaths / cases * 100`
- judge: related=False, score=0.0, reason: Atomic ratios and case fatality rates are conceptually distinct ratios from different fields.
- mapping: `{}` → judge said not related

## F018 · rejected · trivial form
- **A:** [Acoustic impedance](https://en.wikipedia.org/wiki/Acoustic_impedance) (acoustics): `p = R * Q`
- **B:** [Electric field](https://en.wikipedia.org/wiki/Electric_field) (electrical): `F = q * E`
- judge: related=False, score=3.0, reason: Acoustic impedance and electric force share a product form but have different physical dimensions.
- mapping: `{}` → judge said not related

## F019 · rejected · trivial form
- **A:** [Basic reproduction number](https://en.wikipedia.org/wiki/Basic_reproduction_number) (epidemiology): `R_0 = beta / gamma`
- **B:** [Earth–ionosphere waveguide](https://en.wikipedia.org/wiki/Earth–ionosphere_waveguide) (electrical): `f_co = c / (4 * h)`
- judge: related=False, score=0.0, reason: Epidemiological reproduction numbers and earth-ionosphere waveguide cutoff frequencies are completely unrelated.
- mapping: `{}` → judge said not related
