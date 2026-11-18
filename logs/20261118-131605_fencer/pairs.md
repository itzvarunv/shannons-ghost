# Fencer run

Topics kept: 200 · extracted: 128 · pairs: 46

Accepted by judge + checker: 0

## F001 · rejected
- **A:** [Bouncing ball](https://en.wikipedia.org/wiki/Bouncing_ball) (mechanics): `F_G + F_D + F_M + F_B = m * D(v, t, 1)`
- **B:** [Acid catalysis](https://en.wikipedia.org/wiki/Acid_catalysis) (chemistry): `D(R1, t, 1) = -k * SH_plus * R1_conc * R2_conc`
- judge: related=False, score=0.0, reason: Different physical domains, equations represent completely unrelated phenomena.
- mapping: `{}` → judge said not related

## F002 · rejected
- **A:** [Heat exchanger](https://en.wikipedia.org/wiki/Heat_exchanger) (thermal): `J_1 * D(T_1, x, 1) = gamma * (T_2 - T_1)`
- **B:** [Cross section (physics)](https://en.wikipedia.org/wiki/Cross_section_(physics)) (nuclear): `D(Phi, z, 1) = -n * sigma * Phi`
- judge: related=False, score=0.0, reason: PDE for heat exchange versus ODE for nuclear cross-section.
- mapping: `{}` → judge said not related

## F003 · rejected
- **A:** [Slutsky equation](https://en.wikipedia.org/wiki/Slutsky_equation) (economics): `D(x_i, p_j, 1) = D(h_i, p_j, 1) - D(x_i, w, 1) * x_j`
- **B:** [Bickley jet](https://en.wikipedia.org/wiki/Bickley_jet) (fluids): `D(u, x, 1) + D(v, y, 1) = 0`
- judge: related=False, score=0.0, reason: Economics demand relation is not a fluid dynamics jet equation.
- mapping: `{}` → judge said not related

## F004 · rejected
- **A:** [Hyperbolic growth](https://en.wikipedia.org/wiki/Hyperbolic_growth) (population biology): `D(x, t, 1) = x**2 / K`
- **B:** [Optimal rotation age](https://en.wikipedia.org/wiki/Optimal_rotation_age) (economics): `D(V, t, 1) = a / (1 + b * t) * V * (1 - V / K)`
- judge: related=False, score=0.0, reason: Different ODE structures and parameters.
- mapping: `{}` → judge said not related

## F005 · rejected
- **A:** [Diffusion-controlled reaction](https://en.wikipedia.org/wiki/Diffusion-controlled_reaction) (chemistry): `D(B, r, 1) + B / (k_B * T) * D(U, r, 1) = 0`
- **B:** [Pharmacokinetics](https://en.wikipedia.org/wiki/Pharmacokinetics) (pharmacology): `D(C, t, 1) = -k_el * C`
- judge: related=False, score=0.0, reason: Diffusion-controlled reaction spatial PDE-like balance does not match pharmacokinetic decay ODE.
- mapping: `{}` → judge said not related

## F006 · rejected
- **A:** [Lotka–Volterra equations](https://en.wikipedia.org/wiki/Lotka–Volterra_equations) (population biology): `D(x, t, 1) = alpha * x - beta * x * y`
- **B:** [Compartmental models (epidemiology)](https://en.wikipedia.org/wiki/Compartmental_models_(epidemiology)) (epidemiology): `D(I, t, 1) = (beta / N) * I * S - gamma * I`
- judge: related=False, score=0.0, reason: Lotka-Volterra predator-prey equations differ in structure from standard SIR compartmental epidemic models.
- mapping: `{}` → judge said not related

## F007 · rejected
- **A:** [Evolutionary dynamics](https://en.wikipedia.org/wiki/Evolutionary_dynamics) (population biology): `D(s_i, t, 1) = k_i * D(W_i, s_i, 1)`
- **B:** [Heat bath](https://en.wikipedia.org/wiki/Heat_bath) (thermal): `D(S_Res, t, 1) = D(Q, t, 1) / T`
- judge: related=False, score=0.0, reason: Evolutionary dynamics PDE does not match thermal reservoir ODE.
- mapping: `{}` → judge said not related

## F008 · rejected
- **A:** [Classical mechanics](https://en.wikipedia.org/wiki/Classical_mechanics) (mechanics): `v = D(r, t, 1)`
- **B:** [Group delay and phase delay](https://en.wikipedia.org/wiki/Group_delay_and_phase_delay) (optics): `tau_g = -D(phi, omega, 1)`
- judge: related=False, score=0.0, reason: Kinematic definition of velocity does not match group delay signal processing relation.
- mapping: `{}` → judge said not related

## F009 · rejected
- **A:** [Consumer-resource model](https://en.wikipedia.org/wiki/Consumer-resource_model) (population biology): `dN_i/dt = N_i * g_i`
- **B:** [Control volume](https://en.wikipedia.org/wiki/Control_volume) (thermal): `d_dt = D(p, t, 1) + v * nabla`
- judge: related=False, score=0.0, reason: Consumer-resource population model does not match continuum mechanics material derivative.
- mapping: `{}` → judge said not related

## F010 · rejected · trivial form
- **A:** [Decay energy](https://en.wikipedia.org/wiki/Decay_energy) (nuclear): `Q = Rest_mass_before * c**2 - Rest_mass_after * c**2`
- **B:** [Classical general equilibrium model](https://en.wikipedia.org/wiki/Classical_general_equilibrium_model) (economics): `pi = Y_S - (w / p) * L_D`
- judge: related=False, score=0.0, reason: Nuclear decay energy mass-energy equivalence formula differs from general equilibrium profit equation.
- mapping: `{}` → judge said not related

## F011 · rejected · trivial form
- **A:** [Dead-beat control](https://en.wikipedia.org/wiki/Dead-beat_control) (control): `C_z = (A_z / B_1) / (z**d - B_z / B_1)`
- **B:** [Coate–Loury model](https://en.wikipedia.org/wiki/Coate–Loury_model) (economics): `xi = (pi * f_q) / (pi * f_q + (1 - pi) * f_u)`
- judge: related=False, score=0.0, reason: Different algebraic structures and parameters.
- mapping: `{}` → judge said not related

## F012 · rejected · trivial form
- **A:** [Critical heat flux](https://en.wikipedia.org/wiki/Critical_heat_flux) (thermal): `q_DNB = i_fg * rho_v * ((sigma * g * (rho_l - rho_v)) / rho_v**2)**(1/4) * (1 + rho_v / rho_l)`
- **B:** [Lipophilic efficiency](https://en.wikipedia.org/wiki/Lipophilic_efficiency) (pharmacology): `LiPE = pIC50 - LogP`
- judge: related=False, score=0.0, reason: Different physical and chemical definitions.
- mapping: `{}` → judge said not related

## F013 · rejected · trivial form
- **A:** [Dissipation factor](https://en.wikipedia.org/wiki/Dissipation_factor) (electrical): `DF = omega * C * ESR`
- **B:** [Activation energy asymptotics](https://en.wikipedia.org/wiki/Activation_energy_asymptotics) (fluids): `omega_T / omega_T_b = exp(-beta * (1 - theta) * (1 + q) / (1 + q * theta))`
- judge: related=False, score=0.0, reason: Different formulas representing different physical laws.
- mapping: `{}` → judge said not related

## F014 · rejected · trivial form
- **A:** [Batchelor vortex](https://en.wikipedia.org/wiki/Batchelor_vortex) (fluids): `R = sqrt(R_0**2 + 4 * nu * t)`
- **B:** [Coulomb barrier](https://en.wikipedia.org/wiki/Coulomb_barrier) (nuclear): `U_coulomb = (Z_1 * Z_2 * e**2) / (4 * 3.14159 * epsilon_0 * r)`
- judge: related=False, score=0.0, reason: Fluid dynamics vs electrostatics potential.
- mapping: `{}` → judge said not related

## F015 · rejected · trivial form
- **A:** [Annular velocity](https://en.wikipedia.org/wiki/Annular_velocity) (fluids): `AV = 1029.4 * PO_bpm / (ID**2 - OD**2)`
- **B:** [Kinetic chain length](https://en.wikipedia.org/wiki/Kinetic_chain_length) (chemistry): `nu = R_p / R_i`
- judge: related=False, score=0.0, reason: Hydraulics formula vs polymer chemistry ratio.
- mapping: `{}` → judge said not related

## F016 · rejected · trivial form
- **A:** [Forouhi–Bloomer model](https://en.wikipedia.org/wiki/Forouhi–Bloomer_model) (optics): `kappa = (A * (E - E_g)**2) / (E**2 - B * E + C)`
- **B:** [Cavity perturbation theory](https://en.wikipedia.org/wiki/Cavity_perturbation_theory) (electrical): `epsilon_r_prime - 1 = (f_c - f_s) / (2 * f_s) * (V_c / V_s)`
- judge: related=False, score=0.0, reason: Optics model vs cavity perturbation theory.
- mapping: `{}` → judge said not related

## F017 · rejected · trivial form
- **A:** [Grashof number](https://en.wikipedia.org/wiki/Grashof_number) (thermal): `Gr_L = (g * beta * (T_s - T_inf) * L**3) / (nu**2)`
- **B:** [Gradient-index optics](https://en.wikipedia.org/wiki/Gradient-index_optics) (optics): `n_r = n_o * (1 - A * r**2 / 2)`
- judge: related=False, score=0.0, reason: Dimensionless number vs refractive index profile.
- mapping: `{}` → judge said not related

## F018 · rejected · trivial form
- **A:** [Karlovitz number](https://en.wikipedia.org/wiki/Karlovitz_number) (chemistry): `Ka = t_F / t_eta`
- **B:** [Accumulation function](https://en.wikipedia.org/wiki/Accumulation_function) (finance): `A = A_0 * a`
- judge: related=False, score=0.0, reason: Ratio of time scales vs financial accumulation function.
- mapping: `{}` → judge said not related

## F019 · rejected · trivial form
- **A:** [Aghion–Howitt model](https://en.wikipedia.org/wiki/Aghion–Howitt_model) (economics): `y = A * x**alpha`
- **B:** [Mark and recapture](https://en.wikipedia.org/wiki/Mark_and_recapture) (population biology): `N_hat = n * K / k`
- judge: related=False, score=0.0, reason: Cobb-Douglas production function vs mark-recapture formula.
- mapping: `{}` → judge said not related

## F020 · rejected · trivial form
- **A:** [Dielectric loss](https://en.wikipedia.org/wiki/Dielectric_loss) (electrical): `tan_delta = (omega * epsilon + sigma) / (omega * epsilon_prime)`
- **B:** [Beat (acoustics)](https://en.wikipedia.org/wiki/Beat_(acoustics)) (mechanics): `f_beat = f_1 - f_2`
- judge: related=False, score=0.0, reason: Dielectric loss tangent vs acoustic beat frequency.
- mapping: `{}` → judge said not related

## F021 · rejected · trivial form
- **A:** [Binomial options pricing model](https://en.wikipedia.org/wiki/Binomial_options_pricing_model) (finance): `Binomial_Value = (p * Option_up + (1 - p) * Option_down) * exp(-r * delta_t)`
- **B:** [Blade element momentum theory](https://en.wikipedia.org/wiki/Blade_element_momentum_theory) (fluids): `0.5*rho*v**2 + P + rho*g*h = const`
- judge: related=False, score=0.0, reason: Finance option pricing and fluid dynamics Bernoulli/hydrostatic equations are entirely unrelated.
- mapping: `{}` → judge said not related

## F022 · rejected · trivial form
- **A:** [Bartels–Stewart algorithm](https://en.wikipedia.org/wiki/Bartels–Stewart_algorithm) (control): `A*X - X*B = C`
- **B:** [Analytical regularization](https://en.wikipedia.org/wiki/Analytical_regularization) (electrical): `X + A * X = B`
- judge: related=False, score=1.0, reason: Matrix Sylvester equation and Fredholm integral equation are from different mathematical domains.
- mapping: `{}` → judge said not related

## F023 · rejected · trivial form
- **A:** [AK model](https://en.wikipedia.org/wiki/AK_model) (economics): `Y = A*K`
- **B:** [Bennett acceptance ratio](https://en.wikipedia.org/wiki/Bennett_acceptance_ratio) (thermal): `delta_F = -k * T * log(exp(beta * (U_A - U_B)))`
- judge: related=False, score=0.0, reason: Economic growth linear production function and thermodynamic free energy difference equation are completely different.
- mapping: `{}` → judge said not related

## F024 · rejected · trivial form
- **A:** [Atomic ratio](https://en.wikipedia.org/wiki/Atomic_ratio) (chemistry): `atomic_ratio = atomic_percent_i / atomic_percent_j`
- **B:** [Huygens principle of double refraction](https://en.wikipedia.org/wiki/Huygens_principle_of_double_refraction) (optics): `k = omega / c`
- judge: related=False, score=0.0, reason: Chemistry atomic ratio and optics dispersion relation are unrelated.
- mapping: `{}` → judge said not related

## F025 · rejected · trivial form
- **A:** [Controllability Gramian](https://en.wikipedia.org/wiki/Controllability_Gramian) (control): `A * W_c + W_c * A_T = -B * B_T`
- **B:** [Input–output model](https://en.wikipedia.org/wiki/Input–output_model) (economics): `x = A * x + y`
- judge: related=False, score=1.0, reason: Controllability Gramian Lyapunov equation and economic input-output model are distinct.
- mapping: `{}` → judge said not related

## F026 · rejected · trivial form
- **A:** [Binding potential](https://en.wikipedia.org/wiki/Binding_potential) (pharmacology): `BP = R / K_i`
- **B:** [Electronic entropy](https://en.wikipedia.org/wiki/Electronic_entropy) (thermal): `p = 1 / (exp((E - E_F) / (k_B * T)) + 1)`
- judge: related=False, score=0.0, reason: Pharmacology receptor binding ratio and Fermi-Dirac electronic entropy distribution are unrelated.
- mapping: `{}` → judge said not related

## F027 · rejected · trivial form
- **A:** [Double marginalization](https://en.wikipedia.org/wiki/Double_marginalization) (economics): `p = 5 + 0.5 * w`
- **B:** [Electromagnetic stress–energy tensor](https://en.wikipedia.org/wiki/Electromagnetic_stress–energy_tensor) (electrical): `T_mu_nu = (1 / mu_0) * (F_mu_alpha * F_nu_alpha - 0.25 * eta_mu_nu * F_alpha_beta * F_alpha_beta)`
- judge: related=False, score=0.0, reason: Linear demand-price relation and relativistic electromagnetic stress-energy tensor are completely different.
- mapping: `{}` → judge said not related

## F028 · rejected · trivial form
- **A:** [Hydraulic engineering](https://en.wikipedia.org/wiki/Hydraulic_engineering) (fluids): `p = rho * g * y`
- **B:** [Detailed balance](https://en.wikipedia.org/wiki/Detailed_balance) (chemistry): `pi_i * P_ij = pi_j * P_ji`
- judge: related=False, score=0.0, reason: Hydrostatic pressure formula and Markov detailed balance condition describe completely different physical phenomena.
- mapping: `{}` → judge said not related

## F029 · rejected · trivial form
- **A:** [Fradkin tensor](https://en.wikipedia.org/wiki/Fradkin_tensor) (mechanics): `F_ij = (p_i * p_j) / (2 * m) + 0.5 * m * omega**2 * x_i * x_j`
- **B:** [Attributable fraction for the population](https://en.wikipedia.org/wiki/Attributable_fraction_for_the_population) (epidemiology): `AF_p = (I_p - I_u) / I_p`
- judge: related=False, score=0.0, reason: Harmonic oscillator energy tensor and epidemiological population attributable fraction are unrelated.
- mapping: `{}` → judge said not related

## F030 · rejected · trivial form
- **A:** [Classical probability density](https://en.wikipedia.org/wiki/Classical_probability_density) (mechanics): `P = (1/T) * (2 * m / (E - U))**0.5`
- **B:** [Electromagnetic mass](https://en.wikipedia.org/wiki/Electromagnetic_mass) (electrical): `m_elec = (2/3) * (e**2 / (a * c**2))`
- judge: related=False, score=0.0, reason: Classical harmonic oscillator probability density and electromagnetic mass formula are unrelated.
- mapping: `{}` → judge said not related

## F031 · rejected · trivial form
- **A:** [Electromagnetic tensor](https://en.wikipedia.org/wiki/Electromagnetic_tensor) (electrical): `F_mu_nu = D(A_nu, mu, 1) - D(A_mu, nu, 1)`
- **B:** [Asymptotic gain model](https://en.wikipedia.org/wiki/Asymptotic_gain_model) (control): `G = G_inf * (T / (T + 1)) + G_0 * (1 / (T + 1))`
- judge: related=False, score=0.0, reason: Different physical and mathematical domains.
- mapping: `{}` → judge said not related

## F032 · rejected · trivial form
- **A:** [Collision theory](https://en.wikipedia.org/wiki/Collision_theory) (chemistry): `r = k * n_A * n_B = Z * rho * exp(-E_a / (R * T))`
- **B:** [Acoustic tweezers](https://en.wikipedia.org/wiki/Acoustic_tweezers) (acoustics): `F_rad = -D(U, x, 1)`
- judge: related=False, score=0.0, reason: Chemistry reaction rates and acoustic radiation force are unrelated equations.
- mapping: `{}` → judge said not related

## F033 · rejected · trivial form
- **A:** [Acid dissociation constant](https://en.wikipedia.org/wiki/Acid_dissociation_constant) (chemistry): `K_a = (A_minus * H_plus) / HA`
- **B:** [Bonnet's theorem](https://en.wikipedia.org/wiki/Bonnet's_theorem) (mechanics): `v_combined = (v_1**2 + v_2**2 + v_n**2)**0.5`
- judge: related=False, score=0.0, reason: Chemical equilibrium constant and mechanical speed combination are completely different.
- mapping: `{}` → judge said not related

## F034 · rejected · trivial form
- **A:** [Case fatality rate](https://en.wikipedia.org/wiki/Case_fatality_rate) (epidemiology): `CFR = deaths / cases * 100`
- **B:** [Cross Gramian](https://en.wikipedia.org/wiki/Cross_Gramian) (control): `A * W_X + W_X * A = -B * C`
- judge: related=False, score=0.0, reason: Epidemiology percentage and control theory matrix Sylvester equation are unrelated.
- mapping: `{}` → judge said not related

## F035 · rejected · trivial form
- **A:** [Compound interest](https://en.wikipedia.org/wiki/Compound_interest) (finance): `A = P * (1 + r / n)**(t * n)`
- **B:** [Dividend discount model](https://en.wikipedia.org/wiki/Dividend_discount_model) (economics): `P = D_1 / (r - g)`
- judge: related=False, score=0.0, reason: Compound interest formula and dividend discount model do not match structurally.
- mapping: `{}` → judge said not related

## F036 · rejected · trivial form
- **A:** [Chemisorption](https://en.wikipedia.org/wiki/Chemisorption) (chemistry): `delta_G = delta_H - T * delta_S`
- **B:** [Spatial acceleration](https://en.wikipedia.org/wiki/Spatial_acceleration) (mechanics): `psi_P = a_P - omega * v_P`
- judge: related=False, score=0.0, reason: Gibbs free energy and rigid body spatial acceleration are unrelated.
- mapping: `{}` → judge said not related

## F037 · rejected · trivial form
- **A:** [Acoustic impedance](https://en.wikipedia.org/wiki/Acoustic_impedance) (acoustics): `p = R * Q`
- **B:** [Productive matrix](https://en.wikipedia.org/wiki/Productive_matrix) (economics): `P = (I_n - A)**-1 * U`
- judge: related=False, score=0.0, reason: Ohm's law-like acoustic impedance and Leontief inverse matrix product are different.
- mapping: `{}` → judge said not related

## F038 · rejected · trivial form
- **A:** [Churchill–Bernstein equation](https://en.wikipedia.org/wiki/Churchill–Bernstein_equation) (thermal): `Nu_D = 0.3 + (0.62 * Re_D**0.5 * Pr**(1/3)) / (1 + (0.4 / Pr)**(2/3))**0.25 * (1 + (Re_D / 282000)**(5/8))**0.8`
- **B:** [Cointegration](https://en.wikipedia.org/wiki/Cointegration) (finance): `y_t - beta * x_t = u_t`
- judge: related=False, score=0.0, reason: Empirical heat transfer Nusselt number correlation and econometric cointegration are unrelated.
- mapping: `{}` → judge said not related

## F039 · rejected · trivial form
- **A:** [Acoustic resonance](https://en.wikipedia.org/wiki/Acoustic_resonance) (acoustics): `f = n * v / (2 * L)`
- **B:** [Circular motion](https://en.wikipedia.org/wiki/Circular_motion) (mechanics): `F_c = m * v**2 / r`
- judge: related=False, score=0.0, reason: Standing wave frequency and centripetal force equations are structurally different.
- mapping: `{}` → judge said not related

## F040 · rejected · trivial form
- **A:** [Electric field](https://en.wikipedia.org/wiki/Electric_field) (electrical): `F = q * E`
- **B:** [Basic reproduction number](https://en.wikipedia.org/wiki/Basic_reproduction_number) (epidemiology): `R_0 = beta / gamma`
- judge: related=False, score=0.0, reason: Electrostatic force and epidemiological reproduction number are completely different.
- mapping: `{}` → judge said not related

## F041 · rejected · trivial form
- **A:** [Exact solutions of classical central-force problems](https://en.wikipedia.org/wiki/Exact_solutions_of_classical_central-force_problems) (mechanics): `F = a * r**n`
- **B:** [Cladding (fiber optics)](https://en.wikipedia.org/wiki/Cladding_(fiber_optics)) (optics): `NA = (n_core**2 - n_clad**2)**0.5`
- judge: related=False, score=0.0, reason: Different physical domains, distinct mathematical formulations.
- mapping: `{}` → judge said not related

## F042 · rejected · trivial form
- **A:** [Electromagnetism](https://en.wikipedia.org/wiki/Electromagnetism) (electrical): `F = q * (E + v * B)`
- **B:** [Arnold diffusion](https://en.wikipedia.org/wiki/Arnold_diffusion) (mechanics): `H_epsilon = H_0 + epsilon * H_1`
- judge: related=False, score=0.0, reason: Electromagnetic force law is not Arnold diffusion.
- mapping: `{}` → judge said not related

## F043 · rejected · trivial form
- **A:** [Delta neutral](https://en.wikipedia.org/wiki/Delta_neutral) (finance): `k = D(V, S, 1)`
- **B:** [Earth–ionosphere waveguide](https://en.wikipedia.org/wiki/Earth–ionosphere_waveguide) (electrical): `f_co = c / (4 * h)`
- judge: related=False, score=0.0, reason: Finance delta and waveguide cutoff frequency are completely unrelated.
- mapping: `{}` → judge said not related

## F044 · rejected · trivial form
- **A:** [Goldbeter–Koshland kinetics](https://en.wikipedia.org/wiki/Goldbeter–Koshland_kinetics) (chemistry): `z = (2 * v_1 * J_2) / (B + (B**2 - 4 * (v_2 - v_1) * v_1 * J_2)**0.5)`
- **B:** [Elastic energy](https://en.wikipedia.org/wiki/Elastic_energy) (mechanics): `U = 1/2 * k * x**2`
- judge: related=False, score=0.0, reason: Enzyme kinetics equation and elastic potential energy formula differ fundamentally.
- mapping: `{}` → judge said not related

## F045 · rejected · trivial form
- **A:** [Four factor formula](https://en.wikipedia.org/wiki/Four_factor_formula) (nuclear): `k = neutron_population_following_nth_generation / neutron_population_during_nth_generation`
- **B:** [Black-body radiation](https://en.wikipedia.org/wiki/Black-body_radiation) (thermal): `B_nu = (2 * h * nu**3) / (c**2 * (exp(h * nu / (k * T)) - 1))`
- judge: related=False, score=0.0, reason: Nuclear neutron multiplication and Planck's law for black-body radiation are unrelated.
- mapping: `{}` → judge said not related

## F046 · rejected · trivial form
- **A:** [Generation time](https://en.wikipedia.org/wiki/Generation_time) (population biology): `T = log(R_0) / r`
- **B:** [Ramsey problem](https://en.wikipedia.org/wiki/Ramsey_problem) (economics): `epsilon_i = D(q_i, p_i, 1) * p_i / q_i`
- judge: related=False, score=0.0, reason: Population generation time and Ramsey pricing elasticity formula are completely different.
- mapping: `{}` → judge said not related
