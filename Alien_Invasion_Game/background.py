# coding:gbk
import pygame
from pygame.sprite import Sprite
from time import sleep

class Background(Sprite):

	def __init__(self, ai_settings, screen):
		"""初始化动态背景并设置其初始位置"""
		super(Background, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# 加载背景图像并获取其外接矩形
		self.image = pygame.image.load('images/background.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		# 将初始背景图放在屏幕底部中央
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		#存储背景图的准确位置
		self.y = float(self.rect.y)
		
		
	def blitme(self):
		"""在指定位置绘制背景图"""
		self.screen.blit(self.image, self.rect)
	
	def update(self):
		"""向下移动图像"""
		self.y += self.ai_settings.background_speed_factor
		self.rect.y = self.y

