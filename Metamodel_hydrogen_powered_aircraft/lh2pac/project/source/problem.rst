Problem
=======

We seek to design a liquid hydrogen powered aircraft
with the Python library `MARILib <https://github.com/marilib/MARILib_obj>`_.

Context
-------

The design problem aims to minimize the maximal take off weight of the aircraft
whilst ensuring some constraints such as a maximal take off field length
and a maximal approach speed.

For this purpose,
it will be possible to play with four design parameters.

By the way,
the design takes place in an uncertain environment
where the technological choices can be probabilized.

In the current page,
we will note :math:`f:x,u\mapsto f(x,u)`
the MARILib-based model of a liquid hydrogen powered model
where :math:`x` are the design parameters and :math:`u` the uncertain ones.

Sub-problem 1 - Surrogate modeling and optimization
---------------------------------------------------

We will create a surrogate model of :math:`g:x\mapsto g(x)=f(x,u_{\mathrm{default}})`
to approximate the objective and constraints of the design problem
with respect to the design parameters :math:`x`.
Then,
we will use this surrogate model in an optimization process
to minimize the objective whilst ensuring the constraints
by varying the design parameters.

Sub-problem 2 - Surrogate modeling and uncertainty quantification
-----------------------------------------------------------------

We will create a surrogate model of :math:`h:u\mapsto h(x)=f(x_{\mathrm{default}},u)`
to approximate the objective and constraints of the design problem
with respect to the uncertain parameters :math:`u`.
Then,
we will use this surrogate model in an uncertainty study
to propagate the uncertainty related to the technological choices,
quantify the resulting output uncertainty
and explain it from the uncertainty sources (sensitivity analysis).


Sub-problem 3 - Surrogate modeling and robust optimization
----------------------------------------------------------

We will create a surrogate model of :math:`h:x,u\mapsto h(x)=f(x,u)`
to approximate the objective and constraints of the design problem
with respect to both design parameters :math:`x` and uncertain parameters :math:`u`.
Then,
we will use this surrogate model to to seek the best aircraft concept
taking into account the uncertainty of technological choices.