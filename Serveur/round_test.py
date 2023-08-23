from Round import Round
from Step import Step

round = Round([],2234)

print(id(round.board))

step = Step("pre_flop",[],round.board,round.deck)

print(id(step.board))

step.flop_board()

print(step.board)
print(round.board)