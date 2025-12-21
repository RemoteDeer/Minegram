class CreateTable:
    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username TEXT,
            role TEXT NOT NULL DEFAULT 'user'
        );
        """

        sql_indexes = {
            "idx_users_role":
                """
                CREATE INDEX IF NOT EXISTS idx_users_role
                ON users (role);
                """
        }

        try:
            await self.execute(sql)
            print("[DB] Table 'users' created or already exists")
        except Exception as e:
            print("[DB ERROR] Failed to create 'users':", e)
        
        for index, sql in sql_indexes.items():
            try: 
                await self.execute(sql)
                print(f"[DB] Index '{index}' created or already exists")
            except Exception as e:
                print(f"[DB ERROR] Failed to create index '{index}':", e)

    async def create_table_requests(self):
        sql = """
        CREATE TABLE IF NOT EXISTS requests (
            request_id SERIAL PRIMARY KEY,
            status TEXT NOT NULL DEFAULT 'open',
            user_id BIGINT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            text_req TEXT NOT NULL,
            answered_at TIMESTAMP,
            text_ans TEXT,

            CONSTRAINT fk_request_user
                FOREIGN KEY (user_id)
                REFERENCES users (user_id)
                ON DELETE CASCADE
        );
        """

        sql_indexes = {
            "idx_requests_user_id":
                """
                CREATE INDEX IF NOT EXISTS idx_requests_user_id
                ON requests (user_id);
                """,
            "idx_requests_status":
                """
                CREATE INDEX IF NOT EXISTS idx_requests_status
                ON requests (status);
                """,
            "idx_requests_created_at":
                """
                CREATE INDEX IF NOT EXISTS idx_requests_created_at
                ON requests (created_at DESC);
                """,
            "idx_requests_user_status":
                """
                CREATE INDEX IF NOT EXISTS idx_requests_user_status
                ON requests (user_id, status);
                """
        }

        try:
            await self.execute(sql)
            print("[DB] Table 'requests' created or already exists")
        except Exception as e:
            print("[DB ERROR] Failed to create 'requests':", e)
        
        for index, sql in sql_indexes.items():
            try: 
                await self.execute(sql)
                print(f"[DB] Index '{index}' created or already exists")
            except Exception as e:
                print(f"[DB ERROR] Failed to create index '{index}':", e)
                
    async def create_table_minecraft_worlds(self):
        sql = """
        CREATE TABLE IF NOT EXISTS minecraft_worlds ( 
            port INTEGER PRIMARY KEY, 
            name TEXT NOT NULL, password TEXT, 
            creator_id BIGINT, 

            CONSTRAINT fk_world_creator 
                FOREIGN KEY (creator_id) 
                REFERENCES users (user_id) 
                ON DELETE SET NULL
        );
        """

        try:
            await self.execute(sql)
            print("[DB] Table 'minecraft_worlds' created or already exists")
        except Exception as e:
            print("[DB ERROR] Failed to create 'minecraft_worlds':", e)

    async def create_table(self):

        if not self.pool:
            raise ConnectionError("[DB ERROR] Database pool not initialized. Call db.connect() first!")

        await self.create_table_users()
        await self.create_table_requests()
        #await create_table_minecraft_worlds()