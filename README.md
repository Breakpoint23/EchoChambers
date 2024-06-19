# Objective

The reason behind this project is to create deep learning models to make people understand that they have to get out of their echochambers and see the bigger picture


# LLAMA 3

-  could be interesting to utilize the llama 3 and see how it performs in the followin categories.

    1. presenting an opposite view to the prompt
    2. see how to perform factual checks with it
    3. live answers/ suggestions from what's being typed (has to be our own API, Can not use open AI api as it would be very expensive)


# Features

1. Provide opposing views (By views I mean phylosophical,sociological etc. Not factual)
2. Provide factual checks
3. Provide hypocrisy rating (0-1)


# Implementation

- First thing and I guess the easiest out of this is the 1st feature. Pretty sure chatGPT should be able to do this for proof  of concept.
- Factual checks can not be solely based on a LLM as they have tendencies to hallucinate
- It is a necessity to have a knowledgebase (Repo of links to search for articles)
- Along with the ability crawl web for these articles and digest the appropriate content.


# Steps for Implementation

1. we'll start with the ability to present the philosophy of the other side. try with the GPT3.5 and see how it performs.
2. Then we can work on LLAMA3 8B model to see how it does.
3. In the mean time, after step 1 have to work on building the knowledgebase and the ability to crawl the web for information.
4. Once we can produce the opposing views (while the user is typing their input) we can create a proof of concept for the app/tool.

## How to test Chat GPT 3.5

1. One idea is to let it create articles that presents the opposite view of the article that was fed in.
2. Test it on some political and theological idealogies as well.
 for the app/tool.

## How to test Chart GPT 3.5

1. One idea is to let it create articles that presents the opposite view of the article that was fed in.
2. Test it on some political and theological idealogies as well.
 for the app/tool.

## How to test Chat GPT 3.5

1. One idea is to let it create articles that presents the opposite view of the article that was fed in.
2. Test it on some political and theological idealogies as well.
 for the app/tool.

## How to test Chat GPT 3.5

1. One idea is to let it create articles that presents the opposite view of the article that was fed in.
2. Test it on some political and theological idealogies as well.
3. Although while testing step 1 it might try to present some factual hypocrisies that we don't want to right now.


# Challenges

## Computing power

- I do not think it's possible to run llama 3 on this machine, have to try kaggle and see
