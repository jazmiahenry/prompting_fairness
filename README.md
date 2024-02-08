# Prompting Fairness

This repository is the companion code base for the paper, "Prompting Fairness: Artificial Intelligence as Game Players". To find out more about the paper or experiments run, contact the author: [Jazmia Henry](https://jazmiahenry.com/contact). 

## Abstract
Utilitarian games such as dictator games to measure fairness have been studied in the social sciences for decades. These games have given us insight into not only how humans view fairness but also in what conditions the frequency of fairness, altruism and greed increase or decrease. While these games have traditionally been focused on humans, the rise of AI gives us the ability to study how these models play these games. AI is becoming a constant in human interaction and examining how these models portray fairness in game play can give us some insight into how AI makes decisions. Over 101 rounds of the dictator game, I conclude that AI has a strong sense of fairness that is dependant of it it deems the person it is playing with as trustworthy, framing has a strong effect on how much AI gives a recipient when designated the trustee, and there may be evidence that AI experiences inequality aversion just as humans.

## Dictator Game

The Dictator Game gives one player- the trustee- the ability to decide how much of a share of money they are willing to share with a recipient. This game measures fairness. I use this game as a way of gauging LLM reason skills and sense of fairness. The rules of this game is better explained in `dictator_response.jinja2`.

Output can be found in the `dictator_reponse.txt` file.

## Dictator Game (Random Response)

This version of the dictator game examines if the LLM behaves differently if they have a turn at being the recipient and the 'trustee' randomly gives them money. The role of the LLM is randomly assigned. More is descriped in `recipient_response.jinja2`.

Output for the responses can be found in the `recipient_response.txt` file.

## Dictator Game (Framing)

If the LLM gets graming with information explicitly about it gave vs received, how will it behave? I explore this below using the prompt `dictator_history.jinja2`.

The output for this set of runs is in the `framed_response.txt` file. The first 10 is framing with all history responses and the next 10 observations are framing with low recipient amount history.

### Dictator Persona

Let's see if framing the identity of the LLM makes it behave any differently. The prompt for the personas based game is at `dictator_personas.jinja2`.

#### Persona Information

**HR Executive**: The LLM has the persona of a HR executive living in the city and a caretaker of two children. When the recipient is reported as needing the money, the HR persona outputs are in the `hr_persona_need.txt` file. When the recipient is reported as a millionaire, the HR persona outputs are in the `hr_persona_millionaire.txt` file.

**Rancher**: The LLM has the persona of a rancher from a rural city. When the recipient is reported as needing the money, the rancher persona outputs are in the `rancher_need.txt` file. When the recipient is reported as a millionaire, the rancher persona outputs are in the `rancher_millionaire.txt` file.

#### Recipient Information

**Needs Money**: The LLM receives information that the recipient needs the money

**Millionaire**: The LLM receives information that the recipient is a millionaire.

## Dictator Game Exit Interview

Now that the LLM has played the game up until now, I ask the LLM to agree or disagree with the following:

1. The money I have been give rightfully is mine.
2. If I choose to give, this means I am being nice.
3. It is not fair to share this money.
4. The recipient has not earned this money.
5. I am more deserving of the money than the recipient.
6. If the person I am playing with is rich, I deserve the money more.
7. If the perosn I am playing with is poor, they deserve the money more.
   
The responses from the LLM to this is found in `exit_interview.txt`.
