import numpy as np


class Support_Type:
    def __init__(
        self, support_type, lumber_type, depth, breadth, length, mod_of_elast, **kwargs
    ):
        """Used to cover all support types: beams, columns, and thier combination
        Parameters
        ----------
        support_type : str
            Type of structure to be used {"beam", "column", "beam_column"}
        lumber_type : str
            Type of wood to be used {"lumber", "glulam", "log"}
        depth : float
            depth of support (inches)
        breadth : float
            width (breadth) of support (inches)
        length : float
            length of support (inches)
        mod_of_elast: float
            modulus of elasticity (psi)
        """
        if support_type.lower in ["beam", "column", "beam_column"]:
            self.support_type = support_type
        else:
            raise ValueError(
                "support_type can only be 'beam', 'column', or 'beam_column'."
            )

        if lumber_type.lower in ["lumber", "glulam", "log"]:
            self.lumber_type = lumber_type.lower
        else:
            raise ValueError("lumber_type can only be 'log', 'lumber', or 'glulam'.")

        self.depth = depth
        self.breadth = breadth
        self.mod_of_elast = mod_of_elast

    def modulus_of_elasticity(self):
        """
        Notes
        -----
        E_05 : The 5% exclusion limit value
        CoVE : coefficient of variation for modulus of elasticity
            0.25 for visually graded lumber
            0.1 for structural glued laminated timber
        """
        if self.lumber_type == "lumber":
            CoVE = 0.25
            E_05 = self.mod_of_elast * (1 - 1.645 * CoVE)
            self.mod_of_elast_min = 1.03 * E_05 / 1.66
        elif self.lumber_type == "glulam":
            CoVE = 0.1
            E_05 = self.mod_of_elast * (1 - 1.645 * CoVE)
            self.mod_of_elast_min = 1.05 * E_05 / 1.66
        elif self.lumber_type == "log":
            raise NotImplementedError()
        else:
            raise ValueError("lumber_type can only be 'log', 'lumber', or 'glulam'.")

    def effective_length(self, l_u, K_e):
        """Can also be found in table 3.4.3.1.1-1 pg. 80
        Parameters
        ----------
        l_u : The unbraced length of a compression member, i.e. the distance between two points along its length,
            between which the member is not prevented from buckling.
        K_e : Effective Column Length Factor for various bracing (see Table 3.4.3.9.2-1 pg. 89)
        """
        return K_e * l_u

    def estimated_shrinkage(self, S_0, m_i, m_f):
        """Estimates Wood Shrinkage.
        From American Institute of Timber Construction - Timber construction manual-Wiley (2012) page 51.
        Parameters
        ----------
        S_0 : total shrinkage from Table 2.3.1-1
        m_f : final moisture content (at or below 30%)
        m_i : initial moisture content (at or below 30%)
        """
        return S_0 * (m_i - m_f) / 0.3

    def tension_stresses(self, T, A_n):
        """
        Parameters
        ----------
        T : tension force
        A_n : net or effective area considering section loss due to holes and notches
        """
        return T / A_n

    def volume_factor(self, Length, x=10.0):
        """Used for Glulam
        Parameters
        ----------
        Length = length of member between points of zero moment (feet)
        x : 20 for Southern Pine, and 10 for other species
        """
        return (
            ((5.125 / self.breadth) ** (1 / x))
            * ((12.0 / self.depth) ** (1 / x))
            * ((21.0 / Length) ** (1 / x))
        )

    def moment_of_inertia(self):
        """
        Parameters
        ----------
        d : depth of beam
        b : width (breadth) of beam
        """
        return self.breadth * (self.depth ** 3) / 12.0

    def slenderness_ratio(
        self, l_u, l_e=0.0, K_e=0.0, k=1.73, structure_type="beam", moments={}
    ):
        """
        Parameters
        ----------
        l_u : the unbraced length
        l_e : effective length of "beam"
        K_e : Effective Column Length Factor for various bracing (see Table 3.4.3.9.2-1 pg. 89)
        k : The value of k is given in Table 3.4.3.1.2-1 for select cases
             and can be conservatively taken as 1.72 for all other cases.
        structure_type : Used to select either "beam" or "column"
        moments : Used to calculate slenderness_ratio with method of moments on beam Equation 3.4.3.1.2-2
        """
        if structure_type == "column":
            if l_e == 0.0:
                l_e = self.effective_length(l_u, K_e)
            return l_e / self.depth
        elif structure_type == "beam":
            if moments:
                eta = 1.3 * k * self.depth / l_u
                C_e = np.sqrt(eta ** 2 + 1) - eta
                if "M_max" in moments.keys():
                    C_b = (
                        12.5
                        * moments["M_max"]
                        / (
                            3 * moments["M_a"]
                            + 4 * moments["M_b"]
                            + 3 * moments["M_c"]
                            + 2.5 * moments["M_max"]
                        )
                    )
                else:
                    # Eqn. 3.4.3.1.2-5 for top braced beams?
                    C_b = (
                        3.0
                        - (2 / 3) * (moments["M_1"] / moments["M_0"])
                        - (8 / 3) * moments["M_CL"] / (moments["M_1"] + moments["M_0"])
                    )
                return np.sqrt(1.84 * l_u * self.depth / C_b / C_e / self.breadth ** 2)
            else:
                return np.sqrt(l_e * self.depth / self.breadth ** 2)
        else:
            raise ValueError("structure_type can only be 'beam' or 'column'.")

    def critical_buckling_design_value(
        self,
        l_e,
        E_min_prime,
        K_e=1.0,
        material_type="log",
        structure_type="beam",
    ):
        """Calculates critical buckling design value.
        From American Institute of Timber Construction - Timber construction manual-Wiley (2012) page 140
        Parameters
        ----------
        l_e : effective length in bending found in table 3.4.3.1.1-1
        E_min_prime :  adjusted modulus of elasticity for beam and column stability calculations
        lumber_type : Used to determine scaling and slenderness ratio
        structure_type : Used to select either "beam" or "column"
        """
        # print(f"Using structure type: {structure_type}")
        # print(f"Using material type: {material_type}")
        s_r = self.slenderness_ratio(
            l_e,
            self.depth,
            l_e=l_e,
            b=self.breadth,
            K_e=K_e,
            structure_type=structure_type,
        )
        if structure_type == "column":
            if material_type == "log":
                if s_r > 43.0:
                    print("slenderness_ratio must be less than 43.")
                scale = 0.617
            else:
                if s_r > 50.0:  # <75 for construction
                    print(
                        "slenderness_ratio must be less",
                        "than 50 in the completed structure and less than 75 during construction.",
                    )
                scale = 0.822
        elif structure_type == "beam":
            if material_type == "log":
                print("EMPTY")
                scale = 1.2
            else:
                scale = 1.2
        else:
            raise ValueError("structure_type can only be 'beam' or 'column'.")

        return scale * E_min_prime / (s_r ** 2)

    def stability_factor(self, F_E, F_star, lumber_type="log", structure_type="beam"):
        """
        Parameters
        ----------
        F_E : critical buckling design value (either F_bE for 'beam' or F_cE for 'column')
            (Equation 3.4.3.1-2 or Equation 3.4.3.9-2, respectively)
        F_star :
            'column' : reference compression design value multiplied by all applicable adjustment factors except C_P
            'beam' : reference bending design value multiplied by all applicable adjustment factors
                 except Cfu, CL, CV, and CI
        lumber_type : Used to determine "c":
            "lumber" = 0.8 for sawn lumber
            "log" = 0.85 for round timber poles and piles
            "glulam" = 0.90 for structural glued laminated timber
        structure_type : Used to select either "beam" or "column"
        """
        # print(f"Using structure type: {structure_type}")
        if structure_type == "column":
            if self.lumber_type == "log":
                c = 0.8
            elif self.lumber_type == "lumber":
                c = 0.85
            elif self.lumber_type == "glulam":
                c = 0.9
            else:
                raise ValueError(
                    "lumber_type can only be 'log', 'lumber', or 'glulam'."
                )

            first_factor = (1 + F_E / F_star) / 2.0 / c
            second_factor = np.sqrt(first_factor ** 2 - F_E / F_star / c)
        elif structure_type == "beam":
            first_factor = (1 + (F_E / F_star)) / 1.9
            second_factor = np.sqrt(first_factor ** 2 - (F_E / F_star / 0.95))
        else:
            raise ValueError("structure_type can only be 'beam' or 'column'.")

        return first_factor - second_factor

    def general_eqn_for_beam_columns(
        self,
        d1,
        d2,
        l_e_c,
        l_e_b,
        e1,
        e2,
        f_c,
        f_b1,
        f_b2,
        F_c_prime,
        F_b1_prime,
        F_b2_prime,
        E_min_prime_1,
        E_min_prime_2,
        E_min_prime_c,
    ):
        """
        Parameters
        ----------
        d1 : wide face dimension
        d2 : narrow face dimension
        l_e_c : Effective length of the column (inches)
        l_e_b : Effective length of the beam (inches)
        e1 : strong axis load eccentricity
        e2 : weak axis load eccentricity
        f_c : axial compression stress
        f_b1 : strong axis bending stress
        f_b2 : weak axis bending stress
        F_c_prime : adjusted compression stress
        F_b1_prime : strong axis adjusted bending stress b1
        F_b2_prime : weak axis adjusted bending stress b2
        E_min_prime_1 : strong axis Minimum Modulus of Eccentricity
        E_min_prime_2 : weak axis Minimum Modulus of Eccentricity
        Notes
        -----
        F_bE : critical buckling design value for bending
        F_cE1 : critical buckling design value for strong axis buckling
        F_cE2 : critical buckling design value for weak axis buckling
        """
        F_cE1 = self.critical_buckling_design_value(
            l_e_c,
            E_min_prime_1,
            d1,
            b=0.0,
            K_e=1.0,
            material_type="lumber",
            structure_type="column",
        )
        F_cE2 = self.critical_buckling_design_value(
            l_e_c,
            E_min_prime_2,
            d2,
            b=0.0,
            K_e=1.0,
            material_type="lumber",
            structure_type="column",
        )
        F_bE = self.critical_buckling_design_value(
            l_e_b,
            E_min_prime_c,
            d1,
            b=d2,
            K_e=1.0,
            material_type="lumber",
            structure_type="beam",
        )

        print(F_cE1, F_cE2, F_bE)
        if f_c >= F_cE1:
            print(
                f"{f_c} >= {F_cE1} compression stress exceeds critical buckling design value for strong axis buckling"
            )
        else:
            print(
                f"{f_c} < {F_cE1} compression stress within critical buckling design value for strong axis buckling"
            )

        if f_c >= F_cE2:
            print(
                f"{f_c} >= {F_cE2} compression stress exceeds critical buckling design value for weak axis buckling"
            )
        else:
            print(
                f"{f_c} < {F_cE2} compression stress exceeds critical buckling design value for weak axis buckling"
            )

        if f_b1 >= F_bE:
            print(
                f"{f_b1} >= {F_bE} compression stress exceeds critical buckling design value for weak axis buckling"
            )
        else:
            print(
                f"{f_b1} < {F_bE} compression stress exceeds critical buckling design value for weak axis buckling"
            )

        first_factor = (f_c / F_c_prime) ** 2
        second_factor_top = f_b1 + f_c * (6 * e1 / d1) * (1 + (0.234 * f_c / F_cE1))
        second_factor_bottom = F_b1_prime * (1 - (f_c / F_cE1))
        third_factor_subfactor = ((f_b1 + f_c * (6 * e1 / d1)) / F_bE) ** 2

        excess_capacity = f_c / F_cE2 + third_factor_subfactor
        if excess_capacity >= 1.0:
            print(
                f"{excess_capacity} >= {1.} overstress in weak axis bending",
                "is being masked by excess capacity in compression and strong axis bending",
            )
        else:
            print(
                f"{excess_capacity} < {1.} overstress in weak axis bending is not masked by",
                "excess capacity in compression and strong axis bending",
            )

        if F_cE2 == 0.0:  # Don't divide by zero
            return first_factor + (second_factor_top / second_factor_bottom)
        else:
            third_factor_top = f_b2 + f_c * (6 * e2 / d2) * (
                1 + (0.234 * f_c / F_cE2) + 0.234 * third_factor_subfactor
            )
            third_factor_bottom = F_b2_prime * (
                1 - (f_c / F_cE2) - third_factor_subfactor
            )
            if third_factor_bottom == 0.0:  # Don't divide by zero
                return first_factor + (second_factor_top / second_factor_bottom)
            else:
                return (
                    first_factor
                    + (second_factor_top / second_factor_bottom)
                    + (third_factor_top / third_factor_bottom)
                )


