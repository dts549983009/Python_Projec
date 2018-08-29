#coding:gbk
import sys
import json
from time import sleep
from random import randint

import pygame
from bullet import Bullet
from alien import Alien
from background import Background
from alien_attack import AlienAttack


def check_keydown_events(event, ai_settings, screen, ship, aliens,
		bullets, sound):
	"""��Ӧ����"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
		# �����ӵ�ʱ�������ض���Ч
		sound.creat_bullet_sound()
	elif event.key == pygame.K_q:
		sys.exit()
			
def check_keyup_events(event, ship):
	"""��Ӧ�ɿ�"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False
		
def fire_bullet(ai_settings, screen, ship, bullets):
	"""�����û�дﵽ���ƣ��ͷ���һ���ӵ�"""
	#����һ���ӵ�����������뵽����bullets��
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)


		
def check_events(ai_settings, screen, background, backgrounds, stats,
		sb, play_button, ship, aliens, bullets, attacks, sound):
	"""��Ӧ����������¼�"""
	for event in pygame.event.get():
		if not stats.game_active:
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				check_play_button(ai_settings, screen, background,
					backgrounds, stats, sb, play_button, ship, aliens,
						bullets, attacks, mouse_x, mouse_y)
		elif stats.game_active:
			if event.type == pygame.QUIT:
				with open(stats.filename, 'w') as f_json:
					json.dump(stats.high_score, f_json)
				sys.exit()
			elif event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				check_keydown_events(event, ai_settings, screen, ship,
					aliens, bullets, sound)
			elif event.type == pygame.KEYUP:	
				check_keyup_events(event, ship)
		

