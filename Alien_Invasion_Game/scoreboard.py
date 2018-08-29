#coding:gbk
import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():	
	"""��ʾ�÷���Ϣ����"""
	
	def __init__(self, ai_settings, screen, stats):
		"""��ʼ����ʾ�÷��漰������"""
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		# ��ʾ�÷���Ϣʱʹ�õ���������
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 18)
		
		# ׼����ʼ�÷�ͼ��
		self.prep_score()
		self.prep_level()
		self.prep_high_score()
		self.prep_ships()
	

		
	def prep_score(self):
		"""���÷�ת��Ϊһ����Ⱦ��ͼ��"""
		rounded_score = round(self.stats.score, -1)
		score_str = "Score: " + "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color)
		
		# ���÷ַ�����Ļ���Ͻ�
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 10
		self.score_rect.top = 10
		
	def prep_level(self):
		"""���ȼ�ת��Ϊ��Ⱦ��ͼ��"""
		level_str = "Level: " + str(self.stats.level)
		self.level_image = self.font.render(level_str, True,
			self.text_color)
		
		# ���ȼ����ڵ÷�����
		self.level_rect = self.level_image.get_rect()
		self.level_rect.centerx = self.screen_rect.centerx
		self.level_rect.top = self.score_rect.top
	
	def prep_high_score(self):
		"""����ߵ÷�ת��Ϊ��Ⱦ��ͼ��"""
		high_score = round(self.stats.high_score, -1)
		high_score_str = "High Score: " + "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True, 
			self.text_color)
		
		# ����ߵ÷ַ�����Ļ��������
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.right = self.score_rect.right
		self.high_score_rect.top = self.score_rect.bottom + 5
	
	
	
	def prep_ships(self):
		"""��ʾ�����¶��ٷɴ�"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 5 + ship_number * ship.rect.width
			ship.rect.y = 0
			self.ships.add(ship)
	
	def show_score(self):
		"""����Ļ����ʾ�÷֡���߷��Լ��ȼ�"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)
		
