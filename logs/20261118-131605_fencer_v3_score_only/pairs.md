# Fencer run

Topics kept: 200 · extracted: 128 · pairs: 19

Flagged for review (judge score >= 7): 9, of which the checker verified the mapping: 6

## F003 · REVIEW · mapping verified
- **A:** [Optimal rotation age](https://en.wikipedia.org/wiki/Optimal_rotation_age) (economics): `D(V, t, 1) = a / (1 + b * t) * V * (1 - V / K)`
- **B:** [Carrying capacity](https://en.wikipedia.org/wiki/Carrying_capacity) (population biology): `D(N, t, 1) = r * N * (1 - N / K)`
- judge score: 9.0/10 · The economic tree growth model generalizes the standard logistic population growth equation.
- mapping: `{"V": "N", "t": "t", "a": "r", "b": "0", "K": "K"}` → A becomes B (A/B = 1)

## F006 · REVIEW · mapping verified
- **A:** [Aghion–Howitt model](https://en.wikipedia.org/wiki/Aghion–Howitt_model) (economics): `y = A * x**alpha`
- **B:** [Exact solutions of classical central-force problems](https://en.wikipedia.org/wiki/Exact_solutions_of_classical_central-force_problems) (mechanics): `F = a * r**n`
- judge score: 9.0/10 · Identical power-law algebraic relationship between economic output/forces and variables.
- mapping: `{"y": "F", "x": "r", "alpha": "n", "A": "a"}` → A becomes B (A/B = 1)

## F013 · REVIEW · mapping verified · trivial form
- **A:** [Lipophilic efficiency](https://en.wikipedia.org/wiki/Lipophilic_efficiency) (pharmacology): `LiPE = pIC50 - LogP`
- **B:** [Beat (acoustics)](https://en.wikipedia.org/wiki/Beat_(acoustics)) (mechanics): `f_beat = f_1 - f_2`
- judge score: 9.0/10 · Both equations are simple differences between two quantities yielding a metric.
- mapping: `{"LiPE": "f_beat", "pIC50": "f_1", "LogP": "f_2"}` → A becomes B (A/B = 1)

## F015 · REVIEW · mapping verified · trivial form
- **A:** [Karlovitz number](https://en.wikipedia.org/wiki/Karlovitz_number) (chemistry): `Ka = t_F / t_eta`
- **B:** [Binding potential](https://en.wikipedia.org/wiki/Binding_potential) (pharmacology): `BP = R / K_i`
- judge score: 9.0/10 · Both equations express a dimensionless or specific ratio between two characteristic parameters.
- mapping: `{"Ka": "BP", "t_F": "R", "t_eta": "K_i"}` → A becomes B (A/B = 1)

## F018 · REVIEW · mapping verified · trivial form
- **A:** [Acoustic impedance](https://en.wikipedia.org/wiki/Acoustic_impedance) (acoustics): `p = R * Q`
- **B:** [Electric field](https://en.wikipedia.org/wiki/Electric_field) (electrical): `F = q * E`
- judge score: 9.0/10 · Both represent a linear proportional relationship where a field multiplies a source term to yield a flow or force.
- mapping: `{"p": "F", "R": "E", "Q": "q"}` → A becomes B (A/B = 1)

## F005 · REVIEW
- **A:** [Lotka–Volterra equations](https://en.wikipedia.org/wiki/Lotka–Volterra_equations) (population biology): `D(x, t, 1) = alpha * x - beta * x * y`
- **B:** [Compartmental models (epidemiology)](https://en.wikipedia.org/wiki/Compartmental_models_(epidemiology)) (epidemiology): `D(I, t, 1) = (beta / N) * I * S - gamma * I`
- judge score: 8.0/10 · Epidemiological compartmental models are a direct reformulation of Lotka-Volterra predator-prey dynamics.
- mapping: `{"x": "I", "y": "S", "t": "t", "alpha": "-gamma", "beta": "0", "gamma": "0", "delta": "beta / N"}` → A does not become B (A/B = N*(gamma*I(t) + Derivative(I(t), t))/(N*(gamma*I(t) + Derivative(I(t), t)) - beta*I(t)*S(t)))

## F010 · REVIEW · mapping verified
- **A:** [Classical mechanics](https://en.wikipedia.org/wiki/Classical_mechanics) (mechanics): `v = D(r, t, 1)`
- **B:** [Group delay and phase delay](https://en.wikipedia.org/wiki/Group_delay_and_phase_delay) (optics): `tau_g = -D(phi, omega, 1)`
- judge score: 8.0/10 · Both define a derivative of a potential/phase function with respect to an independent scale.
- mapping: `{"v": "tau_g", "r": "-phi", "t": "omega"}` → A becomes B (A/B = 1)

## F011 · REVIEW
- **A:** [Input–output model](https://en.wikipedia.org/wiki/Input–output_model) (economics): `x = A * x + y`
- **B:** [Cointegration](https://en.wikipedia.org/wiki/Cointegration) (finance): `y_t - beta * x_t = u_t`
- judge score: 8.0/10 · Both equations represent linear relationships between dependent and independent variables with structural coefficients.
- mapping: `{"x": "y_t", "A": "beta", "y": "u_t"}` → A does not become B (A/B = (beta*y_t + u_t - y_t)/(beta*x_t + u_t - y_t))

## F017 · REVIEW · trivial form
- **A:** [Atomic ratio](https://en.wikipedia.org/wiki/Atomic_ratio) (chemistry): `atomic_ratio = atomic_percent_i / atomic_percent_j`
- **B:** [Case fatality rate](https://en.wikipedia.org/wiki/Case_fatality_rate) (epidemiology): `CFR = deaths / cases * 100`
- judge score: 7.0/10 · Both formulas compute proportions or relative ratios between two subsets of a population.
- mapping: `{"atomic_ratio": "CFR", "atomic_percent_i": "deaths", "atomic_percent_j": "cases"}` → A does not become B (A/B = (CFR*cases - deaths)/(CFR*cases - 100*deaths))

## F016 · low score · trivial form
- **A:** [Accumulation function](https://en.wikipedia.org/wiki/Accumulation_function) (finance): `A = A_0 * a`
- **B:** [AK model](https://en.wikipedia.org/wiki/AK_model) (economics): `Y = A*K`
- judge score: 6.0/10 · Both represent multiplicative growth models, though one is temporal and the other static.
- mapping: `{"A": "Y", "A_0": "1", "a": "A*K"}` → no independent variable in B for t

## F009 · low score
- **A:** [Detailed balance](https://en.wikipedia.org/wiki/Detailed_balance) (chemistry): `pi_i * P_ij = pi_j * P_ji`
- **B:** [Cross Gramian](https://en.wikipedia.org/wiki/Cross_Gramian) (control): `A * W_X + W_X * A = -B * C`
- judge score: 4.0/10 · Both express balance or symmetry conditions in linear systems.
- mapping: `{"pi_i": "W_X", "P_ij": "A", "pi_j": "W_X", "P_ji": "A"}` → A does not become B (A/B = 0)

## F001 · low score · mapping verified
- **A:** [Bloch oscillation](https://en.wikipedia.org/wiki/Bloch_oscillation) (mechanics): `D(p, t, 1) = -e * E`
- **B:** [Heat bath](https://en.wikipedia.org/wiki/Heat_bath) (thermal): `D(S_Res, t, 1) = D(Q, t, 1) / T`
- judge score: 3.0/10 · Both equations relate derivatives of a state variable to a forcing term over time.
- mapping: `{"p": "S_Res", "t": "t", "e": "-1", "E": "D(Q, t, 1) / T", "hbar": "1", "k": "1"}` → A becomes B (A/B = 1)

## F012 · low score
- **A:** [Group-velocity dispersion](https://en.wikipedia.org/wiki/Group-velocity_dispersion) (optics): `GVD = D(k, omega, 2)`
- **B:** [Control volume](https://en.wikipedia.org/wiki/Control_volume) (thermal): `d_dt = D(p, t, 1) + v * nabla`
- judge score: 3.0/10 · Both involve derivatives and rates of change, though in completely different physical contexts.
- mapping: `{"GVD": "d_dt", "omega_0": "t", "k": "v"}` → A does not become B (A/B = -d_dt(t)/(nabla*v - d_dt(t)))

## F014 · low score · mapping verified · trivial form
- **A:** [Kinetic chain length](https://en.wikipedia.org/wiki/Kinetic_chain_length) (chemistry): `nu = R_p / R_i`
- **B:** [Huygens principle of double refraction](https://en.wikipedia.org/wiki/Huygens_principle_of_double_refraction) (optics): `k = omega / c`
- judge score: 3.0/10 · Both define a ratio of physical quantities, but share little underlying mathematical methodology.
- mapping: `{"nu": "k", "R_p": "omega", "R_i": "c"}` → A becomes B (A/B = 1)

## F004 · low score
- **A:** [Cross section (physics)](https://en.wikipedia.org/wiki/Cross_section_(physics)) (nuclear): `D(Phi, z, 1) = -n * sigma * Phi`
- **B:** [Diffusion-controlled reaction](https://en.wikipedia.org/wiki/Diffusion-controlled_reaction) (chemistry): `D(B, r, 1) + B / (k_B * T) * D(U, r, 1) = 0`
- judge score: 2.0/10 · Both involve exponential attenuation or gradient transport, but different differential equations.
- mapping: `{"Phi": "B", "z": "r", "n": "1 / (k_B * T)", "sigma": "D_AB"}` → A does not become B (A/B = (D_AB*B(r) + T*k_B*Derivative(B(r), r))/(T*k_B*Derivative(B(r), r)))

## F007 · low score · mapping verified
- **A:** [Mark and recapture](https://en.wikipedia.org/wiki/Mark_and_recapture) (population biology): `N_hat = n * K / k`
- **B:** [Acid dissociation constant](https://en.wikipedia.org/wiki/Acid_dissociation_constant) (chemistry): `K_a = (A_minus * H_plus) / HA`
- judge score: 2.0/10 · Simple ratio algebra appears in both, but underlying concepts of ecology and chemistry differ.
- mapping: `{"N_hat": "K_a", "n": "A_minus", "K": "H_plus", "k": "HA"}` → A becomes B (A/B = 1)

## F008 · low score
- **A:** [Analytical regularization](https://en.wikipedia.org/wiki/Analytical_regularization) (electrical): `X + A * X = B`
- **B:** [Chemisorption](https://en.wikipedia.org/wiki/Chemisorption) (chemistry): `delta_G = delta_H - T * delta_S`
- judge score: 2.0/10 · Superficially linear algebraic, but completely unrelated thermodynamic and regularization contexts.
- mapping: `{"X": "delta_G", "A": "T", "B": "delta_H - delta_S"}` → A does not become B (A/B = (T*delta_G + delta_G - delta_H + delta_S)/(T*delta_S + delta_G - delta_H))

## F019 · low score · mapping verified · trivial form
- **A:** [Basic reproduction number](https://en.wikipedia.org/wiki/Basic_reproduction_number) (epidemiology): `R_0 = beta / gamma`
- **B:** [Earth–ionosphere waveguide](https://en.wikipedia.org/wiki/Earth–ionosphere_waveguide) (electrical): `f_co = c / (4 * h)`
- judge score: 2.0/10 · Both are algebraic quotients of two parameters, but represent entirely unrelated physical phenomena.
- mapping: `{"R_0": "f_co", "beta": "c", "gamma": "4 * h"}` → A becomes B (A/B = 1)

## F002 · low score · mapping verified
- **A:** [Dissipation factor](https://en.wikipedia.org/wiki/Dissipation_factor) (electrical): `DF = omega * C * ESR`
- **B:** [Hydraulic engineering](https://en.wikipedia.org/wiki/Hydraulic_engineering) (fluids): `p = rho * g * y`
- judge score: 1.0/10 · Completely different physical domains and mathematical structures sharing only algebraic variable formatting.
- mapping: `{"DF": "p", "omega": "rho", "C": "g", "ESR": "y"}` → A becomes B (A/B = 1)
