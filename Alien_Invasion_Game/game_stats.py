# coding:gbk
import json

class GameStats():
	"""跟踪游戏的统计信息"""
	def __init__(self, ai_settings, filename):
		"""初始化统计信息"""
		self.ai_settings = ai_settings
		self.filename = filename
		self.reset_stats()
		# 让游戏一开始处于非活跃状态
		self.game_active = False
		# 在任何情况下都不应重置最高得分，并从文件中读取数据
		self.load_filename()
		
	def load_filename(self):
		"""从文件中读取数据"""
		try:
			with open(self.filename) as f_obj:
				self.high_score = json.load(f_obj)
		except FileNotFoundError:
			# 游戏第一次启动，文件不存在，自动生成文件
			self.high_score = 0
			with open(self.filename, 'w') as f_json:
				json.dump(self.high_score, f_json)	
					
	def reset_stats(self):
		"""初始化在游戏运行期间可能变化的统计信息"""
		self.ships_left = self.ai_settings.ship_limit
		self.aliens_type_left = self.ai_settings.alien_type_limit
		self.score = 0
		self.level = 1
		self.attacks_number = 0
		self.attacks_initial_value = 0
