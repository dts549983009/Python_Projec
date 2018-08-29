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
	"""响应按键"""
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
		# 发射子弹时，发出特定音效
		sound.creat_bullet_sound()
	elif event.key == pygame.K_q:
		sys.exit()
			
def check_keyup_events(event, ship):
	"""响应松开"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False
		
def fire_bullet(ai_settings, screen, ship, bullets):
	"""如果还没有达到限制，就发射一颗子弹"""
	#创建一颗子弹，并将其加入到编组bullets中
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)


		
def check_events(ai_settings, screen, background, backgrounds, stats,
		sb, play_button, ship, aliens, bullets, attacks, sound):
	"""响应按键和鼠标事件"""
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
	"""在玩家单机Play按钮时开始新游戏"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# 将初始背景添加到列表中
		backgrounds.add(background)
		
		# 重置游戏设置
		ai_settings.initialize_dynamic_settings()
		
		# 隐藏光标
		pygame.mouse.set_visible(False)
		
		# 重置游戏统计信息
		stats.reset_stats()
		stats.game_active = True
		
		# 初始化移动标志
		ship.moving_direction()
		
		# 重置记分牌图像
		sb.prep_score()
		sb.prep_level()
		sb.prep_ships()
		
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		attacks.empty()
		
		# 创建一群新的外星人，并让飞船居中
		creat_fleet_1(ai_settings, screen, ship, aliens)
		ship.center_ship()

def update_screen(ai_settings, screen, background, backgrounds, stats,
		sb, ship, aliens, bullets, attacks, play_button):
	"""更新屏幕上的图像，并切换到新屏幕"""
	# 每次循环时都重绘屏幕
	screen.fill(ai_settings.bg_color)
	background.blitme()
	backgrounds.draw(screen)

	# 在飞船和外星人后面重绘所有子弹	
	ship.blitme()
	aliens.draw(screen)
	bullets.draw(screen)
	attacks.draw(screen)
	sb.show_score()
	
	# 如果游戏处于非活跃状态，就绘制Play按钮
	if not stats.game_active:
		play_button.draw_button()

	# 让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,
		attacks, sound):
	"""更新子弹的位置，并删除已消失的子弹"""
	#更新子弹的位置
	for bullet in bullets.sprites():
		bullet.update()
	
	#删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
		aliens, bullets, attacks, sound)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
		aliens, bullets, attacks, sound):
	"""检查是否有子弹击中了外星人"""
	# 如果是这样，就删除相应的子弹和外星人
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		# 击中外星人时，得分相应增加
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points*len(aliens)
			sb.prep_score()
			# 击中外星人时，发出外星人爆炸的音效
			sound.creat_alien_bomb_sound()
		check_high_score(stats, sb)
		
	"""检查是否有子弹击中了外星人攻击波"""
	#如果是这样，就删除相应的子弹和外星人攻击波	
	collisions = pygame.sprite.groupcollide(bullets, attacks, True, True)

	if len(aliens) == 0:
		# 删除现有的所有子弹、并新建一个新的外星人群
		bullets.empty()
		attacks.empty()
		stats.attacks_number = 0
		stats.attacks_interval_time = 0
		creat_fleet(ai_settings, screen, stats, sb, ship, aliens)

def creat_fleet(ai_settings, screen, stats, sb, ship, aliens):
	# 新建一个新的外星人群
	if stats.aliens_type_left > 1:
		# 将aliens_type_left减1
		stats.aliens_type_left -= 1
		if stats.aliens_type_left == 2:
			creat_fleet_2(ai_settings, screen, ship, aliens)
		elif stats.aliens_type_left == 1:
			creat_fleet_3(ai_settings, screen, ship, aliens)
	elif stats.aliens_type_left <= 1:
		creat_fleet_1(ai_settings, screen, ship, aliens)
		# 重置外星人种类数目
		stats.aliens_type_left = 3
		# 提高等级
		stats.level += 1
		sb.prep_level()
		# 加快游戏速度
		ai_settings.increase_speed()	
		
def get_number_aliens_x(ai_settings, alien_width):
	"""计算每行可容纳多少个外星人"""
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x/(2*alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	"""计算屏幕可容纳多少行外星人"""
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
	
	# 创建外星人群
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):                               
			creat_alien_1(ai_settings, screen, aliens, alien_number,
				row_number)

def get_add_space_x(ai_settings):
	"""计算外星人可控区域的x值"""
	available_space_x = ai_settings.screen_width
	add_space_x = available_space_x/2
	return add_space_x

