# coding:gbk

import pygame
import json
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from background import Background
import game_functions as gf
from sound import Sound

def run_game():
	# ��ʼ����Ϸ������һ����Ļ����
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,
		ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	# ����Play��ť
	play_button = Button(ai_settings, screen, "Play")
	
	# ����һ�����ڴ洢��Ϸͳ����Ϣ��ʵ��
	stats = GameStats(ai_settings, 'highscore.json')
	
	# ����һ���Ƿ���
	sb = Scoreboard(ai_settings, screen, stats)
	
	# ����һ�ҷɴ���һ���ӵ������һ�������˱���
	ship = Ship(ai_settings, screen)
	background = Background(ai_settings, screen)
	backgrounds = Group()
	bullets = Group()
	aliens = Group()
	attacks = Group()
	
	# ������������ѭ��
	sound = Sound(ai_settings)
	sound.creat_bg_music()
	
	# ����������Ⱥ
	gf.creat_fleet_1(ai_settings, screen, ship, aliens)
	
	# ��ʼ��Ϸ����ѭ��  
	while True:
		
		gf.check_events(ai_settings, screen, background, backgrounds,
			stats, sb, play_button, ship, aliens, bullets, attacks, sound)          
		if stats.game_active: 
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
				bullets, attacks, sound)
			gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
				bullets, attacks)
			gf.update_attacks(ai_settings, screen, stats, sb, ship, aliens,
				bullets, attacks, sound)
			gf.update_backgrounds(ai_settings, screen, background, backgrounds)
		gf.update_screen(ai_settings, screen, background, backgrounds,
			stats, sb, ship, aliens, bullets, attacks, play_button)
	
run_game()      
