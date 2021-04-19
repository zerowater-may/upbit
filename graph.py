import matplotlib.pyplot as plt

# # figure, 즉 그래프를 표현할 액자를 먼저 만든다.
# plt.figure()

# # figure 를 출력한다.
# plt.show()


# 한 주의 요일(0: 일, 1: 월 ~ 6: 토)
days = [0, 1, 2, 3, 4, 5, 6]
# 내가 사용한 돈(천원)
money_spent = [10, 12, 12, 10, 14, 22, 24]
# 친구가 사용한 돈(천원)
money_spent_2 = [11, 14, 15, 15, 22, 21, 12]
# 내가 사용한 돈을 그래프로 그립니다
plt.plot(days, money_spent)
# 같은 그림에 친구가 사용한 돈도 그래프로 그립니다
plt.plot(days, money_spent_2)
# 화면에 그래프를 보여줍니다
plt.show()