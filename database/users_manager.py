class UsersManager:
    async def add_user(self, user_id, username):
        sql = 'INSERT INTO users (user_id, username) VALUES ($1, $2) ON CONFLICT (user_id) DO NOTHING'
        await self.execute(sql, user_id, username)

    async def select_all_users(self):
        sql = 'SELECT * FROM users'
        return await self.fetch(sql)
    
    async def select_user(self, **kwargs):
        sql = 'SELECT * FROM users WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        sql += " LIMIT 1"
        return await self.fetchrow(sql, *parameters)
    
    async def delete_user(self, user_id):
        sql = 'DELETE FROM users WHERE user_id = $1'
        await self.execute(sql, user_id)
    
    async def update_user_role(self, user_id, role):
        sql = f"UPDATE users SET role = $1 WHERE user_id = $2"
        return await self.execute(sql, role, user_id)

    async def update_username(self, user_id, username):
        sql = "UPDATE users SET username = $1 WHERE user_id = $2"
        return await self.execute(sql, username, user_id)
