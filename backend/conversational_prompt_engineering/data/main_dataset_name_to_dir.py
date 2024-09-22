# (c) Copyright contributors to the conversational-prompt-engineering project

# LICENSE: Apache License 2.0 (Apache-2.0)
# http://www.apache.org/licenses/LICENSE-2.0

# TODO: move to configs
dataset_name_to_dir = {
    "Reddit posts": {
        "train": "conversational_prompt_engineering/data/public/tldr/train.csv",
        "eval": "conversational_prompt_engineering/data/public/tldr/test.csv",
        "eval_llm": "conversational_prompt_engineering/data/public/tldr/test_full.csv",
        "desc": "This dataset consists of posts from Reddit (TL;DR dataset)",
    },
    "Space Newsgroup": {
        "train": "conversational_prompt_engineering/data/public/20_newsgroup/train.csv",
        "eval": "conversational_prompt_engineering/data/public/20_newsgroup/test.csv",
        "eval_llm": "conversational_prompt_engineering/data/public/20_newsgroup/test_full.csv",
        "desc": "This is part of the 20 Newsgroups dataset, a collection of \nnewsgroup documents. The topic of the documents is Space.",
    },
    "Debate Speeches": {
        "train": "conversational_prompt_engineering/data/public/debate_speeches/train.csv",
        "eval": "conversational_prompt_engineering/data/public/debate_speeches/test.csv",
        "eval_llm": "conversational_prompt_engineering/data/public/debate_speeches/test_full.csv",
        "desc": "This is part of the Debate Speeches dataset.\nThe dataset contains manually-corrected transcripts \nof speeches recorded by expert debaters.",
    },
    "Wikipedia Animal pages": {
        "train": "conversational_prompt_engineering/data/public/wiki_animals/train.csv",
        "eval": "conversational_prompt_engineering/data/public/wiki_animals/test.csv",
        "eval_llm": "conversational_prompt_engineering/data/public/wiki_animals/test_full.csv",
        "desc": "This dataset consists of animal pages extracted from \nWikipedia",
    },
    "Wikipedia Movie pages": {
        "train": "conversational_prompt_engineering/data/public/wiki_movies/train.csv",
        "eval": "conversational_prompt_engineering/data/public/wiki_movies/test.csv",
        "eval_llm": "conversational_prompt_engineering/data/public/wiki_movies/test_full.csv",
        "desc": "This dataset consists of movies pages extracted from \nWikipedia",
    },
}