class Beam(Support_Type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Wood Type to get all the properties
        # Extract this from choice/database?

    def flat_use_or_size_factor(self):
        """The size factor for 5 in. × 5 in. and larger sawn timbers of depth greater than 12 in.
        with loads applied to the narrow face is determined by Equation 3.4.3.2-1
        Notes
        -----
        AKA Flat Use Factor: members are placed flat-wise and loaded perpendicular to the wide face,
        the design values for bending may be increased using the flat-use factor by this factor.
        """
        # 12 inches
        return (12 / self.depth) ** (1 / 9)

    def deflection(self, w, load_case=2, a=0.0):
        """Calculates deflection
        Parameters
        ----------
        w : force on beam (either uniform or at a) (in psi
        load_case : int between 0 and 5 corresponding to above diagram
        a : location of force if non-uniform
        """
        mom_of_inert = self.moment_of_inertia(self.depth, self.breadth)
        if load_case == 0:
            return (w * self.length ** 3) / 3.0 / self.mod_of_elast / self.length
        elif load_case == 1:
            return (
                (w * a ** 2 * (3.0 * self.length - a))
                / 6.0
                / self.mod_of_elast
                / mom_of_inert
            )
        elif load_case == 2:
            return (w * (self.length ** 4)) / 8.0 / self.mod_of_elast / mom_of_inert
        elif load_case == 3:
            return (w * self.length ** 4) / 30.0 / self.mod_of_elast / mom_of_inert
        elif load_case == 4:
            return (
                (11.0 * w * self.length ** 4) / 120.0 / self.mod_of_elast / mom_of_inert
            )
        elif load_case == 5:
            return (w * self.length ** 2) / 2.0 / self.mod_of_elast / mom_of_inert

    def bending_stress(self, M, F_b_prime=0.0):
        """Calculates bending stress for a square beam, for nonsquare, see eqn. 4.2.1-1.
        From American Institute of Timber Construction - Timber construction manual-Wiley (2012) page 103
        Parameters
        ----------
        d : "column" : member diameter
            "beam" : member depth
        b : width (breadth) if "beam"
        M : bending moment due to applied loads
        F_b_prime : adjusted bending stress
        """
        f_b = 6 * M / self.breadth / self.depth ** 2
        if F_b_prime > 0:
            if f_b > F_b_prime:
                print(f"{f_b} > {F_b_prime} bending stress exceeds allowable design")
            else:
                print(f"{f_b} <= {F_b_prime} bending stress within allowable design")
        else:
            print("No adjusted bending stress assigned.")
        return f_b

    def shear_force(self, force):
        """force at end of the beam from a uniform force.
        Since we can exclude the distributed loads applied within a distance d of the end, we subtract it off.
        Parameters
        ----------
        force : uniform force on beam
        """
        return force * self.length / 2 - force * self.depth

    def shear_stress(self, V, F_v_prime=0.0):
        """Calculates shear stress for a square beam, for nonsquare, see eqn. 4.2.2-1.
        From American Institute of Timber Construction - Timber construction manual-Wiley (2012) page 104
        Parameters
        ----------
        V : Shear Force
        F_v_prime : adjusted shear stress
        """
        f_v = 3 * V / 2 / self.breadth / self.depth
        if F_v_prime > 0:
            if f_v > F_v_prime:
                print(f"{f_v} > {F_v_prime} shear stress exceeds allowable design")
            else:
                print(f"{f_v} <= {F_v_prime} shear stress within allowable design")
        else:
            print("No adjusted shear stress assigned.")
        return f_v

    def beam_weight(self, density):
        """Calculates beam weight
        Parameters
        ----------
        density : wood density (pounds per cubic inch)
        """
        return self.depth * self.breadth * density

    def allowable_bending_stress(self, f_c, F_bx_star, C_V, C_L):
        """
        Parameters
        ----------
        F_bx_star :
        C_V :
        C_L :
        f_c : flexural compression stress
        """
        if f_c >= F_bx_star * (1 - C_V):
            print(
                f"{f_c} >= {F_bx_star*(1-C_V)} bending stress exceeds allowable design"
            )
        else:
            print(
                f"{f_c} >= {F_bx_star*(1-C_V)} bending stress within allowable design"
            )

        F_bx_prime = F_bx_star * C_V + f_c
        if F_bx_prime >= F_bx_star * C_L:
            print(
                f"{F_bx_prime} >= {F_bx_star*C_L} bending stress exceeds allowable design"
            )
        else:
            print(
                f"{F_bx_prime} >= {F_bx_star*C_L} bending stress within allowable design"
            )
        return F_bx_prime

    def get_beam_moments(self, forces={}):
        """Used to get moments on beam Equation 3.4.3.1.2-2
        Parameters
        ----------
        forces : dictionary with
            F_max : force at end of the beam
            F_a : force at l/4 of the beam
            F_b : force at l/2 of the beam
            F_c : force at 3l/4 of the beam
            or
            F_0 = end force resulting in the larger compression stress on the bottom face
            F_1 = other end force on the unbraced length
            F_CL = force at centerline of the unbraced length
            or
            F_1, F_2, etc. describing all uniform loads on beam
        """
        if "F_max" in forces.keys():
            return {
                "M_max": forces["F_max"] * self.length,
                "M_a": forces["F_a"] * self.length / 4.0,
                "M_b": forces["F_b"] * self.length / 2.0,
                "M_c": forces["F_c"] * 3.0 * self.length / 4.0,
            }
        elif "F_CL" in forces.keys():
            if "F_0" in forces.keys() and "F_1" in forces.keys():
                return {
                    "M_0": forces["F_0"] * self.length,
                    "M_1": forces["F_1"] * self.length,
                    "M_CL": forces["F_CL"] * self.length / 2.0,
                }
            else:
                return forces["F_CL"] * self.length / 8.0
        else:
            # Uniform Load
            final_force = 0.0
            for force in forces.values():
                final_force += force
            return final_force * (self.length ** 2.0) / 8.0


class Column(Support_Type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Wood Type to get all the properties
        # Extract this from choice/database?

    def column_design_criteria(self, P, A_g, A_n, F_c_prime, F_c_star):
        """
        Parameters
        ----------
        P : concentric axial compression load
        A_g : gross cross-sectional area
        A_n : net cross-sectional area
        F_c_prime : Adjusted compression design value
        F_c_star : Adjusted compression design value (without C_p)
        """
        if P / A_g <= F_c_prime:
            print(f"{P/A_g} <= {F_c_prime} compression stress within allowable design")
        else:
            print(f"{P/A_g} > {F_c_prime} compression stress exceeds allowable design")

        if P / A_n <= F_c_star:
            print(f"{P/A_n} <= {F_c_star} compression stress within allowable design")
        else:
            print(f"{P/A_n} > {F_c_star} compression stress exceeds allowable design")


class Loads:
    def __init__(self, *args, **kwargs):
        print("Nothing Here.")

    def live_load(self, L_0, A_f, F, structure_type="roof"):
        """Calculate Live Load for roof or floor
        Parameters
        ----------
        L_0 : minimum unreduced uniformly distributed roof live load prescribed by the International Building code.
        A_f : tributary area supported by any structural member (ft2)
        F : inches of rise per foot for a sloped roof or the rise-to-span ratio multiplied by 32 for an arch or dome.
        structure_type : Used to select either "roof" or "floor"
        """
        if structure_type == "roof":
            if A_f <= 200.0:
                R1 = 1.0
            elif A_f > 200.0 and A_f < 600.0:
                R1 = 1.2 - 0.001 * A_f
            else:
                R1 = 0.6

            if F < 4.0:
                R2 = 1.0
            elif F >= 4.0 and F < 12.0:
                R2 = 1.2 - 0.05 * F
            else:
                R2 = 0.6
            return L_0 * R1 * R2  # psf
        elif structure_type == "floor":
            if A_f > 200:
                return L_0 * (0.25 * 10.6 / np.sqrt(A_f))
            else:
                return L_0
        else:
            raise ValueError("structure_type can only be 'roof' or 'floor'.")

    def allowable_stress_design(self, D, L=0, Lr=0, S=0, R=0, W=0, E=0):
        """Calculates Allowable Stress Design for relevant load combinations
        Parameters
        ----------
        D : Dead load
        L : Live load
        Lr : Roof live load
        S : Snow load
        R : Rain load
        W : Wind load
        E : Earthquake load
        """
        ASD = {}
        ASD["D"] = D
        if W != 0.0:
            print(f"Dead + Wind Load: {0.6*D+W}")
            ASD["D+W"] = 0.6 * D + W

        if E != 0.0:
            print(f"Dead + Earthquake Load: {0.6*D+0.7*E}")
            ASD["D+E"] = 0.6 * D + 0.7 * E

        if L != 0.0:
            print(f"Dead + Live Load: {D+L}")
            ASD["D+L"] = D + L

        if Lr != 0.0:
            print(f"Dead + Roof Live Load: {D+Lr}")
            ASD["D+Lr"] = D + L

        if S != 0.0:
            print(f"Dead + Snow Live Load: {D+S}")
            ASD["D+S"] = D + S

        if R != 0.0:
            print(f"Dead + Rain Live Load: {D+R}")
            ASD["D+R"] = D + R

        if W != 0.0:
            print(f"Dead + Wind Live Load: {D+W}")
            ASD["D+WL"] = D + W

        if E != 0.0:
            print(f"Dead + Earthquake Live Load: {D+.7*E}")
            ASD["D+EL"] = D + 0.7 * E

        if L != 0.0:
            if Lr != 0.0:
                print(f"Dead + Live + Roof + Load: {D+0.75*L+0.75*Lr}")
                ASD["D+L+Lr"] = D + 0.75 * L + 0.75 * Lr

            if S != 0.0:
                print(f"Dead + Live + Snow + Load: {D+0.75*L+0.75*S}")
                ASD["D+L+S"] = D + 0.75 * L + 0.75 * S

            if R != 0.0:
                print(f"Dead + Live + Rain + Load: {D+0.75*L+0.75*R}")
                ASD["D+L+R"] = D + 0.75 * L + 0.75 * R

            if W != 0.0 and Lr != 0.0:
                print(f"Dead + Wind + Live + Roof + Load: {D+0.75*W+0.75*L+0.75*Lr}")
                ASD["D+W+L+Lr"] = D + 0.75 * W + 0.75 * L + 0.75 * Lr

            if W != 0.0 and S != 0.0:
                print(f"Dead + Wind + Live + Snow + Load: {D+0.75*W+0.75*L+0.75*S}")
                ASD["D+W+L+S"] = D + 0.75 * W + 0.75 * L + 0.75 * S

            if W != 0.0 and R != 0.0:
                print(f"Dead + Wind + Live + Rain + Load: {D+0.75*W+0.75*L+0.75*R}")
                ASD["D+W+L+R"] = D + 0.75 * W + 0.75 * L + 0.75 * R

            if E != 0.0 and Lr != 0.0:
                print(
                    f"Dead + Earthquake + Live + Roof + Load: {D+0.75*E+0.75*L+0.75*Lr}"
                )
                ASD["D+E+L+Lr"] = D + 0.75 * E + 0.75 * L + 0.75 * Lr

            if E != 0.0 and S != 0.0:
                print(
                    f"Dead + Earthquake + Live + Snow + Load: {D+0.75*E+0.75*L+0.75*S}"
                )
                ASD["D+E+L+S"] = D + 0.75 * E + 0.75 * L + 0.75 * S

            if E != 0.0 and R != 0.0:
                print(
                    f"Dead + Earthquake + Live + Rain + Load: {D+0.75*E+0.75*L+0.75*R}"
                )
                ASD["D+E+L+R"] = D + 0.75 * E + 0.75 * L + 0.75 * R
        else:
            if Lr != 0.0:
                print(f"Dead + Roof + Load: {D+0.75*Lr}")
                ASD["D+Lr"] = D + 0.75 * Lr

            if S != 0.0:
                print(f"Dead + Snow + Load: {D+0.75*S}")
                ASD["D+S"] = D + 0.75 * S

            if R != 0.0:
                print(f"Dead + Rain + Load: {D+0.75*R}")
                ASD["D+R"] = D + 0.75 * R

            if W != 0.0 and Lr != 0.0:
                print(f"Dead + Wind + Roof + Load: {D+0.75*W+0.75*Lr}")
                ASD["D+W+Lr"] = D + 0.75 * W + 0.75 * Lr

            if W != 0.0 and S != 0.0:
                print(f"Dead + Wind + Snow + Load: {D+0.75*W+0.75*S}")
                ASD["D+W+S"] = D + 0.75 * W + 0.75 * S

            if W != 0.0 and R != 0.0:
                print(f"Dead + Wind + Rain + Load: {D+0.75*W+0.75*R}")
                ASD["D+W+R"] = D + 0.75 * W + 0.75 * R

            if E != 0.0 and Lr != 0.0:
                print(f"Dead + Earthquake + Roof + Load: {D+0.75*E+0.75*Lr}")
                ASD["D+E+Lr"] = D + 0.75 * E + 0.75 * Lr

            if E != 0.0 and S != 0.0:
                print(f"Dead + Earthquake + Snow + Load: {D+0.75*E+0.75*S}")
                ASD["D+E+S"] = D + 0.75 * E + 0.75 * S

            if E != 0.0 and R != 0.0:
                print(f"Dead + Earthquake + Rain + Load: {D+0.75*E+0.75*R}")
                ASD["D+E+R"] = D + 0.75 * E + 0.75 * R

        return ASD
