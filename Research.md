# Research

There is a good amount of research that went into this repository. Below are major considerations that went into the repo's build.

[Prompt Logic](#prompt-logic): explores how I created my prompts.

[Games](#games): explains the games I get the LLMs to play in this repo: the [Dictator Game](#dictator-game) and the [Prisoner's Dilemma](#prisoners-dilemma).

[Symbolic Logic](#symbolic-logic): shares information on what symbolic logic is and how it is used to help LLMs in this repo better self-reason.

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

## Games
The Dictator and Prisoner's Dilemma games are fairly common two player games in Game Theory.

### Dictator Game

The dictator game was originally created by Daniel Kaheman. 

However, the style of play I deploy in this repository is more closely inspired by the paper Fairness in Simple Bargaining Experiments by [Forsythe et al](https://www.sciencedirect.com/science/article/abs/pii/S0899825684710219). 

Forsythe et al's dictator game can be summarized as thus: two players get one or the other role-  (ultimatum or dictator, though called "recipient or trustee" in this repo). The trustee has the ability to pay as much as they would like. In this repo, I do not double the prize, but instead see if the LLM adjusts their sense of "fairness" based on the recipient's actions. 

The prompt defining the rules of this game is [here](../data/game_prompts/dictator_prompt.jinja2) for the assistant prompt and [here](../data/game_prompts/dictator_response.jinja2) for the response prompt.

In one experiment, I look to see if the order in which the LLM plays with their opponent causes different behavior. That can be found [here](../data/game_prompts/dictator_switch.jinja2).

### Prisoner's Dilemma
The [Prisoner's Dilemma](https://plato.stanford.edu/entries/prisoner-dilemma/) is described by William Poundstone as an experiment that gauges cooperation or self-preservation between two "rational agents".

In this repo, I define the game differently, focusing instead on a selfish or collaborative option for the LLM and opponent to choose from. The prompt defining the rules of this game is [here](../data/game_prompts/prisoners_dilemma.jinja2).

## Symbolic Logic
[Symbolic Logic](https://maa.org/sites/default/files/images/upload_library/46/Pengelley_projects/symbolic_logic_final.pdf) is the mathematical breakdown of sentences to gather their logical conclusions. 

I define symbolic logic within this repository for the LLM to make better informed conclusions within the [logic prompt](../data/logic_prompts/logic_prompts.jinja2).
