import gurobipy as gp, pandas as pd, numpy as np
from returns_from_prices import mu, sigma



def solve_risk_aversion(
        mu: pd.Series, 
        sigma: pd.DataFrame, 
        la: float, 
        ss: bool = True) -> pd.Series:
    # True = permite shorts, False = long-only

    lb = -gp.GRB.INFINITY if ss else 0

    # Creamos el modelo
    model = gp.Model('risk-aversion')
    model.Params.OutputFlag = 0
    # Creamos las variables (nuestros stocks)
    vars = pd.Series(
        model.addVars(sigma.columns, lb=lb), 
        index = sigma.columns)

    portfolio_risk   = vars.T.dot(sigma).dot(vars)
    portfolio_return = mu.T.dot(vars)

    model.setObjective(
        portfolio_return - la/2 * portfolio_risk, 
        gp.GRB.MAXIMIZE)

    # Restricción de presupuesto
    model.addConstr(vars.sum() == 1, 'budget')

    model.optimize()

    weights = vars.apply(lambda v: v.X)
    return weights



if __name__ == "__main__":

    lambdas = np.logspace(-1, 4, 30)  # de 0.1 a 10,000, espaciado logarítmico

    frontier = []
    for lam in lambdas:
        w = solve_risk_aversion(mu, sigma, lam, ss=True)
        port_return = mu.dot(w)
        port_risk = np.sqrt(w.dot(sigma).dot(w))
        frontier.append({'lambda': lam, 'risk': port_risk, 'return': port_return})

    frontier = pd.DataFrame(frontier)
    print(frontier)