class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = (0, 0, width, height)

    def apply(self, target):
        # возвращаем смещённые координаты обьекта
        return target.rect.move(self.state[0], self.state[1])

    def update(self, target):
        # обновляем смещение относительно обьекта
        self.state = self.camera_func(self.state, target.rect)
