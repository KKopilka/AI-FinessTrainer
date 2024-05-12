"""
TaskCounter - The counter of exercise execution.

It is counted through the Count(percent, isCorrect) method and the % of the exercise execution is passed to it.
If the exercise has reached 100%, the exercise phase (e.g. the direction of movement of a body part) is changed.
The exercise is scored when both phases are passed. If an error isCorrect = False during one of the phases.
The counter will not count the exercise as successful. The ResetState() method resets the error state of the counter.
The Reset() method resets the counter to its original state.
ErrorAmount() returns the number of unsuccessful approaches.
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