import gurobipy as gp, pandas as pd
from returns_from_prices import mu, sigma


ss = False # True = permite shorts, False = long-only

lb = -gp.GRB.INFINITY if ss else 0


LAMBDA = 20
# Creamos el modelo
model = gp.Model('risk-aversion')


# Creamos las variables (nuestros stocks)
vars = pd.Series(
    model.addVars(sigma.columns, lb=lb), 
    index = sigma.columns)

portfolio_risk   = vars.T.dot(sigma).dot(vars)
portfolio_return = mu.T.dot(vars)

model.setObjective(
    portfolio_return - LAMBDA/2 * portfolio_risk, 
    gp.GRB.MAXIMIZE)

# Restricción de presupuesto
model.addConstr(vars.sum() == 1, 'budget')

model.optimize()

weights = vars.apply(lambda v: v.X)
print(weights)