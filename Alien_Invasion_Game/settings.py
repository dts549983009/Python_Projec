# coding:gbk
class Settings():
	"""存储《外星人入侵》的所有设置的类"""
	
	def __init__(self):
		"""初始化游戏的静态设置"""
		# 屏幕设置
		self.screen_width = 300
		self.screen_height = 650
		self.bg_color = (255, 255, 0)
		
		#飞船设置
		
		self.ship_limit = 3
		
		# 子弹设置
		self.bullet_width = 3 
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 20
		
		
		# 外星人设置
		self.fleet_drop_speed = 1
		self.alien_type_limit = 3
		self.alien_3_left = 10
		self.attacks_allowed = 2
		self.attacks_interval_distance = 50

		
		# 背景设置
		self.background_speed_factor = 1
		self.bg_music_volume = 0.3
		
		# 音效设置
		self.bullet_sound_volume = 0.2
		self.ship_bomb_sound_volume = 0.4
		self.alien_bomb_sound_volume = 0.4
		
		# 以什么样的速度加快游戏节奏
		self.speedup_scale = 1.1
		# 外星人点数的提高倍数
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
	
	def initialize_dynamic_settings(self):
		"""初始化随游戏进行而变化的设置"""           
		self.ship_speed_factor = 1
		self.bullet_speed_factor = 3
		self.alien_1_attack_speed_factor = 0.4
		self.alien_2_attack_speed_factor = 0.3
		self.alien_3_attack_speed_factor = 1
		self.alien_speed_factor = 0.3
		self.alien_2_speed_factor = 0.1
		self.alien_3_speed_factor = 0.3
		# fleet_direction为1表示向右移；为-1表示向左移
		self.fleet_direction = 1
		# 记分
		self.alien_points = 100
		self.ship_points = 50
	
	def increase_speed(self):
		"""提高速度设置"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_1_attack_speed_factor *= self.speedup_scale
		self.alien_2_attack_speed_factor *= self.speedup_scale
		self.alien_3_attack_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_2_speed_factor *= self.speedup_scale
		self.alien_3_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
		
