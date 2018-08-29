# coding:gbk
class Settings():
	"""�洢�����������֡����������õ���"""
	
	def __init__(self):
		"""��ʼ����Ϸ�ľ�̬����"""
		# ��Ļ����
		self.screen_width = 300
		self.screen_height = 650
		self.bg_color = (255, 255, 0)
		
		#�ɴ�����
		
		self.ship_limit = 3
		
		# �ӵ�����
		self.bullet_width = 3 
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 20
		
		
		# ����������
		self.fleet_drop_speed = 1
		self.alien_type_limit = 3
		self.alien_3_left = 10
		self.attacks_allowed = 2
		self.attacks_interval_distance = 50

		
		# ��������
		self.background_speed_factor = 1
		self.bg_music_volume = 0.3
		
		# ��Ч����
		self.bullet_sound_volume = 0.2
		self.ship_bomb_sound_volume = 0.4
		self.alien_bomb_sound_volume = 0.4
		
		# ��ʲô�����ٶȼӿ���Ϸ����
		self.speedup_scale = 1.1
		# �����˵�������߱���
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
	
	def initialize_dynamic_settings(self):
		"""��ʼ������Ϸ���ж��仯������"""           
		self.ship_speed_factor = 1
		self.bullet_speed_factor = 3
		self.alien_1_attack_speed_factor = 0.4
		self.alien_2_attack_speed_factor = 0.3
		self.alien_3_attack_speed_factor = 1
		self.alien_speed_factor = 0.3
		self.alien_2_speed_factor = 0.1
		self.alien_3_speed_factor = 0.3
		# fleet_directionΪ1��ʾ�����ƣ�Ϊ-1��ʾ������
		self.fleet_direction = 1
		# �Ƿ�
		self.alien_points = 100
		self.ship_points = 50
	
	def increase_speed(self):
		"""����ٶ�����"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_1_attack_speed_factor *= self.speedup_scale
		self.alien_2_attack_speed_factor *= self.speedup_scale
		self.alien_3_attack_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_2_speed_factor *= self.speedup_scale
		self.alien_3_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
		
