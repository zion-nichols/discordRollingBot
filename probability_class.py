class probability_distribution:
    def __init__(self, successes: int, failures: int):
        self.successes = successes
        self.failures = failures
        self.sux_chance = successes/(successes+failures)

    def __str__(self) -> str:
        return f'Successes: {self.successes} | Failures: {self.failures} | Chance: {self.sux_chance:.2%}'