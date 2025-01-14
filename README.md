# Optimization Suite in Python (Simulated annealing)

## Team
- Piotr Żeberek (team leder)
- Przemysław Ryś

## Description
Graphical user interface for performing optimization tasks in Python. The main goal is to create a graphical interface that will allow the user to solve an optimization problem based on pre-defined or user-defined scenarios and present the results in a clear and understandable way.

## Project Roadmap

### Week 1 (25.11 - 01.12)

- Designing general app layout, learning GUI toolkit (PyQt6)
- Developing general requirements for optimization scenario

### Week 2 (02.12 - 08.12)

- Implementation of simple scenario with user-defined simulation parameters e.g. gradient descent
- Real-time plots of:
    - convergence
    - error
    - system changes

### Week 3 (09.12 - 15.12)

- Implementation of more complex scenarios (may be moved to later weeks):
  1. Investment portfolio optimization
  2. Modeling the structure of fullerenes
  3. More to come if time allows
- Additional interface elements:
  - Progress indicators
  - Estimated time remaining

### Week 4 (16.12 - 22.12)

- Session save and restore 
- Importing user-defined scenarios
 
### Week 5 (06.01 - 12.01)

- Results exporting (plots, tables, etc.) in different formats
- debugging

### Week 6 (13.01 - 19.01)

- additional functionalities, packaging in installer/exec

### Week 7 (20.01 - 24.01)

- final touches

***

## Description of project scenarios

#### 0. Gradient Descent
Starting with an initial guess $x$ for a function $f(x)$, iteratively move in the direction of greatest decrease of $f(x)$ given by the negative of a gradient until the minimum is reached.

#### 1. Investment portfolio optimization
Optimizing an investment portfolio involves finding the best distribution of investments, i.e. how much percentage to invest in a given asset (Maximize return while minimizing risk).

    - Objective function definition - Sharpe ratio maximization:
        |Sharpe = (E[R_p] - R_f) / \sigma_p            |
        |where:                                        |
        |E[R_p] - expected return of the portfolio     |
        |R_f - The risk-free rate (can be 0)           |
        |sigma_p - Portfolio risk (standard deviation) |
    - Import of historical data of specific assets
    - Pre-generation of random portfolios.
    - Portfolio evaluation based on the objective function.
    - Making “moves” in the space of possible portfolios to get closer to the optimal solution
    - Input data (List of assets, Expected returns and risks for each asset, Budget)
    - Limits (The sum of all allocations must be 100%)
    - The maximum share of any one asset may not exceed 




    - (extra) Integration with machine learning models to predict future returns or risks based on historical data.

#### 2. Modeling the structure of fullerenes (Energy Minimization)
Miminimizing the energy of a system of $n$ atoms given by the empirical Brenners potential (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.42.9458)