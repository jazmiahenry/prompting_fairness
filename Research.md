# Research

There is a good amount of research that went into this repository. Below are major considerations that went into the repo's build.

[Prompt Logic](#prompt-logic): explores how I created my prompts.

[Games](#games): explains the [Dictator Game](#dictator-game).

## Prompting Fairness 
The Dictator is fairly common two player utilitarian game in Game Theory.

### Dictator Game

The dictator game was originally created by Daniel Kaheman. 

However, the style of play I deploy in this repository is more closely inspired by the paper Fairness in Simple Bargaining Experiments by [Forsythe et al](https://www.sciencedirect.com/science/article/abs/pii/S0899825684710219). 

Forsythe et al's dictator game can be summarized as thus: two players get one or the other role-  (ultimatum or dictator, though called "recipient or trustee" in this repo). The trustee has the ability to pay as much as they would like. In this repo, I do not double the prize, but instead see if the LLM adjusts their sense of "fairness" based on the recipient's actions. 

## Prompt Logic

*Plan and Execute Agents*

Based on BabyAGI repo and [Plan and Solve](https://arxiv.org/abs/2305.04091) paper

BabyAGI is an open source repository that scales down the proposal from the Task Driven Autonomous Agent paper by Yohei Nakajima. 

    1. Has three agents: code writer agent, code executor agent and code refactor agent. 

    2. Code writer: writes code or functions and saves or appends them to file for later use.

    3. Code refactor: Modifies code to meet requirements

    4. Code executor: executes commands such as creating directories or installing dependencies

Agents do the following:

    1. Analyzes the objective

    2. Breaks down into subtasks

    3. Assigns a unique ID by subtask

    4. Organizes tasks by logical
            order from start to finish

    5. Provides contest for each task

    6. Evaluates each objective

    7. Compiles into a JSON file for retrieval

These objectives are defined into a JSON file where humans can provide feedback. 

Plan and Solve paper improves upon zero shot chain of thought by getting an agent to divide tasks into subtasks by prompting an agent to formulate a plan to get to a solution. 

    1. Have to create input data with examples that show the following: “Q: [X]. A: Let’s first understand the problem and devise a plan to solve the problem. Then, let’s carry out the plan and solve the problem step by step.”

    2. Next, create a step that prompts LLM to “pay attention to its calculation” by extracting relevant examples. This enables better output. 

Summary: Plan and executor agent in LangChainAI allows you to search the LLM for relevant examples to solve a problem, divide solution into subtasks, prioritize these subtasks, calculate the solution if calculations are necessary and execute. Suggesting our team settles on a chain of thought approach, this can be a good path to consider. This approach is sai to reduce semantic misunderstandings, missing steps and miscalculations of traditional few-shot or zero-shot prompt agents. 

In this repo, I use this logic to assist with prompt logic but do not adhere to it strictly. 

