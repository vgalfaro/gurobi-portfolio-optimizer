import gurobipy as gp, pandas as pd
from returns_from_prices import mu, sigma

def solve_min_var(
        mu: pd.Series, 
        sigma: pd.DataFrame, 
        ss: bool = True) -> pd.Series:
    #ss: True = permite shorts, False = long-only

    lb = -gp.GRB.INFINITY if ss else 0

    # Creamos el modelo
    model = gp.Model('portfolio-min-var')
    model.Params.OutputFlag = 0
    # Creamos las variables (nuestros stocks)
    vars = pd.Series(
        model.addVars(sigma.columns, lb=lb), 
        index = sigma.columns)

    # Definimos la función objetivo, 
    # en este caso el riesgo cuadrático del portfolio
    portfolio_risk = vars.T.dot(sigma).dot(vars)

    # Seteamos el objetivo
    model.setObjective(portfolio_risk, gp.GRB.MINIMIZE)

    # Restricción de presupuesto
    model.addConstr(vars.sum() == 1, 'budget')

    model.optimize()

    weights = vars.apply(lambda v: v.X)
    return weights

if __name__ == "__main__":
    sol = solve_min_var(mu, sigma, False)
    print(sol)