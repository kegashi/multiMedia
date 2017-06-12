# -*- coding: utf-8 -*-

import sys
import MySQLdb
import MeCab
import math

def main():

	#引数に渡された文章を取得する
	args = sys.argv
	#print args[1]
	tagger = MeCab.Tagger("-Owakati")
	result = tagger.parse(args[1]).split(" ")

	#print "meta-data"
	conn = MySQLdb.connect(
		host='localhost',
		user='#######',
		passwd='########',
		db='emoji_db',
		charset='utf8mb4'
	)
	c = conn.cursor()
	
	#テキストデータベース
	text_sql = "select * from text_info"
	c.execute(text_sql)
	#print text_sql

	textfeel = [0, 0, 0, 0, 0, 0, 0, 0]
	for row in result:
		for row2 in c:
			word = row2[0].encode('utf-8')

			if row.find(word) != -1:
				for num in range(8):
					textfeel[num] = textfeel[num] + (row2[num+1] * 5)

	#絵文字データベース
	emoji_sql = "select * from emoji_info"
	c.execute(emoji_sql)
	
	d_max = 100000000
	d_max_emoji = "hoge"
	for row in c:
		d = distance(row, textfeel)
		if d < d_max:
			d_max = d
			d_max_emoji = row[0]
	
	print d_max_emoji

	conn.commit()
	c.close()
	conn.close()

def distance(row, textfeel):
	d = 0
	for num in range(8):
		d = d + math.fabs(textfeel[num] - row[num+1])
	#d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
	return d

if __name__ == '__main__':
	main()
