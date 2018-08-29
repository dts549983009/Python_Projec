#coding:gbk
import pygame
from pygame.sprite import Sprite
from alien import Alien

class AlienAttack(Sprite):
	"""一个对外星人发射的子弹进行管理的类"""
	
	def __init__(self, ai_settings, screen):
		"""在外星人所处的位置创建一个子弹对象"""
		super(AlienAttack, self).__init__()
		self.alien = Alien(ai_settings, screen)
		self.screen = screen
		#创建图像
		self.image = pygame.image.load('images/bullets_1_alien.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx = self.alien.rect.centerx
		self.rect.top = self.alien.rect.bottom
		#存储用小数表示的子弹位置
		self.y = float(self.rect.top)
		#确定子弹攻击的初始速度
		self.speed_factor = ai_settings.alien_1_attack_speed_factor
		
	def update(self):
		"""向下移动子弹"""
		#更新表示子弹位置的小数值
		self.y += self.speed_factor
		#更新表示子弹的rect的位置
		self.rect.top = self.y
		
	def draw_bullet(self):
		"""在屏幕上绘制子弹"""
		pygame.draw.rect(self.screen, self.color, self.rect)