def check_play_button(ai_settings, screen, background, backgrounds, stats,
		sb, play_button, ship, aliens, bullets, attacks, mouse_x, mouse_y):
	"""����ҵ���Play��ťʱ��ʼ����Ϸ"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# ����ʼ������ӵ��б���
		backgrounds.add(background)
		
		# ������Ϸ����
		ai_settings.initialize_dynamic_settings()
		
		# ���ع��
		pygame.mouse.set_visible(False)
		
		# ������Ϸͳ����Ϣ
		stats.reset_stats()
		stats.game_active = True
		
		# ��ʼ���ƶ���־
		ship.moving_direction()
		
		# ���üǷ���ͼ��
		sb.prep_score()
		sb.prep_level()
		sb.prep_ships()
		
		# ����������б���ӵ��б�
		aliens.empty()
		bullets.empty()
		attacks.empty()
		
		# ����һȺ�µ������ˣ����÷ɴ�����
		creat_fleet_1(ai_settings, screen, ship, aliens)
		ship.center_ship()

def update_screen(ai_settings, screen, background, backgrounds, stats,
		sb, ship, aliens, bullets, attacks, play_button):
	"""������Ļ�ϵ�ͼ�񣬲��л�������Ļ"""
	# ÿ��ѭ��ʱ���ػ���Ļ
	screen.fill(ai_settings.bg_color)
	background.blitme()
	backgrounds.draw(screen)

	# �ڷɴ��������˺����ػ������ӵ�	
	ship.blitme()
	aliens.draw(screen)
	bullets.draw(screen)
	attacks.draw(screen)
	sb.show_score()
	
	# �����Ϸ���ڷǻ�Ծ״̬���ͻ���Play��ť
	if not stats.game_active:
		play_button.draw_button()

	# ��������Ƶ���Ļ�ɼ�
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,
		attacks, sound):
	"""�����ӵ���λ�ã���ɾ������ʧ���ӵ�"""
	#�����ӵ���λ��
	for bullet in bullets.sprites():
		bullet.update()
	
	#ɾ������ʧ���ӵ�
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
		aliens, bullets, attacks, sound)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
		aliens, bullets, attacks, sound):
	"""����Ƿ����ӵ�������������"""
	# �������������ɾ����Ӧ���ӵ���������
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		# ����������ʱ���÷���Ӧ����
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points*len(aliens)
			sb.prep_score()
			# ����������ʱ�����������˱�ը����Ч
			sound.creat_alien_bomb_sound()
		check_high_score(stats, sb)
		
	"""����Ƿ����ӵ������������˹�����"""
	#�������������ɾ����Ӧ���ӵ��������˹�����	
	collisions = pygame.sprite.groupcollide(bullets, attacks, True, True)

	if len(aliens) == 0:
		# ɾ�����е������ӵ������½�һ���µ�������Ⱥ
		bullets.empty()
		attacks.empty()
		stats.attacks_number = 0
		stats.attacks_interval_time = 0
		creat_fleet(ai_settings, screen, stats, sb, ship, aliens)

def creat_fleet(ai_settings, screen, stats, sb, ship, aliens):
	# �½�һ���µ�������Ⱥ
	if stats.aliens_type_left > 1:
		# ��aliens_type_left��1
		stats.aliens_type_left -= 1
		if stats.aliens_type_left == 2:
			creat_fleet_2(ai_settings, screen, ship, aliens)
		elif stats.aliens_type_left == 1:
			creat_fleet_3(ai_settings, screen, ship, aliens)
	elif stats.aliens_type_left <= 1:
		creat_fleet_1(ai_settings, screen, ship, aliens)
		# ����������������Ŀ
		stats.aliens_type_left = 3
		# ��ߵȼ�
		stats.level += 1
		sb.prep_level()
		# �ӿ���Ϸ�ٶ�
		ai_settings.increase_speed()	
		
def get_number_aliens_x(ai_settings, alien_width):
	"""����ÿ�п����ɶ��ٸ�������"""
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x/(2*alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	"""������Ļ�����ɶ�����������"""
	available_space_y = (ai_settings.screen_height - 
							(5*alien_height) - (2*ship_height))
	number_rows = int(available_space_y/(2*alien_height))
	return number_rows

def creat_alien_1(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien.x = alien.rect.width + 2*alien.rect.width*alien_number
	alien.rect.x = alien.x 
	alien.rect.y = 2 * alien.rect.height + 2*alien.rect.height*row_number
	aliens.add(alien)

	
def creat_fleet_1(ai_settings, screen, ship, aliens):
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, 
						alien.rect.height)
	
	# ����������Ⱥ
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):                               
			creat_alien_1(ai_settings, screen, aliens, alien_number,
				row_number)

def get_add_space_x(ai_settings):
	"""���������˿ɿ������xֵ"""
	available_space_x = ai_settings.screen_width
	add_space_x = available_space_x/2
	return add_space_x

def get_add_space_y(ai_settings, ship_height, alien_height):
	"""���������˿ɿ������yֵ"""
	available_space_y = (ai_settings.screen_height - 
							(6 * alien_height + 2 * ship_height))
	add_space_y = available_space_y/2
	return add_space_y

def creat_alien_2(ai_settings, screen, ship, aliens, add_space_x, 
		add_space_y, value_1, value_2):
	"""����������"""
	alien = Alien(ai_settings, screen)
	alien.image = pygame.image.load('images/alien_2.png').convert_alpha()
	alien.rect.x = (randint((0 + value_2 * add_space_x), ((1+value_2) 
						* add_space_x - alien.rect.width)))
	alien.y = (randint((ship.rect.height + value_1 * add_space_y), 
				(ship.rect.height + (1 + value_1) * add_space_y - 
					alien.rect.height)))
	alien.rect.y = alien.y
	aliens.add(alien)
	

def creat_fleet_2(ai_settings, screen, ship, aliens):
	"""����������Ⱥ"""
	alien = Alien(ai_settings, screen)
	alien.image = pygame.image.load('images/alien_2.png').convert_alpha()
	add_space_x = get_add_space_x(ai_settings)
	add_space_y = get_add_space_y(ai_settings, ship.rect.height, 
		alien.rect.height)
	for value_1 in range(0,2):
		for value_2 in range(0,2):
			creat_alien_2(ai_settings, screen, ship, aliens, add_space_x,
				add_space_y, value_1, value_2)

def creat_alien_3(ai_settings, screen, ship, aliens, alien_3_number):
	"""����������"""
	alien = Alien(ai_settings, screen)
	alien.image = pygame.image.load('images/alien_3.png').convert_alpha()
	# ��ʼ��alien_3��xֵ
	alien.centerx = (- (alien_3_number + 0.5) * alien.rect.width)		
	alien.rect.centerx = alien.centerx
	# ��ʼ��alien_3��yֵ
	alien.centery = 3 * ship.rect.height
	alien.rect.centery = alien.centery
	# ��ӵ�aliens
	aliens.add(alien)
	
def creat_fleet_3(ai_settings, screen, ship, aliens):
	"""����������Ⱥ"""
	for alien_3_number in range(ai_settings.alien_3_left):
		creat_alien_3(ai_settings, screen, ship, aliens, alien_3_number)
		
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets,
		attacks):
	"""��alien_3���и���"""
	if stats.aliens_type_left == 1:
		screen_rect = screen.get_rect()
		for alien in aliens.sprites():
			if (alien.rect.centerx <= screen_rect.left and   
					(alien.rect.centery <= 6 * ship.rect.height)):
				# alien_3����Ļ��������·��
				ai_settings.fleet_direction = 1
				alien.update_centerx()
				
			elif (alien.rect.centerx > screen_rect.left and  
					(alien.rect.centery < 6 * ship.rect.height)):
				# alien_3����Բ�ϰ���������·��
				ai_settings.fleet_direction = 1
				alien.update_centerx()
				alien.centery = (- 1.5 * ((10000 - (alien.rect.centerx  
									** 2)) ** 0.5) + 6 * ship.rect.height)
				alien.rect.centery = alien.centery
				
			elif (alien.rect.centerx > screen_rect.left and 
					(alien.rect.centery >= 6 * ship.rect.height)):
				# alien_3����Բ�°���������·��
				ai_settings.fleet_direction = -1
				alien.update_centerx()
				alien.centery = (1.5 * ((10000 - (alien.rect.centerx  
									** 2)) ** 0.5) + 6 * ship.rect.height)
				alien.rect.centery = alien.centery
				
			elif (alien.rect.centerx <= screen_rect.left and 
					(alien.rect.centery >= 6 * ship.rect.height)):
				#alien_3����Ļ��������·��"""		
				ai_settings.fleet_direction = -1
				alien.update_centerx()
				if alien.rect.x <= - alien.rect.width:
					aliens.remove(alien)
					

	"""��alien_2���и���"""
	if stats.aliens_type_left == 2:
		for alien in aliens.sprites():
			alien.update_y()
			
	"""��alien_1���и���"""		
	if stats.aliens_type_left == 3:
		# ����Ƿ���������λ����Ļ��Ե����������Ⱥ�����˵�λ��	
		check_fleet_edges(ai_settings, aliens)
		for alien in aliens.sprites():
			alien.update_x()		

	"""�����������˽��и���"""
	# ��������˺ͷɴ�֮�����ײ
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets,
			attacks)
		
	# ����Ƿ��������˵�����Ļ�׶�
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, 
		bullets, attacks)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, 
		bullets, attacks):
	"""����Ƿ��������˵�����Ļ�׶�"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			"""��ɴ���ײ��һ�����д���"""
			ship_hit(ai_settings, screen, stats, sb, ship, aliens,
				bullets, attacks)
			break
		

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, 
		attacks):
	"""��Ӧ��������ײ���ķɴ�"""
	if stats.ships_left > 1:
		#��ship_left��1
		stats.ships_left -= 1
		
		#���¼Ƿ���
		sb.prep_ships()
	
		#����������б���ӵ��б�
		aliens.empty()
		bullets.empty()
		attacks.empty()
		
		#����һȺ�µ�������
		if stats.aliens_type_left == 1:
			creat_fleet_3(ai_settings, screen, ship, aliens)
		if stats.aliens_type_left == 2:
			creat_fleet_2(ai_settings, screen, ship, aliens)
		elif stats.aliens_type_left == 3:
			creat_fleet_1(ai_settings, screen, ship, aliens)
			
		#���ɴ��ŵ���Ļ�ײ�����	
		ship.center_ship()
	
		#��ͣ
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	
def check_fleet_edges(ai_settings, aliens):
	"""�������˵����Եʱ��ȡ��Ӧ�Ĵ�ʩ"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""����Ⱥ���������ƣ����ı����ǵķ���"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def check_high_score(stats, sb):
	"""����Ƿ������µ���ߵ÷�"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		
def check_background_top_edge(ai_settings, screen, backgrounds):
	"""��鱳��ͼ�����Ƿ���˱�Ե"""
	for background in backgrounds.sprites():
		if background.rect.top == 0:
			background = Background(ai_settings, screen)
			background.y = 0 - background.rect.height
			background.rect.y = background.y
			backgrounds.add(background)	
			
def update_backgrounds(ai_settings, screen, background, backgrounds):
	"""��鱳��ͼ�����Ƿ���˱�Ե"""
	check_background_top_edge(ai_settings, screen, backgrounds)
	
	"""�Ա���ͼ���и��£���ɾ������ʧ�ı���ͼ"""
	for background in backgrounds.sprites():
		# ���±���ͼ��λ��	
		background.update()

		# ɾ������ʧ�ı���ͼ
	for background in backgrounds.copy():
		screen_rect = screen.get_rect()
		if background.rect.top > screen_rect.bottom:
			backgrounds.remove(background)


def creat_alien_attack(ai_settings, screen, stats, aliens, attacks):
	"""Ϊÿ��������׼���ӵ�����"""
	for alien in aliens.sprites():
		# ������Ļ�ϵ������˽��в��������alien_3��
		if alien.rect.x > 0:
			attack = AlienAttack(ai_settings, screen)
			# ��ʼ�������ӵ�����ֵ
			attack.rect.centerx = alien.rect.centerx
			# ��ʼ�������ӵ�Yֵ
			attack.y = alien.rect.bottom - ai_settings.attacks_interval_distance * stats.attacks_number
			attack.rect.top = attack.y
			# ��ӵ�attacks
			attacks.add(attack)
			
				
		
def update_attacks(ai_settings, screen, stats, sb, ship, aliens, bullets,
		attacks, sound):
	"""����һ�鹥��������������λ�ã�ɾ������ʧ�Ĺ�����"""
	
	# ��鵥�ι���ǿ��δ������һ�鹥�����ĸ���
	if stats.attacks_number < ai_settings.attacks_allowed:
		
		"""����alien_3�Ĺ�����"""
		if stats.aliens_type_left == 1:
			creat_alien_attack(ai_settings, screen, stats, aliens, attacks)
			stats.attacks_number += 1
			
			
			#����alien_3��������λ��
			for attack in attacks.sprites():
				attack.speed_factor = ai_settings.alien_3_attack_speed_factor
				attack.update()

		"""����alien_2�Ĺ�����"""	
		if stats.aliens_type_left == 2:
			creat_alien_attack(ai_settings, screen, stats, aliens, attacks)
			stats.attacks_number += 1
			
			#����alien_2��������λ��
			for attack in attacks.sprites():
				attack.speed_factor = ai_settings.alien_2_attack_speed_factor
				attack.update()
			
		"""����alien_1�Ĺ�����"""	
		if stats.aliens_type_left == 3:
			stats.attacks_initial_value += 1
			if stats.attacks_initial_value == ai_settings.attacks_interval_distance:
				creat_alien_attack(ai_settings, screen, stats, aliens,
					attacks)
				stats.attacks_initial_value = 0
				stats.attacks_number += 1
				
			#����alien_1��������λ��
			for attack in attacks.sprites():
				attack.speed_factor = ai_settings.alien_1_attack_speed_factor
				attack.update()
				
	# ��鵥�ι���ǿ�ȳ�����һ�鹥�����ĸ������ҹ�����������ʧ����Ļ��
	if (stats.attacks_number == ai_settings.attacks_allowed and
			(len(attacks) == 0)):
		stats.attacks_number = 0
		
		
	for attack in attacks.sprites():
		attack.update()
	
	#ɾ������ʧ���ӵ�
	screen_rect = screen.get_rect()
	for attack in attacks.copy():
		if attack.rect.bottom >= screen_rect.bottom:
			attacks.remove(attack)
			
	check_alien_attack_ship_collisions(ai_settings, screen, stats, sb,
		ship, aliens, bullets, attacks, sound)

def check_alien_attack_ship_collisions(ai_settings, screen, stats, sb,
		ship, aliens, bullets, attacks, sound):
	"""����Ƿ����ӵ������˷ɴ�"""
	"""�������������ɾ����Ӧ���ӵ���������һ�ҷɴ�"""
	if pygame.sprite.spritecollideany(ship, attacks):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets,
			attacks)
			
		# ���зɴ�ʱ���÷���Ӧ����
		stats.score -= ai_settings.ship_points
		sb.prep_score()
		check_high_score(stats, sb)
		
		# ���зɴ�ʱ�������ɴ���ը����Ч
		sound.creat_ship_bomb_sound()
