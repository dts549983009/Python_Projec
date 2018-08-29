# coding:gbk
import json

class GameStats():
	"""������Ϸ��ͳ����Ϣ"""
	def __init__(self, ai_settings, filename):
		"""��ʼ��ͳ����Ϣ"""
		self.ai_settings = ai_settings
		self.filename = filename
		self.reset_stats()
		# ����Ϸһ��ʼ���ڷǻ�Ծ״̬
		self.game_active = False
		# ���κ�����¶���Ӧ������ߵ÷֣������ļ��ж�ȡ����
		self.load_filename()
		
	def load_filename(self):
		"""���ļ��ж�ȡ����"""
		try:
			with open(self.filename) as f_obj:
				self.high_score = json.load(f_obj)
		except FileNotFoundError:
			# ��Ϸ��һ���������ļ������ڣ��Զ������ļ�
			self.high_score = 0
			with open(self.filename, 'w') as f_json:
				json.dump(self.high_score, f_json)	
					
	def reset_stats(self):
		"""��ʼ������Ϸ�����ڼ���ܱ仯��ͳ����Ϣ"""
		self.ships_left = self.ai_settings.ship_limit
		self.aliens_type_left = self.ai_settings.alien_type_limit
		self.score = 0
		self.level = 1
		self.attacks_number = 0
		self.attacks_initial_value = 0
