"""
EWCM-DE implementation for the test rig at Chair of Fluid Systems, TU Darmstadt
Copyright (C) 2026  Kevin Logan, Michaela Lestakova

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from copy import deepcopy

import casadi as ca
import networkx as nx
import numpy as np
from numpy.linalg import inv


class EWCMDESystem:
    """Elastic water column model in state-space formulation.

    Based on:
    M. Imani, A. Zecchin, W. Zeng, and M. F. Lambert, “Generalization and Analysis of
    elastic Water Column model for hydraulic transient analysis of water distribution
    systems,” Journal of Water Resources Planning and Management, vol. 151, no. 10,
    Aug. 2025, doi: 10.1061/jwrmd5.wreng-6946.
    """

    def __init__(self, A=None, B=None, C=None, E=None, F=None):
        self.A = A
        self.B = B
        self.C = C
        self.E = E
        self.F = F
        pass

    def construct_from_json(
        self,
        internal_nodes,
        reservoirs,
        pipes,
        virtual_pipes,
        pumps,
        valves,
        gravitational_constant,
        speed_of_sound,
    ):
        self.internal_nodes = internal_nodes
        self.reservoirs = reservoirs
        self.pipes = pipes
        self.virtual_pipes = virtual_pipes
        self.pumps = pumps
        self.valves = valves
        self.g = gravitational_constant
        self.a = speed_of_sound

        self.alg_vars = dict(self.virtual_pipes)
        self.alg_vars.update(self.pumps)
        self.alg_vars.update(self.valves)

        self.elements = dict(self.pumps)
        self.elements.update(self.valves)

        self.internal_node_list = list(self.internal_nodes.keys())
        self.reservoir_list = list(self.reservoirs.keys())

        self.pipe_list = list(self.pipes.keys())
        self.alg_var_list = list(self.alg_vars.keys())
        self.virtual_pipe_list = list(self.virtual_pipes.keys())
        self.pump_list = list(self.pumps.keys())
        self.valve_list = list(self.valves.keys())

        self.pipe_dict = {
            (pipe["start_node"], pipe["end_node"]): pipe_name
            for pipe_name, pipe in self.pipes.items()
        }

        self.alg_var_dict = {
            (
                alg_var["start_node"],
                alg_var["end_node"],
            ): alg_var_name
            for alg_var_name, alg_var in self.alg_vars.items()
        }

        self.edge_dict = deepcopy(self.pipe_dict)
        self.edge_dict.update(self.alg_var_dict)

        dG = nx.DiGraph()
        dG.add_nodes_from(self.reservoirs.keys())
        dG.add_nodes_from(self.internal_nodes.keys())
        dG.add_edges_from(self.edge_dict.keys())

        self.A_p = -nx.incidence_matrix(
            dG,
            nodelist=self.internal_node_list + self.reservoir_list,
            edgelist=self.pipe_dict.keys(),
            oriented=True,
        )

        self.A_e = -nx.incidence_matrix(
            dG,
            nodelist=self.internal_node_list + self.reservoir_list,
            edgelist=self.alg_var_dict.keys(),
            oriented=True,
        )

        self.A_I_p = self.A_p[: len(self.internal_node_list)]
        self.A_I_e = self.A_e[: len(self.internal_node_list)]

        if len(self.reservoir_list) >= 1:
            self.A_R_p = self.A_p[-len(self.reservoir_list) :]
            self.A_R_e = self.A_e[-len(self.reservoir_list) :]
        else:
            self.A_R_p, self.A_R_e = None, None

        # L,R,C matrices
        self.L = []  # inductance
        self.R = []  # resistance
        self.NC = []  # node capacitance
        self.TC = []  # tank capactitance
        for pipe in pipes.values():
            cross_section_area = np.pi * (pipe["diameter"] / 2) ** 2
            self.L.append(pipe["length"] / (self.g * cross_section_area))
            self.R.append(
                8
                * pipe["length"]
                * pipe["roughness"]
                / (np.pi**2 * self.g * pipe["diameter"] ** 5)
            )
            self.NC.append(
                (2 * self.g * np.pi / 4 * pipe["diameter"] ** 2 * pipe["length"])
                / (self.a**2)
            )

        for node in internal_nodes.values():
            if node["node_type"] == "Tank":
                self.TC.append(node["area"])
            else:
                self.TC.append(0.0)

        for alg_var in self.alg_vars.values():
            self.NC.append(
                (2 * self.g * np.pi / 4 * alg_var["diameter"] ** 2 * alg_var["length"])
                / (self.a**2)
            )

        self.L = np.diag(self.L)
        self.R = np.diag(self.R)

        self.L_inv = inv(self.L)
        self.L_inv_R = self.L_inv @ self.R

        self.G = inv(
            np.diag(
                1
                / 2
                * np.abs(np.block([self.A_I_p.todense(), self.A_I_e.todense()]))
                @ self.NC
                + self.TC
            )
        )

        self.D = np.diag(
            [element["system_coefficient"] for element in self.elements.values()]
        )

        self.D_v = self.D[
            -len(self.valve_list) :,
            -len(self.valve_list) :,
        ]

        self.pump_coeffs_0 = []
        self.pump_coeffs_1 = []
        self.pump_coeffs_2 = []
        for pump in self.pumps.values():
            pump_coeffs = pump["head_coefficients"]
            self.pump_coeffs_0.append(pump_coeffs[0])
            self.pump_coeffs_1.append(pump_coeffs[1])
            self.pump_coeffs_2.append(pump_coeffs[2])

        self.c_d = []
        self.a_0 = []
        for valve in self.valves.values():
            self.c_d.append(valve["valve_coefficient"])
            self.a_0.append(np.pi * (valve["diameter"] / 2) ** 2)

        self.state_dict = {
            "q_p": self.pipe_list,
            "q_e": self.alg_var_list,
            "h_I": self.internal_node_list,
            "z": self.pump_list + self.valve_list,
        }

        self.input_dict = {
            "h_R": self.reservoir_list,
            "Q": self.internal_node_list,
            "u_e": self.pump_list + self.valve_list,
        }

    def set_up_DAE(self):
        n = len(self.state_dict["q_p"])
        m = len(self.state_dict["h_I"])
        ly = len(self.state_dict["q_e"])
        lz = len(self.state_dict["q_e"]) - len(self.virtual_pipe_list)
        r = len(self.reservoir_list)

        # state vector
        self.q_p = ca.vertcat(
            *[ca.MX.sym(f"q_p_{svn}") for svn in self.state_dict["q_p"]]
        )
        self.h_I = ca.vertcat(
            *[ca.MX.sym(f"h_I_{svn}") for svn in self.state_dict["h_I"]]
        )
        # self.z_vp = ca.vertcat(
        #     *[ca.MX.sym(f"z_vp_{svn}") for svn in self.virtual_pipe_list]
        # )
        self.z_p = ca.vertcat(*[ca.MX.sym(f"z_p_{svn}") for svn in self.pump_list])
        self.z_v = ca.vertcat(*[ca.MX.sym(f"z_v_{svn}") for svn in self.valve_list])
        self.z = ca.vertcat(self.z_p, self.z_v)

        self.x = ca.vertcat(self.q_p, self.h_I, self.z)

        # algebraic state vector
        self.q_e_vp = ca.vertcat(
            *[ca.MX.sym(f"q_e_vp_{svn}") for svn in self.virtual_pipe_list]
        )
        self.q_e_p = ca.vertcat(*[ca.MX.sym(f"q_e_p_{svn}") for svn in self.pump_list])
        self.q_e_v = ca.vertcat(*[ca.MX.sym(f"q_e_v_{svn}") for svn in self.valve_list])

        self.q_e = ca.vertcat(self.q_e_vp, self.q_e_p, self.q_e_v)
        self.ax = self.q_e

        # control input vector
        self.h_R = ca.vertcat(
            *[ca.MX.sym(f"h_R_{svn}") for svn in self.input_dict["h_R"]]
        )
        self.Q = ca.vertcat(*[ca.MX.sym(f"Q_{svn}") for svn in self.input_dict["Q"]])
        self.u_e = ca.vertcat(
            *[ca.MX.sym(f"u_e_{svn}") for svn in self.input_dict["u_e"]]
        )

        self.u = ca.vertcat(self.h_R, self.Q, self.u_e)

        # system matrices
        self.A = np.block(
            [
                [
                    np.zeros(shape=(n, n)),
                    self.L_inv @ self.A_I_p.T,
                    np.zeros(shape=(n, lz)),
                ],
                [-self.G @ self.A_I_p, np.zeros(shape=(m, m)), np.zeros(shape=(m, lz))],
                [
                    np.zeros(shape=(lz, n)),
                    np.zeros(shape=(lz, m)),
                    -self.D,
                ],
            ]
        )
        self.EL = np.block(
            [
                [np.zeros(shape=(n, ly))],
                [-self.G @ self.A_I_e],
                [np.zeros(shape=(lz, ly))],
            ]
        )
        self.F = ca.blockcat(
            [
                # [self.L_inv_R @ ca.diag(ca.fabs(self.q_p)) @ self.q_p],
                [self.L_inv_R @ ca.diag(self.q_p) @ ca.fabs(self.q_p)],
                [np.zeros(shape=(m, 1))],
                [np.zeros(shape=(lz, 1))],
            ]
        )

        if self.A_R_p is not None:
            self.B = np.block(
                [
                    [
                        self.L_inv @ self.A_R_p.T,
                        np.zeros(shape=(n, m)),
                        np.zeros(shape=(n, lz)),
                    ],
                    [np.zeros(shape=(m, r)), -self.G, np.zeros(shape=(m, lz))],
                    [np.zeros(shape=(lz, r)), np.zeros(shape=(lz, m)), self.D],
                ]
            )
        else:
            self.B = np.block(
                [
                    [
                        np.zeros(shape=(n, r)),
                        np.zeros(shape=(n, m)),
                        np.zeros(shape=(n, lz)),
                    ],
                    [np.zeros(shape=(m, r)), -self.G, np.zeros(shape=(m, lz))],
                    [np.zeros(shape=(lz, r)), np.zeros(shape=(lz, m)), self.D],
                ]
            )

        self.aF = ca.vertcat(
            -(
                np.diag(self.pump_coeffs_0)
                @ (ca.diag(self.q_e_p) @ ca.diag(self.q_e_p))
                + np.diag(self.pump_coeffs_1)
                @ (ca.diag(self.q_e_p) @ ca.diag(self.z_p))
                # + np.diag(self.pump_coeffs_2) @ (ca.diag(self.z_p) @ ca.diag(self.z_p))
                + np.diag(self.pump_coeffs_2) @ (ca.diag(self.z_p))
            ),
            (
                (1 / (2 * self.g))
                * (inv(np.diag(self.c_d) @ np.diag(self.a_0))) ** 2
                * (ca.diag(self.q_e_v) @ ca.inv(ca.diag(self.z_v))) ** 2
                # * (ca.diag(self.q_e_v) ** 2 @ ca.inv(ca.diag(self.z_v)))
            ),
        )

        # set up state equation
        self.x_dot = self.A @ self.x + self.EL @ self.q_e - self.F + self.B @ self.u

        # set up algebraic equation
        if self.A_R_e is not None:
            self.alg_eq = ca.vertcat(
                (self.q_p[1] - self.q_e[0]),
                (
                    self.A_I_e.todense().T[1:] @ self.h_I
                    - self.aF
                    + self.A_R_e.todense().T[1:] @ self.h_R
                ),
            )
        else:
            self.alg_eq = ca.vertcat(
                (self.q_p[1] - self.q_e[0]),
                (self.q_p[3] - self.q_e[1]),
                (self.A_I_e.todense().T[2:] @ self.h_I - self.aF),
            )

    def set_up_initial_values(self, q_p_0, h_I_0, z_0, q_e_0):
        self.q_p_0 = [q_p_0[i] for i in self.state_dict["q_p"]]
        self.h_I_0 = [h_I_0[i] for i in self.state_dict["h_I"]]
        self.z_0 = [z_0[i] for i in self.state_dict["z"]]
        self.q_e_0 = [q_e_0[i] for i in self.state_dict["q_e"]]

        x0 = np.concatenate([self.q_p_0, self.h_I_0, self.z_0])
        self.x0 = ca.DM(x0)
        self.ax0 = ca.DM(self.q_e_0)

    def simulate_state(self, u, t0=0, t_stop=2, dt=1e-4, x0=None, ax0=None):
        if x0 is not None:
            self.x0 = x0
        if ax0 is not None:
            self.ax0 = ax0

        t = np.arange(t0, t_stop, dt)

        dae = {
            "x": self.x,
            "z": self.ax,
            "p": self.u,
            "ode": self.x_dot,
            "alg": self.alg_eq,
        }
        # opts = {
        #     "tf": 1e-4,  # time step for each integrator call
        #     #     "abstol": 1e-8,
        #     #     "reltol": 1e-8,
        # }

        Fint = ca.integrator(
            "Fint",
            "collocation",  # "idas",
            dae,
            t0,
            dt,
            {
                # "calc_ic": True,
                # "calc_icB": True,
                # "abstol": 1e-8,
                # "reltol": 1e-4,
                # "max_num_steps": 5000,
                # "max_order": 5,  # BDF order cap
                # "max_step_size": dt / 2,  # important for control problems
                # "linear_solver": "csparse",
                "collocation_scheme": "radau",
                "number_of_finite_elements": 1,
                "interpolation_order": 1,
                "rootfinder": "newton",
                "rootfinder_options": {"abstol": 1e-10, "max_iter": 20},
            },
        )

        # initial conditions
        x0 = ca.DM(self.x0)
        z0 = ca.DM(self.ax0)

        nx = x0.numel()
        nz = z0.numel()
        nt = len(t)

        x_vals = np.empty((nt, nx))
        ax_vals = np.empty((nt, nz))

        xt = deepcopy(self.x0)
        axt = deepcopy(self.ax0)

        x_vals[0, :] = np.asarray(xt).ravel(order="F")
        ax_vals[0, :] = np.asarray(axt).ravel(order="F")

        for i in range(1, nt):
            res = Fint(x0=xt, z0=axt, p=u[i])
            xt = res["xf"]
            axt = res["zf"]
            x_vals[i, :] = np.asarray(xt).ravel(order="F")
            ax_vals[i, :] = np.asarray(axt).ravel(order="F")
        return x_vals, ax_vals
