# import torch
#
# from board import Board
# from model import Model
#
# board = Board()
#
# input_channels = Board.WIDTH * Board.HEIGHT
#
# num_actions = 9
# learning_rate = 0.01
# num_epochs = 10
#
# possible_actions = board.get_all_possible_actions()
#
# print(len(possible_actions))
#
# model = Model(input_channels, len(possible_actions))
# optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
#
# for epoch in range(num_epochs):
#     for state, target_policy, target_value in training_data:
#         predicted_policy, predicted_value = model(state)
#
#         policy_loss = torch.sum(-target_policy * predicted_policy)
#         value_loss = F.mse_loss(predicted_value, target_value)
#
#         loss = value_loss + policy_loss
#         print(loss)
#
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()