def get_add_space_y(ai_settings, ship_height, alien_height):
	"""计算外星人可控区域的y值"""
	available_space_y = (ai_settings.screen_height - 
							(6 * alien_height + 2 * ship_height))
	add_space_y = available_space_y/2
	return add_space_y

def creat_alien_2(ai_settings, screen, ship, aliens, add_space_x, 
		add_space_y, value_1, value_2):
	"""创建外星人"""
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
	"""创建外星人群"""
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
	"""创建外星人"""
	alien = Alien(ai_settings, screen)
	alien.image = pygame.image.load('images/alien_3.png').convert_alpha()
	# 初始化alien_3的x值
	alien.centerx = (- (alien_3_number + 0.5) * alien.rect.width)		
	alien.rect.centerx = alien.centerx
	# 初始化alien_3的y值
	alien.centery = 3 * ship.rect.height
	alien.rect.centery = alien.centery
	# 添加到aliens
	aliens.add(alien)
	
def creat_fleet_3(ai_settings, screen, ship, aliens):
	"""创建外星人群"""
	for alien_3_number in range(ai_settings.alien_3_left):
		creat_alien_3(ai_settings, screen, ship, aliens, alien_3_number)
		
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets,
		attacks):
	"""对alien_3进行更新"""
	if stats.aliens_type_left == 1:
		screen_rect = screen.get_rect()
		for alien in aliens.sprites():
			if (alien.rect.centerx <= screen_rect.left and   
					(alien.rect.centery <= 6 * ship.rect.height)):
				# alien_3出屏幕左侧的运行路径
				ai_settings.fleet_direction = 1
				alien.update_centerx()
				
			elif (alien.rect.centerx > screen_rect.left and  
					(alien.rect.centery < 6 * ship.rect.height)):
				# alien_3在椭圆上半区的运行路径
				ai_settings.fleet_direction = 1
				alien.update_centerx()
				alien.centery = (- 1.5 * ((10000 - (alien.rect.centerx  
									** 2)) ** 0.5) + 6 * ship.rect.height)
				alien.rect.centery = alien.centery
				
			elif (alien.rect.centerx > screen_rect.left and 
					(alien.rect.centery >= 6 * ship.rect.height)):
				# alien_3在椭圆下半区的运行路径
				ai_settings.fleet_direction = -1
				alien.update_centerx()
				alien.centery = (1.5 * ((10000 - (alien.rect.centerx  
									** 2)) ** 0.5) + 6 * ship.rect.height)
				alien.rect.centery = alien.centery
				
			elif (alien.rect.centerx <= screen_rect.left and 
					(alien.rect.centery >= 6 * ship.rect.height)):
				#alien_3入屏幕左侧的运行路径"""		
				ai_settings.fleet_direction = -1
				alien.update_centerx()
				if alien.rect.x <= - alien.rect.width:
					aliens.remove(alien)
					

	"""对alien_2进行更新"""
	if stats.aliens_type_left == 2:
		for alien in aliens.sprites():
			alien.update_y()
			
	"""对alien_1进行更新"""		
	if stats.aliens_type_left == 3:
		# 检查是否有外星人位于屏幕边缘，并更新整群外星人的位置	
		check_fleet_edges(ai_settings, aliens)
		for alien in aliens.sprites():
			alien.update_x()		

	"""对所有外星人进行更新"""
	# 检测外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets,
			attacks)
		
	# 检查是否有外星人到达屏幕底端
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, 
		bullets, attacks)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, 
		bullets, attacks):
	"""检查是否有外星人到达屏幕底端"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			"""像飞船被撞倒一样进行处理"""
			ship_hit(ai_settings, screen, stats, sb, ship, aliens,
				bullets, attacks)
			break
		

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, 
		attacks):
	"""响应被外星人撞到的飞船"""
	if stats.ships_left > 1:
		#将ship_left减1
		stats.ships_left -= 1
		
		#更新记分牌
		sb.prep_ships()
	
		#清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		attacks.empty()
		
		#创建一群新的外星人
		if stats.aliens_type_left == 1:
			creat_fleet_3(ai_settings, screen, ship, aliens)
		if stats.aliens_type_left == 2:
			creat_fleet_2(ai_settings, screen, ship, aliens)
		elif stats.aliens_type_left == 3:
			creat_fleet_1(ai_settings, screen, ship, aliens)
			
		#将飞船放到屏幕底部中央	
		ship.center_ship()
	
		#暂停
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	
def check_fleet_edges(ai_settings, aliens):
	"""有外星人到达边缘时采取相应的措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""将整群外星人下移，并改变它们的方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def check_high_score(stats, sb):
	"""检查是否诞生了新的最高得分"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		
def check_background_top_edge(ai_settings, screen, backgrounds):
	"""检查背景图顶端是否过了边缘"""
	for background in backgrounds.sprites():
		if background.rect.top == 0:
			background = Background(ai_settings, screen)
			background.y = 0 - background.rect.height
			background.rect.y = background.y
			backgrounds.add(background)	
			
def update_backgrounds(ai_settings, screen, background, backgrounds):
	"""检查背景图顶端是否过了边缘"""
	check_background_top_edge(ai_settings, screen, backgrounds)
	
	"""对背景图进行更新，并删除已消失的背景图"""
	for background in backgrounds.sprites():
		# 更新背景图的位置	
		background.update()

		# 删除已消失的背景图
	for background in backgrounds.copy():
		screen_rect = screen.get_rect()
		if background.rect.top > screen_rect.bottom:
			backgrounds.remove(background)


def creat_alien_attack(ai_settings, screen, stats, aliens, attacks):
	"""为每个外星人准备子弹攻击"""
	for alien in aliens.sprites():
		# 对在屏幕上的外星人进行操作（针对alien_3）
		if alien.rect.x > 0:
			attack = AlienAttack(ai_settings, screen)
			# 初始化攻击子弹中心值
			attack.rect.centerx = alien.rect.centerx
			# 初始化攻击子弹Y值
			attack.y = alien.rect.bottom - ai_settings.attacks_interval_distance * stats.attacks_number
			attack.rect.top = attack.y
			# 添加到attacks
			attacks.add(attack)
			
				
		
def update_attacks(ai_settings, screen, stats, sb, ship, aliens, bullets,
		attacks, sound):
	"""创建一组攻击波，并更新其位置，删除已消失的攻击波"""
	
	# 检查单次攻击强度未超过了一组攻击波的个数
	if stats.attacks_number < ai_settings.attacks_allowed:
		
		"""创建alien_3的攻击波"""
		if stats.aliens_type_left == 1:
			creat_alien_attack(ai_settings, screen, stats, aliens, attacks)
			stats.attacks_number += 1
			
			
			#更新alien_3攻击波的位置
			for attack in attacks.sprites():
				attack.speed_factor = ai_settings.alien_3_attack_speed_factor
				attack.update()

		"""创建alien_2的攻击波"""	
		if stats.aliens_type_left == 2:
			creat_alien_attack(ai_settings, screen, stats, aliens, attacks)
			stats.attacks_number += 1
			
			#更新alien_2攻击波的位置
			for attack in attacks.sprites():
				attack.speed_factor = ai_settings.alien_2_attack_speed_factor
				attack.update()
			
		"""创建alien_1的攻击波"""	
		if stats.aliens_type_left == 3:
			stats.attacks_initial_value += 1
			if stats.attacks_initial_value == ai_settings.attacks_interval_distance:
				creat_alien_attack(ai_settings, screen, stats, aliens,
					attacks)
				stats.attacks_initial_value = 0
				stats.attacks_number += 1
				
			#更新alien_1攻击波的位置
			for attack in attacks.sprites():
				attack.speed_factor = ai_settings.alien_1_attack_speed_factor
				attack.update()
				
	# 检查单次攻击强度超过了一组攻击波的个数，且攻击波都已消失在屏幕中
	if (stats.attacks_number == ai_settings.attacks_allowed and
			(len(attacks) == 0)):
		stats.attacks_number = 0
		
		
	for attack in attacks.sprites():
		attack.update()
	
	#删除已消失的子弹
	screen_rect = screen.get_rect()
	for attack in attacks.copy():
		if attack.rect.bottom >= screen_rect.bottom:
			attacks.remove(attack)
			
	check_alien_attack_ship_collisions(ai_settings, screen, stats, sb,
		ship, aliens, bullets, attacks, sound)

def check_alien_attack_ship_collisions(ai_settings, screen, stats, sb,
		ship, aliens, bullets, attacks, sound):
	"""检查是否有子弹击中了飞船"""
	"""如果是这样，就删除相应的子弹，并减少一艘飞船"""
	if pygame.sprite.spritecollideany(ship, attacks):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets,
			attacks)
			
		# 击中飞船时，得分相应减少
		stats.score -= ai_settings.ship_points
		sb.prep_score()
		check_high_score(stats, sb)
		
		# 击中飞船时，发出飞船爆炸的音效
		sound.creat_ship_bomb_sound()
