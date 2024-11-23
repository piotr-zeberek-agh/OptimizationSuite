# Simulated Annealing Suite in Python

## Team
- Piotr Żeberek (team leder)
- Przemysław Ryś

## Description
Graphical User Interface for performing optimization using the Simulated Annealing algorithm.
***
## Project Roadmap

### Week 1 (25.11 - 01.12)

- General app layout, learning GUI toolkit (PyQt6)
- Developing general requirements for optimization scenario

### Week 2 (02.12 - 08.12)

- Implementation of sample scenarios with user-defined simulation parameters:
  1. Investment portfolio optimization
  2. Modeling the structure of fullerenes
  3. ...

### Week 3 (09.12 - 15.12)

- Real-time plots of:
    - convergence
    - error
    - system changes
    - Progress indicators
    - Estimated time remaining

### Week 4 (16.12 - 22.12)

- Session save and restore 

### Week 5 (06.01 - 12.01)

- Multi-run option (compare results across multiple runs)

### Week 6 (13.01 - 19.01)

- Results exporting (plots, etc.) in different formats

### Week 7 (20.01 - 24.01)

- final touches

***

## Description of project scenarios

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

  - 