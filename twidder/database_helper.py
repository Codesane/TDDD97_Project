import sqlite3, hashlib, os, binascii


DATABASE_SCHEMA = 'database.schema'
DATABASE_FILE   = 'database.db'

class DatabaseHelper:
	def __init__(self):
		print('DatabseHelper Initialized.')
		
	"""
	Overwrites the database and loads the schema.
	"""
	def load_schema(self):
		print("Loading Database Schema.")
		query = ''
		with open(DATABASE_SCHEMA, 'r') as f:
			query = query.join(f.readlines())

		open(DATABASE_FILE, 'w+').close()

		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()

		c.executescript(query)

		conn.commit()
		conn.close()
		print("Schema loaded.")

	def query(self, query):
		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()
		c.execute(query)
		conn.commit()
		conn.close()


	def get_user_by_credentials(self, email, password):
		sql = "SELECT id, email, password, salt FROM User WHERE email LIKE ?"

		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()

		user = c.execute(sql, [email]).fetchone()

		conn.commit()
		conn.close()

		# The user was not found.
		if not user:
			return None

		salted_password = hashlib.sha512(password + user[3]).hexdigest()

		return user if user[2] == salted_password else None

	def register_user(self, email, password, first_name, family_name, gender, city, country):
		sql = "INSERT INTO User (first_name, family_name, gender, city, country, email, password, salt) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

		gen_salt = binascii.hexlify(os.urandom(16))

		password = hashlib.sha512(password + gen_salt).hexdigest()

		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()

		c.execute(sql, [first_name, family_name, gender, city, country, email, password, gen_salt])

		conn.commit()
		conn.close()

		return c.lastrowid

	def user_change_password(self, user_id, new_password):
		sql = "UPDATE User SET Salt = ?, Password = ? WHERE id = ?"

		gen_salt = binascii.hexlify(os.urandom(16))

		password = hashlib.sha512(new_password + gen_salt).hexdigest()

		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()

		c.execute(sql, [gen_salt, password, user_id])

		conn.commit()
		conn.close()

	def check_password_match(self, user_id, password):
		sql_user_by_id = "SELECT password, salt FROM User WHERE User.id = ?"

		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()

		query_result = c.execute(sql_user_by_id, [user_id]).fetchone();

		conn.commit()
		conn.close()

		if not query_result:
			return False

		salted_password = hashlib.sha512(password + query_result[1]).hexdigest()

		return query_result[0] == salted_password


	def user_exists(self, u_id):
		return self.get_user_by_id(u_id) != None

	def get_user_by_id(self, u_id):
		sql = "SELECT id, first_name, family_name, gender, country, email, city FROM User WHERE id = ?"

		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()

		user = c.execute(sql, [u_id]).fetchone()

		conn.commit()
		conn.close()

		return user

	def get_user_by_email(self, email):
		sql = "SELECT id, first_name, family_name, gender, country, email, city FROM User WHERE email LIKE ?"

		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()

		user = c.execute(sql, [email]).fetchone()

		conn.commit()
		conn.close()

		return user


	def get_user_posts_by_id(self, u_id):
		sql = "SELECT Post.id, Post.message, User.email FROM Post INNER JOIN User ON Post.user_to_id = ? WHERE User.id = Post.user_from_id ORDER BY Post.id DESC"

		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()

		posts = c.execute(sql, [u_id]).fetchall()

		conn.commit()
		conn.close()

		return posts

	def get_user_posts_by_email(self, email):
		user_id = self.get_user_by_email(email)[0]

		return self.get_user_posts_by_id(user_id) if user_id else None

	def post_message_to_id(self, u_id, to_id, message):
		sql = "INSERT INTO Post (user_from_id, user_to_id, message) VALUES(?, ?, ?)"
		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()

		c.execute(sql, [u_id, to_id, message])

		conn.commit()
		conn.close()

		return c.lastrowid

	def post_message_to_email(self, u_id, to_email, message):
		user = self.get_user_by_email(to_email)
		if not user:
			return -1

		to_id = user[0]
		return self.post_message_to_id(u_id, to_id, message)


if __name__ == '__main__':
	db_helper = DatabaseHelper()
	db_helper.load_schema()
	u1 = db_helper.register_user("felix@felix.com", "pass", "Felix", "Novovic", "Male", "Halmstad", "Sweden")
	u2 = db_helper.register_user("erik@erik.com", "pass", "Erik", "Svensson", "Male", "Stockholm", "Sweden")

	db_helper.post_message_to_id(u1, u2, "Hello User Two.")
	db_helper.post_message_to_id(u2, u1, "Hello User One.")






