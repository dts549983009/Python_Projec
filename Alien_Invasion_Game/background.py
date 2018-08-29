# coding:gbk
import pygame
from pygame.sprite import Sprite
from time import sleep

class Background(Sprite):

	def __init__(self, ai_settings, screen):
		"""��ʼ����̬�������������ʼλ��"""
		super(Background, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# ���ر���ͼ�񲢻�ȡ����Ӿ���
		self.image = pygame.image.load('images/background.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		# ����ʼ����ͼ������Ļ�ײ�����
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		#�洢����ͼ��׼ȷλ��
		self.y = float(self.rect.y)
		
		
	def blitme(self):
		"""��ָ��λ�û��Ʊ���ͼ"""
		self.screen.blit(self.image, self.rect)
	
	def update(self):
		"""�����ƶ�ͼ��"""
		self.y += self.ai_settings.background_speed_factor
		self.rect.y = self.y

