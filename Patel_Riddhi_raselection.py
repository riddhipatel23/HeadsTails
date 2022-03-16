import numpy as np
import random
import requests

def coin_em(rolls, theta_A=None, theta_B=None, maxiter=10):
    # Initial Guess
    theta_A = theta_A or random.random()
    theta_B = theta_B or random.random()
    thetas = [(theta_A, theta_B)]
    # Iterate
    for c in range(maxiter):
        print("#%d:\t%0.2f %0.2f" % (c, theta_A, theta_B))
        heads_A, tails_A, heads_B, tails_B = e_step(rolls, theta_A, theta_B)
        theta_A, theta_B = m_step(heads_A, tails_A, heads_B, tails_B)
        
    thetas.append((theta_A,theta_B))    
    return thetas, (theta_A,theta_B)

def e_step(rolls, theta_A, theta_B):
    """Produce the expected value for heads_A, tails_A, heads_B, tails_B 
    over the rolls given the coin biases"""
    
    heads_A, tails_A = 0,0
    heads_B, tails_B = 0,0
    for trial in rolls:
        likelihood_A = coin_likelihood(trial, theta_A)
        likelihood_B = coin_likelihood(trial, theta_B)
        p_A = likelihood_A / (likelihood_A + likelihood_B)
        p_B = likelihood_B / (likelihood_A + likelihood_B)
        heads_A += p_A * trial.count("H")
        tails_A += p_A * trial.count("T")
        heads_B += p_B * trial.count("H")
        tails_B += p_B * trial.count("T") 
    return heads_A, tails_A, heads_B, tails_B

def m_step(heads_A, tails_A, heads_B, tails_B):
    """Produce the values for theta that maximize the expected number of heads/tails"""

    theta_A = heads_A / (heads_A + tails_A)
    theta_B = heads_B / (heads_B + tails_B)
    return theta_A, theta_B

def coin_likelihood(roll, bias):
    # P(X | Z, theta)
    numHeads = roll.count("H")
    flips = len(roll)
    return pow(bias, numHeads) * pow(1-bias, flips-numHeads)

def run():
    rolls=[]
    #Heads/Tails API call 
    for i in range(0,30):
        response = requests.get('https://urldefense.com/v3/__https://24zl01u3ff.execute-api.us-west-1.amazonaws.com/beta__;!!LIr3w8kk_Xxm!6p1tMgJPwY4dLI8WN6lFHT7WnLLYsGHHAOpWSza-D0fM1YNfVBxKJRkjWb9ZuGo$')
        #parse json response
        temp=response.json()['body']

        #format the data by combining as string
        stringed=''.join(temp)
        stringed=stringed.replace('[','')
        stringed=stringed.replace(']','')
        stringed=stringed.replace(',','')
        stringed=stringed.replace(' ','')
        stringed=stringed.replace('1','H')
        stringed=stringed.replace('0','T')
        rolls.append(stringed)
    thetas= coin_em(rolls)

run()
