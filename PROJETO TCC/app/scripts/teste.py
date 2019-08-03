from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

from random import randint


class PongApp(App):
    def build(self):
        game = PongGame()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


class PongGame(Widget):
    ball = ObjectProperty(None)

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.vel = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()

        if(self.ball.y<0) or (self.ball.top>self.height):
            self.ball.vel_y *= -1
        
        if(self.ball.x<0) or (self.ball.right>self.width):
            self.ball.vel_x *= -1


class PongBall(Widget):
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)

    vel = ReferenceListProperty(vel_x, vel_y)

    def move(self):
        self.pos = Vector(*self.vel) + self.pos



if __name__ == '__main__':
    PongApp().run()