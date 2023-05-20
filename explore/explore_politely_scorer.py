from politely.modeling_heuristic_scorer import HeuristicScorer

scorer = HeuristicScorer()
scorer.w2v.score("안녕")

# word2vec
# with hs=1 and negative=0 for this to work.
