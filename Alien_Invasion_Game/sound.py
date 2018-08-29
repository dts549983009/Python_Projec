#coding:gbk
import pygame.mixer
from pygame.locals import *

pygame.init()
pygame.mixer.init()

class Sound():
	"""��ʾ��Ϸ�����и�����Ч����"""
	def __init__(self, ai_settings):
		"""��ʼ��������Ч����·��"""
		self.ai_settings = ai_settings
		self.bullet_sound = pygame.mixer.Sound("sounds/bullet_sound.wav")
		self.ship_bomb_sound = pygame.mixer.Sound("sounds/ship_bomb_sound.wav")
		self.alien_bomb_sound = pygame.mixer.Sound("sounds/alien_bomb_sound.wav")
		
	def creat_bg_music(self):
		"""���ñ�������"""
		pygame.mixer.music.load('sounds/bg_music.ogg')
		pygame.mixer.music.set_volume(self.ai_settings.bg_music_volume)
		pygame.mixer.music.play(-1)
		
	def creat_bullet_sound(self):
		"""�����ӵ���Ч"""
		self.bullet_sound.set_volume(self.ai_settings.bullet_sound_volume)
		self.bullet_sound.play()
		
	def creat_ship_bomb_sound(self):
		"""���÷ɴ���ը��Ч"""
		self.ship_bomb_sound.set_volume(self.ai_settings.ship_bomb_sound_volume)
		self.ship_bomb_sound.play()
		
	def creat_alien_bomb_sound(self):
		"""���������˱�ը��Ч"""
		self.alien_bomb_sound.set_volume(self.ai_settings.alien_bomb_sound_volume)
		self.alien_bomb_sound.play()
