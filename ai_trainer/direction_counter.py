"""
TaskCounter - Счетчик выполнения упражннений.
Подсчет происходит через метод Count(percent, isCorrect) в него передается % - выполнения упражнения.
Если упражение достигло 100%, то происходит смена фазы упражнения (например направления движения части тела).
Упражнение засчитывается, когда проходит обе фазы. Если во время прохождения одной из фаз была подана ошибка isCorrect = False.
То счетчик не засчитает упражнение как успешное. Метод ResetState() сбрасывает состояние ошибки у счетчика.
Метод Reset() сбрасываает счетчик в изначальное состояние.
ErrorAmount() возвращает количество неуспешных подходов.
"""
class TaskCounter:
    def __init__(self) -> None:
        self.phase = 1
        self.count = 0
        self.correctCount = 0
        self.incorrectState = False
    
    def ResetState(self):
        self.incorrectState = False
    
        
    def Reset(self):
        self.phase = 1
        self.count = 0
        self.correctCount = 0
        self.ResetState()
    
    def Count(self, percent, isCorrect = False):
        if not isCorrect:
            self.incorrectState = True

        if percent == 100:
            if self.phase == 0:
                self.phase = 1
        # полное выполнение упражнения
        if percent == 0:
            if self.phase == 1:
                self.count += 1
                # помечаем выполнение, как успешное
                if not self.incorrectState:
                    self.correctCount += 1

                self.phase = 0
                self.ResetState()

    def ErrorAmount(self):
        return self.count - self.correctCount