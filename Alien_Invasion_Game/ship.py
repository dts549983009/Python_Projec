# coding:gbk
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

	def __init__(self, ai_settings, screen):
		"""��ʼ���ɴ����������ʼλ��"""
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# ���طɴ�ͼ�񲢻�ȡ����Ӿ���
		self.image = pygame.image.load('images/ship_1.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		# ��ÿ���·ɴ�������Ļ�ײ�����
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom - self.rect.height
		
		# �ڷɴ�������center�д洢С��ֵ
		self.center = float(self.rect.centerx)
		self.y = float(self.rect.y)
		
		# ��ʼ���ƶ���־
		self.moving_direction()
		
	def moving_direction(self):
		# ��ʼ���ƶ���־
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False 
		self.moving_down = False

	def update(self):
		"""�����ƶ���־�����ɴ���λ��"""
		# ���·ɴ���centerֵ��������rect
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > self.screen_rect.left:
			self.center -= self.ai_settings.ship_speed_factor	
		if self.moving_up and self.rect.top > self.screen_rect.top:
			self.y -= self.ai_settings.ship_speed_factor
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.y += self.ai_settings.ship_speed_factor
		
		# ����self.center��self.y����rect����
		self.rect.centerx = self.center
		self.rect.y = self.y
		
	def blitme(self):
		"""��ָ��λ�û��Ʒɴ�"""	
		self.screen.blit(self.image, self.rect)
		
	def center_ship(self):
		"""�÷ɴ�����Ļ�Ͼ���"""
		self.center = self.screen_rect.centerx
		self.rect.centerx = self.center
		#print(self.rect.centerx)
		self.y = self.screen_rect.bottom - 2 * self.rect.height
		
