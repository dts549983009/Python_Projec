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
	# 初始化游戏并创建一个屏幕对象
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,
		ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	# 创建Play按钮
	play_button = Button(ai_settings, screen, "Play")
	
	# 创建一个用于存储游戏统计信息的实例
	stats = GameStats(ai_settings, 'highscore.json')
	
	# 创建一个记分牌
	sb = Scoreboard(ai_settings, screen, stats)
	
	# 创建一艘飞船、一个子弹编组和一个外星人编组
	ship = Ship(ai_settings, screen)
	background = Background(ai_settings, screen)
	backgrounds = Group()
	bullets = Group()
	aliens = Group()
	attacks = Group()
	
	# 创建背景音乐循环
	sound = Sound(ai_settings)
	sound.creat_bg_music()
	
	# 创建外星人群
	gf.creat_fleet_1(ai_settings, screen, ship, aliens)
	
	# 开始游戏的主循环  
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
