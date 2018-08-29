#coding:gbk
import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
	"""��ʾ���������˵���"""
	
	def __init__(self, ai_settings, screen):
		"""��ʼ�������˲���������ʼλ��"""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#����������ͼ�񣬲�������rect����
		self.image = pygame.image.load('images/alien_1.png').convert_alpha()
		self.rect = self.image.get_rect()
		
		#ÿ�����������������Ļ���ϽǸ���
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		self.rect.centerx = int(0.5 * self.rect.width)
		
		#�洢�����˵�׼ȷλ��
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
		self.centerx = float(self.rect.centerx)
		
		
	def blitme(self):
		"""��ָ��λ�û���������"""
		self.screen.blit(self.image, self.rect)
	
	def check_edges(self):
		"""���������λ����Ļ��Ե���ͷ���True"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
		
	def update_x(self):
		"""�����ƶ�������"""
		self.x += (self.ai_settings.alien_speed_factor*
						self.ai_settings.fleet_direction)
		self.rect.x = self.x
		
	def update_y(self):
		"""�����ƶ�������"""
		self.y += self.ai_settings.alien_2_speed_factor				
		self.rect.y = self.y
	
	def update_centerx(self):
		"""���������������ƶ�"""
		self.centerx += (self.ai_settings.alien_3_speed_factor*
						self.ai_settings.fleet_direction)
		self.rect.centerx = self.centerx
