#coding:gbk
import pygame
from pygame.sprite import Sprite
from alien import Alien

class AlienAttack(Sprite):
	"""һ���������˷�����ӵ����й������"""
	
	def __init__(self, ai_settings, screen):
		"""��������������λ�ô���һ���ӵ�����"""
		super(AlienAttack, self).__init__()
		self.alien = Alien(ai_settings, screen)
		self.screen = screen
		#����ͼ��
		self.image = pygame.image.load('images/bullets_1_alien.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx = self.alien.rect.centerx
		self.rect.top = self.alien.rect.bottom
		#�洢��С����ʾ���ӵ�λ��
		self.y = float(self.rect.top)
		#ȷ���ӵ������ĳ�ʼ�ٶ�
		self.speed_factor = ai_settings.alien_1_attack_speed_factor
		
	def update(self):
		"""�����ƶ��ӵ�"""
		#���±�ʾ�ӵ�λ�õ�С��ֵ
		self.y += self.speed_factor
		#���±�ʾ�ӵ���rect��λ��
		self.rect.top = self.y
		
	def draw_bullet(self):
		"""����Ļ�ϻ����ӵ�"""
		pygame.draw.rect(self.screen, self.color, self.rect)
