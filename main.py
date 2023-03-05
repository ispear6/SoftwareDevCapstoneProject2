from characters import player, EnemyType, spawnenemy
from combat import combatinstance


enemy = spawnenemy(EnemyType.bandit, 1)

combatinstance(player, enemy)
