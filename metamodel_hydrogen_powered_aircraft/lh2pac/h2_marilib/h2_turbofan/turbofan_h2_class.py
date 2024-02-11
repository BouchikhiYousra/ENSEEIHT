from pathlib import Path
from typing import Dict, Iterable, Mapping, Union

from gemseo.algos.opt_problem import OptimizationProblem
from gemseo.core.discipline import MDODiscipline
from marilib.utils import unit
from numpy import array, ndarray

from .turbofan_h2_function import fct_turbofan_h2, str_h2turbofan


class H2TurboFan(MDODiscipline):
    """Wrapper of the MARILib-based function :meth:`fct_turbofan_h2`.

    This discipline evaluates the function :meth:`fct_turbofan_h2`
    from values of :attr:`TECHNOLOGICAL_VARIABLES` and :attr:`DESIGN_VARIABLES`
    passed to the method :meth:`execute` as a dictionary of NumPy arrays.

    The discipline uses :attr:`DEFAULT_DESIGN_VALUES` for unspecified :attr:`DESIGN_VARIABLES`
    and :attr:`DEFAULT_TECHNOLOGICAL_VALUES` for unspecified :attr:`TECHNOLOGICAL_VARIABLES`.
    """

    TECHNOLOGICAL_VARIABLES = ["tgi", "tvi", "sfc", "mass", "drag"]
    DESIGN_VARIABLES = ["thrust", "bpr", "area", "aspect_ratio"]
    OBJECTIVE = "mtow"
    CONSTRAINTS = ["tofl", "vapp", "vz_mcl", "vz_mcr", "oei_path", "ttc", "far"]
    OBSERVABLES = ["fuel", "coc"]
    OUTPUT_VARIABLES = [OBJECTIVE] + CONSTRAINTS + OBSERVABLES
    DEFAULT_DESIGN_VALUES = {
        "thrust": array([125000.0]),
        "bpr": array([8.5]),
        "area": array([160.0]),
        "aspect_ratio": array([9.5]),
    }
    DEFAULT_TECHNOLOGICAL_VALUES = {
        "tgi": array([0.3]),
        "tvi": array([0.845]),
        "drag": array([1.0]),
        "sfc": array([1.0]),
        "mass": array([1.0]),
    }

    def __init__(self) -> None:
        super(H2TurboFan, self).__init__()

        # Define the input and output variables.
        self.input_grammar.update(
            self.DESIGN_VARIABLES + self.TECHNOLOGICAL_VARIABLES
        )
        self.output_grammar.update(self.OUTPUT_VARIABLES)

        # Define the default inputs.
        self.default_inputs.update(self.DEFAULT_DESIGN_VALUES)
        self.default_inputs.update(self.DEFAULT_TECHNOLOGICAL_VALUES)

    def _run(self):
        """Run the wrapped MARILib function :meth:`fct_turbofan_h2`.

        1. Retrieve the inputs passed to :meth:`execute` and store in :attr:`local_data`.
        2. Execute the MARILib-based function :meth:`fct_turbofan_h2`.
        3. Store the results in :attr:`local_data`.
        """
        design_data = self.get_variables(self.local_data, self.DESIGN_VARIABLES)
        techno_data = self.get_variables(self.local_data, self.TECHNOLOGICAL_VARIABLES)
        output_data = fct_turbofan_h2(techno_data, design_data, "eval")
        output_data = {name: array([value]) for name, value in output_data.items()}
        self.local_data.update(output_data)

    @classmethod
    def plot_results(cls, data: Mapping[str, ndarray]) -> None:
        """Plot the results in the MARILib way.

        Args:
            data: The data to be plotted.
        """
        design_data = cls.get_variables(data, cls.DESIGN_VARIABLES)
        techno_data = cls.get_variables(data, cls.TECHNOLOGICAL_VARIABLES)
        fct_turbofan_h2(techno_data, design_data, "draw")

    @classmethod
    def print_results(cls, data: Mapping[str, ndarray]) -> None:
        """Print the results in the MARILib way.

        Args:
            data: The data to be printed.
        """
        design_data = cls.get_variables(data, cls.DESIGN_VARIABLES)
        techno_data = cls.get_variables(data, cls.TECHNOLOGICAL_VARIABLES)
        output_data = cls.get_variables(data, cls.OUTPUT_VARIABLES)
        print(str_h2turbofan(techno_data, design_data, output_data))

    @staticmethod
    def get_variables(
        data: Mapping[str, ndarray], names: Iterable[str]
    ) -> Dict[str, float]:
        """Return the values of the variable readable by :meth:`fct_turbofan_h2`.

        Args:
            data: The data to be converted.
            names: The names of the variables.

        Returns:
            The data readable by :meth:`fct_turbofan_h2`.
        """
        return {name: data[name][0] for name in names}

    @classmethod
    def print_results_from_opt_problem(
        cls, problem: Union[OptimizationProblem, str, Path]
    ) -> None:
        """Print the results in the MARILib way.

        Args:
            problem: The :class:`OptimizationProblem` after resolution,
                either as a :class:`OptimizationProblem`
                or a file path to a saved optimization history.
        """
        if not isinstance(problem, OptimizationProblem):
            problem = OptimizationProblem.import_hdf(problem)

        f_opt, x_opt, is_feas, c_opt, _ = problem.get_optimum()
        x_opt = {
            name: x_opt[i]
            for i, name in enumerate(problem.design_space.variables_names)
        }
        y_opt = {}
        y_opt["mtow"] = f_opt
        for name, value in c_opt.items():
            if name.startswith("-"):
                y_opt[name[1:]] = -value
            else:
                y_opt[name] = value
        data = {name: array([value]) for name, value in x_opt.items()}
        data.update({name: array([value]) for name, value in y_opt.items()})
        data.update(H2TurboFan.DEFAULT_TECHNOLOGICAL_VALUES)
        data["ttc"] += unit.s_min(25)
        data["tofl"] += 2200
        data["vapp"] += unit.mps_kt(137)
        data["vz_mcl"] += unit.mps_ftpmin(300)
        data["oei_path"] += 0.011
        data["far"] += 13.4
        cls.print_results(data)
        return data
